from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionEvent:
    tick: int
    seg_i: int
    action: str
    reason: str
    drift_score: float
    stability_index: float
    grade_deg: float
    human_required: bool
    timestamp: float
