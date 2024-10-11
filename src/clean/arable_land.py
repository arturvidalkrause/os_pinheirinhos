"""
	Contém funções para tratar os dados dataset: "Arable_Land"
"""
import pandas as pd
import big_strings
import big_dicts

def preprocessamento_arable_land(file_path: str) -> pd.DataFrame:
    """Trata o dataset em questão removendo colunas desnecessárias, agrupando os dados necessários, tratando dados NaN e transformando dados de colunas em novas linhas e retornando apenas o necessário para as análises.

    Args:
        file_path (str): Caminho do arquivo CSV a ser tratado.

    Returns:
        pd.DataFrame: DataFrame com os dados tratados.
    """
    # Lendo o arquivo
    df: pd.DataFrame = pd.read_csv(file_path)
    
    # Removendo colunas desnecessárias
    df.drop(['Indicator Code', 'Country Code'], axis=1, inplace=True)
    df.drop(df.columns[-1], axis=1, inplace=True)

    # Transformando o DataFrame
    df_melted: pd.DataFrame = df.melt(id_vars=['Country Name', 'Indicator Name'], 
                                      var_name='Year', 
                                      value_name='terras_araveis(%)')

    # Renomeando as colunas
    df_melted = df_melted.rename(columns={
        'Country Name': 'area_name',
        'Indicator Name': 'indicator_name',
        'Year': 'ano'
    })

    # Convertendo a coluna 'Year' para int
    df_melted['ano'] = df_melted['ano'].astype(int)

    # Removendo coluna desnecessária
    df_melted.drop(['indicator_name'], axis=1, inplace=True)

    # Pegando apenas de 1961 a 2022
    df_periodo: pd.DataFrame = df_melted[(df_melted['ano'] > 1960) & (df_melted['ano'] < 2023)]

    # Obtendo apenas os países e o mundo:
    countries_to_keep = big_strings.countries_to_keep_worldbank
    df_filtered = df_periodo[df_periodo['area_name'].isin(countries_to_keep)]
    df_filtered.reset_index(drop=True, inplace=True)

    # Dando um código para cada, para poder integrar com outros datasets
    country_codes = big_dicts.countries_codes_worldbank
    df_filtered['country_code'] = df_filtered['area_name'].map(country_codes)

    # Removendo os nomes antigos
    df_renamed: pd.DataFrame = df_filtered.drop('area_name', axis=1)

    # Arredonda para tres casas decimais
    df_renamed["terras_araveis(%)"] = df_renamed["terras_araveis(%)"].round(3)

    return df_renamed

# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_arable_land(path_data)[preprocessamento_arable_land(path_data)['ano']>1960])