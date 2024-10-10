"""
	Contém funções para tratar os dados do DataSet: "Fertilizantes_por_nutrientes"
"""

import pandas as pd
import numpy as np
import os
from . import big_strings
from . import big_dicts


def preprocessamento_PIB(path: str) -> pd.DataFrame:
	"""Trata o dataset em questão removendo colunas desnecessárias, agrupas os dados necessários, trata dados NaN e transforma dados de colunas em novas linhas e retorna apenas o necessário para as análises

	Args:
		path (str): path do diretório com todos os datasets que seram tratados

	Returns:
		df_renamed: retorna o dataset com os dados tratados
	"""
    # Lendo o arquivo removendo as primeiras linhas
	df = pd.read_csv(os.path.join(path, "PIB.csv"), skiprows=3)
    
	# Removendo colunas desnecessárias
	df.drop(['Indicator Code', 'Country Code'], axis=1, inplace=True)
	df.drop(df.columns[-1], axis=1, inplace=True)

    # Transformando o DataFrame
	df_melted = df.melt(id_vars=['Country Name', 'Indicator Name'], 
                    var_name='Year', 
                    value_name='PIB')

    # Renomeando as colunas
	df_melted = df_melted.rename(columns={
        'Country Name': 'area_name',
        'Indicator Name': 'indicator_name',
        'Year': 'ano'
    })

    # Convertendo a coluna 'ano' para int
	df_melted['ano'] = df_melted['ano'].astype(int)

    # Removendo coluna desnecessária
	df_melted.drop(['indicator_name'], axis=1, inplace=True)

    # Pegando apenas de 1961 a 2022
	df_periodo = df_melted[(df_melted['ano']>1960)&(df_melted['ano']<2023)]

    # Obtendo apenas os países e o mundo:
	countries_to_keep = big_strings.countries_to_keep_worldbank
	df_filtered = df_periodo[df_periodo['area_name'].isin(countries_to_keep)]
	df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
	country_codes = big_dicts.countries_codes_worldbank
	df_filtered['country_code'] = df_filtered['area_name'].map(country_codes)

    # Removendo os nomes antigos
	df_renamed = df_filtered.drop('area_name', axis=1)

	# Arredonda para duas casas decimais
	df_renamed["PIB"] = df_renamed["PIB"].round(2)

	return df_renamed

# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_PIB(path_data))