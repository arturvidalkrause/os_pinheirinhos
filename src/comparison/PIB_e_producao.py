"""
    Contém funções para analisar a correlação entre a produção total agropecuária e o PIB em diferentes regiões e países, como Brasil, China, União Europeia, 
    América do Sul e África. Utiliza os datasets de produção total e área de produção combinados com o PIB. As correlações são calculadas usando o coeficiente de correlação de Spearman.

    O código carrega os dados de produção e PIB, realiza o merge entre esses datasets e separa os dados por região. Em seguida, ele calcula as correlações para cada região 
    (União Europeia, América do Sul, África e China) e para o Brasil, especificamente. As correlações ajudam a entender a relação entre produção agrícola e o PIB em diferentes contextos.
"""
import pandas as pd
import numpy as np
import os
from scipy.stats import pearsonr, spearmanr

# Definindo o caminho dos datasets limpos
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

# Carregando os datasets
df_producao = pd.read_parquet(os.path.join(path_data, 'producao_total_e_area.parquet'))
df_pib = pd.read_parquet(os.path.join(path_data, 'PIB.parquet'))

# Mesclando os datasets de produção e PIB com base no código do país e ano
merged_df = pd.merge(df_producao, df_pib, on=['country_code', 'ano'])

# Filtrando os dados do Brasil e da China
merged_df_brasil = merged_df[merged_df['country_code'] == 'BRA']
merged_df_china = merged_df[merged_df['country_code'] == 'CHN']

# Códigos de países da União Europeia
ue_country_codes = [
    "AUT", "BEL", "BGR", "HRV", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
    "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"
]

# Códigos de países da América do Sul
south_america_country_codes = [
    "ARG", "BOL", "BRA", "CHL", "COL", "ECU", "GUY", "PRY", "PER", "SUR", "URY", "VEN"
]

# Códigos de países da África
africa_country_codes = [
    "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CPV", "CMR", "CAF", "TCD", "COM", "COD", "COG", 
    "DJI", "EGY", "GNQ", "ERI", "SWZ", "ETH", "GAB", "GMB", "GHA", "GIN", "KEN", "LSO", "LBR", 
    "LBY", "MDG", "MWI", "MLI", "MRT", "MUS", "NAM", "NGA", "RWA", "STP", "SEN", "SYC", "SLE", 
    "SOM", "ZAF", "SSD", "SDN", "TZA", "TGO", "TUN", "UGA", "ZMB", "ZWE"
]

# Filtrando os dados por região
merged_df_EU = merged_df[merged_df['country_code'].isin(ue_country_codes)]
merged_df_SA = merged_df[merged_df['country_code'].isin(south_america_country_codes)]
merged_df_africa = merged_df[merged_df['country_code'].isin(africa_country_codes)]

# Limpando os DataFrames removendo valores nulos e mantendo apenas as colunas de interesse
df_clean_china = merged_df_china[['producao_total(t)', 'PIB']].dropna()
df_clean_EU = merged_df_EU[['producao_total(t)', 'PIB']].dropna()
df_clean_SA = merged_df_SA[['producao_total(t)', 'PIB']].dropna()
df_clean_africa = merged_df_africa[['producao_total(t)', 'PIB']].dropna()

# Calculando e imprimindo a matriz de correlação para o Brasil
print(merged_df_brasil)
print(merged_df_brasil[['producao_total(t)', 'area_total_de_producao(ha)', 'PIB']].corr())

# Calculando as correlações de Spearman para cada região
print(df_clean_EU)
print('União Europeia:', spearmanr(df_clean_EU['producao_total(t)'], df_clean_EU['PIB']))
print('América do Sul:', spearmanr(df_clean_SA['producao_total(t)'], df_clean_SA['PIB']))
print('África:', spearmanr(df_clean_africa['producao_total(t)'], df_clean_africa['PIB']))
print('China:', spearmanr(df_clean_china['producao_total(t)'], df_clean_china['PIB']))
