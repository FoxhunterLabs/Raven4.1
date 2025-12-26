import math
import numpy as np
from typing import List

from raven.models import TerrainSegment


def generate_terrain(n: int = 160, seed: int = 42) -> List[TerrainSegment]:
    """
    Deterministic terrain generator.
    Produces a forward path with slope, roughness, edge exposure, traction,
    and a composite risk score.
    """
    rng = np.random.default_rng(seed)

    x = y = z = 0.0
    terrain: List[TerrainSegment] = []

    for i in range(n):
        t = i / n
        slope = math.sin(t * 2 * math.pi) * 15.0
        z += math.tan(math.radians(slope))
        x += 1.0

        roughness = rng.uniform(0.2, 0.6)
        edge_exposure = rng.uniform(0.1, 0.6)
        traction = rng.uniform(0.4, 0.9)

        risk = min(
            1.0,
            0.4 * roughness +
            0.4 * edge_exposure +
            0.2 * abs(slope) / 18.0
        )

        terrain.append(
            TerrainSegment(
                i=i,
                x=x,
                y=y,
                z=z,
                slope_deg=slope,
                roughness=roughness,
                edge_exposure=edge_exposure,
                traction_coeff=traction,
                risk=risk,
            )
        )

    return terrain
