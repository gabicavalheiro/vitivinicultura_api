import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from io import StringIO

def get_processamento_data():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        html = str(soup)

        # Lê todas as tabelas
        tables = pd.read_html(StringIO(html))

        # Converte todas para listas de dicionários, tratando NaN/infs
        result = []
        for df in tables:
            df_clean = df.replace([np.nan, np.inf, -np.inf], None)
            result.append(df_clean.to_dict(orient="records"))

        return result

    except Exception as e:
        return {"erro": str(e)}
