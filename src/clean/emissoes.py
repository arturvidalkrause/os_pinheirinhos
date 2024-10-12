"""
Módulo de Pré-processamento de Emissões de CO₂

Este módulo contém funções para realizar o pré-processamento dos dados do dataset
"annual-co2-emissions-per-country". Ele trata o conjunto de dados removendo colunas
desnecessárias, preenchendo anos ausentes, renomeando valores e colunas, e
preparando os dados para análises.

"""

import pandas as pd
import os
import big_dicts


def preencher_anos_faltantes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preenche anos faltantes para cada país no dataset, garantindo que todos os anos
    de 1961 a 2022 estejam presentes para cada país.

    Args:
        df (pd.DataFrame): Dataset com os dados de emissões de CO₂ filtrados por período.

    Returns:
        pd.DataFrame: Retorna o dataset completo com os anos ausentes preenchidos.

    Exemplo de uso:
        df_completo = preencher_anos_faltantes(df)
    """
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

def preprocessamento_emissoes(path: str) -> pd.DataFrame:
    """
    Realiza o pré-processamento do dataset "annual-co2-emissions-per-country",
    removendo colunas desnecessárias, agrupando os dados relevantes, tratando valores NaN,
    transformando colunas em linhas, preenchendo anos ausentes e renomeando valores para
    retornar um dataset pronto para análise.

    Args:
        path (str): Caminho do diretório que contém o dataset a ser processado.

    Returns:
        pd.DataFrame: Retorna o dataset tratado, pronto para análises de emissões de CO₂.
        
    Exemplo de uso:
        df_tratado = preprocessamento_emissoes('caminho/para/dataset')
    """
    try:
        df = pd.read_csv(os.path.join(path, "annual-co2-emissions-per-country.csv"), encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(os.path.join(path, "annual-co2-emissions-per-country.csv"), encoding='ISO-8859-1')

    # Removendo a coluna Entity
    df.drop(['Entity'], axis=1, inplace=True)

    # Tomando apenas de 1961 a 2022
    df_periodo = df[(df['Year'] > 1960) & (df['Year'] < 2023)]

    # Renomeando as colunas
    df_periodo = df_periodo.rename(columns={'Year': 'ano', 'Code': 'country_code'})

    # Preenchendo anos faltantes
    df_completo = preencher_anos_faltantes(df_periodo)

    # Remover linhas onde country_code é NaN para obter apenas os países
    df_cleaned = df_completo.dropna(subset=['country_code'])

    # Renomear o total global
    df_final = df_cleaned.replace('OWID_WRL', 'WLD')

    # Renomear Kosovo
    df_final.replace('OWID_KOS', 'XKX', inplace=True)

    # Inverte o dicionário para que o código do país seja a chave
    reversed_dict = {v: k for k, v in big_dicts.countries_codes_emissoes_co2.items()}

    # Faz a substituição
    df_final["pais"] = df_final["country_code"].replace(reversed_dict)

    # Arredondar os valores de emissões anuais de CO₂
    df_final["Annual CO₂ emissions"] = df_final["Annual CO₂ emissions"].round(0)

    # Define o tipo correto para cada coluna
    df_final = df_final.astype({
        'pais': "category",
        'country_code': "category",
        'ano': "category",
        'Annual CO₂ emissions': "Int64"
    })

    return df_final