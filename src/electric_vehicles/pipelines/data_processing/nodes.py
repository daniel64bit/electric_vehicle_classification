"""
Pipeline 'data_processing'
generated using Kedro 0.18.12
"""

import pandas as pd


def normalize_columns(columns: pd.Series) -> pd.Series:
    """
    Remove caracteres especiais e substitui espaços por "_",
    dada uma série de colunas.
    """
    return (
        columns.str.replace("[^-/\w\s]", "", regex=True)
        .str.replace("\s", "_", regex=True)
        .str.upper()
    )


def select_columns_by_type(df: pd.DataFrame, type: str) -> list:
    """
    Seleciona colunas de um dataframe com base no tipo de dado fornecido.
    """
    cols = df.select_dtypes(include=[type]).columns.to_list()
    return cols


def normalize_object_columns(
    df: pd.DataFrame, columns: list[str]
) -> pd.DataFrame:
    """
    Padroniza colunas do tipo string (objeto).
    """
    for col in columns:
        df[col] = (
            df[col]
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .str.upper()
        )

    return df


def normalize_date_columns(
    df: pd.DataFrame, columns: list[str], format: str
) -> pd.DataFrame:
    """
    Converte colunas de datas do tipo string para datetime,
    seguindo um formato especificado.
    """
    for col in columns:
        df[col] = pd.to_datetime(df[col], format=format)

    return df


def remove_outlier(
    df: pd.DataFrame, column: str, return_outlier: bool = False
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

    if return_outlier:
        return df[(df[column] < lower) | (df[column] > upper)]
    else:
        return df[(df[column] >= lower) & (df[column] <= upper)]


def normalize_vehicles_database(
    df_vehicles: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normaliza cabeçalho e conteúdo de colunas da base de dados de veículos.
    """

    df_vehicles.columns = normalize_columns(df_vehicles.columns)

    object_cols = select_columns_by_type(df_vehicles, "object")
    df_vehicles = normalize_object_columns(df_vehicles, object_cols)

    date_cols = ["SALE_DATE", "DOL_TRANSACTION_DATE"]
    df_vehicles = normalize_date_columns(
        df_vehicles, date_cols, format=("%B %d %Y")
    )

    return df_vehicles


def generate_bev_resale_database(
    normalized_df_vehicles: pd.DataFrame,
) -> pd.DataFrame:
    """
    Gera base de dados com transações de revenda de veículos elétricos
    para uso pessoal.
    Para tal, as seguintes regras foram seguidas:
    - Valor de venda válido (maior que zero);
    - Medição do odômetro válida
    - Veículos usados
    - Veículos puramente elétricos
    - Mínimo de 1 ano de uso
    - Carros para uso pessoal
    """

    # Filtrando transações de venda de veículos usados e
    # puramente elétricos com quilometragem válida.
    df_bev = normalized_df_vehicles[
        (normalized_df_vehicles["SALE_PRICE"] > 0)
        & (
            normalized_df_vehicles["CLEAN_ALTERNATIVE_FUEL_VEHICLE_TYPE"]
            == "BATTERY ELECTRIC VEHICLE (BEV)"
        )
        & (normalized_df_vehicles["ODOMETER_CODE"] == "ACTUAL MILEAGE")
        & (normalized_df_vehicles["NEW_OR_USED_VEHICLE"] == "USED")
        & (normalized_df_vehicles["VEHICLE_PRIMARY_USE"] == "PASSENGER")
    ].copy()

    # Criando novas features
    # Idade do carro
    df_bev["CAR_AGE"] = df_bev["TRANSACTION_YEAR"] - df_bev["MODEL_YEAR"]
    # Mês da venda
    df_bev["SALE_MONTH"] = (
        df_bev["SALE_DATE"].dt.strftime("%m").astype("int64")
    )
    # Preço de venda acima do preço de tabela
    df_bev["SALE_ABOVE_MSRP"] = (
        df_bev["SALE_PRICE"] > df_bev["BASE_MSRP"]
    ).astype("int64")

    # Filtrando carros com no mínimo 1 ano de uso
    df_bev = df_bev[df_bev["CAR_AGE"] >= 1].reset_index(drop=True)

    return df_bev
