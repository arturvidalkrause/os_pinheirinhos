"""
Este módulo Streamlit apresenta uma aplicação interativa para visualizar e explorar diferentes hipóteses baseadas em dados agrícolas.

Funcionalidades principais:
1. `st.tabs()`: Divide a interface da aplicação em diferentes abas, permitindo que o usuário explore as hipóteses individualmente.
2. Cada aba contém uma hipótese, representada por um título e uma descrição, que foca em correlações entre dados agrícolas, PIB e produtividade.
3. O objetivo é fornecer um ambiente para explorar visualmente as hipóteses sobre como fatores agrícolas, como produtividade por hectare, uso de fertilizantes e variações de precipitação, afetam o desenvolvimento econômico dos países.

O aplicativo permite fácil navegação entre as hipóteses, facilitando a visualização e análise dos tópicos propostos.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from scipy.stats import spearmanr
import altair as alt
from pathlib import Path
import json
from sklearn.linear_model import LinearRegression
# Carregar os datasets do diretório de configurações
from config import DATA_SET_PRODUCAO, DATA_SET_PIB, DATA_SETS_RESUMOS, DATA_SETS_LIMPOS

# Configuração inicial do aplicativo (deve ser o primeiro comando Streamlit)
st.set_page_config(page_title='Análise de Produtividade Agrícola', layout='wide')
# Lista de hipóteses
hipoteses = [
    {
        "chave": "Hipótese 1",
        "titulo": "Análise do Crescimento Agrícola e Seu Impacto no Desenvolvimento do PIB",
        "descricao": "Baseando-se nos dados agrícolas, é possível ver se um país apresentou desenvolvimento significativo no período (PIB)?"
    },
    {
        "chave": "Hipótese 2",
        "titulo": "Correlação Entre Produção Agrícola e PIB: Comparando Países em Desenvolvimento e Desenvolvidos",
        "descricao": "Há uma correlação maior entre produção agrícola e PIB nos países subdesenvolvidos/em desenvolvimento em relação aos países desenvolvidos?"
    },
    {
        "chave": "Hipótese 3",
        "titulo": "Aumento da Produtividade por Hectare: Uma Tendência de Crescimento nos Países Emergentes",
        "descricao": "A produtividade por hectare de terra arável está aumentando ao longo do tempo, com destaque para os países emergentes."
    },
    {
        "chave": "Hipótese 4",
        "titulo": "Correlação Entre Variação de Precipitação e Mudanças na Produção Agrícola em Regiões Específicas",
        "descricao": "A variação na precipitação ao longo dos anos está correlacionada com mudanças nos índices de produção agrícola em regiões específicas."
    },
    {
        "chave": "Hipótese 5",
        "titulo": "Impacto de Fertilizantes e Pesticidas na Produção por Hectare em Países Subdesenvolvidos e Emergentes",
        "descricao": "O aumento no uso de fertilizantes e pesticidas apresenta uma corelação maior com a produção por hectare em paises subdesenvolvidos e emergentes?"
    }
    
]
tab1, tab2, tab3, tab4, tab5 = st.tabs([hipotese["chave"] for hipotese in hipoteses])

#######################################################################################################################################################################################

with tab1:
    st.title(hipoteses[0]["titulo"])
    st.subheader(hipoteses[0]["descricao"])

    # Carregando os dados
    df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
    df_pib = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

    # Mesclando os datasets
    df_merged = pd.merge(df_producao, df_pib, on=["country_code", "ano"])
    df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]
    df_merged = df_merged[df_merged["country_code"] == "WLD"]
    df_merged = df_merged.dropna()

    # Calculando a correlação de Pearson e Spearman
    corr_PIB_and_producao_total = df_merged[['producao_total(t)', 'PIB']].corr()['producao_total(t)']["PIB"]
    spearman_result = spearmanr(df_merged['producao_total(t)'], df_merged['PIB'])

    # Extraindo a estatística e o p-value de Spearman
    spearman_statistic = spearman_result.statistic
    p_value = spearman_result.pvalue

    # Exibindo os resultados no Streamlit
    st.write(f"A correlação de Spearman entre Produção Total e PIB é: {spearman_statistic:.3f}")
    st.write(f"O valor de p associado é: {p_value:.3e}")
    st.write(f"A correlação entre Produção total(t) e PIB($) é: {round(corr_PIB_and_producao_total, 3)}")

    # Gráfico de dispersão com Plotly
    fig = px.scatter(
        df_merged,
        x='producao_total(t)',
        y='PIB',
        hover_data={'country_code': True, 'ano': True},
        title="Gráfico de dispersão: Produção total(t) vs PIB($)", 
        trendline='ols'
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

    # Carregando os resumos de produção e PIB
    df_resumo_producao = pd.read_parquet(DATA_SETS_RESUMOS + "/produção.parquet", engine="pyarrow")
    df_resumo_pib = pd.read_parquet(DATA_SETS_RESUMOS + "/pib.parquet", engine="pyarrow")

    # Mesclando os resumos
    df_resumo_merged = pd.merge(df_resumo_producao, df_resumo_pib, on=["country_code", "pais"])
    df_resumo_merged = df_resumo_merged[df_resumo_merged["country_code"] != "WLD"]

    # Gráfico de resumo com Plotly
    fig_resumo = px.scatter(
        df_resumo_merged,
        x='slope_x',
        y='slope_y',
        hover_data={'country_code': True},
        title="Resumo de Produção e PIB"
    )

    # Exibindo o gráfico de resumo no Streamlit
    st.plotly_chart(fig_resumo)

    # # Gráfico de dispersão com Altair
    # scatter = alt.Chart(df_merged).mark_point().encode(
    #     x=alt.X('producao_total(t):Q', scale=alt.Scale(domain=[0, 9000000000]), title='Produção total (t)'),
    #     y=alt.Y('PIB:Q', scale=alt.Scale(domain=[0, 110000000000000]), title='PIB ($)'),
    #     tooltip=['country_code', 'ano']  # Dados a serem exibidos ao passar o mouse
    # ).properties(
    #     title='Gráfico de dispersão: Produção total(t) vs PIB($)',
    #     width=600,
    #     height=400
    # )

    # # Linha de regressão com Altair
    # regression_line = scatter.transform_regression(
    #     'producao_total(t)', 'PIB', method='linear', extent=[3000000000, df_merged['producao_total(t)'].max()]
    # ).mark_line(color='red')

    # # Combinando o gráfico de dispersão com a linha de regressão
    # final_chart = scatter + regression_line

    # # Exibindo o gráfico com Altair no Streamlit
    # st.altair_chart(final_chart, use_container_width=True)

#######################################################################################################################################################################################

with tab2:
    st.title(hipoteses[1]["titulo"])
    st.subheader(hipoteses[1]["descricao"])

    # Função para analisar correlação entre duas colunas
    def corr_analise(dataframe: pd.DataFrame, columns: list) -> dict:
        corr = dataframe[columns].corr()[columns[0]][columns[1]]

        # Calculando a correlação de Spearman
        spearman_result = spearmanr(dataframe[columns[0]], dataframe[columns[1]])

        # Extraindo a estatística e o p-value
        spearman_statistic = spearman_result.statistic
        p_value = spearman_result.pvalue

        # Exibindo os resultados de forma formatada
        st.write(f"A correlação de Spearman entre {columns[0]} e {columns[1]} é: {spearman_statistic:.3f}")
        st.write(f"O valor de p associado é: {p_value:.3e}")
        st.write(f"A correlação entre {columns[0]} e {columns[1]} é: {round(corr, 3)}")

        return {"corr": corr, "spearman_statistic": spearman_statistic, "p_value": p_value}

    # Função para calcular correlação por país e ano
    def corr_pais_ano(grupo: pd.DataFrame) -> pd.Series:
        corr = grupo[["producao_total(t)", "PIB"]].corr()["producao_total(t)"]["PIB"]

        # Calculando a correlação de Spearman
        spearman_result = spearmanr(grupo["producao_total(t)"], grupo["PIB"])

        # Extraindo a estatística e o p-value
        spearman_statistic = spearman_result.statistic
        p_value = spearman_result.pvalue

        return pd.Series({"corr": corr, "spearman_statistic": spearman_statistic, "p_value": p_value})

    # Carregar os dados de produção e PIB
    df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
    df_pib = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

    # Mesclar os datasets de produção e PIB
    df_merged = pd.merge(df_producao, df_pib, on=["country_code", "ano"])
    df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]
    df_merged = df_merged.dropna()

    # Carregar o arquivo JSON com a classificação dos países
    json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"
    with open(json_file_path, 'r') as json_file:
        countries_data = json.load(json_file)

    # Dividir o dataframe em três grupos de países
    df_developed = df_merged[df_merged["country_code"].isin(countries_data['developed'])]
    df_emerging = df_merged[df_merged["country_code"].isin(countries_data['emerging'])]
    df_developing_countries = df_merged[df_merged["country_code"].isin(countries_data['developing_countries'])]

    # Analisar correlação para cada grupo de países
    st.write("Correlação para países desenvolvidos:")
    corr_analise(df_developed, ["producao_total(t)", "PIB"])

    st.write("Correlação para países emergentes:")
    corr_analise(df_emerging, ["producao_total(t)", "PIB"])

    st.write("Correlação para países subdesenvolvidos:")
    corr_analise(df_developing_countries, ["producao_total(t)", "PIB"])

    # Resumo das correlações por ano
    df_developed_resume = df_developed.groupby(["ano"], observed=False).apply(corr_pais_ano).reset_index()
    df_emerging_resume = df_emerging.groupby(["ano"], observed=False).apply(corr_pais_ano).reset_index()
    df_developing_countries_resume = df_developing_countries.groupby(["ano"], observed=False).apply(corr_pais_ano).reset_index()

    # Adicionar a coluna "dataset" para identificar os grupos
    df_developed_resume["dataset"] = "developed"
    df_emerging_resume["dataset"] = "emerging"
    df_developing_countries_resume["dataset"] = "developing_countries"

    # Combinar os três dataframes
    df_merge_resume = pd.concat([df_developed_resume, df_emerging_resume, df_developing_countries_resume])

    # Criar gráfico de linhas com Altair
    line_chart = alt.Chart(df_merge_resume).mark_line().encode(
        x=alt.X('ano:O', 
                axis=alt.Axis(
                    values=[1961, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022]
                )), 
        y=alt.Y('corr:Q', scale=alt.Scale(domain=[0.55, 1]), title='Correlação entre Produção agrícola e PIB'),
        color='dataset:N',             # Cor das linhas baseado no dataset
        tooltip=['ano:O', 'dataset:N', 'corr:Q']  # Tooltip com informações
    ).properties(
        title='Gráfico de Linhas Triplo: Correlação por Ano',
        width=600,
        height=400
    )

    # Exibir gráfico de linhas no Streamlit
    st.altair_chart(line_chart, use_container_width=True)


#######################################################################################################################################################################################

with tab3:
    st.title(hipoteses[2]["titulo"])
    st.subheader(hipoteses[2]["descricao"])

    # Função para realizar a regressão linear
    def regressao_por_grupo(grupo: pd.DataFrame) -> np.float64:
        """Realiza uma regressão linear com os dados ao longo de um período."""
        x: pd.Series = grupo[["ano"]]
        y: pd.Series = grupo["Produção por hectare (t)"]

        modelo = LinearRegression()
        modelo.fit(x, y)
        slope = modelo.coef_[0]

        return slope

    # Função para calcular a média de produção por hectare
    def mean(grupo: pd.DataFrame) -> pd.Series:
        return pd.Series({"Produção por hectare (t)": grupo["Produção por hectare (t)"].mean()})

    # Carregar o arquivo JSON com a classificação dos países
    json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"
    with open(json_file_path, 'r') as json_file:
        countries_data = json.load(json_file)

    # Carregar os dados de produção
    df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
    df_producao["Produção por hectare (t)"] = df_producao["producao_total(t)"] / df_producao["area_total_de_producao(ha)"]
    df_producao = df_producao.dropna()

    # Separar os países por grupos
    df_developed = df_producao[df_producao["country_code"].isin(countries_data['developed'])]
    df_emerging = df_producao[df_producao["country_code"].isin(countries_data['emerging'])]
    df_developing_countries = df_producao[df_producao["country_code"].isin(countries_data['developing_countries'])]

    # Resumir os dados por ano
    df_developed_resume = df_developed.groupby(["ano"], observed=False).apply(mean).reset_index()
    df_emerging_resume = df_emerging.groupby(["ano"], observed=False).apply(mean).reset_index()
    df_developing_countries_resume = df_developing_countries.groupby(["ano"], observed=False).apply(mean).reset_index()

    # Calcular o coeficiente de regressão para cada grupo
    slope = {
        "developed": regressao_por_grupo(df_developed_resume),
        "emerging": regressao_por_grupo(df_emerging_resume),
        "developing_countries": regressao_por_grupo(df_developing_countries_resume),
    }

    # Exibir os coeficientes de regressão no Streamlit
    st.write("Coeficientes de Regressão Linear:")
    for group, coefficient in slope.items():
        st.write(f"O coeficiente de regressão para {group} é: {coefficient:.4f}")

    # Adicionar coluna de identificação do dataset
    df_developed_resume["dataset"] = "developed"
    df_emerging_resume["dataset"] = "emerging"
    df_developing_countries_resume["dataset"] = "developing_countries"

    # Unir os dataframes de resumo
    df_merge_resume = pd.concat([df_developed_resume, df_emerging_resume, df_developing_countries_resume])

    # Criar gráfico de linhas com Altair
    line_chart = alt.Chart(df_merge_resume).mark_line().encode(
        x=alt.X('ano:O', 
                axis=alt.Axis(
                    values=[1961, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022]
                )), 
        y=alt.Y('Produção por hectare (t):Q', title='Produção por hectare (t)'),
        color='dataset:N',             # Cor das linhas baseado no dataset
        tooltip=['ano:O', 'dataset:N', 'Produção por hectare (t):Q']  # Tooltip com informações
    ).properties(
        title='Gráfico de Linhas Triplo: Produção por Hectare por Ano',
        width=600,
        height=400
    )

    # Exibir gráfico no Streamlit
    st.altair_chart(line_chart, use_container_width=True)


#######################################################################################################################################################################################

with tab4:
	st.title(hipoteses[3]["titulo"])
	st.subheader(hipoteses[3]["descricao"])
     
	# Carrega os dados do dataset de produção agrícola
	df = pd.read_parquet(DATA_SET_PRODUCAO)

	# Calcula a produção por hectare (toneladas por hectare)
	df["Produção_por_hectare_(t)"] = df["producao_total(t)"] / df["area_total_de_producao(ha)"]

	def regressao_por_pais(grupo: pd.DataFrame) -> pd.Series:
		"""
		Realiza uma regressão linear para analisar a relação entre o ano e a produção por hectare de cada país.

		Args:
			grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Produção_por_hectare_(t)'.

		Returns:
			pd.Series: Retorna uma série contendo o coeficiente angular (slope) da regressão linear e o nome do país.

		Variáveis:
			x (pd.Series): Série com os anos (coluna 'ano').
			y (pd.Series): Série com os dados de produção por hectare (coluna 'Produção_por_hectare_(t)').
		"""
		x: pd.Series = grupo[["ano"]]
		y: pd.Series = grupo["Produção_por_hectare_(t)"]

		if x.isna().any().any() or y.isna().any():
			return pd.Series({"slope": np.nan})

		modelo = LinearRegression()
		modelo.fit(x, y)
		
		slope = modelo.coef_[0]
		return pd.Series({"slope": slope})
		
	def format_dolar(valor: int | None) -> str:
		"""
		Formata um número inteiro ou float para o formato de dólar, separando os milhares por ponto.

		Args:
			valor (int | None): Valor a ser formatado.

		Returns:
			str: Valor formatado como string no formato de dólar (e.g., 1.000.000) ou "N/A" se o valor for nulo.
		"""
		if pd.isna(valor):
			return "N/A"
		return f"{valor:,.0f}".replace(",", ".")

	def map_reg_linear(df: pd.DataFrame) -> None:
		"""
		Gera um gráfico coroplético para representar a taxa média de crescimento anual (slope) da produção por hectare em cada país, utilizando regressão linear.

		Args:
			df (pd.DataFrame): DataFrame com os dados de produção por país, incluindo as colunas 'country_code', 'ano', 'Produção_por_hectare_(t)'.

		Returns:
			None: O gráfico é exibido diretamente e salvo como um arquivo SVG.
		"""
		df = df.dropna()
		# Aplica regressão linear por país
		resultados_regressao = df.groupby(['country_code'], observed=False).apply(regressao_por_pais).reset_index()

		# Formata o slope (taxa de crescimento) em formato de dólar
		resultados_regressao["Slope ($)"] = resultados_regressao["slope"].apply(format_dolar)

		fig_reg_linear = px.choropleth(resultados_regressao,
								locations= "country_code",
								color= "slope",
								hover_data= {"Slope ($)": True, "country_code": False, "slope": True},
								range_color=[0,0.4],
        						color_continuous_scale=px.colors.sequential.Plasma,
								)

		fig_reg_linear.update_layout(
			title={
				'text': "Taxa média de crescimento anual da Produção por hectare(t)",
				'x': 0.2
			}
		)

		fig_reg_linear.add_annotation(
			text= "Periodo: 1961 a 2022",
			y= -0.05,
			showarrow= False
		)
          
		fig_reg_linear.update_layout(
			margin=dict(l=0, r=0, t=40, b=10),
			coloraxis_colorbar=dict(title="Slope", tickprefix=' ')
		)

		st.plotly_chart(fig_reg_linear)
          
	# Gera o mapa da regressão linear
	map_reg_linear(df)

#######################################################################################################################################################################################

with tab5:
	st.title(hipoteses[4]["titulo"])
	st.subheader(hipoteses[4]["descricao"])
    
	from config import DATA_SET_PRODUCAO, DATA_SET_FERTILIZANTES, DATA_SETS_RESUMOS, DATA_SET_PESTICIDAS

	def regressao_por_grupo(grupo: pd.DataFrame) -> pd.DataFrame:
		"""
		Realiza uma regressão linear com os dados ao longo de um período.

		Args:
			grupo (pd.DataFrame): DataFrame contendo os dados de um país agrupados. Deve incluir as colunas 'ano' e 'Produção por hectare (t)'.

		Returns:
			pd.DataFrame: DataraFrame com os coeficientes angulares da reta da regressão linear.

		Variáveis:
			x (pd.Series): Série com os anos.
			y (pd.Series): Série com a produção por hectare.
		"""
		if grupo.empty:
			return np.nan  # Retorna NaN se o grupo estiver vazio

		x: pd.Series = grupo[["ano"]]
		y_fertilizantes: pd.Series = grupo["uso_total_de_fertilizantes(t)"]

		modelo_fertilizantes = LinearRegression()
		modelo_fertilizantes.fit(x, y_fertilizantes)
		slope_fertilizantes = modelo_fertilizantes.coef_[0]
            
		y_pesticidas: pd.Series = grupo["uso_total_de_pesticidas(t)"]

		modelo_pesticidas = LinearRegression()
		modelo_pesticidas.fit(x, y_pesticidas)
		slope_pesticidas = modelo_pesticidas.coef_[0]

		return pd.DataFrame({"slope_fertilizantes": [slope_fertilizantes], "slope_pesticidas": [slope_pesticidas]})

	# Lê o arquivo JSON contendo a classificação dos países
	json_file_path = Path(DATA_SETS_RESUMOS) / "classificação_paises.json"

	with open(json_file_path, 'r') as json_file:
		countries_data = json.load(json_file)

	# Carregando os datasets de produção, pesticidas e fertilizantes
	df_producao = pd.read_parquet(DATA_SET_PRODUCAO, engine="pyarrow")
	df_pesticidas = pd.read_parquet(DATA_SET_PESTICIDAS, engine="pyarrow")
	df_fertilizantes = pd.read_parquet(DATA_SET_FERTILIZANTES, engine="pyarrow")

	# Unindo os DataFrames de produção, pesticidas e fertilizantes
	df_merged = pd.merge(df_producao, df_pesticidas, on=["country_code", "ano"])
	df_merged = pd.merge(df_merged, df_fertilizantes, on=["country_code", "ano"])

	# Calculando a produção por hectare
	df_merged["Produção por hectare (t)"] = df_merged["producao_total(t)"] / df_merged["area_total_de_producao(ha)"]

	# Removendo valores NaN
	df_merged = df_merged.dropna()
      
	# Criando DataFrames separados para países desenvolvidos, emergentes e em desenvolvimento
	df_developed = df_merged[df_merged["country_code"].isin(countries_data['developed'])]
	df_emerging = df_merged[df_merged["country_code"].isin(countries_data['emerging'])]
	df_subdeveloped = df_merged[df_merged["country_code"].isin(countries_data['developing_countries'])]

	# Exibindo as correlações para o conjunto total de países e para cada grupo de países
	st.write('Total:', df_merged[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")

	st.write('Desenvolvidos:', df_developed[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
	st.write('Emergentes:', df_emerging[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
	st.write('Em desenvolvimento:', df_subdeveloped[['Produção por hectare (t)', 'uso_total_de_pesticidas(t)', 'uso_total_de_fertilizantes(t)']].corr(), end="\n\n")
    
	df_merge_reg_linear = df_merged.groupby(["country_code"], observed=False).apply(regressao_por_grupo).reset_index()
      
	# st.write(df_merge_reg_linear)

	fig_reg_linear_fertilizantes = px.choropleth(df_merge_reg_linear,
							locations= "country_code",
							color= "slope_fertilizantes",
							hover_data= {"country_code": False, "slope_fertilizantes": True},
							range_color=[-2000,500000],
							color_continuous_scale=px.colors.sequential.Plasma,
							)

	fig_reg_linear_fertilizantes.update_layout(
		title={
			'text': "Taxa média de crescimento anual do uso de Fertiliznates(t)",
			'x': 0.2
		}
	)

	fig_reg_linear_fertilizantes.add_annotation(
		text= "Periodo: 1961 a 2022",
		y= -0.05,
		showarrow= False
	)
		
	fig_reg_linear_fertilizantes.update_layout(
		margin=dict(l=0, r=0, t=40, b=10),
		coloraxis_colorbar=dict(title="Slope", tickprefix=' ')
	)

	st.plotly_chart(fig_reg_linear_fertilizantes)
      
	fig_reg_linear_pesticidas = px.choropleth(df_merge_reg_linear,
							locations= "country_code",
							color= "slope_pesticidas",
							hover_data= {"country_code": False, "slope_pesticidas": True},
							range_color=[-3000,15000],
							color_continuous_scale=px.colors.sequential.Plasma,
							)

	fig_reg_linear_pesticidas.update_layout(
		title={
			'text': "Taxa média de crescimento anual do uso de Pesticidas(t)",
			'x': 0.2
		}
	)

	fig_reg_linear_pesticidas.add_annotation(
		text= "Periodo: 1961 a 2022",
		y= -0.05,
		showarrow= False
	)
		
	fig_reg_linear_pesticidas.update_layout(
		margin=dict(l=0, r=0, t=40, b=10),
		coloraxis_colorbar=dict(title="Slope", tickprefix=' ')
	)

	st.plotly_chart(fig_reg_linear_pesticidas)