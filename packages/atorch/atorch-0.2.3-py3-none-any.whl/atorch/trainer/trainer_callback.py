from dataclasses import dataclass

from transformers.trainer_callback import TrainerCallback, TrainerControl, TrainerState
from transformers.trainer_utils import IntervalStrategy

from atorch.trainer.args import AtorchTrainingArgs
from atorch.trainer.atorch_args import AtorchArguments
from atorch.trainer.utils import IntervalStrategy as AtorchIntervalStrategy


@dataclass
class AtorchTrainerState(TrainerState):
    steps_in_epoch: int = 0
    current_step_in_epoch: int = 0
    consumed_train_samples: int = 0


class FlowCallback(TrainerCallback):
    """
    A [`TrainerCallback`] that handles the default flow of the training loop for logs, evaluation and checkpoints.
    """

    def on_step_end(self, args: AtorchArguments, state: TrainerState, control: TrainerControl, **kwargs):
        # Log
        if state.global_step == 1 and args.logging_first_step:
            control.should_log = True
        if args.logging_strategy == IntervalStrategy.STEPS and state.global_step % args.logging_steps == 0:
            control.should_log = True

        # Evaluate
        if (
            args.evaluation_strategy == IntervalStrategy.STEPS
            and state.global_step % args.eval_steps == 0
            and args.eval_delay <= state.global_step
        ):
            control.should_evaluate = True

        # Save
        if (
            args.save_strategy == IntervalStrategy.STEPS
            and args.save_steps > 0
            and state.global_step % args.save_steps == 0
        ):
            control.should_save = True

        # End training
        if state.global_step >= state.max_steps:
            control.should_training_stop = True

        return control

    def on_epoch_end(self, args: AtorchArguments, state: TrainerState, control: TrainerControl, **kwargs):
        # Log
        if args.logging_strategy == IntervalStrategy.EPOCH:
            control.should_log = True

        # Evaluate
        if args.evaluation_strategy == IntervalStrategy.EPOCH and args.eval_delay <= state.epoch:
            control.should_evaluate = True

        # Save
        if args.save_strategy == IntervalStrategy.EPOCH:
            control.should_save = True
        elif (
            args.save_at_specific_epoch is not None
            and state.epoch is not None
            and round(state.epoch) in args.save_at_specific_epoch
        ):
            control.should_save = True

        return control


class FlowCallbackV2(TrainerCallback):
    """
    A [`TrainerCallback`] that handles the default flow of the training loop for logs, evaluation and checkpoints.
    """

    def on_step_end(self, args: AtorchTrainingArgs, state: AtorchTrainerState, control: TrainerControl, **kwargs):
        # Log
        if state.global_step == 1 and args.logging_first_step:
            control.should_log = True
        if args.logging_strategy == AtorchIntervalStrategy.STEPS and state.global_step % args.logging_steps == 0:
            control.should_log = True

        # Evaluate
        if (
            args.evaluation_strategy == AtorchIntervalStrategy.STEPS
            and state.global_step % args.eval_steps == 0
            and args.eval_delay <= state.global_step
        ):
            control.should_evaluate = True

        # Save
        if (
            (
                args.save_strategy == AtorchIntervalStrategy.STEPS
                and args.save_steps > 0
                and state.global_step % args.save_steps == 0
            )
            or (
                args.save_strategy == AtorchIntervalStrategy.SAMPLES
                and args.save_samples > 0
                and state.consumed_train_samples % args.save_samples == 0
            )
            or (
                # extra save frequency in each epoch
                args.extra_save_frequency_in_epoch is not None
                and state.current_step_in_epoch in args.extra_save_frequency_in_epoch
            )
        ):
            control.should_save = True

        # End training
        if state.global_step >= state.max_steps:
            control.should_training_stop = True

        return control

    def on_epoch_end(self, args: AtorchTrainingArgs, state: TrainerState, control: TrainerControl, **kwargs):
        # Log
        if args.logging_strategy == AtorchIntervalStrategy.EPOCH:
            control.should_log = True

        # Evaluate
        if args.evaluation_strategy == AtorchIntervalStrategy.EPOCH and args.eval_delay <= state.epoch:
            control.should_evaluate = True

        # Save
        if args.save_strategy == AtorchIntervalStrategy.EPOCH:
            control.should_save = True

        return control
