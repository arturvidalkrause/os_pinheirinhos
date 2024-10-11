import pandas as pd
import big_strings
import big_dicts

def preprocessamento_producao(file_path: str) -> pd.DataFrame:
    """
    Trata o dataset em questão removendo colunas desnecessárias, agrupando os dados necessários,
    tratando dados NaN e transformando dados de colunas em novas linhas, retornando apenas o necessário para as análises.

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

    # Renomear as colunas dos anos para remover o prefixo 'Y'
    df.columns = df.columns.str.replace(r'^Y', '', regex=True)

    # Definir colunas para remover
    colunas_para_remover = ['Area Code', 'Area Code (M49)', 'Item Code (CPC)']
    
    # Remover as colunas que existem no DataFrame
    colunas_existentes = [col for col in colunas_para_remover if col in df.columns]
    df.drop(columns=colunas_existentes, axis=1, inplace=True)

    # Pegar apenas os vegetais
    vegetais = big_strings.vegetais_producao
    df_vegetal = df[df['Item'].isin(vegetais)]

    # Remover colunas desnecessárias
    df_vegetal.drop(['Item Code', 'Element Code'], axis=1, inplace=True, errors='ignore')

    # Separar em área e produção e eliminar colunas desnecessárias
    df_area = df_vegetal[df_vegetal['Element'] == 'Area harvested'].drop(['Element', 'Unit'], axis=1)
    df_production = df_vegetal[df_vegetal['Element'] == 'Production'].drop(['Element', 'Unit'], axis=1)

    # Verificar se o DataFrame resultante está vazio após a filtragem
    if df_area.empty or df_production.empty:
        raise ValueError("Dados insuficientes após a filtragem. Verifique as colunas 'Element' e 'Unit'.")

    # Reorganizando os DataFrames
    # Área
    df_area_melted = df_area.melt(id_vars=['Area', 'Item'], var_name='ano', value_name='area_total_de_producao(ha)')
    df_area_pivot = df_area_melted.pivot_table(index=['Area', 'ano'], columns='Item', values='area_total_de_producao(ha)', fill_value=0).reset_index()

    # Produção
    df_production_melted = df_production.melt(id_vars=['Area', 'Item'], var_name='ano', value_name='producao_total(t)')
    df_production_pivot = df_production_melted.pivot_table(index=['Area', 'ano'], columns='Item', values='producao_total(t)', fill_value=0).reset_index()

    # Criar uma coluna com o total para ambos os DataFrames
    df_area_pivot['Total'] = df_area_pivot.drop(columns=['Area', 'ano']).apply(pd.to_numeric, errors='coerce').sum(axis=1)
    df_production_pivot['Total'] = df_production_pivot.drop(columns=['Area', 'ano']).apply(pd.to_numeric, errors='coerce').sum(axis=1)

    # Pegando os datasets apenas com o total
    df_area_total = df_area_pivot[['Area', 'ano', 'Total']]
    df_production_total = df_production_pivot[['Area', 'ano', 'Total']]

    # Renomear as colunas
    df_production_total.rename(columns={'Total': 'producao_total(t)', 'Area': 'area_name'}, inplace=True)
    df_area_total.rename(columns={'Total': 'area_total_de_producao(ha)', 'Area': 'area_name'}, inplace=True)

    # Unir ambos os DataFrames em um só
    df_combinado = pd.merge(df_production_total, df_area_total, on=['area_name', 'ano'], how='outer')

    # Filtrar apenas países e o mundo
    countries_to_keep = big_strings.countries_to_keep_faostat
    df_filtered = df_combinado[df_combinado['area_name'].isin(countries_to_keep)].reset_index(drop=True)

    # Adicionar o código de país
    country_codes = big_dicts.country_codes_faostat
    df_filtered['country_code'] = df_filtered['area_name'].map(country_codes)

    # Remover a coluna 'area_name'
    df_renamed = df_filtered.drop('area_name', axis=1)

    # Função para preencher anos faltantes
    def preencher_anos_faltantes(df):
        anos = pd.Series(range(1961, 2023))
        country_codes = df['country_code'].unique()
        todos_anos = pd.MultiIndex.from_product([country_codes, anos], names=['country_code', 'ano'])
        df_todos_anos = pd.DataFrame(index=todos_anos).reset_index()
        df['ano'] = df['ano'].astype(int)
        df_completo = pd.merge(df_todos_anos, df, on=['country_code', 'ano'], how='left')
        return df_completo

    df_completo = preencher_anos_faltantes(df_renamed)

    # Arredondar para duas casas decimais
    df_completo["producao_total(t)"] = df_completo["producao_total(t)"].round(2)

    return df_completo




# Exemplos de uso (descomente para executar)
# path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos")
# print(preprocessamento_producao(path_data))
# print(preprocessamento_producao(path_data)['area_name'].unique())