"""
Pipeline 'data_science'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    remove_sale_and_odometer_outliers,
    generate_preprocessor,
    generate_clustering_pipeline,
    generate_regressor,
    train_model,
    split_data,
    evaluate_model,
)


def data_science_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=remove_sale_and_odometer_outliers,
                inputs={
                    "df_bev": "bev_resale_database",
                    "filter_make": "params:filter_make"
                },
                outputs="df_bev_wo_outlier",
                name="remove_sale_and_odometer_outliers",
            ),
            node(
                func=generate_preprocessor,
                inputs=[],
                outputs="preprocessor",
                name="generate_preprocessor",
            ),
            node(
                func=generate_clustering_pipeline,
                inputs={"preprocessor": "preprocessor"},
                outputs="clustering_pipeline",
                name="generate_clustering_pipeline",
            ),
            node(
                func=generate_regressor,
                inputs={"preprocessor": "preprocessor"},
                outputs="regressor",
                name="generate_regressor",
            ),
            node(
                func=split_data,
                inputs={
                    "df_bev_wo_outlier": "df_bev_wo_outlier",
                    "features": "params:feature_cols",
                    "target": "params:target_col",
                },
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data",
            ),
            node(
                func=train_model,
                inputs={
                    "X_train": "X_train",
                    "y_train": "y_train",
                    "cluster_cols": "params:cluster_cols",
                    "clustering_pipeline": "clustering_pipeline",
                    "regressor": "regressor",
                },
                outputs=["bev_clustering", "resale_price_regressor"],
                name="train_model",
            ),
            node(
                func=evaluate_model,
                inputs={
                    "X_test": "X_test",
                    "y_test": "y_test",
                    "cluster_cols": "params:cluster_cols",
                    "clustering_pipeline": "bev_clustering",
                    "regressor": "resale_price_regressor",
                },
                outputs="prediction_plot",
                name="evaluate_model",
            ),
        ]
    )
