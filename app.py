import streamlit as st
from Pages import dados_analisados, graphs, hipoteses, motivos, mapas_exibicao

st.title("Aplicação Principal")

# Função para exibir conteúdo das diferentes páginas
def show_page(page_name):
    if page_name == 'Dados':
        dados_analisados.render()
    elif page_name == 'Gráficos':
        graphs.render()
    elif page_name == 'Hipóteses':
        hipoteses.render()
    elif page_name == 'Motivos':
        motivos.render()
    elif page_name == 'Mapas':
        mapas_exibicao.render()

# Sidebar para navegar pelas páginas
page = st.sidebar.selectbox("Escolha a Página", ["Dados", "Gráficos", "Hipóteses", "Motivos", "Mapas"])
show_page(page)
