"""
Este módulo utiliza o Streamlit para apresentar uma lista interativa de hipóteses de dados, que são expandidas e visualizadas pelos usuários.

Funcionalidades principais:
1. Cria uma interface de visualização interativa, onde uma lista de hipóteses é apresentada utilizando `st.expander`.
2. Cada hipótese contém um título e uma breve descrição, e os usuários podem clicar em cada expander para ver o conteúdo detalhado da hipótese.
3. O objetivo é facilitar a navegação e leitura das diferentes hipóteses formuladas com base em dados agrícolas e suas correlações com PIB, produtividade e outros fatores.

A aplicação é simples e foca na apresentação clara e objetiva das hipóteses.
"""

import streamlit as st

# Título da página
st.title("Hipóteses de Dados")

# Lista de hipóteses
hipoteses = [
    {
        "titulo": "Hipótese 1",
        "descricao": "Baseando-se nos dados agrícolas, é possível ver se um país apresentou desenvolvimento significativo no período (PIB)?"
    },
    {
        "titulo": "Hipótese 2",
        "descricao": "Há uma correlação maior entre produção agrícola e PIB nos países subdesenvolvidos/em desenvolvimento em relação aos países desenvolvidos?"
    },
    {
        "titulo": "Hipótese 3",
        "descricao": "A produtividade por hectare de terra arável está aumentando ao longo do tempo, com destaque para os países emergentes?"
    },
    {
        "titulo": "Hipótese 4",
        "descricao": "A variação na precipitação ao longo dos anos está correlacionada com mudanças nos índices de produção agrícola em regiões específicas?"
    },
    {
        "titulo": "Hipótese 5",
        "descricao": "O aumento no uso de fertilizantes e pesticidas apresenta uma corelação maior com a produção por hectare em paises subdesenvolvidos e emergentes?"
    },
    
]

# Apresentar as hipóteses com botões de expandir
for hipotese in hipoteses:
    with st.expander(hipotese["titulo"]):
        st.write(hipotese["descricao"])