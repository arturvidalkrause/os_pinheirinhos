"""
    Este módulo realiza uma análise de regressão linear da produção agrícola por hectare ao longo dos anos, agrupando os países em três categorias: desenvolvidos, emergentes e em desenvolvimento.

    A análise inclui o cálculo do coeficiente angular da regressão (slope) e a geração de um gráfico de linha que exibe a variação da produção agrícola por hectare ao longo do tempo para cada grupo de países. O módulo também calcula o valor de R² para avaliar a adequação do modelo de regressão linear.

    Funções:
    - regressao_por_grupo: Realiza uma regressão linear dos dados ao longo do tempo para um grupo de países.
    - mean: Calcula a média da produção por hectare para cada grupo de países.
    - calcular_r2_total: Calcula o coeficiente de determinação (R²) da regressão linear para o conjunto de dados combinado.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr
import altair as alt
import json

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SETS_RESUMOS

def regressao_por_grupo(grupo: pd.DataFrame) -> np.float64:
    """
    Realiza uma regressão linear dos dados de produção por hectare ao longo dos anos para um grupo de países.

    Args:
        grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Produção por hectare (t)'.

    Returns:
        np.float64: Coeficiente angular da regressão linear.
    """
    if grupo.empty:
        return np.nan  # Retorna NaN se o grupo estiver vazio

    x: pd.Series = grupo[["ano"]]
    y: pd.Series = grupo["Produção por hectare (t)"]

    modelo = LinearRegression()
    modelo.fit(x, y)
    slope = modelo.coef_[0]

    return slope

def mean(grupo: pd.DataFrame) -> pd.Series:
    """
    Calcula a média da produção por hectare para um grupo de países.

    Args:
        grupo (pd.DataFrame): DataFrame contendo os dados do grupo de países.

    Returns:
        pd.Series: Série contendo a média da produção por hectare.
    """
    return pd.Series({"Produção por hectare (t)": grupo["Produção por hectare (t)"].mean()})

# Lendo o arquivo JSON com a classificação dos países
json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"

with open(json_file_path, 'r') as json_file:
    countries_data = json.load(json_file)

# Carregando o dataset de produção
df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")

# Calculando Produção por hectare
df_producao["Produção por hectare (t)"] = df_producao["producao_total(t)"] / df_producao["area_total_de_producao(ha)"]

# Removendo valores nulos
df_producao = df_producao.dropna()

# Filtrando os países por categoria: desenvolvidos, emergentes e em desenvolvimento
df_developed = df_producao[df_producao["country_code"].isin(countries_data['developed'])]
df_emerging = df_producao[df_producao["country_code"].isin(countries_data['emerging'])]
df_subdeveloped = df_producao[df_producao["country_code"].isin(countries_data['developing_countries'])]

# Aplicando a regressão para cada grupo de países
df_developed_resume = df_developed.groupby(["country_code"], observed=False).apply(regressao_por_grupo).reset_index()
df_emerging_resume = df_emerging.groupby(["country_code"], observed=False).apply(regressao_por_grupo).reset_index()
df_subdeveloped_resume = df_subdeveloped.groupby(["country_code"], observed=False).apply(regressao_por_grupo).reset_index()

# Armazenando os valores de slope
slope = {
    "developed": regressao_por_grupo(df_developed_resume),
    "emerging": regressao_por_grupo(df_emerging_resume),
    "developing_countries": regressao_por_grupo(df_subdeveloped_resume),
}

# Imprimindo os valores de slope para cada grupo de países
for group, coefficient in slope.items():
    print(f"O coeficiente de regressão para {group} é: {coefficient:.4f}")

# Adicionando a categoria do dataset aos resumos
df_developed_resume["dataset"] = "developed"
df_emerging_resume["dataset"] = "emerging"
df_subdeveloped_resume["dataset"] = "developing_countries"

# Combinando os resumos dos grupos em um único DataFrame
df_merge_resume = pd.concat([df_developed_resume, df_emerging_resume, df_subdeveloped_resume])

# Criando o gráfico de linhas com Altair
line_chart = alt.Chart(df_merge_resume).mark_line().encode(
    x=alt.X('ano:O', 
             axis=alt.Axis(
                 values=[1961, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022]
             )), 
    y=alt.Y('Produção por hectare (t):Q'),
    color='dataset:N',             # Cor das linhas baseado no dataset
    tooltip=['ano:O', 'dataset:N', 'Produção por hectare (t):Q']  # Tooltip com informações
).properties(
    title='Gráfico de Linhas Triplo: Produção por Hectare por Ano',
    width=600,
    height=400
)

# Salvando o gráfico gerado como SVG
line_chart.save('./src/graphs/hip_3.svg')

# Calculando estatísticas descritivas para os grupos de países
df_developed_resume_desc = df_developed_resume.describe()["Produção por hectare (t)"].to_frame().rename(columns={"Produção por hectare (t)": "developed"}).transpose()
df_emerging_resume_desc = df_emerging_resume.describe()["Produção por hectare (t)"].to_frame().rename(columns={"Produção por hectare (t)": "emerging"}).transpose()
df_subdeveloped_resume_desc = df_subdeveloped_resume.describe()["Produção por hectare (t)"].to_frame().rename(columns={"Produção por hectare (t)": "developing_countries"}).transpose()

df_resume_desc = pd.concat([df_developed_resume_desc, df_emerging_resume_desc, df_subdeveloped_resume_desc])

print(df_resume_desc)

def calcular_r2_total(grupo: pd.DataFrame) -> float:
    """
    Calcula o R² de uma regressão linear para um DataFrame.

    Args:
        grupo (pd.DataFrame): DataFrame contendo os dados.

    Returns:
        float: R² da regressão linear.
    """
    x = grupo[["ano"]]
    y = grupo["Produção por hectare (t)"]

    modelo = LinearRegression()
    modelo.fit(x, y)
    r_squared = modelo.score(x, y)

    return r_squared

# Calculando o R² total
r_squared_total = calcular_r2_total(df_merge_resume)

# Exibindo o valor de R² total
print(f"O R² total é: {r_squared_total:.4f}")
