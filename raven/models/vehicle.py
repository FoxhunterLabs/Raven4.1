from dataclasses import dataclass


@dataclass
class VehicleState:
    x: float
    y: float
    z: float
    speed_mps: float
    stability_index: float
    drift_score: float
    grade_deg: float
    mode: str
