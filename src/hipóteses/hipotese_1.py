"""
    Este módulo realiza a análise de correlação entre Produção Total (em toneladas) e o Produto Interno Bruto (PIB) para diversos países, utilizando dados unificados de produção agrícola e PIB.

    Ele calcula a correlação de Pearson e Spearman entre os dois indicadores, além de gerar gráficos de dispersão com linhas de regressão para visualizar a relação entre a produção total e o PIB.

    A biblioteca Plotly Express é usada para gerar gráficos interativos e a biblioteca Altair é usada para criar gráficos de dispersão com regressão linear.

    O módulo também carrega resumos de dados de produção e PIB e gera gráficos com essas informações resumidas.
"""

import sys
import pandas as pd
import altair as alt
import plotly.express as px
from scipy.stats import spearmanr
from pathlib import Path

# Adiciona o diretório raiz ao sys.path para importar arquivos de configuração
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PRODUCAO, DATA_SET_PIB, DATA_SETS_RESUMOS

# Carregando os datasets de produção agrícola e PIB
df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
df_pib = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

# Unindo os datasets com base no código do país e ano
df_merged = pd.merge(df_producao, df_pib, on=["country_code", "ano"])

# Calculando a Produção por Hectare
df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]

# Filtro para excluir dados do mundo ('WLD')
df_merged = df_merged[df_merged["country_code"] == "WLD"]

# Removendo valores nulos
df_merged = df_merged.dropna()

# Calculando a correlação de Pearson entre produção total e PIB
corr_PIB_and_producao_total = df_merged[['producao_total(t)', 'PIB']].corr()['producao_total(t)']["PIB"]

# Calculando a correlação de Spearman
spearman_result = spearmanr(df_merged['producao_total(t)'], df_merged['PIB'])

# Extraindo a estatística de Spearman e o p-value
spearman_statistic = spearman_result.statistic
p_value = spearman_result.pvalue

# Exibindo os resultados de correlação
print(f"A correlação de Spearman entre Produção Total e PIB é: {spearman_statistic:.3f}")
print(f"O valor de p associado é: {p_value:.3e}")
print(f"A correlação entre Produção total(t) e PIB($) é: {round(corr_PIB_and_producao_total, 3)}")

# Gerando gráfico de dispersão com Plotly
fig = px.scatter(df_merged,
				 x='producao_total(t)',
				 y='PIB',
				 hover_data={'country_code': True, 'ano': True},
				 title="Gráfico de dispersão: Produção total(t) vs PIB($)",
				 trendline='ols',
				 )

# Centralizando o título do gráfico
fig.update_layout(title_x=0.5)

# plotando o gráfico de dispersão gerado por Plotly
fig.show()

# Carregando resumos de dados de produção e PIB
df_resumo_producao = pd.read_parquet(DATA_SETS_RESUMOS + "/produção.parquet", engine="pyarrow")
df_resumo_pib = pd.read_parquet(DATA_SETS_RESUMOS + "/pib.parquet", engine="pyarrow")

# Unindo os resumos com base no código do país
df_resumo_merged = pd.merge(df_resumo_producao, df_resumo_pib, on=["country_code", "pais"])
df_resumo_merged = df_resumo_merged[df_resumo_merged["country_code"] != "WLD"]

# Gerando gráfico de dispersão para os resumos
fig_resumo = px.scatter(df_resumo_merged,
				 x='slope_x',
				 y='slope_y',
				 hover_data={'country_code': True}
				 )

fig_resumo.show()

# Criando gráfico de dispersão com Altair
scatter = alt.Chart(df_merged).mark_point().encode(
    x=alt.X('producao_total(t):Q', scale=alt.Scale(domain=[0, 9000000000]),  title='Produção total (t)'),
    y=alt.Y('PIB:Q', scale=alt.Scale(domain=[0, 110000000000000]), title='PIB ($)'),
    tooltip=['country_code', 'ano']  # Dados exibidos ao passar o mouse
).properties(
    title='Gráfico de dispersão: Produção total(t) vs PIB($)',
    width=600,
    height=400
)

# Adicionando uma linha de regressão linear ao gráfico de dispersão
regression_line = scatter.transform_regression(
    'producao_total(t)', 'PIB', method='linear', extent=[3000000000, df_merged['producao_total(t)'].max()],
).mark_line(color='red')

# Combinando o gráfico de dispersão e a linha de regressão
final_chart = scatter + regression_line

# Salvando o gráfico final como SVG
final_chart.save('./src/graphs/grafico_dispersao_Produção_vs_PIB.svg')
