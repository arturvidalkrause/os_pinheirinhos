"""
	Contém funções para tratar os dados do DataSet: "Pesticidas"
"""

import pandas as pd
import os
import big_strings
import big_dicts
import numpy as np

def preprocessamento_pesticidas(file_path: str) -> pd.DataFrame:
    """Trata o dataset em questão removendo colunas desnecessárias, agrupando os dados necessários,
    tratando dados NaN e transformando dados de colunas em novas linhas e retornando apenas o necessário para as análises.

    Args:
        file_path (str): Caminho do arquivo CSV a ser tratado.

    Returns:
        pd.DataFrame: DataFrame com os dados tratados.
    """
    # Lendo o arquivo
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Filtrando as colunas que terminam em "F" ou "N"
    cols_to_drop = df.columns[df.columns.str.endswith(("F", "N"))]

    # Removendo essas colunas
    df.drop(columns=cols_to_drop, inplace=True)

    # Renomear as colunas dos anos para remover o Y
    df.columns = df.columns.str.replace(r"^Y", "", regex=True)

    # Remover as colunas Area Code e M49
    df.drop(["Area Code", "Area Code (M49)"], axis=1, inplace=True, errors='ignore')

    # Obter apenas o uso total de pesticidas
    df = df[df["Element Code"] == 5157]
    df = df[df["Item Code"] == 1357]

    # Remover colunas desnecessárias
    df.drop(["Item Code", "Element", "Element Code", "Unit"], axis=1, inplace=True)

    # Agrupar o dataset por país
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
    def preencher_anos_faltantes(df):
        # Criar uma lista de anos de 1961 a 2022
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
    df_completo["uso_total_de_fertilizantes(t)"] = df_completo["uso_total_de_fertilizantes(t)"].round(2)

    return df_completo


# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_pesticidas(path_data))