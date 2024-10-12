# app.py

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression
from typing import Tuple, Dict, Any, List
from config import DATA_SETS_LIMPOS

def main() -> None:
    # Configuração inicial do aplicativo
    st.set_page_config(page_title='Análise de Produtividade Agrícola', layout='wide')
    # Título do aplicativo
    st.title('Análise da Produtividade por Hectare de Terra Arável')

    # Carregamento dos dados
    dados: pd.DataFrame = carregar_dados(DATA_SETS_LIMPOS + '/terras_araveis.parquet')

    # Sidebar
    anos_selecionados, visualizacoes_selecionadas = configurar_sidebar(dados)

    # Filtragem dos dados
    dados_filtrados: pd.DataFrame = filtrar_dados(dados, anos_selecionados)

    # Cálculo das regressões
    regressoes: pd.DataFrame = calcular_regressoes(dados_filtrados)

    # Exibição das visualizações
    if 'Mapa' in visualizacoes_selecionadas:
        exibir_mapa(regressoes)
    if 'Gráfico de Colunas' in visualizacoes_selecionadas:
        exibir_grafico_colunas(dados_filtrados)
    if 'Gráfico de Dispersão' in visualizacoes_selecionadas:
        exibir_grafico_dispersao(dados_filtrados)

    # Funções auxiliares definidas dentro de main()
    def carregar_dados(caminho: str) -> pd.DataFrame:
        """Carrega os dados a partir de um arquivo CSV."""
        dados_local: pd.DataFrame = pd.read_parquet(caminho)
        # Supondo que os dados incluem as colunas 'ano', 'país', 'produtividade', '% de terra arável'

        # Identificar países emergentes
        paises_emergentes: List[str] = ['Brasil', 'China', 'Índia', 'Rússia', 'África do Sul']  # Exemplo
        dados_local['Categoria'] = dados_local['país'].apply(lambda x: 'Emergente' if x in paises_emergentes else 'Outros')

        # Adicionar códigos ISO para os países (necessário para o mapa)
        # Aqui, você deve ter uma maneira de mapear 'país' para 'iso_alpha'
        # Exemplo simplificado:
        iso_codes: Dict[str, str] = {
            'Brasil': 'BRA', 'China': 'CHN', 'Índia': 'IND', 'Rússia': 'RUS', 'África do Sul': 'ZAF'
            # Adicione todos os países necessários
        }
        dados_local['iso_alpha'] = dados_local['país'].map(iso_codes)

        return dados_local

    def configurar_sidebar(dados_local: pd.DataFrame) -> Tuple[List[int], List[str]]:
        """Configura a barra lateral do Streamlit e retorna as seleções do usuário."""
        st.sidebar.title('Opções')

        # Seleção de anos
        anos_disponiveis: List[int] = sorted(dados_local['ano'].unique())
        anos_selecionados_local: List[int] = st.sidebar.multiselect(
            'Selecione os anos',
            options=anos_disponiveis,
            default=anos_disponiveis
        )

        # Seleção de visualizações
        visualizacoes_disponiveis: List[str] = ['Mapa', 'Gráfico de Colunas', 'Gráfico de Dispersão']
        visualizacoes_selecionadas_local: List[str] = st.sidebar.multiselect(
            'Selecione as visualizações',
            options=visualizacoes_disponiveis,
            default=visualizacoes_disponiveis
        )

        return anos_selecionados_local, visualizacoes_selecionadas_local

    def filtrar_dados(dados_local: pd.DataFrame, anos_selecionados_local: List[int]) -> pd.DataFrame:
        """Filtra os dados com base nos anos selecionados."""
        dados_filtrados_local: pd.DataFrame = dados_local[dados_local['ano'].isin(anos_selecionados_local)]
        return dados_filtrados_local

    def regressao_por_pais(grupo: pd.DataFrame) -> pd.Series:
        """
        Realiza uma regressão linear da produtividade ao longo do tempo para um país.

        Args:
            grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados.

        Returns:
            pd.Series: Coeficiente angular (slope) da regressão linear.
        """
        x: np.ndarray = grupo[['ano']].values.reshape(-1, 1)
        y: np.ndarray = grupo['produtividade'].values

        modelo: LinearRegression = LinearRegression()
        modelo.fit(x, y)

        slope: float = modelo.coef_[0]

        return pd.Series({'slope': slope})

    def calcular_regressoes(dados_local: pd.DataFrame) -> pd.DataFrame:
        """Calcula a regressão linear para cada país."""
        regressoes_local: pd.DataFrame = dados_local.groupby('país').apply(regressao_por_pais).reset_index()
        # Adicionar códigos ISO e nomes dos países
        regressoes_local = regressoes_local.merge(dados_local[['país', 'iso_alpha']].drop_duplicates(), on='país', how='left')
        return regressoes_local

    def exibir_mapa(regressoes_local: pd.DataFrame) -> None:
        """Exibe o mapa com a taxa de aumento da produtividade por país."""
        st.header('Mapa da Taxa de Aumento da Produtividade por País')

        fig_mapa = px.choropleth(
            regressoes_local,
            locations='iso_alpha',
            color='slope',
            hover_name='país',
            color_continuous_scale='Blues',
            projection='natural earth',
            title='Taxa de Aumento da Produtividade por País'
        )

        st.plotly_chart(fig_mapa, use_container_width=True)

    def exibir_grafico_colunas(dados_local: pd.DataFrame) -> None:
        """Exibe o gráfico de colunas comparando a produtividade média."""
        st.header('Comparação da Produtividade Média')

        medias: pd.DataFrame = dados_local.groupby(['Categoria', 'ano'])['produtividade'].mean().reset_index()

        fig_colunas = px.bar(
            medias,
            x='ano',
            y='produtividade',
            color='Categoria',
            barmode='group',
            color_discrete_sequence=px.colors.sequential.Blues,
            title='Produtividade Média por Categoria de País'
        )

        st.plotly_chart(fig_colunas, use_container_width=True)

    def exibir_grafico_dispersao(dados_local: pd.DataFrame) -> None:
        """Exibe o gráfico de dispersão com a linha de regressão para um país selecionado."""
        st.header('Gráfico de Dispersão da Produtividade ao Longo do Tempo')

        paises_disponiveis: List[str] = sorted(dados_local['país'].unique())
        pais_selecionado: str = st.selectbox('Selecione um país', options=paises_disponiveis)

        dados_pais: pd.DataFrame = dados_local[dados_local['país'] == pais_selecionado]

        fig_disp = px.scatter(
            dados_pais,
            x='ano',
            y='produtividade',
            trendline='ols',
            color_discrete_sequence=px.colors.sequential.Blues,
            title=f'Produtividade ao Longo do Tempo - {pais_selecionado}'
        )

        st.plotly_chart(fig_disp, use_container_width=True)


