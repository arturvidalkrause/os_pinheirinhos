"""  """

import os
import pandas as pd
import altair as alt

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório da tabela a ser tratada
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/emissoes_co2.parquet")

# Obtendo a tabela tratada
df = pd.read_parquet(path_data)

# Removendo os dados mundiais
df_paises = df[df['country_code'] != 'WLD']

# Encontrar o valor máximo da coluna 'Annual CO₂ emissions'
max_value = df_paises['Annual CO₂ emissions'].max()

# Filtrar o DataFrame para obter a linha correspondente ao valor máximo
max_row = df_paises[df_paises['Annual CO₂ emissions'] == max_value]

# Exibir a linha com o valor máximo
print(max_row)

# Gerando o gráfico
Countries = alt.Chart(df_paises, title="Emissoes CO2 (t)").mark_area(opacity=1.0).encode(
    x = alt.X('ano:N', axis = alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y = alt.Y('Annual CO₂ emissions:Q', title='Emissoes CO2eq (kt)'),
    color = alt.Color('country_code:N').scale(scheme="warmgreys").legend(None)
).properties(
    width=300
)

# Salvando o gráfico
Countries.save('./src/graphs/gráfico_emissoes_temp.svg')
