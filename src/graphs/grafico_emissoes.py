import os
import pandas as pd
import altair as alt

# Desabilitando o máximo de linhas
alt.data_transformers.disable_max_rows()

# Diretório da tabela a ser tratada
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/emissoes_co2eq.csv")

# Obtendo a tabela tratada
df = pd.read_csv(path_data)

# Lista dos países
paises = [
    'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
    'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 
    'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados',
    'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia (Plurinational State of)',
    'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria',
    'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
    'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia',
    'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominica',
    'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea',
    'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'France', 'Gabon', 'Gambia',
    'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 
    'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 
    'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq',
    'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
    'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lesotho',
    'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar',
    'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mexico', 'Monaco',
    'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
    'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
    'Oman', 'Pakistan', 'Palau', 'Panama', 'Peru', 'Philippines', 'Poland',
    'Portugal', 'Qatar', 'Republic of Korea', 'Republic of Moldova', 'Romania',
    'Russian Federation', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia', 
    'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland',
    'Syrian Arab Republic', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo',
    'Trinidad and Tobago', 'Tunisia', 'Turkmenistan', 'Tuvalu', 'Türkiye',
    'Uganda', 'Ukraine', 'United Arab Emirates', 
    'United Kingdom of Great Britain and Northern Ireland', 
    'United Republic of Tanzania', 'United States of America', 'Uruguay',
    'Uzbekistan', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam',
    'Yemen', 'Zambia', 'Zimbabwe'
]

# Obtendo o df com os países apenas
df_paises = df[df['Area'].isin(paises)]

# Obtendo apenas o total de emissões
df_all_sectors = df_paises[df_paises['Item'] == 'All sectors with LULUCF']

# Removendo colunas desnecessárias
df_all_sectors.drop(columns=['Unnamed: 0', 'Item'], inplace=True)
print(df_all_sectors)

# Usando melt para transformar os dados
df_melted = df_all_sectors.melt(id_vars=['Area'], var_name='Year', value_name='emissoes')

# Renomeando a coluna 'Area' para 'country_name'
df_melted.rename(columns={'Area': 'country_name'}, inplace=True)

# Convertendo o ano para um formato numérico
df_melted['Year'] = df_melted['Year'].astype(int)

# Resetando o índice
df_melted.reset_index(drop=True, inplace=True)

# Obtendo apenas os dados a partir de 1990 (o resto está faltando dados)
df = df_melted[df_melted['Year']>1990]


# Países
Countries = alt.Chart(df, title="Emissoes CO2eq (kt)").mark_area(opacity=1.0).encode(
    # x, y, color, shape, size
    x = alt.X('Year:N', axis = alt.Axis(values=[year for year in range(1960, 2021, 10)], title='Ano')),
    y = alt.Y('emissoes:Q', title='Emissoes CO2eq (kt)'),
    color = alt.Color('country_name:N').scale(scheme="warmgreys").legend(None)
).properties(
    width=300
)

# Salvando o gráfico
Countries.save('src/graphs/gráfico_emissoes.svg')
