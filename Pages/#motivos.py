import streamlit as st

st.title("10 Motivos para Escolher Este Tema de Trabalho")

motivos = [
    "Motivo 1: ",
    "Motivo 2: ",
    "Motivo 3: ",
    "Motivo 4: ",
    "Motivo 5: ",
    "Motivo 6: ",
    "Motivo 7: ",
    "Motivo 8: ",
    "Motivo 9: ",
    "Motivo 10: "
]

for i, motivo in enumerate(motivos, 1):
    st.subheader(f"{i}. {motivo}")

