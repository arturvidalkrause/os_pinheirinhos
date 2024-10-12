"""
Módulo de Pré-processamento de Fertilizantes por Nutrientes

Este módulo contém funções para realizar o pré-processamento dos dados do dataset
"Fertilizantes_por_nutrientes". O processo inclui a remoção de colunas desnecessárias,
agrupamento dos dados relevantes, tratamento de valores ausentes (NaN), transformação
de colunas em linhas e preenchimento de anos ausentes. O objetivo é preparar os dados
para análises relacionadas ao uso de fertilizantes por nutrientes em diferentes países.

"""
import pandas as pd
import numpy as np
import os
import big_strings
import big_dicts


def preprocessamento_fertilizantes(path: str) -> pd.DataFrame:
	"""
	Realiza o pré-processamento do dataset "Fertilizantes_por_nutrientes",
	removendo colunas desnecessárias, agrupando os dados relevantes, tratando
	valores NaN, transformando colunas em linhas, preenchendo anos ausentes e
	renomeando valores para retornar um dataset pronto para análise.

	Args:
		path (str): Caminho do diretório que contém o dataset a ser processado.

	Returns:
		pd.DataFrame: Retorna o dataset tratado, pronto para análises de uso de fertilizantes.

	Exemplo de uso:
		df_tratado = preprocessamento_fertilizantes('caminho/para/dataset')
	"""
	try:
		df = pd.read_csv(
			os.path.join(path, "Fertilizantes_por_nutrientes.csv"), encoding="utf-8"
        )
	except UnicodeDecodeError:
        # Se ocorrer um erro de decodificação, tenta com uma codificação diferente
		df = pd.read_csv(
			os.path.join(path, "Fertilizantes_por_nutrientes.csv"),
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

    # Obter apenas o uso total por nutriente
	df = df[df["Element Code"] == 5157]

    # Remover colunas desnecessárias
	df.drop(["Item Code", "Element", "Element Code", "Unit"], axis=1, inplace=True)

    # Obter o total de todos os nutrientes
	df_total = df.groupby("Area").sum(numeric_only=True).reset_index()

    # Usando melt para alterar o formato
	df_melted = df_total.melt(
        id_vars=["Area"], var_name="ano", value_name="uso_total_de_fertilizantes(t)"
    )

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

    # Obtendo apenas de 1961 a 2022
	df_renamed = df_renamed[(df_renamed["ano"] > 1960) & (df_renamed["ano"] < 2023)]

    # Preenchendo anos faltantes
	def preencher_anos_faltantes(df: pd.DataFrame) -> pd.DataFrame:
		"""
		Preenche anos faltantes para cada país no dataset, garantindo que todos os anos
		de 1961 a 2022 estejam presentes para cada país.

		Args:
			df (pd.DataFrame): Dataset com os dados de uso de fertilizantes.

		Returns:
			pd.DataFrame: Retorna o dataset completo com os anos ausentes preenchidos.

		Exemplo de uso:
			df_completo = preencher_anos_faltantes(df)
		"""
		anos = pd.Series(range(1961, 2023))

        # Criar um DataFrame com todas as combinações de country_code e anos
		country_codes = df["country_code"].unique()
		todos_anos = pd.MultiIndex.from_product(
            [country_codes, anos], names=["country_code", "ano"]
        )

        # Criar um DataFrame vazio para os anos de 1961 a 2022
		df_todos_anos = pd.DataFrame(index=todos_anos).reset_index()

        # Certifique-se de que a coluna 'ano' seja do tipo int
		df["ano"] = df["ano"].astype(int)

        # Fazer merge com o DataFrame original
		df_completo = pd.merge(
            df_todos_anos, df, on=["country_code", "ano"], how="left"
        ).replace(0, np.nan)

		return df_completo

	df_completo = preencher_anos_faltantes(df_renamed)

	# Arredonda para duas casas decimais
	df_completo["uso_total_de_fertilizantes(t)"]  = df_completo["uso_total_de_fertilizantes(t)"].round(2)

	# Inverte o dicionário para que o código do país seja a chave
	reversed_dict = {v: k for k, v in big_dicts.countries_codes_emissoes_co2.items()}

	# Substituir os valores em country_code com o dicionário de correspondência
	df_completo["pais"] = df_completo["country_code"].replace(reversed_dict)
	
	# Converter outras colunas para os tipos corretos
	df_completo = df_completo.astype({
		'pais': "category",
		'country_code': "category",
		'ano': "category",
		'uso_total_de_fertilizantes(t)': "float64",
	})

	return df_completo