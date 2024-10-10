import pandas as pd
import numpy as np
import os

path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)

df_temperatura = pd.read_csv(os.path.join(path_data, 'temperatura.csv'), index_col=0)

df_merged = pd.merge(df_producao, df_temperatura, on=['country_code', 'ano'], how='outer')

df_brasil = df_merged[df_merged['country_code']=='BRA']

print(df_brasil)
print(df_brasil[['producao_total(t)', 'temperatura_media_anual(°C)']].corr())

print(df_merged)
print(df_merged[['producao_total(t)', 'temperatura_media_anual(°C)']].corr())