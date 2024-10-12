"""
Este módulo utiliza Streamlit para criar uma interface interativa que exibe múltiplos datasets a partir de arquivos Parquet.

Funcionalidades:
1. Carrega e exibe datasets com caching para otimizar o desempenho.
2. Organiza os dados em abas interativas para visualização fácil e individual de cada dataset (emissões de CO2, fertilizantes, PIB, precipitação anual, produção total e área, temperatura, terras aráveis).

Este módulo facilita a análise de dados de forma organizada e visual.
"""

from config import DATA_SETS_LIMPOS
import streamlit as st
import pandas as pd
from pathlib import Path

# Descrição geral
st.title("Análise de Dados")
st.write("""
Aqui serão apresentados alguns DataFrames das nossas hipóteses.
Utilize as abas abaixo para visualizar cada dataset individualmente.
""")

# Função para carregar os DataFrames com cache
@st.cache_data
def load_data():
    df1 = pd.read_parquet(DATA_SETS_LIMPOS + "/emissoes_co2.parquet")
    df2 = pd.read_parquet(DATA_SETS_LIMPOS + "/fertilizantes_total.parquet")
    df3 = pd.read_parquet(DATA_SETS_LIMPOS + "/PIB.parquet")
    df4 = pd.read_parquet(DATA_SETS_LIMPOS + "/precipitacao_anual.parquet")
    df5 = pd.read_parquet(DATA_SETS_LIMPOS + "/producao_total_e_area.parquet")
    df6 = pd.read_parquet(DATA_SETS_LIMPOS + "/temperatura.parquet")
    df7 = pd.read_parquet(DATA_SETS_LIMPOS + "/terras_araveis.parquet")

    return df1, df2, df3, df4, df5, df6, df7

# Carregar os dados
df1, df2, df3, df4, df5, df6, df7 = load_data()

# Abas para cada dataset
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["emissões co2", "fertilizantes total","PIB","precipitação anual","prod total e area","temperatura","terras araveis"])

with tab1:
    st.header("Emissões CO2")
    st.dataframe(df1)
    st.write("Dados de emissões de CO2 em diferentes países")

with tab2:
    st.header("Fertilizantes Total")
    st.dataframe(df2)
    st.write("Quantidade de fertilizantes usados por cada pais ano a ano")

with tab3:
    st.header("PIB")
    st.dataframe(df3)
    st.write("Produto Interno Bruto (PIB) de países, medido em dólares correntes, usado para avaliar o desempenho econômico.")

with tab4:
    st.header("Precipitação Anual")
    st.dataframe(df4)
    st.write("Dados históricos e projetados sobre precipitação, focando nos impactos agrícolas.")

with tab5:
    st.header("Produção Total e Área")
    st.dataframe(df5)
    st.write("Índices de produção agrícola, medindo a variação no volume de produção ao longo do tempo.")

with tab6:
    st.header("Temperatura")
    st.dataframe(df6)
    st.write("Dados mensais históricos de temperatura de estações meteorológicas, usados para estudar mudanças climáticas.")

with tab7:
    st.header("Terras Aráveis")
    st.dataframe(df7)
    st.write("Proporção de terra arável em relação à área total de cada país, um indicador importante para o potencial agrícola.")