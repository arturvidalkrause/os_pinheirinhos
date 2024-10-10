import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression
from typing import Tuple, Dict, Any, List
from config import DATA_SETS_LIMPOS

# Configuração inicial do aplicativo (deve ser o primeiro comando Streamlit)
st.set_page_config(page_title='Análise de Produtividade Agrícola', layout='wide')
# Lista de hipóteses
hipoteses = [
    {
        "chave": "Hipótese 1",
        "titulo": "Análise do Crescimento Agrícola e Seu Impacto no Desenvolvimento do PIB",
        "descricao": "Baseando-se nos dados agrícolas, é possível ver se um país apresentou desenvolvimento significativo no período (PIB)?"
    },
    {
        "chave": "Hipótese 2",
        "titulo": "Correlação Entre Produção Agrícola e PIB: Comparando Países em Desenvolvimento e Desenvolvidos",
        "descricao": "Há uma correlação maior entre produção agrícola e PIB nos países subdesenvolvidos/em desenvolvimento em relação aos países desenvolvidos?"
    },
    {
        "chave": "Hipótese 3",
        "titulo": "Aumento da Produtividade por Hectare: Uma Tendência de Crescimento nos Países Emergentes",
        "descricao": "A produtividade por hectare de terra arável está aumentando ao longo do tempo, com destaque para os países emergentes."
    },
    {
        "chave": "Hipótese 4",
        "titulo": "Correlação Entre Variação de Precipitação e Mudanças na Produção Agrícola em Regiões Específicas",
        "descricao": "A variação na precipitação ao longo dos anos está correlacionada com mudanças nos índices de produção agrícola em regiões específicas."
    },
    {
        "chave": "Hipótese 5",
        "titulo": "Impacto de Fertilizantes e Pesticidas na Produção por Hectare em Países Subdesenvolvidos e Emergentes",
        "descricao": "O aumento no uso de fertilizantes e pesticidas apresenta uma corelação maior com a produção por hectare em paises subdesenvolvidos e emergentes?"
    }
    
]
tab1, tab2, tab3, tab4, tab5 = st.tabs([hipotese["chave"] for hipotese in hipoteses])

with tab1:
    st.title(hipoteses[0]["titulo"])
    st.subheader(hipoteses[0]["descricao"])

with tab2:
    st.title(hipoteses[1]["titulo"])
    st.subheader(hipoteses[1]["descricao"])

with tab3:
    st.title(hipoteses[2]["titulo"])
    st.subheader(hipoteses[2]["descricao"])


with tab4:
    st.title(hipoteses[3]["titulo"])
    st.subheader(hipoteses[3]["descricao"])

with tab5:
    st.title(hipoteses[4]["titulo"])
    st.subheader(hipoteses[4]["descricao"])
