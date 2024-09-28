import pandas as pd
import numpy as np
import os

def preprocessamento_temperatura(path):
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
        df[months[i]] = df[months[i]].fillna((df[months[(i-1)]]+df[months[(i+1)]])/2)

    # Obtendo uma coluna om o Station_id reduzido
    df['ID'] = df['Station_ID'].str[:2]

    # Lendo o arquivo com a conversão de ID para o nome
    # do país e mapeando no DataFrame original
    with open(os.path.join(path, "Conversão Station_id para Pais.txt"), 'r') as file:
        mapping = {}
        for line in file:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                code, country = parts
                mapping[code] = country

    df['country_name'] = df['ID'].map(mapping)

    # Criando uma coluna com a média anual da temperatura
    df['media_anual'] = df[months].mean(axis=1)

    # Pegando apenas os anos a partir de 1900
    df_1900_atual = df[df['Year']>1900]

    # Agrupando as estações por país e por ano
    df_grouped = df_1900_atual.groupby(['Year', 'country_name'], as_index=False)['media_anual'].mean()
    return df_grouped
