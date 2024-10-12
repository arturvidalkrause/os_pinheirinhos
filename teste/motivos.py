"""
Este módulo cria uma página interativa no Streamlit que justifica a escolha do tema de estudo focado na agricultura, mudanças climáticas, segurança alimentar e sustentabilidade. 

Funcionalidades:
1. Apresenta um título e texto explicativo sobre a relevância do estudo.
2. Explica os principais tópicos analisados, como terra arável, clima, insumos agrícolas e desempenho econômico.
3. Destaca a importância de ferramentas como Pandas e NumPy para garantir a integridade e análise dos dados.
4. Justifica a análise das correlações entre variáveis agrícolas e econômicas, e seu impacto no desenvolvimento de políticas públicas.

"""


import streamlit as st

st.title("Motivos para Escolher Este Tema de Trabalho")

st.write("""
A escolha deste estudo justifica-se pela crescente relevância da agricultura no cenário global, especialmente diante dos desafios impostos pelas mudanças climáticas, segurança alimentar e a necessidade de práticas agrícolas mais sustentáveis. 

Ao integrar e tratar diversos conjuntos de dados que abrangem fatores cruciais para a agricultura, como terra arável, clima, insumos agrícolas e desempenho econômico, buscamos oferecer uma visão mais abrangente e interconectada de como esses elementos se relacionam e influenciam a produção agrícola ao longo do tempo, de 1961 a 2022.

O uso de ferramentas como Pandas e NumPy é fundamental para garantir a integridade dos dados, permitindo manipulações precisas e inferências estatísticas rigorosas. Isso possibilitará uma análise aprofundada das correlações entre variáveis como a produção agrícola e o PIB, além de fatores climáticos, como temperatura e precipitação. Com essa abordagem, poderemos testar hipóteses que abordam, por exemplo, o aumento da produtividade por hectare, o impacto dos insumos (fertilizantes e pesticidas) e a relação entre a variabilidade climática e a produção em regiões específicas.

O objetivo final deste trabalho é fornecer uma base sólida de dados e análises que possam subsidiar o desenvolvimento de políticas públicas e estratégias agrícolas mais eficazes, especialmente em países subdesenvolvidos e emergentes, onde a agricultura desempenha um papel crucial no desenvolvimento econômico e social.
""")