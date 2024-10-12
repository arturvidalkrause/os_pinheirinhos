"""
Módulo para tratamento dos dados do DataSet: "Pesticidas"

Este módulo contém funções para pré-processamento do dataset sobre o uso de pesticidas, incluindo a remoção de colunas desnecessárias,
transformação de dados, preenchimento de dados faltantes, e a preparação dos dados para análises posteriores.

"""

import pandas as pd
import numpy as np
import os
import big_strings
import big_dicts


def preprocessamento_pesticidas(path: str) -> pd.DataFrame:
	"""
    Realiza o pré-processamento dos dados do dataset de pesticidas.

    O pré-processamento inclui:
        - Leitura do arquivo CSV.
        - Remoção de colunas desnecessárias, como códigos de área e códigos M49.
        - Transformação das colunas de ano e uso de pesticidas por país.
        - Conversão dos dados para os tipos corretos.
        - Substituição de valores dos países pelo respectivo código de país.

    Args:
        path (str): Caminho do diretório contendo o dataset a ser tratado.

    Returns:
        pd.DataFrame: Um DataFrame contendo o uso total de pesticidas por país, pronto para análise.
    """
    # Lendo o arquivo
	try:
		df = pd.read_csv(
			os.path.join(path, "Pesticidas.csv"), encoding="utf-8"
        )
	except UnicodeDecodeError:
        # Se ocorrer um erro de decodificação, tenta com uma codificação diferente
		df = pd.read_csv(
			os.path.join(path, "Pesticidas.csv"),
			encoding="ISO-8859-1",
        )

        # Filtrando as colunas que terminam em "F" ou "N"
	cols_to_drop = df.columns[df.columns.str.endswith(("F", "N"))]

    # Removendo essas colunas
	df.drop(columns=cols_to_drop, inplace=True)

    # Renomear as colunas dos anos para remover o Y
	df.columns = df.columns.str.replace(r"^Y", "", regex=True)

    # Remover as colunas Area Code e M49
	df.drop(["Area Code", "Area Code (M49)"], axis=1, inplace=True)

    # Obter apenas o uso total
	df = df[df["Element Code"] == 5157]
	df = df[df["Item Code"] == 1357]

    # Remover colunas desnecessárias
	df.drop(["Item Code", "Element", "Element Code", "Unit"], axis=1, inplace=True)
	
    # Usando melt para alterar o formato
	df_melted = df.melt(
        id_vars=["Area"], var_name="ano", value_name="uso_total_de_pesticidas(t)"
    )

	df_melted = df_melted[df_melted["ano"] != "Item"]

    # Obtendo apenas os países e o mundo:
	countries_to_keep = big_strings.countries_to_keep_faostat
	df_filtered = df_melted[df_melted["Area"].isin(countries_to_keep)]
	df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
	country_codes = big_dicts.country_codes_faostat
	df_filtered["country_code"] = df_filtered["Area"].map(country_codes)

    # Removendo os nomes antigos
	df_renamed = df_filtered.drop("Area", axis=1)

    # Convertendo a coluna 'ano' para int
	df_renamed["ano"] = df_renamed["ano"].astype(int)

	df_completo = df_renamed.copy()

	# Arredonda para duas casas decimais
	df_completo["uso_total_de_pesticidas(t)"]  = df_completo["uso_total_de_pesticidas(t)"].round(2)

	# Inverte o dicionário para que o código do país seja a chave
	reversed_dict = {v: k for k, v in big_dicts.countries_codes_emissoes_co2.items()}

	# Substituir os valores em country_code com o dicionário de correspondência
	df_completo["pais"] = df_completo["country_code"].replace(reversed_dict)
	
	# Converter outras colunas para os tipos corretos
	df_completo = df_completo.astype({
		'pais': "category",
		'country_code': "category",
		'ano': "category",
		'uso_total_de_pesticidas(t)': "float64",
	})

	return df_completo