import plotly.express as px
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
	"""Realiza uma regressão linear com o dados ao longo de um periodo

	Args:
		grupo (pd.DataFrame):  DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Annual CO₂ emissions'.

	Returns:
		pd.Series: Coeficiente da angular da reta da regressão linear

	Variáveis:
		x (pd.Series): Série com os anos
		y (pd.Series): Série com as emissões de anuais de CO₂
	"""
	x: pd.Series = grupo[["ano"]]
	y: pd.Series = grupo["Produção por hectare (t)"]

	modelo = LinearRegression()
	modelo.fit(x, y)
	slope = modelo.coef_[0]

	return slope

def mean(grupo: pd.DataFrame) -> pd.Series:
	return pd.Series({"Produção por hectare (t)": grupo["Produção por hectare (t)"].mean()})

# le o json da classificação dos paises
json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"

with open(json_file_path, 'r') as json_file:
	countries_data = json.load(json_file)

df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")

df_producao["Produção por hectare (t)"] = df_producao["producao_total(t)"] / df_producao["area_total_de_producao(ha)"]

df_producao = df_producao.dropna()

df_developed = df_producao[df_producao["country_code"].isin(countries_data['developed'])]
df_emerging = df_producao[df_producao["country_code"].isin(countries_data['emerging'])]
df_subdeveloped = df_producao[df_producao["country_code"].isin(countries_data['subdeveloped'])]


df_developed_resume = df_developed.groupby(["ano"], observed= False).apply(mean).reset_index()
df_emerging_resume = df_emerging.groupby(["ano"], observed= False).apply(mean).reset_index()
df_subdeveloped_resume = df_subdeveloped.groupby(["ano"], observed= False).apply(mean).reset_index()

# print(df_developed_resume)

slope = {
	"developed": regressao_por_grupo(df_developed_resume),
	"emerging": regressao_por_grupo(df_emerging_resume),
	"subdeveloped": regressao_por_grupo(df_subdeveloped_resume),
}

# Imprimindo os valores de slope
for group, coefficient in slope.items():
    print(f"O coeficiente de regressão para {group} é: {coefficient:.4f}")

df_developed_resume["dataset"] = "developed"
df_emerging_resume["dataset"] = "emerging"
df_subdeveloped_resume["dataset"] = "subdeveloped"

df_merge_resume = pd.concat([df_developed_resume, df_emerging_resume, df_subdeveloped_resume])

# Criando o gráfico de linhas
line_chart = alt.Chart(df_merge_resume).mark_line().encode(
    x=alt.X('ano:O', 
             axis=alt.Axis(
                 values=[1961, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022]
             )), 
    y=alt.Y('Produção por hectare (t):Q'),
    color='dataset:N',             # Cor das linhas baseado no dataset
    tooltip=['ano:O', 'dataset:N', 'Produção por hectare (t):Q']  # Tooltip com informações
).properties(
    title='Gráfico de Linhas Triplo: Correlação por Ano',
    width=600,
    height=400
)

line_chart.save('grafico_dispersao3.svg')