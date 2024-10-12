"""
Este módulo cria uma aplicação Streamlit interativa para visualização geográfica de diversos dados agrícolas, econômicos e ambientais, como terras aráveis, temperatura, precipitação anual, produção agrícola, fertilizantes, PIB e emissões de CO2.

Funcionalidades:
1. Carregamento de múltiplos datasets a partir de arquivos Parquet, incluindo dados sobre terras aráveis, temperatura, precipitação, produção agrícola, fertilizantes, PIB e emissões de CO2.
2. Utiliza gráficos coropléticos (mapas) para exibir visualmente as variações desses dados por país.
3. A aplicação permite selecionar o ano e o dataset a ser visualizado através de uma interface de barra lateral interativa.
4. Inclui a opção de ativar um segundo gráfico para comparar dois temas simultaneamente em diferentes anos.

Principais Componentes:
- `create_map()`: Função responsável pela criação e exibição de mapas coropléticos para o dataset e ano selecionados.
- `themes`: Um dicionário mapeando os datasets para seus temas correspondentes (como terras aráveis, temperatura, etc.).
- `data_info`: Um dicionário que contém informações sobre as colunas e unidades de medida de cada tema.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from config import DATA_SETS_LIMPOS

# Leitura dos arquivos CSV usando pandas
# Ajuste os caminhos dos arquivos conforme necessário
df_terras_araveis = pd.read_parquet(DATA_SETS_LIMPOS + '/terras_araveis.parquet')
df_temperatura = pd.read_parquet(DATA_SETS_LIMPOS + '/temperatura.parquet')
df_precipitacao_anual = pd.read_parquet(DATA_SETS_LIMPOS + '/precipitacao_anual.parquet')
df_producao_total_e_area = pd.read_parquet(DATA_SETS_LIMPOS + '/producao_total_e_area.parquet')
df_fertilizantes_total = pd.read_parquet(DATA_SETS_LIMPOS + '/fertilizantes_total.parquet')
df_pib = pd.read_parquet(DATA_SETS_LIMPOS + '/PIB.parquet')
df_emissoes_co2 = pd.read_parquet(DATA_SETS_LIMPOS + '/emissoes_co2.parquet')

# Corrigir o nome da coluna no DataFrame de temperatura
df_temperatura.rename(columns={'temperatura_media_anual(Â°C)': 'temperatura_media_anual(°C)'}, inplace=True)

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
    'Temperatura': ('temperatura_media_anual(°C)', 'ºC'),
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
year1 = st.sidebar.selectbox('Selecione o ano', sorted(available_years1, reverse=True))

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