from typing import Tuple

from raven.models import TerrainSegment, VehicleState


def evaluate_segment(
    seg: TerrainSegment,
    vehicle: VehicleState
) -> Tuple[float, float, float]:
    """
    Evaluate drift, stability, and grade for a terrain segment
    given current vehicle state.
    """
    speed_factor = min(1.0, vehicle.speed_mps / 15.0)

    drift = (
        0.4 * abs(seg.slope_deg) / 18.0 +
        0.3 * seg.roughness +
        0.3 * (1.0 - seg.traction_coeff)
    ) * 100.0

    stability = max(
        0.0,
        100.0 - drift * (0.6 + 0.4 * speed_factor)
    )

    return drift, stability, seg.slope_deg
