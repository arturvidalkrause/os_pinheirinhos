import pandas as pd
import numpy as np
import os
from scipy.stats import pearsonr, spearmanr

path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos")

df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)

df_pib = pd.read_csv(os.path.join(path_data, 'PIB.csv'), index_col=0)

merged_df = pd.merge(df_producao, df_pib, on=['country_code', 'ano'])

merged_df_brasil = merged_df[merged_df['country_code'] == 'BRA']

merged_df_china = merged_df[merged_df['country_code'] == 'CHN']


ue_country_codes = [
    "AUT",  # Áustria
    "BEL",  # Bélgica
    "BGR",  # Bulgária
    "HRV",  # Croácia
    "CZE",  # República Checa
    "DNK",  # Dinamarca
    "EST",  # Estônia
    "FIN",  # Finlândia
    "FRA",  # França
    "DEU",  # Alemanha
    "GRC",  # Grécia
    "HUN",  # Hungria
    "IRL",  # Irlanda
    "ITA",  # Itália
    "LVA",  # Letônia
    "LTU",  # Lituânia
    "LUX",  # Luxemburgo
    "MLT",  # Malta
    "NLD",  # Países Baixos
    "POL",  # Polônia
    "PRT",  # Portugal
    "ROU",  # Romênia
    "SVK",  # Eslováquia
    "SVN",  # Eslovênia
    "ESP",  # Espanha
    "SWE"   # Suécia
]

south_america_country_codes = [
    "ARG",  # Argentina
    "BOL",  # Bolívia
    "BRA",  # Brasil
    "CHL",  # Chile
    "COL",  # Colômbia
    "ECU",  # Equador
    "GUY",  # Guiana
    "PRY",  # Paraguai
    "PER",  # Peru
    "SUR",  # Suriname
    "URY",  # Uruguai
    "VEN"   # Venezuela
]

africa_country_codes = [
    "DZA",  # Argélia
    "AGO",  # Angola
    "BEN",  # Benin
    "BWA",  # Botswana
    "BFA",  # Burkina Faso
    "BDI",  # Burundi
    "CPV",  # Cabo Verde
    "CMR",  # Camarões
    "CAF",  # República Centro-Africana
    "TCD",  # Chade
    "COM",  # Comores
    "COD",  # República Democrática do Congo
    "COG",  # República do Congo
    "DJI",  # Djibuti
    "EGY",  # Egito
    "GNQ",  # Guiné Equatorial
    "ERI",  # Eritreia
    "SWZ",  # Essuatíni
    "ETH",  # Etiópia
    "GAB",  # Gabão
    "GMB",  # Gâmbia
    "GHA",  # Gana
    "GIN",  # Guiné
    "KEN",  # Quênia
    "LSO",  # Lesoto
    "LBR",  # Libéria
    "LBY",  # Líbia
    "MDG",  # Madagascar
    "MWI",  # Malawi
    "MLI",  # Mali
    "MRT",  # Mauritânia
    "MUS",  # Maurício
    "NAM",  # Namíbia
    "NGA",  # Nigéria
    "RWA",  # Ruanda
    "STP",  # São Tomé e Príncipe
    "SEN",  # Senegal
    "SYC",  # Seicheles
    "SLE",  # Serra Leoa
    "SOM",  # Somália
    "ZAF",  # África do Sul
    "SSD",  # Sudão do Sul
    "SDN",  # Sudão
    "TZA",  # Tanzânia
    "TGO",  # Togo
    "TUN",  # Tunísia
    "UGA",  # Uganda
    "ZMB",  # Zâmbia
    "ZWE"   # Zimbábue
]

merged_df_EU = merged_df[merged_df['country_code'].isin(ue_country_codes)]

merged_df_SA = merged_df[merged_df['country_code'].isin(south_america_country_codes)]

merged_df_africa = merged_df[merged_df['country_code'].isin(africa_country_codes)]

df_clean_china = merged_df_china[['producao_total(t)', 'PIB']].dropna()

df_clean_EU = merged_df_EU[['producao_total(t)', 'PIB']].dropna()

df_clean_SA = merged_df_SA[['producao_total(t)', 'PIB']].dropna()

df_clean_africa = merged_df_africa[['producao_total(t)', 'PIB']].dropna()

print(merged_df_brasil)
print(merged_df_brasil[['producao_total(t)', 'area_total_de_producao(ha)', 'PIB']].corr())
# print(merged_df_brasil[['producao_total(t)', 'PIB']].corr())
print(df_clean_EU)
print('União Europeia:', spearmanr(df_clean_EU['producao_total(t)'], df_clean_EU['PIB']))
print('America do sul:', spearmanr(df_clean_SA['producao_total(t)'], df_clean_SA['PIB']))
print('Africa:', spearmanr(df_clean_africa['producao_total(t)'], df_clean_africa['PIB']))
print('China:', spearmanr(df_clean_china['producao_total(t)'], df_clean_china['PIB']))
