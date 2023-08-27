"""Project pipelines."""
from kedro.pipeline import Pipeline
from electric_vehicles.pipelines.get_electric_vehicle_data.pipeline import (
    download_electric_vehicle_data,
)
from electric_vehicles.pipelines.data_processing.pipeline import (
    data_processing_pipeline,
)
from electric_vehicles.pipelines.data_science.pipeline import (
    data_science_pipeline,
)


def register_pipelines() -> dict[str, Pipeline]:
    """
    Registro de pipelines do projeto.
    """

    return {
        "__default__": download_electric_vehicle_data()
        + data_processing_pipeline()
        + data_science_pipeline(),
        "get_electric_vehicle_data": download_electric_vehicle_data(),
        "data_processing": data_processing_pipeline(),
        "data_science": data_science_pipeline(),
    }
