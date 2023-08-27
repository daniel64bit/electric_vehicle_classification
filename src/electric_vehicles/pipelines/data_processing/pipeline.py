"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import normalize_vehicles_database, generate_bev_resale_database


def data_processing_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=normalize_vehicles_database,
                inputs={"df_vehicles": "electric_vehicle_activity"},
                outputs="normalized_vehicles_database",
                name="normalize_vehicles_database",
            ),
            node(
                func=generate_bev_resale_database,
                inputs={
                    "normalized_df_vehicles": "normalized_vehicles_database"
                },
                outputs="bev_resale_database",
                name="generate_bev_resale_database",
            ),
        ]
    )
