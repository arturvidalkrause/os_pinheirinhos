import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import sys

sys.path.append(
	os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)

import big_strings

path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")
df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)
df_precipitacao = pd.read_csv(os.path.join(path_data, 'precipitacao_anual.csv'), index_col=0)
df_temperatura = pd.read_csv(os.path.join(path_data, 'temperatura.csv'), index_col=0)

df_merged1 = pd.merge(df_producao, df_precipitacao, on=['country_code', 'ano'], how='outer')
df_merged = pd.merge(df_merged1, df_temperatura, on=['country_code', 'ano'], how='outer')

desenvolvidos = big_strings.paises_desenvolvidos
emergentes = big_strings.paises_emergentes

df_desenvolvidos = df_merged[df_merged['country_code'].isin(desenvolvidos)]
df_emergentes = df_merged[df_merged['country_code'].isin(emergentes)]
df_em_desenvolvimento = df_merged[~df_merged['country_code'].isin(desenvolvidos) & ~df_merged['country_code'].isin(emergentes)]


print('total:',df_merged[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())

print('desenvolvidos:', df_desenvolvidos[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('emergentes:', df_emergentes[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('em desenvolvimento:', df_em_desenvolvimento[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())

