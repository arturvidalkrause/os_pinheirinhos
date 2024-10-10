"""
	Contém funções para tratar os dados dos DataSets: "temperatura_mes_a_mes< 1, 2>"
"""

import pandas as pd
import numpy as np
import os
import big_strings
import big_dicts

def preprocessamento_temperatura(path: str) -> pd.DataFrame:
	"""Trata o dataset em questão removendo colunas desnecessárias, agrupas os dados necessários, trata dados NaN e transforma dados de colunas em novas linhas e retorna apenas o necessário para as análises

	Args:
		path (str): path do diretório com todos os datasets que seram tratados

	Returns:
		df_final: retorna o dataset com os dados tratados
	"""
    # Unindo as duas partes da tabela
	df1 = pd.read_parquet(os.path.join(path, "temperatura_mes_a_mes1.parquet"))
	df2 = pd.read_parquet(os.path.join(path, "temperatura_mes_a_mes2.parquet"))
	df = pd.concat((df1, df2), axis=0)

    # Formatando valores -99.99 para NaN
	df.replace(-99.99, np.nan, inplace=True)

    # Lista de meses
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Preencher NaNs com a média dos meses anterior e seguinte
	for i in range(1, len(months)-1):
		df[months[i]] = df[months[i]].fillna((df[months[(i-1)]]+df[months[(i+1)]])/2)

    # Obtendo uma coluna om o Station_id reduzido
	df['ID'] = df['Station_ID'].str[:2]

    # Lendo o arquivo com a conversão de ID para o nome
    # do país e mapeando no DataFrame original
	with open(os.path.join(path, "Conversão Station_id para Pais.txt"), 'r') as file:
		mapping = {}
		for line in file:
			parts = line.strip().split(' ', 1)
			if len(parts) == 2:
				code, country = parts
				mapping[code] = country

	df['area_name'] = df['ID'].map(mapping)

    # Criando uma coluna com a média anual da temperatura
	df['temperatura_media_anual(°C)'] = df[months].mean(axis=1)

    # Pegando apenas os anos a partir de 1961 até 2022
	df_1961_atual = df[(df['Year']>1960) & (df['Year']<2023)]

    # Agrupando as estações por país e por ano
	df_grouped = df_1961_atual.groupby(['Year', 'area_name'], as_index=False)['temperatura_media_anual(°C)'].mean()
    
    # Renomeando a coluna dos anos
	df_grouped.rename(columns={'Year': 'ano'}, inplace=True)

    # Obtendo apenas os países e a Antártica
	countries_to_keep = big_strings.countries_to_keep_temperatura

	df_filtered = df_grouped[df_grouped['area_name'].isin(countries_to_keep)]
	df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
	country_codes = big_dicts.country_codes_temperatura
	df_filtered['country_code'] = df_filtered['area_name'].map(country_codes)

    # Remover a coluna com os nomes
	df_codes = df_filtered.drop(['area_name'], axis=1)

    # Criar um dataframe com as linhas com a média global
	df_world = df_codes.groupby(['ano'], as_index=False)['temperatura_media_anual(°C)'].mean()
	df_world['country_code'] = 'WLD'

    # Unir e ter o dataframe final
	df_final = pd.concat([df_codes, df_world], ignore_index=True)

	# Arredonda para duas casas decimais
	df_final["temperatura_media_anual(°C)"] = df_final["temperatura_media_anual(°C)"].round(2)

	# Inverte o dicionário para que o código do país seja a chave
	reversed_dict = {v: k for k, v in big_dicts.country_codes_temperatura.items()}

	# Faz a substituição
	df_final["pais"] = df_final["country_code"].replace(reversed_dict)

	# Define um tipo correto a cada coluna
	df_final = df_final.astype({
		'pais': "category",
		'ano': "category",
		'temperatura_media_anual(°C)': "float16",
		'country_code': "category"
	})

	return df_final