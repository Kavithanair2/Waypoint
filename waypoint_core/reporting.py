"""Polymorphic reporting helpers for trail-like objects."""

from collections.abc import Iterable
from typing import Protocol


class TrailLike(Protocol):
    """Describe the methods required by the trail-reporting function."""

    def summary(self) -> str:
        """Return a readable summary."""
        ...

    def estimated_time(self) -> float:
        """Return an estimated completion time in hours."""
        ...


def build_trail_report(trails: Iterable[TrailLike]) -> list[str]:
    """Build report lines for any objects that behave like trails."""
    report_lines: list[str] = []

    for trail in trails:
        report_lines.append(
            f"{trail.summary()} | "
            f"estimated time: {trail.estimated_time():.2f} hours"
        )

    return report_lines