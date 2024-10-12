"""
Módulo para tratamento dos dados do DataSet: "Produção agropecuária"

Este módulo contém funções para o pré-processamento do dataset de produção agropecuária, incluindo a remoção de colunas desnecessárias, 
transformação dos dados de colunas para linhas, tratamento de dados NaN, e a preparação dos dados para análises futuras. 

"""

import pandas as pd
import numpy as np
import os
import big_strings
import big_dicts

def preprocessamento_producao(path: str) -> pd.DataFrame:
	"""
	Realiza o pré-processamento dos dados do dataset de produção agropecuária.

	O pré-processamento inclui:
	    - Leitura do arquivo CSV.
	    - Remoção de colunas desnecessárias, como códigos de área e item.
	    - Foco apenas em dados vegetais.
	    - Separação em área colhida e produção total.
	    - Transformação dos dados de formato largo para formato longo e vice-versa.
	    - Preenchimento de anos faltantes e cálculo do total de produção e área colhida.
	    - Arredondamento dos dados de produção total e integração de códigos de países.
	
	Args:
	    path (str): Caminho do diretório contendo o arquivo CSV.
	
	Returns:
	    pd.DataFrame: Um DataFrame contendo a produção total e a área colhida por país e ano, prontos para análise.
	"""
    # Lendo o arquivo
	try:
		df = pd.read_csv(os.path.join(path, "Produção agropecuaria.csv"), encoding='utf-8')
	except UnicodeDecodeError:
        # Se ocorrer um erro de decodificação, tenta com uma codificação diferente
		df = pd.read_csv(os.path.join(path, "Produção agropecuaria.csv"), encoding='ISO-8859-1')
    
    # Renomear as colunas dos anos para remover o Y
	df.columns = df.columns.str.replace(r'^Y', '', regex=True)

    # Remover as colunas Area Code, M49 e Item Code (CPC)
	df.drop(['Area Code', 'Area Code (M49)', 'Item Code (CPC)'], axis=1, inplace=True)

    # Pegar apenas os vegetais
	vegetais = big_strings.vegetais_producao

	df_vegetal = df[df['Item'].isin(vegetais)]

    # Removendo colunas desnecessárias
	df_vegetal = df_vegetal.drop(['Item Code', 'Element Code'], axis=1)

    # Separando em área e produção e eliminando colunas desnecessárias
	df_area = df_vegetal[df_vegetal['Element'] == 'Area harvested']
	df_area = df_area.drop(['Element', 'Unit'], axis=1)

	df_production = df_vegetal[df_vegetal['Element'] == 'Production']
	df_production = df_production.drop(['Element', 'Unit'], axis=1)

    ## Reorganizando os dataframes

    ## Area
    # Usando melt para transformar o DataFrame em formato longo
	df_area_melted = df_area.melt(id_vars=['Area', 'Item'], 
                        var_name='Year', 
                        value_name='Production')

    # Usando pivot_table para transformar em formato largo
	df_area_pivot = df_area_melted.pivot_table(index=['Area', 'Year'], 
                                    columns='Item', 
                                    values='Production', 
                                    fill_value=0)

    # Resetando o índice para transformar em DataFrame padrão
	df_area_pivot = df_area_pivot.reset_index()

    ## Production
    # Usando melt para transformar o DataFrame em formato longo
	df_production_melted = df_production.melt(id_vars=['Area', 'Item'], 
                        var_name='Year', 
                        value_name='Production')

    # Usando pivot_table para transformar em formato largo
	df_production_pivot = df_production_melted.pivot_table(index=['Area', 'Year'], 
                                    columns='Item', 
                                    values='Production', 
                                    fill_value=0)

    # Resetando o índice para transformar em DataFrame padrão
	df_production_pivot = df_production_pivot.reset_index()

    # Criando uma coluna com o total para ambos os datasets
	df_area_pivot['Total'] = df_area_pivot.drop(columns=['Area', 'Year']).sum(axis=1)
	df_production_pivot['Total'] = df_production_pivot.drop(columns=['Area', 'Year']).sum(axis=1)

    # Pegando os datasets apenas com o total
	df_area_total = df_area_pivot[['Area', 'Year', 'Total']]
	df_production_total = df_production_pivot[['Area', 'Year', 'Total']]

    # Renomeando as colunas
	df_production_total = df_production_total.rename(columns={'Total': 'producao_total(t)',
                                        'Area': 'area_name',
                                        'Year': 'ano'})
	df_area_total = df_area_total.rename(columns={'Total': 'area_total_de_producao(ha)',
                                  'Area': 'area_name',
                                  'Year': 'ano'})

    # Unindo ambos os dataframes em um só
	df_combinado = pd.merge(df_production_total, df_area_total, on=['area_name', 'ano'])

    # Obtendo apenas os países e o mundo:
	countries_to_keep = big_strings.countries_to_keep_faostat
	df_filtered = df_combinado[df_combinado['area_name'].isin(countries_to_keep)]
	df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
	country_codes = big_dicts.country_codes_faostat
	df_filtered = df_filtered.copy()
	# Mapeia o country_code e faz a modificação segura
	df_filtered.loc[:, 'country_code'] = df_filtered['area_name'].map(country_codes)
    
    # Removendo os nomes antigos
	df_renamed = df_filtered.drop('area_name', axis=1)

    # Preenchendo anos faltantes
	def preencher_anos_faltantes(df: pd.DataFrame) -> pd.DataFrame:
		"""
		Preenche os anos faltantes no dataset, garantindo que todos os países tenham valores para todos os anos de 1961 a 2022.

		A função cria uma combinação de todos os códigos de países e anos no intervalo de 1961 a 2022 e realiza um merge
		com o DataFrame original. Caso algum ano esteja ausente para um determinado país, ele será adicionado com valores
		NaN para as colunas faltantes.

		Args:
			df (pd.DataFrame): O DataFrame original contendo os dados a serem preenchidos.

		Returns:
			pd.DataFrame: Um DataFrame completo com todos os anos preenchidos de 1961 a 2022 para cada país.
		"""
        # Criar uma lista de anos de 1961 a 2022
		anos = pd.Series(range(1961, 2023))

        # Criar um DataFrame com todas as combinações de country_code e anos
		country_codes = df['country_code'].unique()
		todos_anos = pd.MultiIndex.from_product([country_codes, anos], names=['country_code', 'ano'])

        # Criar um DataFrame vazio para os anos de 1961 a 2022
		df_todos_anos = pd.DataFrame(index=todos_anos).reset_index()

        # Certifique-se de que a coluna 'ano' seja do tipo int
		df['ano'] = df['ano'].astype(int)

        # Fazer merge com o DataFrame original
		df_completo = pd.merge(df_todos_anos, df, on=['country_code', 'ano'], how='left')

		return df_completo
    
	df_completo = preencher_anos_faltantes(df_renamed)

	# Arredonda para duas casas decimais
	df_completo["producao_total(t)"] = df_completo["producao_total(t)"].round(2)

	# Inverte o dicionário para que o código do país seja a chave
	reversed_dict = {v: k for k, v in big_dicts.countries_codes_emissoes_co2.items()}

	# Substituir os valores em country_code com o dicionário de correspondência
	df_completo["pais"] = df_completo["country_code"].replace(reversed_dict)

	# Converter outras colunas para os tipos corretos
	df_completo = df_completo.astype({
		'pais': "category",
		'country_code': "category",
		'ano': "category",
		'producao_total(t)': "float64",
		'area_total_de_producao(ha)': "float64"
	})
	
	return df_completo