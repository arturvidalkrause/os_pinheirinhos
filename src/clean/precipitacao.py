"""
Módulo para tratamento dos dados da tabela: "Preciptação_mes_a_mes.xlsx"

Este módulo contém funções para o pré-processamento do dataset de precipitação mensal, incluindo a remoção de colunas desnecessárias,
transformação dos dados de colunas para linhas, agregação por ano e país, preenchimento de dados faltantes, e a preparação dos dados
para análises posteriores.

"""

import pandas as pd
import os
import big_dicts


def preprocessamento_precipitacao(path):
	"""
    Realiza o pré-processamento dos dados da tabela de precipitação mês a mês.

    O pré-processamento inclui:
        - Leitura do arquivo Excel.
        - Remoção de colunas desnecessárias, como o nome do país.
        - Transposição do DataFrame para ter os anos nas linhas e os países nas colunas.
        - Agrupamento dos dados por ano e cálculo da precipitação total anual por país.
        - Transformação dos dados de forma que cada linha corresponda a um país e ano, com sua precipitação anual.
        - Conversão dos dados para os tipos apropriados e arredondamento dos valores de precipitação para duas casas decimais.

    Args:
        path (str): Caminho do diretório contendo o arquivo Excel.

    Returns:
        pd.DataFrame: Um DataFrame contendo a precipitação anual por país e ano, pronto para análise.
    """
    # Lendo o arquivo removendo as primeiras linhas
	df = pd.read_excel(os.path.join(path, "Precipitação_mes_a_mes.xlsx"))

    # Removendo a coluna com o nome do país
	df.drop(['name'], axis=1, inplace=True)

    # Transpondo o DataFrame para que os anos fiquem nas linhas
	df_transposed = df.set_index('code').T

    # Removendo informações de mês
	df_transposed['ano'] = df_transposed.index.str[:4]

    # Agrupar pelos anos e somar os valores das colunas de precipitação
	annual_totals = df_transposed.groupby('ano').sum(numeric_only=True)

    # Resetando o índice
	annual_totals.reset_index(inplace=True)

    # Transformando com melt
	df_melted = annual_totals.melt(id_vars=['ano'], var_name='country_code', value_name='precipitação_anual')

	# Arredonda para duas casas decimais
	df_melted["precipitação_anual"] = df_melted["precipitação_anual"].round(2)

	# Inverte o dicionário para que o código do país seja a chave
	reversed_dict = {v: k for k, v in big_dicts.country_codes_precipitacao.items()}

	# Faz a substituição
	df_melted["pais"] = df_melted["country_code"].replace(reversed_dict)
	
	# Converter outras colunas para os tipos corretos
	df_melted = df_melted.astype({
		'pais': "category",
		'country_code': "category",
		'ano': "category",
		'precipitação_anual': "float64",
	})

	return df_melted
