import json
import time
from pathlib import Path
from typing import Dict


class AuditLogger:
    """
    Append-only NDJSON audit logger.
    One file per run. Replayable. Human-readable.
    """

    def __init__(self, runs_dir: str = "runs_raven4"):
        self.runs_path = Path(runs_dir)
        self.runs_path.mkdir(exist_ok=True)
        self._run_id = time.strftime("%Y%m%dT%H%M%S")

    @property
    def run_id(self) -> str:
        return self._run_id

    def log(self, record: Dict) -> None:
        path = self.runs_path / f"{self._run_id}.ndjson"
        with open(path, "a") as f:
            f.write(json.dumps(record) + "\n")
