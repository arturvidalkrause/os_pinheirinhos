"""
	Contém funções para tratar os dados do DataSet: "Produção agropecuaria"
"""

import pandas as pd
import numpy as np
import os
from . import big_strings
from . import big_dicts

def preprocessamento_producao(path: str) -> pd.DataFrame:
	"""Trata o dataset em questão removendo colunas desnecessárias, agrupas os dados necessários, trata dados NaN e transforma dados de colunas em novas linhas e retorna apenas o necessário para as análises

	Args:
		path (str): path do diretório com todos os datasets que seram tratados

	Returns:
		df_renamed: retorna o dataset com os dados tratados
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
	df_vegetal.drop(['Item Code', 'Element Code'], axis=1, inplace=True)

    # Separando em área e produção e eliminando colunas desnecessárias
	df_area = df_vegetal[df_vegetal['Element'] == 'Area harvested']
	df_area.drop(['Element', 'Unit'], axis=1, inplace=True)

	df_production = df_vegetal[df_vegetal['Element'] == 'Production']
	df_production.drop(['Element', 'Unit'], axis=1, inplace=True)

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
	df_production_total.rename(columns={'Total': 'producao_total(t)',
                                        'Area': 'area_name',
                                        'Year': 'ano'}, inplace=True)
	df_area_total.rename(columns={'Total': 'area_total_de_producao(ha)',
                                  'Area': 'area_name',
                                  'Year': 'ano'}, inplace=True)

    # Unindo ambos os dataframes em um só
	df_combinado = pd.merge(df_production_total, df_area_total, on=['area_name', 'ano'])

    # Obtendo apenas os países e o mundo:
	countries_to_keep = big_strings.countries_to_keep_faostat
	df_filtered = df_combinado[df_combinado['area_name'].isin(countries_to_keep)]
	df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
	country_codes = big_dicts.country_codes_faostat
	df_filtered['country_code'] = df_filtered['area_name'].map(country_codes)
    
    # Removendo os nomes antigos
	df_renamed = df_filtered.drop('area_name', axis=1)

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
		df['ano'] = df['ano'].astype(int)

        # Fazer merge com o DataFrame original
		df_completo = pd.merge(df_todos_anos, df, on=['country_code', 'ano'], how='left')

		return df_completo
    
	df_completo = preencher_anos_faltantes(df_renamed)

	# Arredonda para duas casas decimais
	df_completo["producao_total(t)"] = df_completo["producao_total(t)"].round(2)
    
	return df_completo

# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_producao(path_data))
# print(preprocessamento_producao(path_data)['area_name'].unique())