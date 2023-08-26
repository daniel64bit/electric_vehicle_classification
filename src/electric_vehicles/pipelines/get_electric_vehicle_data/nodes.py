"""
Pipeline 'get_electric_vehicle_data'
generated using Kedro 0.18.12
"""
import requests


def download_data(url: str, save_path: str) -> None:
    """
    Função que carrega base de dados de um dado endereço na internet.
    """
    data = requests.get(url)

    # Verifica se o download foi bem sucedido
    if data.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(data.content)
    else:
        print("Erro ao carregar dados.")
