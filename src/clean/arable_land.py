"""
Módulo para tratamento dos dados do DataSet: "Arable_Land"

Este módulo contém funções para o pré-processamento do dataset de terras aráveis, incluindo a remoção de colunas desnecessárias,
transformação dos dados de colunas para linhas, preenchimento de dados faltantes, e a preparação dos dados para análises posteriores.

"""


import pandas as pd
import big_strings
import big_dicts
import pyarrow
import os


def preprocessamento_arable_land(path: str) -> pd.DataFrame:
	"""
    Realiza o pré-processamento dos dados do dataset de terras aráveis.

    O pré-processamento inclui:
        - Leitura do arquivo CSV removendo as primeiras linhas de cabeçalho.
        - Remoção de colunas desnecessárias.
        - Transformação das colunas de ano e terras aráveis por país.
        - Conversão dos dados para os tipos corretos.
        - Substituição de valores dos países pelo respectivo código de país.

    Args:
        path (str): Caminho do diretório contendo o dataset a ser tratado.

    Returns:
        pd.DataFrame: Um DataFrame contendo o percentual de terras aráveis por país, pronto para análise.
    """
    # Lendo o arquivo removendo as primeiras linhas
	df: pd.DataFrame  = pd.read_csv(os.path.join(path, "Arable_Land.csv"), skiprows=3)
    
    # Removendo colunas desnecessárias
	df.drop(['Indicator Code', 'Country Code'], axis=1, inplace=True)
	df.drop(df.columns[-1], axis=1, inplace=True)

    # Transformando o DataFrame
	df_melted: pd.DataFrame  = df.melt(id_vars=['Country Name', 'Indicator Name'], 
                    var_name='Year', 
                    value_name='terras_araveis(%)')

    # Renomeando as colunas
	df_melted = df_melted.rename(columns={
        'Country Name': 'pais',
        'Indicator Name': 'indicator_name',
        'Year': 'ano'
    })

    # Convertendo a coluna 'Year' para int
	df_melted['ano'] = df_melted['ano'].astype(int)

    # Removendo coluna desnecessária
	df_melted.drop(['indicator_name'], axis=1, inplace=True)

    # Pegando apenas de 1961 a 2022
	df_periodo: pd.DataFrame  = df_melted[(df_melted['ano'] > 1960) & (df_melted['ano'] < 2023)]

    # Obtendo apenas os países e o mundo:
	countries_to_keep = big_strings.countries_to_keep_worldbank
	df_filtered = df_periodo[df_periodo['pais'].isin(countries_to_keep)]
	df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
	country_codes = big_dicts.countries_codes_worldbank
	df_filtered['country_code'] = df_filtered['pais'].map(country_codes)

    # Removendo os nomes antigos
	# df_renamed: pd.DataFrame = df_filtered.drop('pais', axis=1)
	df_renamed = df_filtered

	# Arredonda para tres casas decimais
	df_renamed["terras_araveis(%)"] = df_renamed["terras_araveis(%)"].round(3)
	
	# Define um tipo correto a cada coluna
	df_renamed = df_renamed.astype({
		'pais': "category",
		'ano': "category",
		'terras_araveis(%)': "float16",
		'country_code': "category"
	})

	return df_renamed
