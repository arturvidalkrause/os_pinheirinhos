import streamlit as st

# Título da página
st.title("Hipóteses de Dados")

# Lista de hipóteses
hipoteses = [
    {
        "titulo": "Hipótese 1",
        "descricao": "Descrição detalhada da Hipótese 1. Aqui você pode adicionar mais informações sobre a hipótese."
    },
    {
        "titulo": "Hipótese 2",
        "descricao": "Descrição detalhada da Hipótese 2. Aqui você pode adicionar mais informações sobre a hipótese."
    },
    {
        "titulo": "Hipótese 3",
        "descricao": "Descrição detalhada da Hipótese 3. Aqui você pode adicionar mais informações sobre a hipótese."
    }
]

# Apresentar as hipóteses com botões de expandir
for hipotese in hipoteses:
    with st.expander(hipotese["titulo"]):
        st.write(hipotese["descricao"])