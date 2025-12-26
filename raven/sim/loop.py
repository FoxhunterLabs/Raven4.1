import time
from typing import Dict, List

from raven.models import VehicleState, DecisionEvent
from raven.terrain import generate_terrain
from raven.decision import evaluate_segment, choose_action
from raven.audit import AuditLogger


class RavenSimulation:
    """
    Deterministic simulation loop with human-gated safety stops.
    """

    def __init__(self):
        self.terrain = generate_terrain()
        self.tick = 0
        self.vehicle = VehicleState(
            x=self.terrain[0].x,
            y=self.terrain[0].y,
            z=self.terrain[0].z,
            speed_mps=0.0,
            stability_index=100.0,
            drift_score=0.0,
            grade_deg=0.0,
            mode="HOLD",
        )

        self.human_lock = False
        self.decisions: List[DecisionEvent] = []
        self.audit = AuditLogger()

    def step(self) -> None:
        if self.human_lock:
            return

        self.tick += 1
        i = min(len(self.terrain) - 1, self.tick)
        seg = self.terrain[i]

        drift, stability, grade = evaluate_segment(seg, self.vehicle)
        action, reason = choose_action(drift, stability, grade)

        human_required = action == "STOP_SAFE"

        if human_required:
            self.human_lock = True
            self.vehicle.speed_mps = 0.0
            self.vehicle.mode = "STOP_SAFE"
        else:
            target_speed = {
                "CRUISE": 12.0,
                "CAUTIOUS": 6.0,
                "CRAWL": 2.0,
            }[action]
            self.vehicle.speed_mps += 0.25 * (target_speed - self.vehicle.speed_mps)
            self.vehicle.mode = action

        self.vehicle.x = seg.x
        self.vehicle.y = seg.y
        self.vehicle.z = seg.z
        self.vehicle.drift_score = drift
        self.vehicle.stability_index = stability
        self.vehicle.grade_deg = grade

        event = DecisionEvent(
            tick=self.tick,
            seg_i=i,
            action=action,
            reason=reason,
            drift_score=drift,
            stability_index=stability,
            grade_deg=grade,
            human_required=human_required,
            timestamp=time.time(),
        )

        self.decisions.append(event)
        self.audit.log(event.__dict__)
