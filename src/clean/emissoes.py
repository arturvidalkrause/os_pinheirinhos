"""
	Contém funções para tratar os dados do DataSet: "annual-co2-emissions-per-country"
"""

import pandas as pd
import os
import big_dicts

def preprocessamento_emissoes(path: str) -> pd.DataFrame:
	"""Trata o dataset em questão removendo colunas desnecessárias, agrupas os dados necessários, trata dados NaN e transforma dados de colunas em novas linhas e retorna apenas o necessário para as análises

	Args:
		path (str): path do diretório com todos os datasets que seram tratados

	Returns:
		df_final: retorna o dataset com os dados tratados
	"""
    # Lendo o arquivo
	try:
		df = pd.read_csv(os.path.join(path, "annual-co2-emissions-per-country.csv"), encoding='utf-8')
	except UnicodeDecodeError:
        # Se ocorrer um erro de decodificação, tenta com uma codificação diferente
		df = pd.read_csv(os.path.join(path, "annual-co2-emissions-per-country.csv"), encoding='ISO-8859-1')

    # Removendo a coluna Entity
	df.drop(['Entity'], axis=1, inplace=True)

    # Tomando apenas de 1961 a 2022
	df_periodo = df[(df['Year']>1960) & (df['Year']<2023)]

	# Renomeando as colunas
	df_periodo = df_periodo.rename(columns={'Year': 'ano', 'Code': 'country_code'})

    # Preenchendo anos faltantes
	def preencher_anos_faltantes(df):
        # Criar uma lista de anos de 1961 a 2022
		anos = pd.Series(range(1961, 2023))

        # Criar um DataFrame com todas as combinações de country_code e anos
		country_codes = df['country_code'].unique()
		todos_anos = pd.MultiIndex.from_product([country_codes, anos], names=['country_code', 'ano'])

        # Criar um DataFrame vazio para os anos de 1961 a 2022
		df_todos_anos = pd.DataFrame(index=todos_anos).reset_index()

    	# Certifique-se de que a coluna 'ano' seja do tipo int
		df.loc[:, 'ano'] = df['ano'].astype(int)

        # Fazer merge com o DataFrame original
		df_completo = pd.merge(df_todos_anos, df, on=['country_code', 'ano'], how='left')

		return df_completo
    
	df_completo = preencher_anos_faltantes(df_periodo)
    
    # Remover linhas onde country_code é nan para obter apeans os países
	df_cleaned = df_completo.dropna(subset=['country_code'])

    # Renomear o total global
	df_final = df_cleaned.replace('OWID_WRL', 'WLD')

    # Renomear Kosovo
	df_final.replace('OWID_KOS', 'XKX', inplace=True)

	# Inverte o dicionário para que o código do país seja a chave
	reversed_dict = {v: k for k, v in big_dicts.countries_codes_emissoes_co2.items()}

	# Faz a substituição
	df_final["pais"] = df_final["country_code"].replace(reversed_dict)

	df_final["Annual CO₂ emissions"] = df_final["Annual CO₂ emissions"].round(0)
	
	# Define um tipo correto a cada coluna
	df_final = df_final.astype({
		'pais': "category",
		'country_code': "category",
		'ano': "category",
		'Annual CO₂ emissions': "Int64"
	})

	return df_final