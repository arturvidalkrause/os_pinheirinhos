import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr


# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SETS_RESUMOS


def regressao_por_pais(grupo: pd.DataFrame) -> pd.Series:
	"""
	Realiza uma regressão linear para analisar a relação entre o ano e a produção por hectare de cada país.

	Args:
		grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Produção_por_hectare_(t)'.

	Returns:
		pd.Series: Retorna uma série contendo o coeficiente angular (slope) da regressão linear e o nome do país.

	Variáveis:
		x (pd.Series): Série com os anos (coluna 'ano').
		y (pd.Series): Série com os dados de produção por hectare (coluna 'Produção_por_hectare_(t)').
	"""
	x: pd.Series = grupo[["ano"]]
	y: pd.Series = grupo["Produção_por_hectare_(t)"]

	if x.isna().any().any() or y.isna().any():
		return pd.Series({"slope": np.nan, "pais": grupo['pais'].iloc[0]})

	modelo = LinearRegression()
	modelo.fit(x, y)
    
	slope = modelo.coef_[0]
	return pd.Series({"slope": slope, "pais": grupo['pais'].iloc[0]})


def format_dolar(valor: int | None) -> str:
	"""
	Formata um número inteiro ou float para o formato de dólar, separando os milhares por ponto.

	Args:
		valor (int | None): Valor a ser formatado.

	Returns:
		str: Valor formatado como string no formato de dólar (e.g., 1.000.000) ou "N/A" se o valor for nulo.
	"""
	if pd.isna(valor):
		return "N/A"
	return f"{valor:,.0f}".replace(",", ".")


def map_anual(df_temporal: pd.DataFrame) -> None:
	"""
	Gera um gráfico do tipo choropleth (mapa coroplético) animado para mostrar a produção agrícola por hectare (t) de cada país ao longo dos anos.

	Args:
		df_temporal (pd.DataFrame): DataFrame contendo os dados da produção agrícola por país, incluindo as colunas 'pais', 'country_code', 'Produção_por_hectare_(t)', e 'ano'.

	Returns:
		None: O gráfico é exibido diretamente e não há retorno.
	"""
	# Cria uma nova coluna com a produção por hectare formatada
	df_temporal["Produção por hectare (t)"] = df_temporal["Produção_por_hectare_(t)"].apply(format_dolar)

	fig_pib = px.choropleth(df_temporal,
							locations= "country_code",
							color="Produção_por_hectare_(t)",
							hover_name="pais",
							hover_data={"Produção por hectare (t)": True, "country_code": False, "Produção_por_hectare_(t)": False},
							range_color=[0, 27],
							animation_frame="ano",
							)

	fig_pib.show()


def map_reg_linear(df: pd.DataFrame) -> None:
	"""
	Gera um gráfico coroplético para representar a taxa média de crescimento anual (slope) da produção por hectare em cada país, utilizando regressão linear.

	Args:
		df (pd.DataFrame): DataFrame com os dados de produção por país, incluindo as colunas 'country_code', 'ano', 'Produção_por_hectare_(t)'.

	Returns:
		None: O gráfico é exibido diretamente e salvo como um arquivo SVG.
	"""
	df = df.dropna()
	# Aplica regressão linear por país
	resultados_regressao = df.groupby(['country_code'], observed=False).apply(regressao_por_pais).reset_index()

	# Formata o slope (taxa de crescimento) em formato de dólar
	resultados_regressao["Slope ($)"] = resultados_regressao["slope"].apply(format_dolar)

	fig_reg_linear = px.choropleth(resultados_regressao,
							locations= "country_code",
							color= "slope",
							hover_name= "pais",
							hover_data= {"Slope ($)": True, "country_code": False, "slope": True},
							range_color=[0,0.4]
							)

	fig_reg_linear.update_layout(
		title={
			'text': "Taxa média de crescimento anual da Produção por hectare(t)",
			'x': 0.5
		}
	)

	fig_reg_linear.add_annotation(
		text= "Periodo: 1961 a 2022",
		y= -0.05,
		showarrow= False
	)

	fig_reg_linear.show()
	fig_reg_linear.write_image("./src/graphs/choropleth_graph.svg")


# Carrega os dados do dataset de produção agrícola
df = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")

# Calcula a produção por hectare (toneladas por hectare)
df["Produção_por_hectare_(t)"] = df["producao_total(t)"] / df["area_total_de_producao(ha)"]

# Gera o mapa anual
map_anual(df)

# Gera o mapa da regressão linear
map_reg_linear(df)