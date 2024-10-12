"""
    Contém funções para analisar a correlação entre a produção agropecuária, precipitação e temperatura média anual em países desenvolvidos, emergentes e em desenvolvimento. 
    Os dados são provenientes de datasets sobre produção total, precipitação anual e temperatura. O código calcula as correlações entre essas variáveis para diferentes grupos de países.
"""
import pandas as pd 
import numpy as np
import os
import statsmodels.api as sm
import sys

# Adiciona o caminho do diretório 'clean' ao sistema
sys.path.append(
	os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)

import big_strings  # Importa strings relevantes

# Define o caminho para os datasets limpos
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

# Carrega os datasets de produção, precipitação e temperatura
df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)
df_precipitacao = pd.read_csv(os.path.join(path_data, 'precipitacao_anual.csv'), index_col=0)
df_temperatura = pd.read_csv(os.path.join(path_data, 'temperatura.csv'), index_col=0)

# Mescla os datasets por código do país e ano
df_merged1 = pd.merge(df_producao, df_precipitacao, on=['country_code', 'ano'], how='outer')
df_merged = pd.merge(df_merged1, df_temperatura, on=['country_code', 'ano'], how='outer')

# Filtrando os dados para países desenvolvidos, emergentes e em desenvolvimento
desenvolvidos = big_strings.paises_desenvolvidos
emergentes = big_strings.paises_emergentes

df_desenvolvidos = df_merged[df_merged['country_code'].isin(desenvolvidos)]
df_emergentes = df_merged[df_merged['country_code'].isin(emergentes)]
df_em_desenvolvimento = df_merged[~df_merged['country_code'].isin(desenvolvidos) & ~df_merged['country_code'].isin(emergentes)]

# Calcula e imprime as correlações para cada grupo de países
print('Total:', df_merged[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('Desenvolvidos:', df_desenvolvidos[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('Emergentes:', df_emergentes[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('Em Desenvolvimento:', df_em_desenvolvimento[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
