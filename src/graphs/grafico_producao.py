"""
	Este módulo carrega e processa dados de produção agrícola total por país ao longo dos anos, gera um gráfico que visualiza essa produção, e salva o gráfico em formato SVG.

	O gráfico de área exibe a produção total agrícola em toneladas ao longo dos anos para diferentes países.
	O módulo utiliza a biblioteca Altair para a visualização de dados e pandas para a manipulação de dados.
"""
import os
import pandas as pd
import altair as alt

# Desabilitando o limite máximo de linhas para visualizações grandes
alt.data_transformers.disable_max_rows()

# Definindo o diretório do dataset de produção total e área
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/producao_total_e_area.csv")

# Carregando o dataset a partir do arquivo CSV
df = pd.read_csv(path_data, index_col=0)

# Gerando o gráfico de área para produção agrícola total por país
Countries = alt.Chart(df, title="Produção ao longo dos anos").mark_area(opacity=1).encode(
	x=alt.X('ano:N', axis=alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
	y=alt.Y('producao_total(t):Q', title='Produção Total (t)'),
	color=alt.Color('country_code:N').scale(scheme="warmgreys").legend(None)
).properties(
	width=300  # Largura do gráfico
)

# Salvando o gráfico gerado no diretório especificado como arquivo SVG
Countries.save('src/graphs/grafico_producao.svg')
