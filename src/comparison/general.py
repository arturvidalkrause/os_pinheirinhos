import pandas as pd
import numpy as np
import os
from functools import reduce

path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

df_emissoes = pd.read_csv(os.path.join(path_data, 'emissoes_co2.csv'), index_col=0)
df_fertilizantes = pd.read_csv(os.path.join(path_data, 'fertilizantes_total.csv'), index_col=0)
df_PIB = pd.read_csv(os.path.join(path_data, 'PIB.csv'), index_col=0)
df_precipitacao = pd.read_csv(os.path.join(path_data, 'precipitacao_anual.csv'), index_col=0)
df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)
df_temperatura = pd.read_csv(os.path.join(path_data, 'temperatura.csv'), index_col=0)

dataframes = [df_emissoes, df_fertilizantes, df_PIB, df_precipitacao, df_producao, df_temperatura]

merged_df = reduce(lambda left, right: pd.merge(left, right, on=['country_code', 'ano'], how='outer'), dataframes)

print(merged_df.columns)
print(merged_df[['Annual CO₂ emissions',
       'uso_total_de_fertilizantes(t)', 'PIB', 'precipitação_anual',
       'producao_total(t)', 'area_total_de_producao(ha)',
       'temperatura_media_anual(°C)']].corr().to_string())