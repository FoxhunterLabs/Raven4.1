from typing import Tuple


def choose_action(
    drift: float,
    stability: float,
    grade_deg: float
) -> Tuple[str, str]:
    """
    Deterministic safety policy.
    Returns (action, rationale).
    """

    if drift > 85 or stability < 30 or abs(grade_deg) > 20:
        return "STOP_SAFE", "outside hard safety envelope"

    if drift > 60 or stability < 50 or abs(grade_deg) > 14:
        return "CRAWL", "high terrain risk"

    if drift > 40 or stability < 65 or abs(grade_deg) > 10:
        return "CAUTIOUS", "moderate terrain risk"

    return "CRUISE", "stable window"
