"""  """

import os
import pandas as pd
import altair as alt
import math

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório das tabelas 
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/")

# Obtendo a tabela tratada
df_producao = pd.read_csv(os.path.join(path_data, 'producao_total_e_area.csv'), index_col=0)
df_pib = pd.read_csv(os.path.join(path_data, 'PIB.csv'), index_col=0)

df = pd.merge(df_producao, df_pib, how='outer')

df = df[df['country_code'] != 'WLD']

print(df)
## Fazendo o gráfico

scatter = alt.Chart(df, title="Produção x PIB (Países)").mark_point(color='black', opacity=1).encode(
    y=alt.Y('PIB:Q', title='PIB (USD)'),
    x=alt.X('producao_total(t):Q', title='Produção Total (t)'),
)

# Adicionando a reta de correlação
regression_line = scatter.transform_regression(
    'PIB', 'producao_total(t)',
    method='linear'
).mark_line(color='grey').encode(
    tooltip=[alt.Tooltip('intercept:Q', title='Intercepto'), alt.Tooltip('slope:Q', title='Inclinação')]
)

graphic = scatter + regression_line

graphic.properties(
    width=300
)

graphic.save('src/graphs/grafico_produção_e_pib.svg')
