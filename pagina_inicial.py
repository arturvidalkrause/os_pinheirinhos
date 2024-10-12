import streamlit as st

# config da pagina
st.set_page_config(page_title="Apresentação do Trabalho", layout="wide")

#Título 
st.title("Apresentação do Trabalho")

#Subtítulo
st.subheader("Descrição Geral")

#Descrição do que falar
st.write("""
Bem-vindo à nossa apresentação! Este trabalho tem como objetivo investigar as correlações entre diversos indicadores do setor agrícola,
buscando fornecer insights valiosos e abrir caminho para futuras pesquisas na área de desenvolvimento econômico e agricultura.
Estamos analisando dados globais de produção agrícola e indicadores econômicos de 1961 a 2022, com ênfase na relação entre 
produtividade agrícola e crescimento econômico.
""")

#Seção de Dados
st.subheader("Dados Analisados")

#Descrição dos dados
st.write("""
Os dados que estamos analisando incluem informações sobre a proporção de terra arável, temperatura, precipitação, insumos agrícolas (fertilizantes e pesticidas),
PIB de cada país e produção agrícola. Esses dados foram coletados de fontes como World Bank, NOAA e FAOSTAT e abrangem o período de 1961 a 2022.
""")

#Seção de Metodologia
st.subheader("Metodologia")

#Descrição da metodologia
st.write("""
Nossa metodologia inclui a integração de múltiplas fontes de dados para realizar análises estatísticas robustas. 
Utilizamos bibliotecas como Pandas e NumPy para manipulação e inferências, aplicando técnicas como regressão linear e análise de correlação (Pearson) 
para explorar as relações entre os fatores econômicos e agrícolas. Além disso, desenvolvemos gráficos de dispersão e mapas interativos para visualizar essas relações.
""")

#Seção de Resultados Esperados
st.subheader("Resultados Esperados")

#Descrição dos resultados esperados
st.write("""
Esperamos encontrar correlações significativas entre a produtividade agrícola e o crescimento econômico, principalmente em países emergentes. 
Esses resultados nos ajudarão a entender melhor como fatores como tecnologia agrícola e mudanças climáticas impactam o desenvolvimento econômico 
e a sustentabilidade no setor agrícola.
""")

# Seção de Conclusão
st.subheader("Conclusão")

# Descrição da conclusão
st.write("""
Em conclusão, observamos que a produção agrícola está fortemente correlacionada com o crescimento econômico em diferentes níveis de desenvolvimento. 
Entender essas dinâmicas pode ajudar a formular políticas mais eficazes que promovam a sustentabilidade e o crescimento econômico global. 
Agradecemos por acompanhar nossa apresentação e estamos abertos a perguntas e sugestões.
""")
