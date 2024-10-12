"""
    Este módulo realiza a análise de correlação entre a produção por hectare, o uso de pesticidas e o uso de fertilizantes em diferentes grupos de países (desenvolvidos, emergentes e em desenvolvimento). Além disso, também realiza uma regressão linear para analisar a relação entre esses fatores ao longo do tempo.

    A análise inclui:
    - Cálculo da correlação para o conjunto total de dados e para cada grupo de países.
    - Cálculo da inclinação de uma regressão linear para prever a produção por hectare ao longo do tempo.

    A saída consiste nas correlações entre as variáveis "Produção por hectare (t)", "uso_total_de_pesticidas(t)" e "uso_total_de_fertilizantes(t)" para o total de países, bem como para os três grupos (desenvolvidos, emergentes e em desenvolvimento).
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr
import altair as alt
import json

# Adiciona o diretório raiz ao sys.path para importar módulos locais
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SET_FERTILIZANTES, DATA_SETS_RESUMOS, DATA_SET_PESTICIDAS

def regressao_por_grupo(grupo: pd.DataFrame) -> np.float64:
    """
    Realiza uma regressão linear com os dados ao longo de um período.

    Args:
        grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Produção por hectare (t)'.

    Returns:
        np.float64: Coeficiente angular da reta da regressão linear.

    Variáveis:
        x (pd.Series): Série com os anos.
        y (pd.Series): Série com a produção por hectare.
    """
    if grupo.empty:
        return np.nan  # Retorna NaN se o grupo estiver vazio

    x: pd.Series = grupo[["ano"]]
    y: pd.Series = grupo["Produção por hectare (t)"]

    modelo = LinearRegression()
    modelo.fit(x, y)
    slope = modelo.coef_[0]

    return slope

# Lê o arquivo JSON contendo a classificação dos países
json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"

with open(json_file_path, 'r') as json_file:
    countries_data = json.load(json_file)

# Carregando os datasets de produção, pesticidas e fertilizantes
df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
df_pesticidas = pd.read_parquet(DATA_SET_PESTICIDAS, engine="pyarrow")
df_fertilizantes = pd.read_parquet(DATA_SET_FERTILIZANTES, engine="pyarrow")

# Unindo os DataFrames de produção, pesticidas e fertilizantes
df_merged = pd.merge(df_producao, df_pesticidas, on=["country_code", "ano"])
df_merged = pd.merge(df_merged, df_fertilizantes, on=["country_code", "ano"])

# Removendo valores NaN
df_merged = df_merged.dropna()

# Calculando a produção por hectare
df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]

# Criando DataFrames separados para países desenvolvidos, emergentes e em desenvolvimento
df_developed = df_merged[df_merged["country_code"].isin(countries_data['developed'])]
df_emerging = df_merged[df_merged["country_code"].isin(countries_data['emerging'])]
df_subdeveloped = df_merged[df_merged["country_code"].isin(countries_data['developing_countries'])]

# Exibindo as correlações para o conjunto total de países e para cada grupo de países
print('Total:', df_merged[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")

print('Desenvolvidos:', df_developed[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
print('Emergentes:', df_emerging[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
print('Em desenvolvimento:', df_subdeveloped[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
