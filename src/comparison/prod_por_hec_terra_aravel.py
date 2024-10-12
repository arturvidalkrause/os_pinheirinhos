"""
    Contém funções para analisar a relação entre a produção por hectare ao longo do tempo em diferentes grupos de países (desenvolvidos, emergentes e em desenvolvimento).
    O código utiliza uma regressão linear para calcular o coeficiente de crescimento da produção por hectare (produção total/área total) em cada país ao longo do tempo.
    Além disso, calcula-se a variância dos coeficientes para cada grupo de países e o R² ponderado para avaliar a qualidade da explicação dos coeficientes obtidos.
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
df = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)

# Calcula a produção por hectare
df['producao_por_hectare'] = df['producao_total(t)'] / df['area_total_de_producao(ha)']

# Remove as linhas com valores nulos para a produção por hectare
df = df.dropna(subset=['producao_por_hectare'])

# Dicionário para armazenar os coeficientes de regressão de cada país
coeficientes = {}

# Regressão para cada país
for country in df['country_code'].unique():
	df_country = df[df['country_code'] == country]
    
    # Verifica se há dados suficientes para a regressão
	if len(df_country) > 1:
        # Variáveis dependente (y) e independente (X)
		X = df_country['ano']
		y = df_country['producao_por_hectare']
        
        # Adiciona uma constante ao modelo
		X = sm.add_constant(X)
        
        # Ajusta o modelo de regressão linear
		model = sm.OLS(y, X).fit()
        
        # Armazena o coeficiente do ano (representando a tendência ao longo do tempo)
		coeficientes[country] = model.params['ano']

# Cria um DataFrame com os coeficientes obtidos para cada país
coeficientes_df = pd.DataFrame(list(coeficientes.items()), columns=['country_code', 'coeficiente'])

# Grupos de países (desenvolvidos, emergentes e em desenvolvimento)
desenvolvidos = big_strings.paises_desenvolvidos
emergentes = big_strings.paises_emergentes

# Divide os coeficientes por grupo de países
df_desenvolvidos = coeficientes_df[coeficientes_df['country_code'].isin(desenvolvidos)]
df_emergentes = coeficientes_df[coeficientes_df['country_code'].isin(emergentes)]
df_em_desenvolvimento = coeficientes_df[~coeficientes_df['country_code'].isin(desenvolvidos) & ~coeficientes_df['country_code'].isin(emergentes)]

# Remove valores nulos dos DataFrames de cada grupo de países
df_clean_desenvolvidos = df_desenvolvidos.dropna()
df_clean_emergentes = df_emergentes.dropna()
df_clean_em_desenvolvimento = df_em_desenvolvimento.dropna()

# Exibe os resultados
print(df)
print(coeficientes_df)
print(df_clean_desenvolvidos.describe())
print(df_clean_emergentes.describe())
print(df_clean_em_desenvolvimento.describe())

# Calcula os pesos para o cálculo do R² ponderado
peso_desenvolvidos = len(df_clean_desenvolvidos) / (len(df_clean_desenvolvidos) + len(df_clean_em_desenvolvimento) + len(df_clean_emergentes))
peso_emergentes = len(df_clean_emergentes) / (len(df_clean_desenvolvidos) + len(df_clean_em_desenvolvimento) + len(df_clean_emergentes))
peso_em_desenvolvimento = len(df_clean_em_desenvolvimento) / (len(df_clean_desenvolvidos) + len(df_clean_em_desenvolvimento) + len(df_clean_emergentes))

# Calcula a variância dos coeficientes em cada grupo de países
var_desenvolvidos = df_clean_em_desenvolvimento['coeficiente'].var()
var_emergentes = df_clean_emergentes['coeficiente'].var()
var_em_desenvolvimento = df_clean_em_desenvolvimento['coeficiente'].var()

# Adiciona uma coluna de status para cada grupo
df_clean_emergentes['status'] = 'emergente'
df_clean_desenvolvidos['status'] = 'desenvolvido'
df_clean_em_desenvolvimento['status'] = 'em desenvolvimento'

# Combina todos os grupos em um único DataFrame
df_total = pd.concat([df_clean_desenvolvidos, df_clean_em_desenvolvimento, df_clean_emergentes])
print(df_total)

# Calcula a variância total dos coeficientes
var_total = df_total['coeficiente'].var()

# Calcula o R² ponderado
r_squared = 1 - (peso_desenvolvidos * var_desenvolvidos + peso_emergentes * var_emergentes + peso_em_desenvolvimento * var_em_desenvolvimento) / var_total

# Exibe os resultados de variância e R²
print(f'Variância para países desenvolvidos: {var_desenvolvidos:.4f}')
print(f'Variância para países emergentes: {var_emergentes:.4f}')
print(f'Variância para países em desenvolvimento: {var_em_desenvolvimento:.4f}')
print(f'Variância total: {var_total:.4f}')
print(f'R²: {r_squared:.4f}')
