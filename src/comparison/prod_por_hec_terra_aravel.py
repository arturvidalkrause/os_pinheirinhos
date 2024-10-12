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
df = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)

df['producao_por_hectare'] = df['producao_total(t)'] / df['area_total_de_producao(ha)']

df = df.dropna(subset=['producao_por_hectare'])

coeficientes = {}

for country in df['country_code'].unique():
    df_country = df[df['country_code'] == country]
    
    # Verificar se há dados suficientes para a regressão
    if len(df_country) > 1:
        # Definir variáveis dependente (Y) e independente (X)
        X = df_country['ano']
        y = df_country['producao_por_hectare']
        
        # Adicionar constante para o modelo
        X = sm.add_constant(X)
        
        # Ajustar o modelo
        model = sm.OLS(y, X).fit()
        
        # Armazenar o coeficiente da variável ano
        coeficientes[country] = model.params['ano']

coeficientes_df = pd.DataFrame(list(coeficientes.items()), columns=['country_code', 'coeficiente'])

desenvolvidos = big_strings.paises_desenvolvidos
emergentes = big_strings.paises_emergentes

df_desenvolvidos = coeficientes_df[coeficientes_df['country_code'].isin(desenvolvidos)]
df_emergentes = coeficientes_df[coeficientes_df['country_code'].isin(emergentes)]
df_em_desenvolvimento = coeficientes_df[~coeficientes_df['country_code'].isin(desenvolvidos) & ~coeficientes_df['country_code'].isin(emergentes)]

df_clean_desenvolvidos = df_desenvolvidos.dropna()
df_clean_emergentes = df_emergentes.dropna()
df_clean_em_desenvolvimento = df_em_desenvolvimento.dropna()

print(df)
print(coeficientes_df)
print(df_clean_desenvolvidos.describe())
print(df_clean_emergentes.describe())
print(df_clean_em_desenvolvimento.describe())

peso_desenvolvidos = len(df_clean_desenvolvidos)/(len(df_clean_desenvolvidos) + len(df_clean_em_desenvolvimento) + len(df_clean_emergentes))
peso_emergentes = len(df_clean_emergentes)/(len(df_clean_desenvolvidos) + len(df_clean_em_desenvolvimento) + len(df_clean_emergentes))
peso_em_desenvolvimento = len(df_clean_em_desenvolvimento)/(len(df_clean_desenvolvidos) + len(df_clean_em_desenvolvimento) + len(df_clean_emergentes))

var_desenvolvidos = df_clean_em_desenvolvimento['coeficiente'].var()
var_emergentes = df_clean_emergentes['coeficiente'].var()
var_em_desenvolvimento = df_clean_em_desenvolvimento['coeficiente'].var()

df_clean_emergentes['status'] = 'emergente'
df_clean_desenvolvidos['status'] = 'desenvolvido'
df_clean_em_desenvolvimento['status'] = 'em desenvolvimento'

df_total = pd.concat([df_clean_desenvolvidos, df_clean_em_desenvolvimento, df_clean_emergentes])
print(df_total)

var_total = df_total['coeficiente'].var()

r_squared = 1 - (peso_desenvolvidos * var_desenvolvidos + peso_emergentes * var_emergentes + peso_em_desenvolvimento * var_em_desenvolvimento) / var_total


print(f'Variância para países desenvolvidos: {var_desenvolvidos:.4f}')
print(f'Variância para países emergentes: {var_emergentes:.4f}')
print(f'Variância para países em desenvolvimento: {var_em_desenvolvimento:.4f}')
print(f'Variância total: {var_total:.4f}')
print(f'R²: {r_squared:.4f}')