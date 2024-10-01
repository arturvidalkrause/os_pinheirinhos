import pandas as pd
import numpy as np
import os

path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)

df_pib = pd.read_csv(os.path.join(path_data, 'PIB.csv'), index_col=0)

merged_df = pd.merge(df_producao, df_pib, on=['country_code', 'ano'])

merged_df_brasil = merged_df[merged_df['country_code'] == 'BRA']

print(merged_df_brasil)
print(merged_df_brasil[['producao_total(t)', 'area_total_de_producao(ha)', 'PIB']].corr())
# print(merged_df_brasil[['producao_total(t)', 'PIB']].corr())