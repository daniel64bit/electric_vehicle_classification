"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline
from electric_vehicles.pipelines.get_electric_vehicle_data.pipeline import \
    download_electric_vehicle_data


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    return {
        "__default__": download_electric_vehicle_data(),
        "get_electric_vehicle_data": download_electric_vehicle_data(),
        }
