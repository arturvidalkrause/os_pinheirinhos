import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr
import altair as alt

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SET_PIB, DATA_SETS_RESUMOS

df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
df_pib = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

df_merged = pd.merge(df_producao, df_pib, on=["country_code", "ano", "pais"])

df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]

df_merged = df_merged[df_merged["country_code"] == "WLD"]

df_merged = df_merged.dropna()

corr_PIB_and_producao_total = df_merged[['producao_total(t)', 'PIB']].corr()['producao_total(t)']["PIB"]

# Calculando a correlação de Spearman
spearman_result = spearmanr(df_merged['producao_total(t)'], df_merged['PIB'])

# Extraindo a estatística e o p-value
spearman_statistic = spearman_result.statistic
p_value = spearman_result.pvalue

# Exibindo os resultados de forma formatada
print(f"A correlação de Spearman entre Produção Total e PIB é: {spearman_statistic:.3f}")
print(f"O valor de p associado é: {p_value:.3e}")

print(f"A correlação entre Produção total(t) e PIB($) é: {round(corr_PIB_and_producao_total, 3)}")

fig = px.scatter(df_merged,
				 x='producao_total(t)',
				 y='PIB',
				 hover_data={'country_code': True, 'ano': True},
				 title="Gráfico de dispersão: Produção total(t) vs PIB($)",
				 trendline='ols',
				 )

# Centralizando o título
fig.update_layout(title_x=0.5)

# fig.show()

df_resumo_producao = pd.read_parquet(DATA_SETS_RESUMOS + "/produção.parquet", engine="pyarrow")
df_resumo_pib = pd.read_parquet(DATA_SETS_RESUMOS + "/pib.parquet", engine="pyarrow")

df_resumo_merged = pd.merge(df_resumo_producao, df_resumo_pib, on=["country_code", "pais"])
# print(df_resumo_merged)
df_resumo_merged = df_resumo_merged[df_resumo_merged["country_code"] != "WLD"]

fig_resumo = px.scatter(df_resumo_merged,
				 x='slope_x',
				 y='slope_y',
				 hover_data={'country_code': True}
				 )

# fig_resumo.show()


# Criando o gráfico de dispersão com Altair
scatter = alt.Chart(df_merged).mark_point().encode(
    x=alt.X('producao_total(t):Q',scale=alt.Scale(domain=[0, 9000000000]),  title='Produção total (t)'),
    y=alt.Y('PIB:Q', scale=alt.Scale(domain=[0, 110000000000000]), title='PIB ($)'),
    tooltip=['country_code', 'ano']  # Dados a serem exibidos ao passar o mouse
).properties(
    title='Gráfico de dispersão: Produção total(t) vs PIB($)',
    width=600,
    height=400
)

# Adicionando a linha de regressão
regression_line = scatter.transform_regression(
    'producao_total(t)', 'PIB', method='linear', extent=[3000000000, df_merged['producao_total(t)'].max()],
).mark_line(color='red')

# Combinando o gráfico de dispersão e a linha de regressão
final_chart = scatter + regression_line

# Exibindo o gráfico
# final_chart.show()

# Exportando para SVG
final_chart.save('./src/graphs/grafico_dispersao_Produção_vs_PIB.svg')