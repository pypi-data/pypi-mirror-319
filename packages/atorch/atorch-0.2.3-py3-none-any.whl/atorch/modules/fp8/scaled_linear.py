import math
from typing import Optional, Union

import torch
from torch.nn import init
from torch.nn.parameter import Parameter

from .quantize import (
    Fp8Quantization,
    QuantizeParams,
    ScaleComputMethod,
    ScaleType,
    get_linear_axiswise_quantize_params,
    get_linear_tensorwise_quantize_params,
    get_linear_tileblock_quantize_params,
)


def fp8_valid_shape_check(shape):
    # row/col dim must be divided by 16 for fp8.
    return shape[0] % 16 == 0 and shape[1] % 16 == 0


def is_row_major(tensor):
    stride = tensor.stride()
    return len(stride) == 2 and stride[0] >= stride[1] and stride[1] == 1


def is_col_major(tensor):
    stride = tensor.stride()
    return len(stride) == 2 and stride[1] >= stride[0] and stride[0] == 1


def switch_major(tensor):
    if is_row_major(tensor):
        return tensor.t().contiguous().t()
    else:
        return tensor.contiguous()


def _fp8_gemm(fp8_x, fp8_w, x_inverse_scale, w_inverse_scale, bias, out_dtype, quantize_params, method):
    # FBGEMM uses fp8_weight while PYTORCH method uses fp8_weight_t.
    if isinstance(fp8_w, tuple):
        fp8_weight, fp8_weight_t = fp8_w
        weight_inverse_scale, weight_t_inverse_scale = w_inverse_scale
    else:
        fp8_weight_t = fp8_w
        weight_t_inverse_scale = w_inverse_scale
    if bias is not None:
        bias = bias.to(out_dtype)
    if method == ScaleComputMethod.DEFAULT or method == ScaleComputMethod.PYTORCH:
        if fp8_weight_t is None:
            fp8_weight_t = fp8_weight.t()
        if weight_t_inverse_scale is None:
            weight_t_inverse_scale = weight_inverse_scale.t()
        return _fp8_gemm_pt(
            fp8_x, fp8_weight_t, x_inverse_scale, weight_t_inverse_scale, bias, out_dtype, quantize_params
        )
    elif method == ScaleComputMethod.FBGEMM:
        return _fp8_gemm_fbgemm(
            fp8_x, fp8_weight, x_inverse_scale, weight_inverse_scale, bias, out_dtype, quantize_params
        )
    elif method == ScaleComputMethod.TRITON:
        return _fp8_gemm_triton(fp8_x, fp8_weight, x_inverse_scale, weight_inverse_scale, bias, out_dtype)
    else:
        assert 0, f"fp8_gemm method {method} is not implemented yet"


def _fp8_gemm_pt(fp8_x, fp8_w, x_inverse_scale, w_inverse_scale, bias, out_dtype, quantize_params):
    if not is_row_major(fp8_x):
        fp8_x = switch_major(fp8_x)
    if not is_col_major(fp8_w):
        fp8_w = switch_major(fp8_w)

    if x_inverse_scale.shape != []:
        x_inverse_scale = x_inverse_scale.view(-1, 1)
        w_inverse_scale = w_inverse_scale.view(1, -1)

    out = torch._scaled_mm(
        fp8_x,  # must row major
        fp8_w,  # must column major
        x_inverse_scale,
        w_inverse_scale,
        bias=bias,
        out_dtype=out_dtype,
        use_fast_accum=quantize_params.use_fast_accum,
    )
    return out


def _fp8_gemm_fbgemm(fp8_x, fp8_w, x_inverse_scale, w_inverse_scale, bias, out_dtype, quantize_params):
    assert out_dtype == torch.bfloat16
    if x_inverse_scale.shape == []:  # tensorwise
        out = torch.ops.fbgemm.f8f8bf16(
            fp8_x, fp8_w, x_inverse_scale * w_inverse_scale, use_fast_accum=quantize_params.use_fast_accum
        )
    else:  # axiswise
        out = torch.ops.fbgemm.f8f8bf16_rowwise(
            fp8_x,
            fp8_w,
            x_inverse_scale.view(-1),
            w_inverse_scale.view(-1),
            use_fast_accum=quantize_params.use_fast_accum,
        )
    if bias:
        out = out + bias
    return out


def _fp8_gemm_triton(fp8_x, fp8_w, x_inverse_scale, w_inverse_scale, bias, out_dtype):
    # Now only supports x tilewise and w blockwise
    from .triton_kernel import fp8_gemm

    out = fp8_gemm(fp8_x, x_inverse_scale, fp8_w, w_inverse_scale, dtype=out_dtype)
    if bias:
        out = out + bias
    return out


class _ScaledLinear(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        input: torch.Tensor,
        weight: torch.Tensor,
        bias: Optional[torch.Tensor],
        quantize_params: QuantizeParams,
        fp8_valid: bool,
    ):
        ctx.input_requires_grad = input.requires_grad
        ctx.weight_requires_grad = weight.requires_grad
        ctx.bias_requires_grad = bias is not None and bias.requires_grad
        ctx.quantize_params = quantize_params
        ctx.out_dtype = input.dtype
        ctx.fp8_valid = fp8_valid
        ctx.input_shape = input.shape
        out_shape = (*input.shape[0:-1], -1)
        inputmat = input.view(-1, input.shape[-1])
        ctx.input_fp8_valid = fp8_valid_shape_check(inputmat.shape)

        saved_weight = weight.to(input.dtype) if input.requires_grad else None
        saved_input = inputmat if weight.requires_grad else None
        saved_fp8_input = None
        saved_fp8_input_scale = None
        saved_fp8_weight_t = None
        saved_fp8_weight_t_scale = None

        if quantize_params.use_fp8 and fp8_valid:
            assert "input" in quantize_params.fp8_meta
            assert "weight" in quantize_params.fp8_meta
            quantize_method = quantize_params.get_quantization_compute_method()

            # 1. quantize input
            (fp8_dtype, scale_type, scale_args) = quantize_params.fp8_meta["input"]
            if scale_type == ScaleType.TENSORWISE:
                fp8_input, input_inverse_scale = Fp8Quantization.quantize_tensorwise(
                    inputmat, fp8_dtype, method=quantize_method
                )
                if (
                    weight.requires_grad
                    and quantize_params.fp8_meta["weight"][1] == ScaleType.TENSORWISE
                    and ctx.input_fp8_valid
                ):
                    saved_fp8_input = fp8_input
                    saved_fp8_input_scale = input_inverse_scale
                    saved_input = None
            elif scale_type == ScaleType.AXISWISE:
                fp8_input, input_inverse_scale = Fp8Quantization.quantize_axiswise(
                    inputmat, fp8_dtype, dim=1, method=quantize_method
                )
            elif scale_type == ScaleType.TILEWISE:
                fp8_input, input_inverse_scale = Fp8Quantization.quantize_tilewise(
                    inputmat, fp8_dtype, block_size=scale_args, dim=1, method=quantize_method
                )
            else:
                assert 0, f"scale type {scale_type} not implemented yet"

            # 2. quantize weight
            fp8_weight = None
            fp8_weight_t = None
            weight_inverse_scale = None
            weight_t_inverse_scale = None
            (fp8_dtype, scale_type, scale_args) = quantize_params.fp8_meta["weight"]
            if scale_type == ScaleType.TENSORWISE:
                fp8_weight_t, weight_t_inverse_scale = Fp8Quantization.quantize_tensorwise(
                    weight.t(), fp8_dtype, method=quantize_method
                )
                if input.requires_grad and quantize_params.fp8_meta["input"][1] == ScaleType.TENSORWISE:
                    saved_fp8_weight_t = fp8_weight_t
                    saved_fp8_weight_t_scale = weight_t_inverse_scale
                    saved_weight = None
            elif scale_type == ScaleType.AXISWISE:
                fp8_weight, weight_inverse_scale = Fp8Quantization.quantize_axiswise(
                    weight, fp8_dtype, dim=1, method=quantize_method
                )
            elif scale_type == ScaleType.BLOCKWISE:
                fp8_weight, weight_inverse_scale = Fp8Quantization.quantize_blockwise(
                    weight, fp8_dtype, block_size=scale_args, method=quantize_method
                )
            else:
                assert 0, f"scale type {scale_type} not implemented yet"

            # 3. fp8 gemm
            fp8_gemm_method = quantize_params.get_fp8_compute_method()
            out = _fp8_gemm(
                fp8_input,
                (fp8_weight, fp8_weight_t),
                input_inverse_scale,
                (weight_inverse_scale, weight_t_inverse_scale),
                bias,
                input.dtype,
                quantize_params,
                fp8_gemm_method,
            )
        else:
            # not use fp8
            # y = mm(x, w.t()) + b
            if bias is not None:
                out = torch.addmm(bias, inputmat, weight.t())
            else:
                out = torch.mm(inputmat, weight.t())

        saved_tensors = [
            saved_weight,
            saved_input,
            saved_fp8_input,
            saved_fp8_input_scale,
            saved_fp8_weight_t,
            saved_fp8_weight_t_scale,
        ]

        ctx.save_for_backward(*saved_tensors)
        return out.view(out_shape)

    @staticmethod
    def backward(
        ctx,
        output_grad: torch.Tensor,
    ):
        (
            saved_weight,
            saved_input,
            saved_fp8_input,
            saved_fp8_input_scale,
            saved_fp8_weight_t,
            saved_fp8_weight_t_scale,
        ) = ctx.saved_tensors
        results = [None, None, None, None, None]

        quantize_method = ctx.quantize_params.get_quantization_compute_method()

        fp8_gemm_method = ctx.quantize_params.get_fp8_compute_method()

        output_grad = output_grad.view(-1, output_grad.shape[-1])

        if ctx.input_requires_grad:
            # calculate input grad and assign to results[0]
            if ctx.quantize_params.use_fp8 and ctx.fp8_valid:  # dgrad fp8
                assert "grad" in ctx.quantize_params.fp8_meta
                assert "weight" in ctx.quantize_params.fp8_meta
                (fp8_dtype, scale_type, _) = ctx.quantize_params.fp8_meta["grad"]
                if scale_type == ScaleType.TENSORWISE:
                    fp8_grad, grad_inverse_scale = Fp8Quantization.quantize_tensorwise(
                        output_grad, fp8_dtype, method=quantize_method
                    )
                elif scale_type == ScaleType.AXISWISE:
                    fp8_grad, grad_inverse_scale = Fp8Quantization.quantize_axiswise(
                        output_grad, fp8_dtype, dim=1, method=quantize_method
                    )
                else:
                    assert 0, f"scale type {scale_type} not implemented yet"

                (fp8_dtype, scale_type, _) = ctx.quantize_params.fp8_meta["weight"]
                if scale_type == ScaleType.TENSORWISE:
                    if saved_weight is None:
                        weight_inverse_scale = saved_fp8_weight_t_scale
                        fp8_weight = saved_fp8_weight_t.t()
                    else:
                        fp8_weight, weight_inverse_scale = Fp8Quantization.quantize_tensorwise(
                            saved_weight, fp8_dtype, method=quantize_method
                        )
                elif scale_type == ScaleType.AXISWISE:
                    fp8_weight, weight_inverse_scale = Fp8Quantization.quantize_axiswise(
                        saved_weight, fp8_dtype, dim=0, method=quantize_method
                    )
                else:
                    assert 0, f"scale type {scale_type} not implemented yet"

                dx = _fp8_gemm(
                    fp8_grad,
                    fp8_weight,
                    grad_inverse_scale,
                    weight_inverse_scale,
                    bias=None,
                    out_dtype=ctx.out_dtype,
                    quantize_params=ctx.quantize_params,
                    method=fp8_gemm_method,
                )
            else:
                # dx = mm(dy, w)
                dx = torch.mm(output_grad, saved_weight)
            results[0] = dx.view(ctx.input_shape)

        if ctx.weight_requires_grad:
            # calculate weight grad and assign to results[1]
            if ctx.quantize_params.use_fp8 and ctx.input_fp8_valid:  # wgrad fp8
                assert "grad" in ctx.quantize_params.fp8_meta
                assert "input" in ctx.quantize_params.fp8_meta
                (fp8_dtype, scale_type, _) = ctx.quantize_params.fp8_meta["grad"]
                if scale_type == ScaleType.TENSORWISE:
                    fp8_grad_t, grad_t_inverse_scale = Fp8Quantization.quantize_tensorwise(
                        output_grad.t(), fp8_dtype, method=quantize_method
                    )
                elif scale_type == ScaleType.AXISWISE:
                    fp8_grad_t, grad_t_inverse_scale = Fp8Quantization.quantize_axiswise(
                        output_grad.t(), fp8_dtype, dim=1, method=quantize_method
                    )
                else:
                    assert 0, f"scale type {scale_type} not implemented yet"

                (fp8_dtype, scale_type, _) = ctx.quantize_params.fp8_meta["input"]
                if scale_type == ScaleType.TENSORWISE:
                    if saved_input is None:
                        fp8_input, input_inverse_scale = saved_fp8_input, saved_fp8_input_scale
                    else:
                        fp8_input, input_inverse_scale = Fp8Quantization.quantize_tensorwise(
                            saved_input, fp8_dtype, method=quantize_method
                        )
                elif scale_type == ScaleType.AXISWISE:
                    fp8_input, input_inverse_scale = Fp8Quantization.quantize_axiswise(
                        saved_input, fp8_dtype, dim=0, method=quantize_method
                    )
                else:
                    assert 0, f"scale type {scale_type} not implemented yet"

                dw = _fp8_gemm(
                    fp8_grad_t,
                    fp8_input,
                    grad_t_inverse_scale,
                    input_inverse_scale,
                    bias=None,
                    out_dtype=ctx.out_dtype,
                    quantize_params=ctx.quantize_params,
                    method=fp8_gemm_method,
                )
            else:
                # dw = mm(dy.t(), x)
                dw = torch.mm(output_grad.t(), saved_input)
            results[1] = dw

        if ctx.bias_requires_grad:
            # calculate bias grad and assign to results[2]
            # db = sum(dy)
            results[2] = torch.sum(output_grad, dim=0)

        return tuple(results)


class ScaledLinear(torch.nn.Module):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        bias: bool = True,
        device=None,
        dtype=None,
        quantize_params: Optional[Union[QuantizeParams, str]] = None,
    ):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        if quantize_params is None or quantize_params == "tensorwise":
            self.quantize_params = get_linear_tensorwise_quantize_params()
        elif quantize_params == "axiswise":
            self.quantize_params = get_linear_axiswise_quantize_params()
        elif quantize_params == "tileblock":
            self.quantize_params = get_linear_tileblock_quantize_params(128)
        elif isinstance(quantize_params, QuantizeParams):
            self.quantize_params = quantize_params
        else:
            assert 0, f"quantize_params {quantize_params} not supported"
        self.weight = Parameter(torch.empty((out_features, in_features), device=device, dtype=dtype))
        if bias:
            self.bias = Parameter(torch.empty(out_features, device=device, dtype=dtype))
        else:
            self.bias = None
        self.reset_parameters()
        self.fp8_valid = fp8_valid_shape_check((in_features, out_features))

    @property
    def use_fp8(self):
        return self.quantize_params.use_fp8

    def set_use_fp8(self, use_fp8=True):
        self.quantize_params.use_fp8 = use_fp8

    def set_quantize_params(self, qparams):
        self.quantize_params = qparams

    def reset_parameters(self) -> None:
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            init.uniform_(self.bias, -bound, bound)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        if torch.is_autocast_enabled():
            input = input.to(torch.get_autocast_gpu_dtype())
        return _ScaledLinear.apply(input, self.weight, self.bias, self.quantize_params, self.fp8_valid)

    def extra_repr(self) -> str:
        return f"in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}"
