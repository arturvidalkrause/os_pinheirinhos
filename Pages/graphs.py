from config import DATA_SETS_LIMPOS
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Função para exibir o gráfico de emissões de CO2
@st.cache_resource
def show_chart_1():
        # Removendo os dados mundiais
        df_paises = df1[df1['country_code'] != 'WLD']

        # Encontrar o valor máximo da coluna 'Annual CO₂ emissions'
        max_value = df_paises['Annual CO₂ emissions'].max()

        # Filtrar o DataFrame para obter a linha correspondente ao valor máximo
        max_row = df_paises[df_paises['Annual CO₂ emissions'] == max_value]

        # Exibir a linha com o valor máximo
        st.write("Linha com o valor máximo de emissões anuais de CO₂:")
        st.write(max_row)

        # Pivotar o DataFrame para que cada país seja uma coluna
        df_pivot = df_paises.pivot(index='ano', columns='country_code', values='Annual CO₂ emissions')

        # Criação da figura e do eixo
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotar o gráfico de área
        colors=sns.color_palette('Blues', n_colors=len(df_pivot.columns))
        df_pivot.plot(kind='area', stacked=True, ax=ax, legend=False, color=colors)

        # Configurações do gráfico
        ax.set_title('Emissões de CO₂ (kt)')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Emissões anuais de CO₂')

        # Ajustar a legenda para estar abaixo do gráfico em 4 colunas
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            handles=handles,
            labels=labels,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.15),
            ncol=4
        )

        # Ajustar layout
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.35)

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

# Função para exibir o gráfico de produção total
@st.cache_resource
def show_chart_2():
        # Obtendo a tabela tratada
        df=df5[df5['country_code']!='WLD']

        # Criação da figura e do eixo
        fig, ax = plt.subplots()

        # Plotar os dados usando seaborn
        colors = sns.color_palette('Blues', n_colors=len(df['country_code'].unique()))
        sns.lineplot(data=df, x='ano', y='producao_total(t)', hue='country_code', ax=ax,palette=colors)

        # Configurações do gráfico
        ax.set_title('Produção Total ao longo dos anos')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Produção Total (t)')


        # Ajustar a legenda para estar abaixo do gráfico em 4 colunas
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            handles=handles,
            labels=labels,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.15),
            ncol=4
        )

        # Ajustar layout para evitar sobreposição de elementos
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.25)

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

# Função para exibir o gráfico de temperatura
@st.cache_resource
def show_chart_3():
    # Remover 'WLD' do dataset
    df_paises = df6[df6['country_code'] != 'WLD']
    df_world = df6[df6['country_code'] == 'WLD']

    # Criação da figura e do eixo
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotar os dados usando Seaborn
    sns.lineplot(
    data=df_paises,
    x='ano',
    y='temperatura_media_anual(°C)',
    hue='country_code',
    ax=ax,
    alpha=0.2,
    legend=False
    )

    # Plotar a média global com opacidade completa
    sns.lineplot(
        data=df_world,
        x='ano',
        y='temperatura_media_anual(°C)',
        label='Média Global',
        color='black',
        ax=ax
    )

    # Configurações do gráfico
    ax.set_title('Temperatura ao longo dos anos')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Temperatura média anual (°C)')

    # Ajustar a legenda para estar abaixo do gráfico em 4 colunas
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=handles,
        labels=labels,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=4
    )

    # Ajustar layout para evitar sobreposição de elementos
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    st.write("A função show chart 3 foi chamada.")

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
