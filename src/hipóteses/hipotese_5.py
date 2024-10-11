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

from config import DATA_SET_PRODUCAO, DATA_SET_FERTILIZANTES, DATA_SETS_RESUMOS, DATA_SET_PESTICIDAS

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
	if grupo.empty:
		return np.nan  # Retorna NaN se o grupo estiver vazio

	x: pd.Series = grupo[["ano"]]
	y: pd.Series = grupo["Produção por hectare (t)"]

	modelo = LinearRegression()
	modelo.fit(x, y)
	slope = modelo.coef_[0]

	return slope

# le o json da classificação dos paises
json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"

with open(json_file_path, 'r') as json_file:
	countries_data = json.load(json_file)

df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
df_pesticidas = pd.read_parquet(DATA_SET_PESTICIDAS, engine="pyarrow")
df_fertilizantes = pd.read_parquet(DATA_SET_FERTILIZANTES, engine="pyarrow")

df_merged = pd.merge(df_producao, df_pesticidas, on=["country_code", "ano", "pais"])
df_merged = pd.merge(df_merged, df_fertilizantes, on=["country_code", "ano", "pais"])

df_merged = df_merged.dropna()

df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]

df_mergedd = df_merged.dropna()

df_developed = df_merged[df_merged["country_code"].isin(countries_data['developed'])]
df_emerging = df_merged[df_merged["country_code"].isin(countries_data['emerging'])]
df_subdeveloped = df_merged[df_merged["country_code"].isin(countries_data['developing_countries'])]

print('total:',df_mergedd[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")

print('Desenvolvidos:', df_developed[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
print('Emergentes:', df_emerging[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
print('Em desenvolvimento:', df_subdeveloped[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")