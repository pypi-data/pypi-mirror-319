import os

import safetensors
import torch
import torch.distributed as dist
from torch.distributed.fsdp.fully_sharded_data_parallel import FullyShardedDataParallel

from atorch.distributed.distributed import (
    parallel_group,
    parallel_group_and_ranks,
    parallel_group_size,
    parallel_rank,
    rank,
)
from atorch.utils.config import Config


def has_file_with_suffix(path, suffix):
    for filenanme in os.listdir(path):
        if str(filenanme).endswith(suffix):
            return True
    return False


def get_files_with_suffix(path, suffix):
    filenames = [f for f in os.listdir(path) if str(f).endswith(suffix)]
    filenames.sort()
    return filenames


def load_expert_from_safetensor(
    i,
    safe_weights_files,
    config,
    pretrained_model_name_or_path,
    ep_rank,
    ep_size,
    expert_w1_key,
    expert_w2_key,
    transpose_expert,
):
    state_dict_cur_expert = {}
    # load cur layer expert safetensors
    expert_indexes = [
        ind for ind in range(ep_rank * (config.num_experts // ep_size), (ep_rank + 1) * (config.num_experts // ep_size))
    ]
    expert_down_proj_weights_cur_ep_rank = []
    expert_gate_proj_weights_cur_ep_rank = []
    expert_up_proj_weights_cur_ep_rank = []

    safe_weights_file = os.path.join(pretrained_model_name_or_path, safe_weights_files[i])
    with safetensors.safe_open(safe_weights_file, framework="pt", device="cpu") as f1:
        for expert_ind in expert_indexes:
            name = "glm.transformer.layers." + str(i) + ".mlp.experts.expert_" + str(expert_ind) + ".down_proj.weight"
            buffer = f1.get_tensor(name)
            expert_down_proj_weights_cur_ep_rank.append(buffer)

            name = "glm.transformer.layers." + str(i) + ".mlp.experts.expert_" + str(expert_ind) + ".gate_proj.weight"
            buffer = f1.get_tensor(name)
            expert_gate_proj_weights_cur_ep_rank.append(buffer)

            name = "glm.transformer.layers." + str(i) + ".mlp.experts.expert_" + str(expert_ind) + ".up_proj.weight"
            buffer = f1.get_tensor(name)
            expert_up_proj_weights_cur_ep_rank.append(buffer)

    # merge w1 w2
    merged_gate = torch.stack(expert_gate_proj_weights_cur_ep_rank, dim=0)
    merged_up = torch.stack(expert_up_proj_weights_cur_ep_rank, dim=0)
    merged_w2 = torch.stack(expert_down_proj_weights_cur_ep_rank, dim=0)

    if transpose_expert:
        merged_gate = merged_gate.permute(0, 2, 1).contiguous()
        merged_up = merged_up.permute(0, 2, 1).contiguous()
        merged_w2 = merged_w2.permute(0, 2, 1).contiguous()

    merged_w1 = torch.cat([merged_gate, merged_up], dim=2)

    state_dict_cur_expert[expert_w1_key] = merged_w1.cuda().to(torch.float32)
    state_dict_cur_expert[expert_w2_key] = merged_w2.cuda().to(torch.float32)
    return state_dict_cur_expert


def assign_weight_to_fsdp(
    fsdp_module, state_dict, key_to_module, recurse=False, skip_keys=None, layer_index=None, check=False
):
    global_rank = rank()
    assert isinstance(fsdp_module, FullyShardedDataParallel)
    with FullyShardedDataParallel.summon_full_params(fsdp_module, recurse=recurse, writeback=True), torch.no_grad():
        for key in state_dict:
            if skip_keys is not None and key in skip_keys:
                continue
            module_ins = key_to_module[key]
            if global_rank == 0:
                print("assign", key, module_ins.weight.shape, state_dict[key].shape)
            assert module_ins.weight.shape == state_dict[key].shape, (
                "rank: " + str(global_rank) + " " + key + " layer:" + str(layer_index)
            )
            module_ins.weight.data.copy_(state_dict[key])
            assert torch.allclose(state_dict[key], module_ins.weight)

    if check:
        torch.distributed.barrier()
        with FullyShardedDataParallel.summon_full_params(
            fsdp_module, recurse=recurse, writeback=False
        ), torch.no_grad():
            for key in state_dict:
                if skip_keys is not None and key in skip_keys:
                    continue

                module_ins = key_to_module[key]
                res = torch.allclose(state_dict[key], module_ins.weight)
                if global_rank == 0:
                    print("check reshard value")
                if not res and torch.distributed.get_rank() == 0:
                    print(key, " state_dict", state_dict[key])
                    print(key, " module_ins.weight", module_ins.weight)
                    assert res, key

    del state_dict
    del key_to_module
    torch.distributed.barrier()


def load_3d_safetensors_to_fsdp(
    fsdp_model,
    config,
    key_list,
    key_to_shape,
    check_reshard_value=False,
    check_broadcast_value=False,
    transpose_expert=False,
):
    """
    config:{
            "pretrained_model_name_or_path":,
            "vocab_size":,
            "hidden_size":,
            "num_layers":,
            "num_key_value_heads":,
            "num_attention_heads":,
            "num_experts":,
            "moe_expert_parallel_size":,
            "moe_config": {
                "expert_intermediate_size":,
            }
        }

    outer_most_key_list = []
    attn_and_shared_expert_key_list = []
    experts_key_list = []
    outer_most_key_to_shape = {}
    attn_and_shared_expert_key_to_shape = {}
    experts_key_to_shape = {}
    key_list = [outermost_key_list, attn_and_shared_expert_key_list, experts_key_list]
    key_to_shape = [outer_most_key_to_shape, attn_and_shared_expert_key_to_shape, experts_key_to_shape]
    """
    assert len(key_list) >= 3 and len(key_to_shape) >= 3
    config = Config(config)
    # load safetensors
    pretrained_model_name_or_path = config.pretrained_model_name_or_path

    global_rank = rank()
    safe_weights_files = get_files_with_suffix(pretrained_model_name_or_path, ".safetensors")

    outer_most_key_list = key_list[0]
    world_embedding_key = outer_most_key_list[0]
    final_layernorm_key = outer_most_key_list[1]
    lm_head_key = outer_most_key_list[2]
    state_dict_outer_most = {}
    if global_rank == 0:
        print(safe_weights_files)
        print(fsdp_model)
        for name, module_ins in fsdp_model.named_parameters():
            print(name)
        print("named modules")
        for name, module_ins in fsdp_model.named_modules():
            print(name)

        # Load world_embeddings/final_layernorm/lm_head
        safe_weights_file = os.path.join(pretrained_model_name_or_path, safe_weights_files[0])
        with safetensors.safe_open(safe_weights_file, framework="pt", device="cpu") as f1:
            state_dict_outer_most[world_embedding_key] = f1.get_tensor(world_embedding_key).cuda().to(torch.float32)

        safe_weights_file = os.path.join(pretrained_model_name_or_path, safe_weights_files[-1])
        with safetensors.safe_open(safe_weights_file, framework="pt", device="cpu") as f2:
            state_dict_outer_most[final_layernorm_key] = f2.get_tensor(final_layernorm_key).cuda().to(torch.float32)
            state_dict_outer_most[lm_head_key] = f2.get_tensor(lm_head_key).cuda().to(torch.float32)

        for key in state_dict_outer_most:
            print("broadcast", key)
            dist.broadcast(state_dict_outer_most[key], src=0, group=parallel_group("data"))
    else:
        outer_most_key_to_shape = key_to_shape[0]
        for key in outer_most_key_to_shape:
            buffer = torch.empty(outer_most_key_to_shape[key], device="cuda", dtype=torch.float32)
            dist.broadcast(buffer, src=0, group=parallel_group("data"))
            state_dict_outer_most[key] = buffer

    key_to_module_outer_most = {}
    for name, module_ins in fsdp_model.named_modules():
        if "word_embeddings" in name:
            key_to_module_outer_most[world_embedding_key] = module_ins

        if "final_layernorm" in name:
            key_to_module_outer_most[final_layernorm_key] = module_ins

        if "lm_head" in name:
            key_to_module_outer_most[lm_head_key] = module_ins

    # Assign world_embeddings/final_layernorm/lm_head weight to FSDP flat param
    # Note: call summon_full_params in every rank
    assign_weight_to_fsdp(fsdp_model, state_dict_outer_most, key_to_module_outer_most, check=check_reshard_value)

    # Load attention/input_layernorm/post_attention_layernorm/router/shared_experts per layer
    attn_and_shared_expert_key_list = key_list[1]
    attn_and_shared_expert_key_to_shape = key_to_shape[1]
    for i in range(config.num_layers):
        cur_layer = "layers." + str(i)

        for weight_key in attn_and_shared_expert_key_list:
            state_dict_cur_layer = {}
            if global_rank == 0:
                # load cur layer safetensors
                safe_weights_file = os.path.join(pretrained_model_name_or_path, safe_weights_files[i])
                with safetensors.safe_open(safe_weights_file, framework="pt", device="cpu") as f1:
                    for name in f1.keys():
                        if weight_key in name and cur_layer in name:
                            state_dict_cur_layer[weight_key] = f1.get_tensor(name).cuda().to(torch.float32)

                print("layer ", i, "broadcast", weight_key, state_dict_cur_layer[weight_key].shape)
                dist.broadcast(state_dict_cur_layer[weight_key], src=0, group=parallel_group("data"))
            else:
                buffer = torch.empty(
                    attn_and_shared_expert_key_to_shape[weight_key], device="cuda", dtype=torch.float32
                )
                dist.broadcast(buffer, src=0, group=parallel_group("data"))
                state_dict_cur_layer[weight_key] = buffer

                if check_broadcast_value:
                    loaded_dict_cur_layer = {}
                    safe_weights_file = os.path.join(pretrained_model_name_or_path, safe_weights_files[i])
                    with safetensors.safe_open(safe_weights_file, framework="pt", device="cpu") as f1:
                        for name in f1.keys():
                            if weight_key in name and cur_layer in name:
                                loaded_dict_cur_layer[weight_key] = f1.get_tensor(name).cuda().to(torch.float32)

                    res = torch.allclose(loaded_dict_cur_layer[weight_key], state_dict_cur_layer[weight_key])
                    if global_rank == 1:
                        print("check broadcast value")
                    if not res:
                        print(key, " from broadcast ", state_dict_cur_layer[weight_key])
                        print(key, " from safetensors ", loaded_dict_cur_layer[weight_key])
                    assert res
                    del loaded_dict_cur_layer

            key_to_module_cur_layer = {}
            fsdp_module_cur_layer = None
            fsdp_module_name_cur_layer = "_fsdp_wrapped_module.glm.transformer.layers." + str(i)
            for name, module_ins in fsdp_model.named_modules():
                # search fsdp module
                if name == fsdp_module_name_cur_layer:
                    fsdp_module_cur_layer = module_ins
                    # create key_to_module_cur_layer

                    for name_inner, module_ins_inner in fsdp_module_cur_layer.named_modules():
                        if weight_key in name_inner:
                            key_to_module_cur_layer[weight_key] = module_ins_inner

                    fsdp_module_cur_layer._reset_lazy_init()
                    assign_weight_to_fsdp(
                        fsdp_module_cur_layer,
                        state_dict_cur_layer,
                        key_to_module_cur_layer,
                        recurse=False,
                        layer_index=i,
                        check=check_reshard_value,
                    )
                    fsdp_module_cur_layer._reset_lazy_init()
                    break

            assert fsdp_module_cur_layer is not None
            del state_dict_cur_layer
            del key_to_module_cur_layer

    # Load and merge experts
    experts_key_list = key_list[2]
    experts_key_to_shape = key_to_shape[2]
    expert_w1_key = experts_key_list[0]
    expert_w2_key = experts_key_list[1]
    expert_fsdp_rank = parallel_rank("expert_fsdp")
    ep_rank = parallel_rank("expert")
    ep_size = parallel_group_size("expert")
    _, ranks_cur_expert_fsdp_group = parallel_group_and_ranks("expert_fsdp")
    for i in range(config.num_layers):
        state_dict_cur_expert = {}

        if expert_fsdp_rank == 0:
            state_dict_cur_expert = load_expert_from_safetensor(
                i,
                safe_weights_files,
                config,
                pretrained_model_name_or_path,
                ep_rank,
                ep_size,
                expert_w1_key,
                expert_w2_key,
                transpose_expert,
            )
            for key in state_dict_cur_expert:
                if global_rank == 0:
                    print("layer ", i, "broadcast expert", key, state_dict_cur_expert[key].shape)
                dist.broadcast(state_dict_cur_expert[key], src=global_rank, group=parallel_group("expert_fsdp"))
        else:
            for key in experts_key_list:
                buffer = torch.empty(experts_key_to_shape[key], device="cuda", dtype=torch.float32)
                dist.broadcast(buffer, src=ranks_cur_expert_fsdp_group[0], group=parallel_group("expert_fsdp"))
                state_dict_cur_expert[key] = buffer

            if expert_fsdp_rank == 1 and check_broadcast_value:
                loaded_state_dic_cur_expert = load_expert_from_safetensor(
                    i,
                    safe_weights_files,
                    config,
                    pretrained_model_name_or_path,
                    ep_rank,
                    ep_size,
                    expert_w1_key,
                    expert_w2_key,
                    transpose_expert,
                )
                for key in experts_key_list:
                    torch.allclose(state_dict_cur_expert[key], loaded_state_dic_cur_expert[key])
                if global_rank == 1:
                    print("check expert broadcast value")
                del loaded_state_dic_cur_expert

        key_to_module_cur_expert = {}
        fsdp_module_cur_expert = None
        fsdp_module_name_cur_expert = (
            "_fsdp_wrapped_module.glm.transformer.layers."
            + str(i)
            + "._fsdp_wrapped_module._checkpoint_wrapped_module.mlp.experts"
        )

        for name, module_ins in fsdp_model.named_modules():
            # search fsdp module
            if name == fsdp_module_name_cur_expert:
                fsdp_module_cur_expert = module_ins

                for k in experts_key_list:
                    key_to_module_cur_expert[k] = module_ins

                fsdp_module_cur_expert._reset_lazy_init()
                with FullyShardedDataParallel.summon_full_params(
                    fsdp_module_cur_expert, recurse=False, writeback=True
                ), torch.no_grad():
                    module_ins = key_to_module_cur_expert[expert_w1_key]
                    if global_rank == 0:
                        print(
                            "assign",
                            expert_w1_key,
                            module_ins.w1.shape,
                            state_dict_cur_expert[expert_w1_key].shape,
                        )
                    assert module_ins.w1.shape == state_dict_cur_expert[expert_w1_key].shape, (
                        str(global_rank) + expert_w1_key + str(i)
                    )
                    module_ins.w1.data.copy_(state_dict_cur_expert[expert_w1_key])
                    assert torch.allclose(state_dict_cur_expert[expert_w1_key], module_ins.w1)

                    module_ins = key_to_module_cur_expert[expert_w2_key]
                    if global_rank == 0:
                        print(
                            "assign",
                            expert_w2_key,
                            module_ins.w2.shape,
                            state_dict_cur_expert[expert_w2_key].shape,
                        )
                    assert module_ins.w2.shape == state_dict_cur_expert[expert_w2_key].shape, (
                        str(global_rank) + expert_w2_key + str(i)
                    )
                    module_ins.w2.data.copy_(state_dict_cur_expert[expert_w2_key])
                    assert torch.allclose(state_dict_cur_expert[expert_w2_key], module_ins.w2)

                if check_reshard_value:
                    torch.distributed.barrier()
                    with FullyShardedDataParallel.summon_full_params(
                        fsdp_module_cur_expert, recurse=False, writeback=True
                    ), torch.no_grad():
                        module_ins = key_to_module_cur_expert[expert_w1_key]
                        assert torch.allclose(state_dict_cur_expert[expert_w1_key], module_ins.w1)
                        module_ins = key_to_module_cur_expert[expert_w2_key]
                        assert torch.allclose(state_dict_cur_expert[expert_w2_key], module_ins.w2)

                del state_dict_cur_expert
                del key_to_module_cur_expert
                torch.distributed.barrier()
                fsdp_module_cur_expert._reset_lazy_init()
                break

        assert fsdp_module_cur_expert is not None

    fsdp_model._reset_lazy_init()
