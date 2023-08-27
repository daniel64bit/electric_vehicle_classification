"""
Pipeline 'data_science'
generated using Kedro 0.18.12
"""

import logging
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_selector, ColumnTransformer
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_absolute_percentage_error,
)


def remove_outlier(
    df: pd.DataFrame,
    column: str,
    upper_only: bool = False,
    return_outlier: bool = False,
) -> pd.DataFrame:
    """
    Remove outlier pelo método de distância interquatílica.
    Se return_outlier for True, retorna apenas outliers da série.
    """

    # Intervalo interquartil
    p25 = df[column].quantile(0.25)
    p75 = df[column].quantile(0.75)
    iqr = p75 - p25

    # Limites inferior e superior
    lower = p25 - 1.5 * iqr
    upper = p75 + 1.5 * iqr
    if upper_only:
        if return_outlier:
            return df[(df[column] > upper)]
        else:
            return df[(df[column] <= upper)]
    else:
        if return_outlier:
            return df[(df[column] < lower) | (df[column] > upper)]
        else:
            return df[(df[column] >= lower) & (df[column] <= upper)]


def remove_sale_and_odometer_outliers(
    df_bev: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove outliers de preço de revenda venda e
    medições de odômetro.
    """

    # Outliers de preço de revenda
    df_bev_wo_outlier = remove_outlier(df_bev, "SALE_PRICE", upper_only=True)
    df_bev_wo_outlier = df_bev_wo_outlier[
        df_bev_wo_outlier["SALE_PRICE"]
        > df_bev_wo_outlier["SALE_PRICE"].quantile(0.01)
    ]

    # Outliers de medições de odômetro
    df_bev_wo_outlier = remove_outlier(df_bev_wo_outlier, "ODOMETER_READING")

    # Linhas removidas
    pct_remocao = (
        (df_bev.shape[0] - df_bev_wo_outlier.shape[0]) / df_bev.shape[0]
    ) * 100

    logger = logging.getLogger(__name__)
    logger.info(f"Percentual de linhas removidas: {pct_remocao:.2f}%")

    return df_bev_wo_outlier


def generate_preprocessor() -> ColumnTransformer:
    """
    Gera um pré-processador para os dados.
    """

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OrdinalEncoder(),
                make_column_selector(dtype_include=object),
            ),
            (
                "numerical",
                StandardScaler(),
                make_column_selector(dtype_exclude=object),
            ),
        ]
    )
    return preprocessor


def generate_clustering_pipeline(preprocessor: ColumnTransformer) -> Pipeline:
    """
    Gera pipeline para clusterização.
    """

    clustering_pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "cluster",
                GaussianMixture(
                    n_components=4, init_params="kmeans", random_state=42
                ),
            ),
        ]
    )

    return clustering_pipeline


def generate_regressor(preprocessor: ColumnTransformer) -> Pipeline:
    """
    Gera pipeline para regressão.
    """

    regressor_pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(random_state=42)),
        ]
    )

    search_grid = {
        "regressor__bootstrap": [True, False],
        "regressor__max_depth": np.linspace(10, 100, 10).astype(int),
        "regressor__max_features": ["log2", "sqrt"],
        "regressor__min_samples_leaf": np.linspace(1, 10, 10).astype(int),
        "regressor__min_samples_split": np.linspace(2, 10, 5).astype(int),
        "regressor__n_estimators": np.linspace(100, 1000, 10).astype(int),
    }

    regressor = RandomizedSearchCV(
        regressor_pipeline, search_grid, n_jobs=6, n_iter=10, random_state=42
    )
    return regressor


def split_data(
    df_bev_wo_outlier: pd.DataFrame, features: list, target: str
) -> tuple:
    """
    Divide os dados em treino e teste.
    """

    X = df_bev_wo_outlier[features]
    y = df_bev_wo_outlier[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    cluster_cols: list,
    clustering_pipeline: Pipeline,
    regressor: Pipeline,
) -> tuple:
    """
    Treina o modelo.
    """

    clustering_pipeline.fit(X_train[cluster_cols])

    X_train["CLUSTER"] = clustering_pipeline.predict(X_train[cluster_cols])

    regressor.fit(X_train, y_train)
    return clustering_pipeline, regressor


def evaluate_model(
    X_test: pd.DataFrame,
    y_test: pd.Series,
    cluster_cols: list,
    clustering_pipeline: Pipeline,
    regressor: Pipeline,
) -> plt:
    """
    Gera métricas de avaliação do modelo e gera gráfico para avaliação visual.
    """

    X_test["CLUSTER"] = clustering_pipeline.predict(X_test[cluster_cols])
    y_pred = regressor.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100

    logger = logging.getLogger(__name__)
    logger.info(f"R2: {r2:.2f}")
    logger.info(f"MAE: {mae:.2f}")
    logger.info(f"MAPE: {mape:.2f}%")

    # Gerando gráfico
    df_pred = pd.concat([X_test, y_test], axis=1)
    df_pred["PREDICTION"] = y_pred

    df_pred["OUTLIER"] = np.where(
        abs(df_pred["PREDICTION"] - df_pred["SALE_PRICE"])
        / df_pred["SALE_PRICE"]
        > 0.65,
        1,
        0,
    )

    sns.scatterplot(
        data=df_pred,
        x="SALE_PRICE",
        y="PREDICTION",
        hue="OUTLIER",
        palette="bright",
    )
    plt.legend(title="MAPE > 65%")

    return plt
