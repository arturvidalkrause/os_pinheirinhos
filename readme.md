# Tema: Agricultura

O objetivo é tratar e unificar diversos datasets sobre agricultura, abrangendo um período comum, utilizando Pandas para manipulação de dados e NumPy para facilitar inferências estatísticas. O foco é garantir a integridade dos dados e permitir análises sobre fatores como terra arável, temperatura, precipitação e produção agrícola, visando identificar correlações e tendências ao longo do tempo.  

## Datasets:

### Arable Land (% of land area)
Proporção de terra arável em relação à área total de um país, usada para medir o potencial agrícola. Fonte: Banco Mundial.

Tratamentos: dados faltantes, dados repetidos, valores atípicos etc.

#### Fonte: [WorldBank](https://data.worldbank.org/indicator/AG.LND.ARBL.ZS)


### Temperature (GHCN)
Dados mensais históricos de temperatura de estações meteorológicas terrestres, usados para estudos de mudanças climáticas. Fonte: NOAA.

**Desafios:** ao baixar os dados eles vêm em dois arquivos, um `.dat` e outro `.env`. Deve-se lê-los com Python e transformá-los em um DataFrame para começar o tratamento dos dados, com cerca de 1.400.000 linhas.

Tratamentos: conversão de unidade (estão em centésimos °C), valores nulos (-9999), transformar em dados anuais, identificação correta dos países, agrupar os dados por país.

#### Fonte: [NOAA](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly)


### Precipitação Agro
Dados históricos e projetados sobre precipitação focados nos impactos agrícolas. Fonte: Banco Mundial.

Tratamentos: dados faltantes, conversão de strings, agrupamento de dados, transformar em dados anuais.

#### Fonte: [WorldBank](https://climateknowledgeportal.worldbank.org/download-data)


### Production Indices
Índices de produção agrícola que medem a variação no volume de produção agrícola ao longo do tempo. Fonte: FAO.

Tratamentos: dados faltantes, conversão de unidades, segmentação de dados.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/QI)



### PIB
Produto Interno Bruto de países, medido em dólares correntes, usado para avaliar o desempenho econômico. Fonte: Banco Mundial.

Tratamentos: dados faltantes.

#### Fonte: [WorldBank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)


### Fertilizantes por Nutrientes
Quantidade de fertilizantes usados por tipo de nutriente na agricultura. Fonte: FAO.

Tratamentos: dados faltantes, retirar dados úteis da tabela, conversão de unidades.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/RFN)


### Pesticidas
Uso de pesticidas agrícolas por categoria (herbicidas, inseticidas, etc.). Fonte: FAO.

Tratamentos: valores faltantes, segmentação de dados, conversão de unidades.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/RP)


### Emissões
O dataset contém dados de emissões de gases de efeito estufa na agricultura, abrangendo diversas atividades agrícolas e mais de 200 países desde 1961. Fonte: FAO.

Tratamentos: agrupamento de dados por elementos e países, dados nulos, conversão de unidades, segmentação dos dados necessários.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/##data/GT)

## Hipóteses Levantadas:

- Baseando-se nos dados agrícolas, é possível ver se um país apresentou desenvolvimento significativo no período (PIB)?

- Há uma correlação maior entre produção agrícola e PIB nos países subdesenvolvidos/em desenvolvimento em relação aos países desenvolvidos?

- A produtividade por hectare de terra arável está aumentando ao longo do tempo, com destaque para os países emergentes.

- A variação na precipitação ao longo dos anos está correlacionada com mudanças nos índices de produção agrícola em regiões específicas.

-  O aumento no uso de fertilizantes e pesticidas apresenta uma correlação maior com a produção por hectare em países subdesenvolvidos e emergentes?


## Pré Processamento 
O pré-processamento dos dados foi uma etapa essencial para garantir a integridade das informações. Dada a diversidade dos conjuntos de dados, essa fase também visou uniformizá-los, facilitando sua integração. Para isso, realizamos o tratamento de valores ausentes, preenchendo dados mensais de temperatura com a média entre os períodos anterior e posterior. Também adicionamos uma variável global, incluindo dados agregados do mundo para cada país, e garantimos a conversão de tipos de dados, assegurando que todas as colunas estivessem no formato correto e sem erros de arredondamento. Além disso, padronizamos o formato dos datasets, de modo que o país e o ano figurassem como linhas e as colunas corresponderiam aos indicadores, preenchendo valores faltantes de 1961 a 2022 com NaN e convertendo os nomes dos países para o código ISO de três dígitos.

## Contribuições
- #### Bruno:
	- Tratou os dados
	- Escreveu o artigo

- #### Artur: 
	- Documentação dos módulos e funções
	- Fez o readme

- #### Gustavo:
	- Streamlit
   	- Fez os Geomaps 

- #### Kauan:
	- Testes unitários

- #### Gabriel:
	- Testes unitários
	- Streamlit
