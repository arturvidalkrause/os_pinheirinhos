import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

# Carregar os dados (substitua 'data.csv' pelo caminho do seu arquivo de dados)
data = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_A1\\complex_data.csv')

# Função para criar o mapa com cache
@st.cache_resource
def create_map(year, data_type):
    # Filtrar os dados pelo ano e tipo de informação
    filtered_data = data[(data['year'] == year) & (data['type'] == data_type)]
    
    # Criar o mapa
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Adicionar os dados ao mapa
    for _, row in filtered_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            popup=f"{row['country']}: {row['value']}",
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)
    
    return m

# Interface do Streamlit
st.title('Exibição de Mapas')

# Widgets para selecionar o ano e tipo de informação
year = st.slider('Selecione o Ano', int(data['year'].min()), int(data['year'].max()), int(data['year'].min()))
data_type = st.selectbox('Selecione o Tipo de Informação', data['type'].unique())

# Criar e exibir o mapa
mapa = create_map(year, data_type)
folium_static(mapa)

# Adicionar texto exclusivo para cada dataset
if data_type == 'Tipo 1':
    st.write("Texto para Dataset 1")
elif data_type == 'Tipo 2':
    st.write("Texto para Dataset 2")
else:
    st.write("Texto para outros tipos de Dataset")