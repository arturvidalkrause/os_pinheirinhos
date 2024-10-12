"""
	Contém funções para tratar os dados dos DataSets: "temperatura_mes_a_mes< 1, 2>"
"""
import pandas as pd
import numpy as np
import os

def preprocessamento_temperatura(path: str) -> pd.DataFrame:
    """Trata o dataset em questão removendo colunas desnecessárias, agrupando os dados necessários,
    tratando dados NaN e transformando dados de colunas em novas linhas e retornando apenas o necessário para as análises.

    Args:
        path (str): Caminho do diretório com todos os datasets que serão tratados.

    Returns:
        pd.DataFrame: DataFrame com os dados tratados.
    """
    # Unindo as duas partes da tabela
    df1 = pd.read_parquet(os.path.join(path, "temperatura_mes_a_mes1.parquet"))
    df2 = pd.read_parquet(os.path.join(path, "temperatura_mes_a_mes2.parquet"))
    df = pd.concat((df1, df2), axis=0)
    
    # Formatando valores -99.99 para NaN
    df.replace(-99.99, np.nan, inplace=True)

    # Lista de meses
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Preencher NaNs com a média dos meses anterior e seguinte
    for i in range(1, len(months)-1):
        df[months[i]] = df[months[i]].fillna((df[months[i-1]] + df[months[i+1]]) / 2)

    # Obtendo uma coluna com o Station_ID reduzido
    df['ID'] = df['Station_ID'].str[:2]

    # Lendo o arquivo com a conversão de ID para o nome do país e mapeando no DataFrame original
    with open(os.path.join(path, "Conversão_Station_id_para_Pais.txt"), 'r') as file:
        mapping = {}
        for line in file:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                code, country = parts
                mapping[code] = country

    df['area_name'] = df['ID'].map(mapping)

    # Criando uma coluna com a média anual da temperatura
    df['temperatura_media_anual(°C)'] = df[months].mean(axis=1)

    # Pegando apenas os anos a partir de 1961 até 2022
    df_1961_atual = df[(df['Year'] > 1960) & (df['Year'] < 2023)]

    # Agrupando as estações por país e por ano
    df_grouped = df_1961_atual.groupby(['Year', 'area_name'], as_index=False)['temperatura_media_anual(°C)'].mean()
    
    # Renomeando a coluna dos anos
    df_grouped.rename(columns={'Year': 'ano'}, inplace=True)

    # Definindo os países a manter para o teste
    countries_to_keep = ['TestCountry']

    df_filtered = df_grouped[df_grouped['area_name'].isin(countries_to_keep)]
    df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
    country_codes = {'TestCountry': 'TST'}
    df_filtered['country_code'] = df_filtered['area_name'].map(country_codes)

    # Remover a coluna com os nomes
    df_codes = df_filtered.drop(['area_name'], axis=1)

    # Criar um dataframe com as linhas com a média global
    df_world = df_codes.groupby(['ano'], as_index=False)['temperatura_media_anual(°C)'].mean()
    df_world['country_code'] = 'WLD'

    # Unir e ter o dataframe final
    df_final = pd.concat([df_codes, df_world], ignore_index=True)

    # Arredonda para duas casas decimais
    df_final["temperatura_media_anual(°C)"] = df_final["temperatura_media_anual(°C)"].round(2)

    return df_final


# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_temperatura(path_data))