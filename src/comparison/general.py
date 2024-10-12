"""
    Este módulo carrega múltiplos datasets relacionados a emissões de CO₂, uso de fertilizantes, PIB, precipitação, produção agropecuária e temperatura média anual. 
    Ele mescla todos os DataFrames com base no código do país e no ano, e calcula a correlação entre as variáveis selecionadas. O resultado final exibe a matriz de 
    correlação entre as principais variáveis ambientais e econômicas para análise de tendências.

    O arquivo final gerado é um DataFrame mesclado que contém dados sobre emissões de CO₂, uso de fertilizantes, PIB, precipitação, produção agropecuária, área de produção 
    e temperatura média anual. A função de mesclagem e correlação permite observar a relação entre essas variáveis.
"""
import pandas as pd
import numpy as np
import os
from functools import reduce

# Definindo o caminho dos datasets limpos
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

# Carregando os datasets
df_emissoes = pd.read_csv(os.path.join(path_data, 'emissoes_co2.csv'), index_col=0)
df_fertilizantes = pd.read_csv(os.path.join(path_data, 'fertilizantes_total.csv'), index_col=0)
df_PIB = pd.read_csv(os.path.join(path_data, 'PIB.csv'), index_col=0)
df_precipitacao = pd.read_csv(os.path.join(path_data, 'precipitacao_anual.csv'), index_col=0)
df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)
df_temperatura = pd.read_csv(os.path.join(path_data, 'temperatura.csv'), index_col=0)

# Lista contendo os DataFrames a serem mesclados
dataframes = [df_emissoes, df_fertilizantes, df_PIB, df_precipitacao, df_producao, df_temperatura]

# Mesclando os DataFrames com base em 'country_code' e 'ano'
merged_df = reduce(lambda left, right: pd.merge(left, right, on=['country_code', 'ano'], how='outer'), dataframes)

# Exibindo as colunas do DataFrame mesclado
print(merged_df.columns)

# Exibindo a matriz de correlação entre as variáveis selecionadas
print(merged_df[['Annual CO₂ emissions',
       'uso_total_de_fertilizantes(t)', 'PIB', 'precipitação_anual',
       'producao_total(t)', 'area_total_de_producao(ha)',
       'temperatura_media_anual(°C)']].corr().to_string())
