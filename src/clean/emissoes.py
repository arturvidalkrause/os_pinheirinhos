import pandas as pd
import numpy as np
import os

def preprocessamento_emissoes(path):
    # Lendo o arquivo
    try:
        df = pd.read_csv(os.path.join(path, "annual-co2-emissions-per-country.csv"), encoding='utf-8')
    except UnicodeDecodeError:
        # Se ocorrer um erro de decodificação, tenta com uma codificação diferente
        df = pd.read_csv(os.path.join(path, "annual-co2-emissions-per-country.csv"), encoding='ISO-8859-1')

    # Removendo a coluna Entity
    df.drop(['Entity'], axis=1, inplace=True)

    # Tomando apenas de 1961 a 2022
    df_periodo = df[(df['Year']>1960) & (df['Year']<2023)]

    # Renomeando as colunas
    df_periodo.rename(columns={'Year': 'ano', 'Code': 'country_code'}, inplace=True)

    # Preenchendo anos faltantes
    def preencher_anos_faltantes(df):
        # Criar uma lista de anos de 1961 a 2022
        anos = pd.Series(range(1961, 2023))

        # Criar um DataFrame com todas as combinações de country_code e anos
        country_codes = df['country_code'].unique()
        todos_anos = pd.MultiIndex.from_product([country_codes, anos], names=['country_code', 'ano'])

        # Criar um DataFrame vazio para os anos de 1961 a 2022
        df_todos_anos = pd.DataFrame(index=todos_anos).reset_index()

        # Certifique-se de que a coluna 'ano' seja do tipo int
        df['ano'] = df['ano'].astype(int)

        # Fazer merge com o DataFrame original
        df_completo = pd.merge(df_todos_anos, df, on=['country_code', 'ano'], how='left')

        return df_completo
    
    df_completo = preencher_anos_faltantes(df_periodo)
    
    # Remover linhas onde country_code é nan para obter apeans os países
    df_cleaned = df_completo.dropna(subset=['country_code'])

    # Renomear o total global
    df_final = df_cleaned.replace('OWID_WRL', 'WLD')

    # Renomear Kosovo
    df_final.replace('OWID_KOS', 'XKS', inplace=True)

    return df_final



# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_emissoes(path_data))
# print(preprocessamento_emissoes(path_data)['country_code'].unique())