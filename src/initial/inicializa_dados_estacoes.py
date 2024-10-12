"""
    Este módulo carrega um arquivo de largura fixa contendo dados sobre estações meteorológicas, trata e transforma os dados em um DataFrame pandas, e em seguida, salva o resultado em formato Parquet.

    Passos realizados:
    1. Define-se o caminho do arquivo de entrada e o caminho de saída.
    2. Carrega o arquivo de entrada com base nas especificações manuais de larguras de colunas.
    3. Define nomes de colunas adequados para o DataFrame resultante.
    4. Exibe as primeiras linhas do DataFrame para visualização.
    5. Salva o DataFrame processado em um arquivo Parquet.

    O arquivo de saída será salvo no diretório especificado como Parquet com o uso do motor 'pyarrow'.
"""

import pandas as pd
from pathlib import Path
import os

# Define o caminho atual do diretório de trabalho
path_atual = os.getcwd()

# Carregar o arquivo no caminho especificado
file_path_read = Path('data/brutos/dados_sobre_estacoes_metereologicas.inv')
file_path_write = Path('data/tratados/dados_sobre_estacoes_metereologicas.parquet')

# Definir as larguras das colunas manualmente (usando colspecs)
colspecs = [(0, 12), (12, 21), (22, 30), (31, 37), (38, 100)]  # Ajustar conforme necessário

# Carregar o arquivo de largura fixa com as larguras de coluna especificadas
df_uploaded = pd.read_fwf(path_atual / file_path_read, colspecs=colspecs, header=None)

# Definir os nomes das colunas
df_uploaded.columns = ['Station_ID', 'Latitude', 'Longitude', 'Elevation', 'Location_Name']

# Exibir as primeiras linhas do DataFrame
print(df_uploaded.head())

# Salvar o DataFrame em um novo arquivo Parquet (se necessário)
df_uploaded.to_parquet(path_atual / file_path_write, engine="pyarrow", index=False)