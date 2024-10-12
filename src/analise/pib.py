"""Realiza uma análise exploratória dos dados do dataSet sobre o PIB de cada pais, afim de interpletar melhor os dados"""

import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PIB, DATA_SETS_RESUMOS


def regressao_por_pais(grupo: pd.DataFrame) -> pd.Series:
	"""
	Realiza uma regressão linear dos dados de PIB ao longo de um período para cada país.

	Args:
		grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'PIB'.

	Returns:
		pd.Series: Retorna uma série contendo o coeficiente angular (slope) da regressão linear e o nome do país.

	Variáveis:
		x (pd.Series): Série com os anos (coluna 'ano').
		y (pd.Series): Série com os dados de PIB (coluna 'PIB').
	"""
	x: pd.Series = grupo[["ano"]]
	y: pd.Series = grupo["PIB"]

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
		str: Valor formatado como string no formato de dólar (e.g., $1.000.000) ou "N/A" se o valor for nulo.
	"""
	if pd.isna(valor):
		return "N/A"
	return f"${valor:,.0f}".replace(",", ".")


# Carrega os dados do dataset de PIB
df = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")
df2 = df.groupby(["country_code"])

# Cria uma cópia do DataFrame para trabalhar com os dados temporais
df_temporal = df.copy()

# Calcula o log do PIB e adiciona como nova coluna
df_temporal["pib_log"] = np.log(df_temporal["PIB"])
df_temporal["PIB ($)"] = df_temporal["PIB"].apply(format_dolar)

# Gera o gráfico choropleth (mapa coroplético) animado para exibir o log do PIB por país ao longo dos anos
fig_pib = px.choropleth(df_temporal,
						locations= "country_code",
						color="pib_log",
						hover_name="pais",
						hover_data={"PIB ($)": True, "country_code": False, "pib_log": False},
						range_color=[20, 30],
						animation_frame="ano"
						)

# fig_pib.show()


# Aplica regressão linear por país, agrupando pelos códigos dos países
resultados_regressao = df.groupby(['country_code'], observed=False).apply(regressao_por_pais).reset_index().round(0)

# Calcula o log do coeficiente de inclinação (slope) para comparar as taxas de crescimento do PIB
resultados_regressao["slope_log"] = np.log(resultados_regressao["slope"])
resultados_regressao["Slope ($)"] = resultados_regressao["slope"].apply(format_dolar)

# Gera o gráfico choropleth que exibe o log do coeficiente de inclinação da regressão linear do PIB
fig_reg_linear = px.choropleth(resultados_regressao,
						locations= "country_code",
						color= "slope_log",
						hover_name= "pais",
						hover_data= {"Slope ($)": True, "country_code": False, "slope_log": False},
						range_color= [17, 27]
						)

# Ajusta o layout do gráfico
fig_reg_linear.update_layout(
	title={
		'text': "Compara o log da regressão linear do PIB ano a ano de cada país",
		'x': 0.5
	}
)

# Adiciona uma anotação ao gráfico explicando o cálculo
fig_reg_linear.add_annotation(
	text= "Agrupa os dados por país e calcula a regressão linear, porém utiliza-se o log do coeficiente de inclinação para comparar",
	y= -0.05,
	showarrow= False
)

# Exibe o gráfico
fig_reg_linear.show()

# Salva os resultados da regressão em um arquivo parquet
# resultados_regressao.to_parquet(DATA_SETS_RESUMOS + "/pib.parquet", engine="pyarrow", index=False)