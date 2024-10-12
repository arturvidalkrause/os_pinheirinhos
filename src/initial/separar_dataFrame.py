"""
    Este módulo particiona um arquivo CSV muito grande em dois arquivos Parquet menores para que possam ser salvos no GitHub, que possui limitações de tamanho de arquivo.

    O arquivo `temperatura_mes_a_mes.csv` é dividido em dois arquivos menores:
    - `temperatura_mes_a_mes1.parquet`
    - `temperatura_mes_a_mes2.parquet`

"""

import pandas as pd
import numpy as np
import os

# Diretório atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho para o arquivo .csv
csv_path = os.path.join(script_dir, "temperatura_mes_a_mes.csv")

# Carrega o arquivo CSV
df = pd.read_csv(csv_path)

# Particiona o DataFrame em dois e salva em arquivos .parquet separados
serie1 = df.index >= df.shape[0] / 2  # Seleciona a segunda metade do DataFrame
serie2 = df.index < df.shape[0] / 2   # Seleciona a primeira metade do DataFrame

df1 = df[serie1]  # Segunda metade
df1.to_parquet("data/temperatura_mes_a_mes1.parquet", engine="pyarrow")

df2 = df[serie2]  # Primeira metade
df2.to_parquet("data/temperatura_mes_a_mes2.parquet", engine="pyarrow")
