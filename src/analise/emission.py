"""Realiza uma análise exploratória dos dados do dataSet sobre emissões de CO², afim de interpletar melhor os dados"""

import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_EMISSION

def regressao_por_pais(grupo: pd.DataFrame) -> pd.Series:
	"""
	Realiza uma regressão linear dos dados de emissões de CO₂ ao longo de um período para cada país.

	Args:
		grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Annual CO₂ emissions'.

	Returns:
		pd.Series: Retorna uma série contendo o coeficiente angular (slope) da regressão linear.

	Variáveis:
		x (pd.Series): Série com os anos (coluna 'ano').
		y (pd.Series): Série com os dados de emissões de CO₂ (coluna 'Annual CO₂ emissions').
	"""
	x: pd.Series = grupo[["ano"]]
	y: pd.Series = grupo["Annual CO₂ emissions"]

	modelo = LinearRegression()
	modelo.fit(x, y)
	
	slope = modelo.coef_[0]

	return pd.Series({"slope": slope})


def format_num(valor: int | None) -> str:
	"""
	Formata um número inteiro ou float, separando os milhares por ponto.

	Args:
		valor (int | None): Valor a ser formatado.

	Returns:
		str: Valor formatado como string com separação de milhares (e.g., 1.000.000) ou "N/A" se o valor for nulo.
	"""
	if pd.isna(valor):
		return "N/A"
	return f"{valor:,.0f}".replace(",", ".")


# Carrega os dados do dataset de emissões de CO₂
PATH_DATASET_EMISSION: Path = Path(DATA_SET_EMISSION)

df: pd.DataFrame = pd.read_parquet(PATH_DATASET_EMISSION, engine="pyarrow")

# Exclui valores NaN (para a regressão linear) e remove a Antártida dos dados
df = df.dropna()
df = df[df["country_code"] != "ATA"]

# Cria uma nova coluna com o log dos valores de emissões
df["log_emissions"] = np.log(df["Annual CO₂ emissions"] + 1)

# Aplica regressão linear por país e agrupa pelos códigos e nomes dos países
resultados_regressao = df.groupby(['country_code', 'pais'], observed=False).apply(regressao_por_pais).reset_index().round(0)

# Cria uma nova coluna com o valor das emissões formatado
resultados_regressao["slope (t)"] = resultados_regressao["slope"].apply(format_num)

# Calcula o log do coeficiente de inclinação (slope) para comparar as taxas de crescimento
resultados_regressao["slope_log"] = np.log(resultados_regressao["slope"])

# Gera o gráfico choropleth que exibe o log do coeficiente de inclinação da regressão linear das emissões de CO₂
fig_reg_linear = px.choropleth(resultados_regressao, 
                    locations="country_code",
                    color="slope_log",
                    hover_name="pais",
					hover_data={"slope (t)": True,"slope": False, "country_code": False, "slope_log": False},
					)

# Ajusta o layout do gráfico
fig_reg_linear.update_layout(
	title={
		'text': "Compara o log da regressão linear do total de emissões ano a ano por país",
		'x': 0.5
	}
)

# Adiciona uma anotação ao gráfico explicando o cálculo
fig_reg_linear.add_annotation(
    text="Agrupa os dados por país e calcula a regressão linear, utilizando o log do coeficiente de inclinação para comparação",
	y= -0.05,
	showarrow=False,
)

# Exibe o gráfico
fig_reg_linear.show()
