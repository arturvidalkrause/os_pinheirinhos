"""
    Este módulo realiza uma análise de correlação entre Produção Agrícola (em toneladas) e o Produto Interno Bruto (PIB) para diferentes países classificados como desenvolvidos, emergentes e em desenvolvimento.

    A análise é feita com base nos dados de produção agrícola e PIB, com cálculos de correlação de Pearson e Spearman. O módulo também gera um gráfico de linha que mostra a evolução dessas correlações ao longo do tempo para cada grupo de países.

    Gráficos:
    - Um gráfico de linhas é gerado usando Altair, mostrando a evolução da correlação ao longo dos anos para os grupos de países desenvolvidos, emergentes e em desenvolvimento.
"""

import pandas as pd
import sys
from pathlib import Path
from scipy.stats import spearmanr
import altair as alt
import json

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SET_PIB, DATA_SETS_RESUMOS

def corr_analise(dataframe: pd.DataFrame, columns: list) -> dict:
    """
    Calcula a correlação de Pearson e Spearman entre duas colunas de um DataFrame.

    Args:
        dataframe (pd.DataFrame): O DataFrame contendo os dados.
        columns (list): Lista com os nomes das colunas a serem analisadas.

    Returns:
        dict: Dicionário com a correlação de Pearson, estatística de Spearman e valor p.
    """
    corr = dataframe[columns].corr()[columns[0]][columns[1]]

    # Calculando a correlação de Spearman
    spearman_result = spearmanr(dataframe[columns[0]], dataframe[columns[1]])

    # Extraindo a estatística e o p-value
    spearman_statistic = spearman_result.statistic
    p_value = spearman_result.pvalue

    # Exibindo os resultados de forma formatada
    print(f"A correlação de Spearman entre {columns[0]} e {columns[1]} é: {spearman_statistic:.3f}")
    print(f"O valor de p associado é: {p_value:.3e}")
    print(f"A correlação entre {columns[0]} e {columns[1]} é: {round(corr, 3)}")

    return {"corr": corr, "spearman_statistic": spearman_statistic, "p_value": p_value}

def corr_pais_ano(grupo: pd.DataFrame) -> pd.Series:
    """
    Calcula a correlação de Pearson e Spearman entre produção total e PIB para um grupo de países por ano.

    Args:
        grupo (pd.DataFrame): O DataFrame agrupado por país e ano.

    Returns:
        pd.Series: Série com a correlação de Pearson, estatística de Spearman e valor p.
    """
    corr = grupo[["producao_total(t)", "PIB"]].corr()["producao_total(t)"]["PIB"]

    # Calculando a correlação de Spearman
    spearman_result = spearmanr(grupo["producao_total(t)"], grupo["PIB"])

    # Extraindo a estatística e o p-value
    spearman_statistic = spearman_result.statistic
    p_value = spearman_result.pvalue

    return pd.Series({"corr": corr, "spearman_statistic": spearman_statistic, "p_value": p_value})

# Carregando o arquivo JSON com a classificação dos países
json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"

with open(json_file_path, 'r') as json_file:
    countries_data = json.load(json_file)

# Carregando os datasets de produção agrícola e PIB
df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
df_pib = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

# Unindo os datasets com base no código do país, ano e nome do país
df_merged = pd.merge(df_producao, df_pib, on=["country_code", "ano"])

# Calculando Produção por Hectare
df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]

# Removendo valores nulos
df_merged = df_merged.dropna()

# Filtrando os países por categoria: desenvolvidos, emergentes e em desenvolvimento
df_developed = df_merged[df_merged["country_code"].isin(countries_data['developed'])]
df_emerging = df_merged[df_merged["country_code"].isin(countries_data['emerging'])]
df_subdeveloped = df_merged[df_merged["country_code"].isin(countries_data['developing_countries'])]

# Resumindo a correlação por ano para cada grupo de países
df_developed_resume = df_developed.groupby(["ano"], observed=False).apply(corr_pais_ano).reset_index()
df_emerging_resume = df_emerging.groupby(["ano"], observed=False).apply(corr_pais_ano).reset_index()
df_subdeveloped_resume = df_subdeveloped.groupby(["ano"], observed=False).apply(corr_pais_ano).reset_index()

# Adicionando a classificação do dataset em cada resumo
df_developed_resume["dataset"] = "developed"
df_emerging_resume["dataset"] = "emerging"
df_subdeveloped_resume["dataset"] = "developing_countries"

# Unindo os resumos em um único DataFrame
df_merge_resume = pd.concat([df_developed_resume, df_emerging_resume, df_subdeveloped_resume])

# Criando o gráfico de linhas com Altair
line_chart = alt.Chart(df_merge_resume).mark_line().encode(
    x=alt.X('ano:O', 
             axis=alt.Axis(
                 values=[1961, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022]
             )), 
    y=alt.Y('corr:Q', scale=alt.Scale(domain=[0.55, 1]), title='Correlação entre Produção agrícola e PIB'),
    color='dataset:N',             # Cor das linhas baseado no dataset
    tooltip=['ano:O', 'dataset:N', 'corr:Q']  # Tooltip com informações
).properties(
    title='Gráfico de Linhas Triplo: Correlação por Ano',
    width=600,
    height=400
)

# Salvando o gráfico gerado como SVG
line_chart.save('./src/graphs/Produção_agricola_vs_ano.svg')