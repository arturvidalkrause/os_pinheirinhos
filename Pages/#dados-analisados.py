import streamlit as st
import pandas as pd

# Descrição geral
st.title("Análise de Dados")
st.write("""
Aqui serão apresentados alguns DataFrames das nossas hipóteses.
Utilize as abas abaixo para visualizar cada dataset individualmente.
""")

# Função para carregar os DataFrames com cache
@st.cache_data
def load_data():
    df1 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\emissoes_co2.csv')

    df2 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\fertilizantes_total.csv')

    df3 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\PIB.csv')

    df4 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\precipitacao_anual.csv')

    df5 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\producao_total_e_area.csv')

    df6 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\temperatura.csv')

    df7 = pd.read_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\LP\\trabalho_a1\\data\\limpos\\terras_araveis.csv')
    
    return df1, df2, df3, df4, df5, df6, df7

# Carregar os DataFrames
df1, df2, df3, df4, df5, df6, df7 = load_data()

# Abas para cada dataset
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["emissões co2", "fertilizantes total","PIB","precipitação anual","prod total e area","temperatura","terras araveis"])

with tab1:
    st.header("Emissões CO2")
    st.dataframe(df1)
    st.write("Texto para Emissões CO2")

with tab2:
    st.header("Fertilizantes Total")
    st.dataframe(df2)
    st.write("Texto para Fertilizantes Total")

with tab3:
    st.header("PIB")
    st.dataframe(df3)
    st.write("Texto para PIB")

with tab4:
    st.header("Precipitação Anual")
    st.dataframe(df4)
    st.write("Texto para Precipitação Anual")

with tab5:
    st.header("Produção Total e Área")
    st.dataframe(df5)
    st.write("Texto para Produção Total e Área")

with tab6:
    st.header("Temperatura")
    st.dataframe(df6)
    st.write("Texto para Temperatura")

with tab7:
    st.header("Terras Aráveis")
    st.dataframe(df7)
    st.write("Texto para Terras Aráveis")