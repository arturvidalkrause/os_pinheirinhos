import pandas as pd
import numpy as np
import os

def preprocessamento_emissoes(path):
    # Lendo o arquivo
    try:
        df = pd.read_csv(os.path.join(path, "Emissões.csv"), encoding='utf-8')
    except UnicodeDecodeError:
        # Se ocorrer um erro de decodificação, tenta com uma codificação diferente
        df = pd.read_csv(os.path.join(path, "Emissões.csv"), encoding='ISO-8859-1')

    # Remover colunas que terminam em F ou N
    df = df.loc[:, ~df.columns.str.endswith(('F', 'N'))]

    # Renomear as colunas dos anos para remover o Y
    df.columns = df.columns.str.replace(r'^Y', '', regex=True)

    # Remover os anos 2030 e 2050
    df = df.iloc[:, :-2]

    # Remover as colunas Area Code, M49, Source Code, Source
    df.drop(['Area Code', 'Area Code (M49)', 'Source Code', 'Source'], axis=1, inplace=True)

    # Filtrando apenas os setores desejados
    df_filtered_use = df[df['Item Code'].isin([1707, 6825, 6829])]

    # Filtrando apenas o CO2 e equivalentes
    df_filtered_co2eq = df_filtered_use[df_filtered_use['Element Code'].isin([7273, 717815, 724413, 724313, 723113])]
    
    # Removendo colunas inúteis
    df_filtered_co2eq.drop(['Item Code', 'Element Code'], axis=1, inplace=True)

    # Somando todos os equivalentes em CO2
    df_soma_co2eq = df_filtered_co2eq.groupby(['Area', 'Item'], as_index=False).sum(numeric_only=True)

    print(df_soma_co2eq.columns)
    return df_soma_co2eq



# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_emissoes(path_data))
# print(preprocessamento_emissoes(path_data)['Area'].unique())