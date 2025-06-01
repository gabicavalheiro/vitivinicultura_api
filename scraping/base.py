#LOGICA BASE PARA SCRAPING

#Importa o módulo `requests`, que permite fazer **requisições HTTP**.
#Usado para acessar a página da web onde está a tabela que queremos extrair.

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

### - Define uma função chamada `fetch_table_from_url`.
#Recebe:
#`url`: endereço da página da web.
#table_index`: índice da tabela desejada (caso haja mais de uma na página).
#Retorna um `DataFrame` (tabela) com os dados.

def fetch_table_from_url(url: str, table_index: int = 0) -> pd.DataFrame:
    response = requests.get(url)
    #response.content conterá o HTML completo da página.
    soup = BeautifulSoup(response.content, 'html.parser')
    html = str(soup)
    #Importa o StringIO, que permite tratar uma string como se fosse um arquivo.
    #Necessário porque pd.read_html() espera um arquivo ou buffer, e não uma string diretamente.
    tables = pd.read_html(StringIO(html))
    #- `pandas.read_html()` procura automaticamente por `<table>` no HTML.
    #Retorna uma **lista de DataFrames** com todas as tabelas encontradas.
    #Envolvemos com `StringIO` para simular um arquivo de entrada.
    #Seleciona uma tabela específica da lista retornada.
    # Por padrão, é a primeira tabela (table_index=0), mas pode ser ajustado se houver várias.
    df = tables[table_index]
    #Converte NaN para None (compatível com JSON)
    df = df.where(pd.notna(df), None)  # <-- converte NaN para None (compatível com JSON)
    return df
#Retorna o DataFrame final, pronto para ser transformado em JSON, CSV, ou tratado em análise de dados
