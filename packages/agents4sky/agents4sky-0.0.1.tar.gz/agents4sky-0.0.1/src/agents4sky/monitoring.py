
from .utils import console
from rich.text import Text


class Monitor:
    def __init__(self, tracked_model):
        self.step_durations = []
        self.tracked_model = tracked_model
        if (
            getattr(self.tracked_model, "last_input_token_count", "Not found")
            != "Not found"
        ):
            self.total_input_token_count = 0
            self.total_output_token_count = 0

    def get_total_token_counts(self):
        return {
            "input": self.total_input_token_count,
            "output": self.total_output_token_count,
        }

    def reset(self):
        self.step_durations = []
        self.total_input_token_count = 0
        self.total_output_token_count = 0

    def update_metrics(self, step_log):
        step_duration = step_log.duration
        self.step_durations.append(step_duration)
        console_outputs = (
            f"[Step {len(self.step_durations)-1}: Duration {step_duration:.2f} seconds"
        )

        if getattr(self.tracked_model, "last_input_token_count", None) is not None:
            self.total_input_token_count += self.tracked_model.last_input_token_count
            self.total_output_token_count += self.tracked_model.last_output_token_count
            console_outputs += f"| Input tokens: {self.total_input_token_count:,} | Output tokens: {self.total_output_token_count:,}"
        console_outputs += "]"
        console.print(Text(console_outputs, style="dim"))


__all__ = ["Monitor"]
