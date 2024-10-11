import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SET_PIB, DATA_SETS_RESUMOS

df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
df_pib = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

df_merged = pd.merge(df_producao, df_pib, on=["country_code", "ano", "pais"])

print(df_merged)
print(df_merged[['producao_total(t)', 'area_total_de_producao(ha)', 'PIB']].corr())
print(spearmanr(df_merged['producao_total(t)'], df_merged['PIB']))

df_resumo_producao = pd.read_parquet(DATA_SETS_RESUMOS + "/produção.parquet", engine="pyarrow")
df_resumo_pib = pd.read_parquet(DATA_SETS_RESUMOS + "/pib.parquet", engine="pyarrow")


df_resumo_merged = pd.merge(df_resumo_producao, df_resumo_pib, on=["country_code", "pais"])

# print(df_resumo_merged.columns)