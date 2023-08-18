"""
This is a boilerplate pipeline 'get_electric_vehicle_data'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import download_data


def download_electric_vehicle_data(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=download_data,
                inputs={
                    "url": "params:electric_vehicle_data_url",
                    "save_path": "params:electric_vehicle_data_save_path",
                    },
                outputs=None,
                name="download_electric_vehicle_data",
            )
        ]
    )
