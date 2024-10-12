"""
    Este módulo carrega e processa dados de temperatura média anual por país e mundial ao longo dos anos, gera um gráfico que visualiza essa temperatura, e salva o gráfico em formato SVG.

    O gráfico exibe a temperatura média anual de diferentes países com uma linha de tendência para a média global.
    O módulo utiliza a biblioteca Altair para a visualização de dados e pandas para a manipulação de dados.
"""
import os
import pandas as pd
import altair as alt

# Desabilitando o limite máximo de linhas para visualizações grandes
alt.data_transformers.disable_max_rows()

# Definindo o diretório do dataset de temperatura
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/temperatura.parquet")

# Carregando o dataset a partir do arquivo Parquet
df = pd.read_parquet(path_data)

# Filtrando os dados de países e do mundo
df_paises = df[df['country_code'] != 'WLD']
df_world = df[df['country_code'] == 'WLD']

# Exibindo os DataFrames para depuração
print(df_paises)
print(df_world)

# Gerando o gráfico de linhas para temperatura média anual por país
Countries = alt.Chart(df_paises, title="Temperatura ao longo dos anos").mark_line(opacity=0.2).encode(
    x=alt.X('ano:N', axis=alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y=alt.Y('temperatura_media_anual(°C)', title='Temperatura média anual(°C)'),
    color=alt.Color('country_code:N').scale(scheme="warmgreys").legend(None)
)

# Gerando o gráfico de linha para a média global
World = alt.Chart(df_world).mark_line(opacity=1).encode(
    x=alt.X('ano:N', axis=alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y=alt.Y('temperatura_media_anual(°C)', title='Temperatura média anual(°C)'),
    color=alt.value('black')
)

# Combinando ambos os gráficos
combined_chart = (Countries + World).properties(
    width=300  # Ajuste da largura do gráfico
)

# Salvando o gráfico combinado como arquivo SVG
combined_chart.save('src/graphs/grafico_temperatura.svg')
