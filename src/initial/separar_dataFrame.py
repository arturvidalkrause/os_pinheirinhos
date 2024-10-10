"""Particiona arquivos muito grandes para salvar no github

O arquivo temperatura_mes_a_mes.csv tinha cerca de 130MB e o guithub não aceitou o tamanho do arquivo"""

import pandas as pd
import numpy as np
import os

# Diretório atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho para arquivo .csv
csv_path = os.path.join(script_dir, "temperatura_mes_a_mes.csv")

df = pd.read_csv(csv_path)

# Particiona o dataFrame em dois e salva em arquivos .parquets separados
serie1 = df.index >= df.shape[0]/2
serie2 = df.index < df.shape[0]/2

df1 = df[serie1]
df1.to_parquet("data/temperatura_mes_a_mes1.parquet", engine="pyarrow")

df2 = df[serie2]
df2.to_parquet("data/temperatura_mes_a_mes2.parquet", engine="pyarrow")
