"""
    Este módulo realiza a análise de correlação entre a produção total, precipitação anual e temperatura média anual, separando os dados em três categorias de países: desenvolvidos, emergentes e em desenvolvimento.

    A análise inclui o cálculo de correlações para o conjunto total de dados e para cada grupo de países individualmente.

    A saída consiste nas correlações entre as variáveis "producao_total(t)", "precipitação_anual" e "temperatura_media_anual(°C)" para o total de países, bem como para os três grupos (desenvolvidos, emergentes e em desenvolvimento).
"""

import pandas as pd
import os
import sys

# Adicionando o caminho para importar módulos locais
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)

import big_strings

# Caminho para os dados
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

# Carregando os datasets de produção, precipitação e temperatura
df_producao = pd.read_parquet(os.path.join(path_data, 'producao_total_e_area.parquet'))
df_precipitacao = pd.read_parquet(os.path.join(path_data, 'precipitacao_anual.parquet'))
df_temperatura = pd.read_parquet(os.path.join(path_data, 'temperatura.parquet'))

# Convertendo os anos para int
df_producao['ano'] = df_producao['ano'].astype(int)
df_precipitacao['ano'] = df_precipitacao['ano'].astype(int)
df_temperatura['ano'] = df_temperatura['ano'].astype(int)

# Unindo os DataFrames de produção, precipitação e temperatura
df_merged1 = pd.merge(df_producao, df_precipitacao, on=['country_code', 'ano'], how='outer')
df_merged = pd.merge(df_merged1, df_temperatura, on=['country_code', 'ano'], how='outer')

# Filtrando países desenvolvidos e emergentes com base em big_strings
desenvolvidos = big_strings.paises_desenvolvidos
emergentes = big_strings.paises_emergentes

df_desenvolvidos = df_merged[df_merged['country_code'].isin(desenvolvidos)]
df_emergentes = df_merged[df_merged['country_code'].isin(emergentes)]
df_em_desenvolvimento = df_merged[~df_merged['country_code'].isin(desenvolvidos) & ~df_merged['country_code'].isin(emergentes)]

# Exibindo correlações para o conjunto total e para cada grupo de países
print('total:', df_merged[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())

print('desenvolvidos:', df_desenvolvidos[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('emergentes:', df_emergentes[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())
print('em desenvolvimento:', df_em_desenvolvimento[['producao_total(t)', 'precipitação_anual', 'temperatura_media_anual(°C)']].corr())