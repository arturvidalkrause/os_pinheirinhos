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
	y: pd.Series = grupo["Annual CO₂ emissions"]

	modelo = LinearRegression()
	modelo.fit(x, y)
	
	slope = modelo.coef_[0]

	return pd.Series({"slope": slope})

def format_num(valor: int | None) -> str:
	"""Formata em número

	Args:
		valor (int): valor a ser formatado

	Returns:
		str: Valor formatado
	"""
	if pd.isna(valor):
		return "N/A"
	return f"{valor:,.0f}".replace(",", ".")


PATH_DATASET_EMISSION: Path = Path(DATA_SET_EMISSION)

df: pd.DataFrame = pd.read_parquet(PATH_DATASET_EMISSION, engine="pyarrow")

# Exclui valores NaN(para a regressão linear) e a Antartida
df = df.dropna()
df = df[df["country_code"] != "ATA"]

# Cria uma nova coluna com o log dos valores
df["log_emissions"] = np.log(df["Annual CO₂ emissions"] + 1)

# Nas proximas versões do pandas pode ser necessário usar "include_groups=False" ou explicitamente selecionar as colunas após o agrupamento.
resultados_regressao = df.groupby(['country_code', 'pais'], observed=False).apply(regressao_por_pais).reset_index().round(0)
# resultados_regressao = resultados_regressao.dropna().reset_index()
print(resultados_regressao)

# Cria uma nova coluna com o valor das emissões formatado
resultados_regressao["slope (t)"] = resultados_regressao["slope"].apply(format_num)

resultados_regressao["slope_log"] = np.log(resultados_regressao["slope"])

fig_reg_linear = px.choropleth(resultados_regressao, 
                    locations="country_code",
                    color="slope_log",
                    hover_name="pais",
					hover_data={"slope (t)": True,"slope": False, "country_code": False, "slope_log": False},
					)

fig_reg_linear.update_layout(
	title={
		'text': "Compara o log da regressão linear do total de emissões ano a ano por país",
		'x': 0.5
	}
)

fig_reg_linear.add_annotation(
    text="Agrupa os dados por pais e calcula a regressão linear, porém utiliza-se o log do coeficiente de inclinação comparar",
	y= -0.05,
	showarrow=False,
)

fig_reg_linear.show()