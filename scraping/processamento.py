import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from io import StringIO

URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"

def get_data():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        html = str(soup)

        # Lê todas as tabelas
        tables = pd.read_html(StringIO(html))

        # Converte todas para listas de dicionários, tratando NaN/infs
        result = []
        for df in tables:
            # Adiciona tratamento específico para dados de processamento
            df_clean = df.replace([np.nan, np.inf, -np.inf], None)
            # Converte colunas numéricas para float
            for col in df_clean.select_dtypes(include=['int64', 'float64']).columns:
                df_clean[col] = df_clean[col].astype(float)
            # Adiciona metadados para ML
            data_dict = {
                "data": df_clean.to_dict(orient="records"),
                "features": list(df_clean.columns),
                "numeric_features": list(df_clean.select_dtypes(include=['int64', 'float64']).columns)
            }
            result.append(data_dict)

        return result

    except Exception as e:
        return {"erro": str(e)}
