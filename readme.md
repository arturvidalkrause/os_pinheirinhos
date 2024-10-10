# Tema: Agricultura

O objetivo é tratar e unificar diversos datasets sobre que afetam a agricultura em geral, abrangendo um período de 1961 a 2022, utilizando Pandas para manipulação de dados e NumPy para facilitar inferências estatísticas. O foco é garantir a integridade dos dados e permitir análises sobre fatores como quantidade de terra arável, temperatura, precipitação, insumos em geral, pip de cada pais e produção agrícola, visando identificar correlações e tendências ao longo do tempo	.  

## Datasets:

- #### Arable Land (% of land area)
	Proporção de terra arável em relação à área total de um país, usada para medir o potencial agrícola de cada pais.
	#### Fonte: [WorldBank](https://data.worldbank.org/indicator/AG.LND.ARBL.ZS)

- #### Temperature (GHCN)
	Dados mensais históricos de temperatura de mais de 25.000 estações meteorológicas terrestres, usados para estudos de mudanças climáticas.
	#### Fonte: [NOAA](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly)

- #### Precipitação Agro
	Dados históricos e projetados(futuro) sobre precipitação focados nos impactos agrícolas.
	#### Fonte: [WorldBank](https://climateknowledgeportal.worldbank.org/download-data)

- #### Production Indices
	Índices de produção agrícola que medem a variação no volume de produção agrícola ao longo do tempo de diversas culturas, além de dados sobre quantidade de terra cultivada e produção por area(produção/area produzida).
	#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/QI)

- #### PIB
	Produto Interno Bruto de países, medido em dólares correntes, usado para avaliar o desempenho econômico.
	#### Fonte: [WorldBank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)

- #### Fertilizantes por Nutrientes
	Quantidade de fertilizantes usados por tipo de nutriente na agricultura.
	#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/RFN)

- #### Pesticidas
	Uso de pesticidas agrícolas por categoria (herbicidas, inseticidas, etc) em cada pais ao longo dos anos.
	#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/RP)

- #### Emissões
	O dataset contém dados de emissões de gases de efeito estufa na agricultura, abrangendo diversas atividades agrícolas e mais de 200 países desde 1961.
	#### Fonte: [Faostat](https://www.fao.org/faostat/en/##data/GT)

- #### Emissões CO2
	O dataset contém dados de emissões de CO2 de mais de 200 países ao longo dos anos, desde 1750.
	#### Fonte: [Our World in Data](https://ourworldindata.org/co2-emissions)


## Hipóteses Levantadas:

- Baseando-se nos dados agrícolas, é possível ver se um país apresentou desenvolvimento significativo no período (PIB)?

- Há uma correlação maior entre produção agrícola e PIB nos países subdesenvolvidos/em desenvolvimento em relação aos países desenvolvidos?

- A produtividade por hectare de terra arável está aumentando ao longo do tempo, com destaque para os países emergentes.

- A variação na precipitação ao longo dos anos está correlacionada com mudanças nos índices de produção agrícola em regiões específicas.

-  O aumento no uso de fertilizantes e pesticidas apresenta uma correlação maior com a produção por hectare em países subdesenvolvidos e emergentes?


## Pré Processamento 
(@Bruno_Luiz)


## Desafios 
- Encontrar o Macri

## Contribuições
- #### Bruno:
	- Tratou os dados
	- Fez mais nada

- #### Artur: 
	- Documentação dos módulos e funções
	- Fez o readme

- #### Gustavo:
	- Streamlit

- #### Kauan:
	- 

- #### Gabriel:
	- Testes unitários
