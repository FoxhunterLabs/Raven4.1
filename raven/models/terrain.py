from dataclasses import dataclass


@dataclass(frozen=True)
class TerrainSegment:
    i: int
    x: float
    y: float
    z: float
    slope_deg: float
    roughness: float
    edge_exposure: float
    traction_coeff: float
    risk: float
