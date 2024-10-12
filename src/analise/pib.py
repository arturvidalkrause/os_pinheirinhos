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
	y: pd.Series = grupo["PIB"]

	if x.isna().any().any() or y.isna().any():
		return pd.Series({"slope": np.nan, "pais": grupo['pais'].iloc[0]})

	modelo = LinearRegression()
	modelo.fit(x, y)
    
	slope = modelo.coef_[0]
	return pd.Series({"slope": slope, "pais": grupo['pais'].iloc[0]})

def format_dolar(valor: int | None) -> str:
	"""Formata um numero para dolar

	Args:
		valor (int): valor a ser formatado

	Returns:
		str: Valor em dolar
	"""
	if pd.isna(valor):
		return "N/A"
	return f"${valor:,.0f}".replace(",", ".")


df = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")
df2 = df.groupby(["country_code"])

df_temporal = df.copy()

df_temporal["pib_log"] = np.log(df_temporal["PIB"])
# Cria uma nova coluna com o PIB formatado
df_temporal["PIB ($)"] = df_temporal["PIB"].apply(format_dolar)

fig_pib = px.choropleth(df_temporal,
						locations= "country_code",
						color="pib_log",
						hover_name="pais",
						hover_data={"PIB ($)": True, "country_code": False, "pib_log": False},
						range_color=[20, 30],
						animation_frame="ano"
						)

# fig_pib.show()


# Nas proximas versões do pandas pode ser necessário usar "include_groups=False" ou explicitamente selecionar as colunas após o agrupamento.
resultados_regressao = df.groupby(['country_code'], observed=False).apply(regressao_por_pais).reset_index().round(0)

resultados_regressao["slope_log"] = np.log(resultados_regressao["slope"])
resultados_regressao["Slope ($)"] = resultados_regressao["slope"].apply(format_dolar)

fig_reg_linear = px.choropleth(resultados_regressao,
						locations= "country_code",
						color= "slope_log",
						hover_name= "pais",
						hover_data= {"Slope ($)": True, "country_code": False, "slope_log": False},
						range_color= [17, 27]
						)

fig_reg_linear.update_layout(
	title={
		'text': "Compara o log da regressão linear do pib ano a ano de cada pais",
		'x': 0.5
	}
)

fig_reg_linear.add_annotation(
	text= "Agrupa os dados por pais e calcula a regressão linear, porém utiliza-se o log do coeficiente de inclinação comparar",
	y= -0.05,
	showarrow= False
)

fig_reg_linear.show()


# resultados_regressao.to_parquet(DATA_SETS_RESUMOS + "/pib.parquet", engine="pyarrow", index=False)