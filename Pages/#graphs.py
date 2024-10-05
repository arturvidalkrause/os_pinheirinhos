import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

# Função para exibir o gráfico de emissões de CO2
@st.cache_resource
def show_chart_1():
    def exibir_dados_emissoes():
        # Diretório da tabela a ser tratada
        path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/emissoes_co2.csv")

        # Obtendo a tabela tratada
        df = pd.read_csv(path_data, index_col=0)

        # Removendo os dados mundiais
        df_paises = df[df['country_code'] != 'WLD']

        # Encontrar o valor máximo da coluna 'Annual CO₂ emissions'
        max_value = df_paises['Annual CO₂ emissions'].max()

        # Filtrar o DataFrame para obter a linha correspondente ao valor máximo
        max_row = df_paises[df_paises['Annual CO₂ emissions'] == max_value]

        # Exibir a linha com o valor máximo
        st.write("Linha com o valor máximo de emissões anuais de CO₂:")
        st.write(max_row)

        # Gerando o gráfico usando matplotlib
        fig, ax = plt.subplots()

        for country_code in df_paises['country_code'].unique():
            df_country = df_paises[df_paises['country_code'] == country_code]
            ax.plot(df_country['ano'], df_country['Annual CO₂ emissions'], label=country_code)

        ax.set_title('Emissões de CO₂ (kt)')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Emissões anuais de CO₂')

        # Adicionar uma legenda
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

        # Ajustar layout
        plt.tight_layout()

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    # Chamar a função para exibir os dados e o gráfico
    exibir_dados_emissoes()

# Função para exibir o gráfico de produção total
@st.cache_resource
def show_chart_2():
    def gerar_grafico_producao():
        # Diretório da tabela a ser tratada
        path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/producao_total_e_area.csv")

        # Obtendo a tabela tratada
        df = pd.read_csv(path_data, index_col=0)

        # Criação da figura e do eixo
        fig, ax = plt.subplots()

        # Plotar os dados para cada país
        for country_code in df['country_code'].unique():
            df_country = df[df['country_code'] == country_code]
            ax.plot(df_country['ano'], df_country['producao_total(t)'], label=country_code)

        # Configurações do gráfico
        ax.set_title('Produção Total ao longo dos anos')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Produção Total (t)')

        # Adicionar uma legenda
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

        # Ajustar layout para evitar sobreposição de elementos
        plt.tight_layout()

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    # Chamar a função para gerar o gráfico
    gerar_grafico_producao()

# Função para exibir o gráfico de temperatura
@st.cache_resource
def show_chart_3():
    # Diretório da tabela a ser tratada
    path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/limpos/temperatura.csv")

    # Obtendo a tabela tratada
    df = pd.read_csv(path_data, index_col=0)

    df_paises = df[df['country_code'] != 'WLD']
    df_world = df[df['country_code'] == 'WLD']

    # Função para gerar o gráfico de temperatura
    
    def gerar_grafico_temperatura():
        # Criação da figura e do eixo
        fig, ax = plt.subplots()

        # Plotar os dados para cada país
        for country_code in df_paises['country_code'].unique():
            df_country = df_paises[df_paises['country_code'] == country_code]
            ax.plot(df_country['ano'], df_country['temperatura_media_anual(°C)'], label=country_code, alpha=0.2)

        # Plotar a média global com opacidade completa
        ax.plot(df_world['ano'], df_world['temperatura_media_anual(°C)'], label='Média Global', color='black')

        # Configurações do gráfico
        ax.set_title('Temperatura ao longo dos anos')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Temperatura média anual (°C)')

        # Adicionar uma legenda
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

        # Ajustar layout para evitar sobreposição de elementos
        plt.tight_layout()

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    # Chamar a função para gerar o gráfico
    gerar_grafico_temperatura()

# Título da página
st.title('Visualização de Gráficos')

# Sidebar para trocar os gráficos
st.sidebar.title("Escolha o gráfico para exibição")
chart_selection = st.sidebar.selectbox("Selecione um gráfico:", ["Gráfico 1", "Gráfico 2", "Gráfico 3"])

# Renderização do gráfico escolhido
if chart_selection == "Gráfico 1":
    show_chart_1()
elif chart_selection == "Gráfico 2":
    show_chart_2()
elif chart_selection == "Gráfico 3":
    show_chart_3()
