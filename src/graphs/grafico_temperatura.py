"""  """

import os
import pandas as pd
import altair as alt

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório da tabela a ser tratada
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/temperatura.csv")

# Obtendo a tabela tratada
df = pd.read_csv(path_data, index_col=0)

df_paises = df[df['country_code'] != 'WLD']

df_world = df[df['country_code'] == 'WLD']

print(df_paises)
print(df_world)
## Fazendo o gráfico

# Países
Countries = alt.Chart(df_paises, title="Temperatura ao longo dos anos").mark_line(opacity=0.2).encode(
    x = alt.X('ano:N', axis = alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y = alt.Y('temperatura_media_anual(°C)', title='Temperatura média anual(°C)'),
    color = alt.Color('country_code:N').scale(scheme="warmgreys").legend(None)
)

# Média global
World = alt.Chart(df_world).mark_line(opacity=1).encode(
    x = alt.X('ano:N', axis = alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y = alt.Y('temperatura_media_anual(°C)', title='Temperatura média anual(°C)'),
    color=alt.value('black')
)

# Combinando ambos
combined_chart = (Countries + World).properties(
    width=300  # Ajuste a largura aqui
)

# Salvando o gráfico
combined_chart.save('src/graphs/gráfico_temperatura.svg')