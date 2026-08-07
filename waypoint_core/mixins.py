"""Reusable mixins for extending Waypoint trail summaries."""


class PermitRequiredMixin:
    """Add permit information to a trail summary."""

    def summary(self) -> str:
        """Extend the next summary in the method-resolution order."""
        return f"{super().summary()}, permit required"


class SeasonalAccessMixin:
    """Add seasonal-access information to a trail summary."""

    def summary(self) -> str:
        """Extend the next summary in the method-resolution order."""
        return f"{super().summary()}, seasonal access"