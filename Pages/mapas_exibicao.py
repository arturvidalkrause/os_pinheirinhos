import pandas as pd
import streamlit as st
import plotly.express as px

# Leitura dos arquivos CSV usando pandas
# Ajuste os caminhos dos arquivos conforme necessário
df_terras_araveis = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\terras_araveis.csv')
df_temperatura = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\temperatura.csv')
df_precipitacao_anual = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\precipitacao_anual.csv')
df_producao_total_e_area = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\producao_total_e_area.csv')
df_fertilizantes_total = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\fertilizantes_total.csv')
df_pib = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\PIB.csv')
df_emissoes_co2 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\terras_araveis.csv')

# Mapeamento dos temas para os dataframes correspondentes
themes = {
    'Terras Aráveis': df_terras_araveis,
    'Temperatura': df_temperatura,
    'Precipitação Anual': df_precipitacao_anual,
    'Produção Total e Área': df_producao_total_e_area,
    'Fertilizantes Total': df_fertilizantes_total,
    'PIB': df_pib,
    'Emissões de CO2': df_emissoes_co2
}

# Mapeamento dos temas para as colunas de dados e suas unidades de medida
# Ajuste os nomes das colunas e unidades conforme seus arquivos CSV
# Por exemplo:
# 'Terras Aráveis': ('Porcentagem_Terras_Araveis', '%') significa que no arquivo 'terras_araveis.csv',
# a coluna com a porcentagem de terras aráveis é chamada 'Porcentagem_Terras_Araveis' e é medida em '%'

data_info = {
    'Terras Aráveis': ('terras_araveis(%)', '%'),
    'Temperatura': ('temperatura_media_anual(Â°C)', 'ºC'),
    'Precipitação Anual': ('precipitação_anual', 'mm'),
    'Produção Total e Área': ('producao_total(t)', 'toneladas'),
    'Fertilizantes Total': ('uso_total_de_fertilizantes(t)', 'toneladas'),
    'PIB': ('PIB', 'USD'),
    'Emissões de CO2': ('Annual CO₂ emissions', 'kt')
}

st.title('Visualização Geográfica')

# Opções da barra lateral para o Mapa 1
st.sidebar.header('Opções de Mapa 1')

# Seleção do tema para o Mapa 1
theme1 = st.sidebar.selectbox('Selecione o dado para visualizar', list(themes.keys()))

# Obtenção do DataFrame e da coluna de dados para o tema selecionado
df1 = themes[theme1]
data_column1, unit1 = data_info[theme1]

# Obtenção dos anos disponíveis no DataFrame
available_years1 = df1['ano'].unique()
year1 = st.sidebar.selectbox('Selecione o ano', sorted(available_years1))

# Opção para ativar o duplo gráfico
double_graph = st.sidebar.checkbox('Ativar Duplo Gráfico')

# Função para criar o mapa
def create_map(df, data_column, year, map_title, unit):
    
    # Filtra o DataFrame para o ano selecionado
    df_year = df[df['ano'] == year]
    
    # Garante que o 'country-code' esteja em letras maiúsculas (ISO alpha-3)
    df_year['country_code'] = df_year['country_code'].str.upper()
    
    # Cria rótulos para a barra de cores
    labels = {data_column: f"{data_column} ({unit})"}
    
    # Cria o mapa coroplético usando Plotly Express
    fig = px.choropleth(
        df_year,
        locations='country_code',
        color=data_column,
        hover_name='country_code',
        color_continuous_scale=px.colors.sequential.Plasma,
        title=map_title,
        labels=labels
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=10),
        coloraxis_colorbar=dict(title=unit, tickprefix=' ')

    )
    
    # Exibe o mapa no Streamlit
    st.plotly_chart(fig)

# Criação do Mapa 1
create_map(df1, data_column1, year1, f"{theme1} - {year1}", unit1)

# Se o duplo gráfico estiver ativado, exibe as opções e o mapa para o Mapa 2
if double_graph:
    st.sidebar.header('Opções de Mapa 2')
    
    # Seleção do tema para o Mapa 2
    theme2 = st.sidebar.selectbox('Selecione o dado para visualizar (Mapa 2)', list(themes.keys()))
    
    # Obtenção do DataFrame e da coluna de dados para o tema selecionado
    df2 = themes[theme2]
    data_column2, unit2 = data_info[theme2]
    
    # Obtenção dos anos disponíveis no DataFrame
    available_years2 = df2['ano'].unique()
    year2 = st.sidebar.selectbox('Selecione o ano (Mapa 2)', sorted(available_years2))
    
    # Criação do Mapa 2
    create_map(df2, data_column2, year2, f"{theme2} - {year2}", unit2)