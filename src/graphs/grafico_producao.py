"""  """

import os
import pandas as pd
import altair as alt

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório da tabela a ser tratada
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/producao_total_e_area.csv")

# Obtendo a tabela tratada
df = pd.read_csv(path_data, index_col=0)

## Fazendo o gráfico

# Países
Countries = alt.Chart(df, title="Produção ao longo dos anos").mark_area(opacity=1).encode(
    x = alt.X('ano:N', axis = alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y = alt.Y('producao_total(t):Q', title='Produção Total (t)'),
    color = alt.Color('country_code:N').scale(scheme="warmgreys").legend(None)
).properties(
    width=300
)

Countries.save('src/graphs/grafico_produção.svg')
