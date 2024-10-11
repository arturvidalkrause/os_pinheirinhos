import streamlit as st

# config da pagina
st.set_page_config(page_title="Apresentação do Trabalho", layout="wide")

#Título 
st.title("Apresentação do Trabalho")

#Subtítulo
st.subheader("Descrição Geral")

#Descrição do que falar
st.write("""
Bem-vindo à nossa apresentação! Este trabalho tem como objetivo [insira o objetivo do trabalho aqui].
Estamos analisando [insira a descrição dos dados aqui].
""")

#Seção de Dados
st.subheader("Dados Analisados")

#Descrição dos dados
st.write("""
Os dados que estamos analisando incluem [insira a descrição dos dados aqui].
Esses dados foram coletados de [insira a fonte dos dados aqui] e abrangem o período de [insira o período aqui].
""")

#Seção de Metodologia
st.subheader("Metodologia")

#Descrição da metodologia
st.write("""
Nossa metodologia inclui [insira a descrição da metodologia aqui].
Utilizamos técnicas como [insira as técnicas utilizadas aqui] para analisar os dados.
""")

#Seção de Resultados Esperados
st.subheader("Resultados Esperados")

#Descrição dos resultados esperados
st.write("""
Esperamos encontrar [insira os resultados esperados aqui].
Esses resultados nos ajudarão a [insira o propósito dos resultados aqui].
""")

# Seção de Conclusão
st.subheader("Conclusão")

# Descrição da conclusão
st.write("""
Em conclusão, [insira a conclusão aqui].
Agradecemos por acompanhar nossa apresentação e estamos abertos a perguntas e sugestões.
""")