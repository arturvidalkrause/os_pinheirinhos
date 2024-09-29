import os
import pandas as pd
import altair as alt

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório da tabela a ser tratada
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/brutos/annual-co2-emissions-per-country.csv")

# Obtendo a tabela tratada
df = pd.read_csv(path_data)

df = df.drop(columns=['Code'])

print(df)

Countries = alt.Chart(df, title="Emissoes CO2eq (t)").mark_area(opacity=1.0).encode(
    # x, y, color, shape, size
    x = alt.X('Year:N', axis = alt.Axis(values=[year for year in range(1700, 2021, 20)], title='Ano')),
    y = alt.Y('Annual CO₂ emissions:Q', title='Emissoes CO2eq (kt)'),
    color = alt.Color('Entity:N').scale(scheme="warmgreys").legend(None)
).properties(
    width=300
)

# Salvando o gráfico
Countries.save('src/graphs/gráfico_emissoes2.svg')
