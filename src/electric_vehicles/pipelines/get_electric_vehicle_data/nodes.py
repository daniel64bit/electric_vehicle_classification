"""
Pipeline 'get_electric_vehicle_data'
generated using Kedro 0.18.12
"""
import requests
import pandas as pd
from io import BytesIO


def download_data(url: str) -> pd.DataFrame:
    """
    Função que carrega base de dados de um dado endereço na internet.
    """
    data = requests.get(url)

    # Verifica se o download foi bem sucedido
    if data.status_code == 200:
        return pd.read_csv(BytesIO(data.content), sep=',')
    else:
        print("Erro ao carregar dados.")
