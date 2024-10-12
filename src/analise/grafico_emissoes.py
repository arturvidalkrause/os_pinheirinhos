"""
    Este módulo carrega e processa dados de emissões de CO₂, gera um gráfico das emissões ao longo dos anos para diferentes países, e salva o gráfico em formato SVG.

    O gráfico de área exibe as emissões anuais de CO₂ por país e exclui os dados globais ('WLD').
    O valor máximo de emissões por país também é identificado e impresso no terminal.

    O módulo utiliza a biblioteca Altair para visualização de dados e pandas para manipulação de dados.
"""
import os
import pandas as pd
import altair as alt

# Desabilitando o limite máximo de linhas para visualizações grandes
alt.data_transformers.disable_max_rows()

# Definindo o diretório do dataset de emissões de CO2 tratado
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/emissoes_co2.parquet")

# Carregando o dataset a partir do arquivo Parquet
df = pd.read_parquet(path_data)

# Removendo os dados referentes às emissões globais ('WLD')
df_paises = df[df['country_code'] != 'WLD']

# Encontrando o valor máximo da coluna 'Annual CO₂ emissions'
max_value = df_paises['Annual CO₂ emissions'].max()

# Filtrando o DataFrame para obter a linha correspondente ao valor máximo de emissões
max_row = df_paises[df_paises['Annual CO₂ emissions'] == max_value]

# Exibindo a linha correspondente ao valor máximo de emissões
print(max_row)

# Gerando o gráfico de área para emissões de CO2 por país
Countries = alt.Chart(df_paises, title="Emissões CO2 (t)").mark_area(opacity=1.0).encode(
    x=alt.X('ano:N', axis=alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y=alt.Y('Annual CO₂ emissions:Q', title='Emissões CO₂eq (kt)'),
    color=alt.Color('country_code:N').scale(scheme="warmgreys").legend(None)
).properties(
    width=300  # Largura do gráfico
)

# Salvando o gráfico gerado no diretório especificado como arquivo SVG
Countries.save('./src/graphs/grafico_emissoes_temp.svg')