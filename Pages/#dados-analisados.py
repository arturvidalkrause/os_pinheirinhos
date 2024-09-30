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
    df1 = pd.DataFrame({
        'Coluna A': [1, 2, 3],
        'Coluna B': [4, 5, 6]
    })

    df2 = pd.DataFrame({
        'Coluna X': [7, 8, 9],
        'Coluna Y': [10, 11, 12]
    })
    
    return df1, df2

# Carregar os DataFrames
df1, df2 = load_data()

# Abas para cada dataset
tab1, tab2 = st.tabs(["Dataset 1", "Dataset 2"])

with tab1:
    st.header("Dataset 1")
    st.dataframe(df1)
    st.write("Texto para Dataset 1")

with tab2:
    st.header("Dataset 2")
    st.dataframe(df2)
    st.write("Texto para Dataset 2")