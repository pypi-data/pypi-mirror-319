from abc import ABC, abstractmethod

import plotly.graph_objects as go  # type: ignore


class Evaluator(ABC):

    @abstractmethod
    def run(self):
        """Run the evaluation on the benchmark result."""

    @abstractmethod
    def visualize(self) -> go.Figure:
        """Visualize the evaluation results."""
