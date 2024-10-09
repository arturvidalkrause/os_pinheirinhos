"""Trata todos os dados da tabela 'Preciptação_mes_a_mes.xlsx'"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import big_strings
import big_dicts


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

	return df_melted

# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_precipitacao(path_data))