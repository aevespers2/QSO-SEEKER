from __future__ import annotations

from dataclasses import dataclass

from .models import DevelopmentMetrics


@dataclass(frozen=True)
class EvaluationSignal:
    coherence: float = 0.0
    uncertainty_calibration: float = 0.0
    self_correction: float = 0.0
    transfer_learning: float = 0.0
    ethical_consistency: float = 1.0
    cybernetic_integration: float = 0.0
    weight: float = 1.0


class MomentumTracker:
    """Maintain a bounded running estimate of operational development."""

    def update(self, metrics: DevelopmentMetrics, signal: EvaluationSignal) -> DevelopmentMetrics:
        if signal.weight <= 0:
            raise ValueError("signal weight must be positive")
        previous_weight = max(0, metrics.evaluated_steps)
        total_weight = previous_weight + signal.weight
        for name in (
            "coherence",
            "uncertainty_calibration",
            "self_correction",
            "transfer_learning",
            "ethical_consistency",
            "cybernetic_integration",
        ):
            prior = float(getattr(metrics, name))
            observed = float(getattr(signal, name))
            setattr(metrics, name, (prior * previous_weight + observed * signal.weight) / total_weight)
        metrics.evaluated_steps = int(total_weight)
        return metrics.bounded()

    @staticmethod
    def momentum_score(metrics: DevelopmentMetrics) -> float:
        metrics.bounded()
        return (
            0.20 * metrics.coherence
            + 0.20 * metrics.uncertainty_calibration
            + 0.20 * metrics.self_correction
            + 0.15 * metrics.transfer_learning
            + 0.15 * metrics.ethical_consistency
            + 0.10 * metrics.cybernetic_integration
        )
