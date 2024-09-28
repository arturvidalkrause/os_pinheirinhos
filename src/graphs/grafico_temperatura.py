import os
import pandas as pd
import altair as alt

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório da tabela a ser tratada
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/temperatura.csv")

# Obtendo a tabela tratada
df = pd.read_csv(path_data)

# Criando uma tabela com a média mundial
df_world = df.groupby(['Year'], as_index=False)['media_anual'].mean()
df_world['country_name'] = 'World'

## Fazendo o gráfico

# Países
Countries = alt.Chart(df, title="Temperatura ao longo dos anos").mark_line(opacity=0.2).encode(
    # x, y, color, shape, size
    x = alt.X('Year:N', axis = alt.Axis(values=[year for year in range(1900, 2021, 10)], title='Ano')),
    y = alt.Y('media_anual:Q', title='Temperatura média'),
    color = alt.Color('country_name:N').scale(scheme="warmgreys").legend(None)
)

# Média global
World = alt.Chart(df_world).mark_line(opacity=1).encode(
    x = alt.X('Year:N', axis = alt.Axis(values=[year for year in range(1900, 2021, 10)], title='Ano')),
    y = alt.Y('media_anual:Q', title='Temperatura média'),
    color=alt.value('black')
)

# Combinando ambos
combined_chart = (Countries + World).properties(
    width=300  # Ajuste a largura aqui
)

# Salvando o gráfico
combined_chart.save('src/graphs/gráfico_temperatura.svg')