import pandas as pd
import numpy as np
import os

def preprocessamento_PIB(path):
    # Lendo o arquivo removendo as primeiras linhas
    df = pd.read_csv(os.path.join(path, "PIB.csv"), skiprows=3)
    
    # Removendo colunas desnecessárias
    df.drop(['Indicator Code', 'Country Code'], axis=1, inplace=True)
    df.drop(df.columns[-1], axis=1, inplace=True)

    # Transformando o DataFrame
    df_melted = df.melt(id_vars=['Country Name', 'Indicator Name'], 
                    var_name='Year', 
                    value_name='PIB')

    # Renomeando as colunas
    df_melted = df_melted.rename(columns={
        'Country Name': 'country_name',
        'Indicator Name': 'indicator_name'
    })

    # Convertendo a coluna 'Year' para int
    df_melted['Year'] = df_melted['Year'].astype(int)

    # Removendo coluna desnecessária
    df_melted.drop(['indicator_name'], axis=1, inplace=True)

    return df_melted

# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_PIB(path_data))