import pandas as pd
import numpy as np
import os
from scipy.stats import pearsonr, spearmanr
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)
import big_strings

path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)
df_pib = pd.read_csv(os.path.join(path_data, 'PIB.csv'), index_col=0)

merged_df = pd.merge(df_producao, df_pib, on=['country_code', 'ano'])
merged_paises = merged_df[merged_df['country_code'] != 'WLD']
desenvolvidos = big_strings.paises_desenvolvidos
emergentes = big_strings.paises_emergentes

df_desenvolvidos = merged_df[merged_df['country_code'].isin(desenvolvidos)]
df_emergentes = merged_df[merged_df['country_code'].isin(emergentes)]
df_em_desenvolvimento = merged_df[~merged_df['country_code'].isin(desenvolvidos) & ~merged_df['country_code'].isin(emergentes)]

df_clean_desenvolvidos = df_desenvolvidos[['producao_total(t)', 'PIB']].dropna()
df_clean_emergentes = df_emergentes[['producao_total(t)', 'PIB']].dropna()
df_clean_em_desenvolvimento = df_em_desenvolvimento[['producao_total(t)', 'PIB']].dropna()

# Calcular as correlações
correlações_desenvolvidos = {}
for country in df_desenvolvidos['country_code'].unique():
    df_pais = df_desenvolvidos[df_desenvolvidos['country_code'] == country]
    corr = df_pais[['producao_total(t)', 'PIB']].corr()
    correlações_desenvolvidos[country] = corr

correlações_emergentes = {}
for country in df_emergentes['country_code'].unique():
    df_pais = df_emergentes[df_emergentes['country_code'] == country]
    corr = df_pais[['producao_total(t)', 'PIB']].corr()
    correlações_emergentes[country] = corr

correlações_em_desenvolvimento = {}
for country in df_em_desenvolvimento['country_code'].unique():
    df_pais = df_em_desenvolvimento[df_em_desenvolvimento['country_code'] == country]
    corr = df_pais[['producao_total(t)', 'PIB']].corr()
    correlações_em_desenvolvimento[country] = corr

# Extrair as correlações para um DataFrame
correlacoes_list = []
for country, corr in correlações_desenvolvidos.items():
    correlacoes_list.append({
        'country_code': country,
        'correlation': corr.loc['producao_total(t)', 'PIB'],
        'status': 'Desenvolvido'
    })

for country, corr in correlações_emergentes.items():
    correlacoes_list.append({
        'country_code': country,
        'correlation': corr.loc['producao_total(t)', 'PIB'],
        'status': 'Emergente'
    })

for country, corr in correlações_em_desenvolvimento.items():
    correlacoes_list.append({
        'country_code': country,
        'correlation': corr.loc['producao_total(t)', 'PIB'],
        'status': 'Em Desenvolvimento'
    })

correlacoes_df = pd.DataFrame(correlacoes_list)

# Calcular a variância das correlações
var_desenvolvidos = np.var(correlacoes_df[correlacoes_df['status'] == 'Desenvolvido']['correlation'], ddof=1)
var_emergentes = np.var(correlacoes_df[correlacoes_df['status'] == 'Emergente']['correlation'], ddof=1)
var_em_desenvolvimento = np.var(correlacoes_df[correlacoes_df['status'] == 'Em Desenvolvimento']['correlation'], ddof=1)

# Calcular a variância total
var_total = np.var(correlacoes_df['correlation'], ddof=1)

# Calcular R² ponderado
peso_desenvolvidos = len(correlacoes_df[correlacoes_df['status'] == 'Desenvolvido']) / len(correlacoes_df)
peso_emergentes = len(correlacoes_df[correlacoes_df['status'] == 'Emergente']) / len(correlacoes_df)
peso_em_desenvolvimento = len(correlacoes_df[correlacoes_df['status'] == 'Em Desenvolvimento']) / len(correlacoes_df)

r_squared = 1 - (peso_desenvolvidos * var_desenvolvidos + peso_emergentes * var_emergentes + peso_em_desenvolvimento * var_em_desenvolvimento) / var_total


merged_paises_limpo = merged_paises.dropna()


# Imprimir os resultados
print(f'Variância para países desenvolvidos: {var_desenvolvidos:.4f}')
print(f'Variância para países emergentes: {var_emergentes:.4f}')
print(f'Variância para países em desenvolvimento: {var_em_desenvolvimento:.4f}')
print(f'Variância total: {var_total:.4f}')
print(f'R²: {r_squared:.4f}')
print('Correlação total:', pearsonr(merged_paises_limpo['PIB'], merged_paises_limpo['producao_total(t)']))