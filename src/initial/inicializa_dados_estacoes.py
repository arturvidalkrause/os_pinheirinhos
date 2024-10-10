import pandas as pd
from pathlib import Path
import os

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

# Salvar o DataFrame em um novo arquivo CSV (se necessário)
df_uploaded.to_parquet(path_atual / file_path_write, engine="pyarrow", index=False)
