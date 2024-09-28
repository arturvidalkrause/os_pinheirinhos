"""Trata todos os dados da tabela 'Preciptação_mes_a_mes.csv'"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Diretório da tabela a ser tratada
path_data= os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos/Precipitação_mes_a_mes.xlsx")

df = pd.read_excel(path_data)

# print(df.columns[2:])

year_columns = [col[:4] for col in df.columns]

df_year = df.groupby(year_columns, axis=1).sum()

# Escolher um pais específico
ano_especifico = 2024
serie = df_year[df_year['code'] == "BRA"]

anos = df_year.index.tolist()
valores = serie.values[0][:-2].tolist()
print(anos)
print(valores)

# plt.figure(figsize=(30, 10))  # Tamanho do gráfico
# plt.bar(anos, valores, marker='o', linestyle='-', color='b')

# # Adicionar título e rótulos aos eixos
# plt.title('Precipitação ao longo dos anos (1901-2022)', fontsize=14)
# plt.xlabel('Ano', fontsize=12)
# plt.ylabel('Precipitação (mm)', fontsize=12)

# # Exibir o gráfico
# # plt.grid(True)
# plt.show()