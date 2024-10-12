"""Trata todos os dados da tabela 'Preciptação_mes_a_mes.xlsx'"""

import pandas as pd
import matplotlib.pyplot as plt
import os
<<<<<<< HEAD
from . import big_strings
from . import big_dicts
=======
import big_dicts
>>>>>>> main


def preprocessamento_precipitacao(path):
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
