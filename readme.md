# Tema: Agricultura

O objetivo é tratar e unificar diversos datasets sobre agricultura, abrangendo um período comum, utilizando Pandas para manipulação de dados e NumPy para facilitar inferências estatísticas. O foco é garantir a integridade dos dados e permitir análises sobre fatores como terra arável, temperatura, precipitação e produção agrícola, visando identificar correlações e tendências ao longo do tempo.  

## Datasets:

### Arable Land (% of land area)
Proporção de terra arável em relação à área total de um país, usada para medir o potencial agrícola. Fonte: Banco Mundial.

Tratamentos: dados faltantes, dados repetidos, valores atípicos etc.

#### Fonte: [WorldBank](https://data.worldbank.org/indicator/AG.LND.ARBL.ZS)

| Country N    | aCountry C | oIndicator  | NIndicator       | C            | 1960         | 1961         | 1962         | 1963         | 1964         | 1965         | 1966         |
|--------------|------------|-------------|------------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| Aruba        | ABW        | Arable lan  | AG.LND.ARBL.ZS    | 1.111.111.111| 1.111.111.111| 1.111.111.111| 1.111.111.111| 1.111.111.111| 1.111.111.111|              |
| Africa East  | AFE        | Arable lan  | AG.LND.ARBL.ZS    | 4.702.843.083| 4.754.587.533| 4.866.723.384| 4.918.673.714| 4.972.682.842| 5.002.260.903|              |
| Afghanistan  | AFG        | Arable lan  | AG.LND.ARBL.ZS    | 1.172.899.131| 1.180.565.138| 1.188.231.145| 1.195.897.153| 1.195.897.153| 1.201.263.358|              |
| Africa West  | AFW        | Arable lan  | AG.LND.ARBL.ZS    | 6.976.669.636| 7.004.636.006| 7.041.556.036| 7.065.985.157| 7.102.573.569| 7.129.213.471|              |


### Temperature (GHCN)
Dados mensais históricos de temperatura de estações meteorológicas terrestres, usados para estudos de mudanças climáticas. Fonte: NOAA.

**Desafios:** ao baixar os dados eles vêm em dois arquivos, um `.dat` e outro `.env`. Deve-se lê-los com Python e transformá-los em um DataFrame para começar o tratamento dos dados, com cerca de 1.400.000 linhas.

Tratamentos: conversão de unidade (estão em centésimos °C), valores nulos (-9999), transformar em dados anuais, identificação correta dos países, agrupar os dados por país.

#### Fonte: [NOAA](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly)

| Station_ID   | Year | Jan  | Feb  | Mar  | Apr  | May  | Jun  | Jul  | Aug  | Sep  | Oct  | Nov  | Dec  |
|--------------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| ACW00011604  | 1961 |  -71 |  254 |   49 |  791 | 1146 | 1617 | 1588 | 1499 | 1431 | 1192 |  528 |  -21 |
| ACW00011604  | 1962 |  131 |  103 | -136 |  653 |  926 | 1399 | 1528 | 1411 | 1181 | 1012 |  341 | -108 |
| ACW00011604  | 1963 | -695 | -535 |  -81 |  559 | 1242 | 1645 | 1638 | 1614 |  135 |  958 |  584 |   -9 |
| ACW00011604  | 1964 |    8 |  -67 |   73 |  756 | 1237 |  146 | 1524 | 1575 | 1239 |  806 |  564 |  -13 |
| ACW00011604  | 1965 |   62 |  -87 |   56 |  608 | 1005 | 1518 | 1505 | 1495 | 1395 |  992 |   49 |  -16 |
| ACW00011604  | 1966 | -419 | -543 |  179 |  317 | 1153 | 1713 | 1691 | 1542 | 1266 |  874 |   73 |  -16 |
| ACW00011604  | 1967 | -199 |  107 |  468 |  552 | 1123 | 1444 | 1726 | 1669 | 1389 | 1068 |   63 |  -25 |


### Precipitação Agro
Dados históricos e projetados sobre precipitação focados nos impactos agrícolas. Fonte: Banco Mundial.

Tratamentos: dados faltantes, conversão de strings, agrupamento de dados, transformar em dados anuais.

#### Fonte: [WorldBank](https://climateknowledgeportal.worldbank.org/download-data)

| code | name       | 1901-01 | 1901-02 | 1901-03 | 1901-04 | 1901-05 | 1901-06 | 1901-07 | 1901-08 | 1901-09 | 1901-10 |
|------|------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| ABW  | Aruba      |    33.3 |    16.7 |         |       9 |    16.9 |    20.1 |    19.9 |    25.8 |    22.6 |    41.9 |
| AFG  | Afghanist  |   48.21 |   31.63 |   52.23 |    34.86|    53.82|    17.11|     4.48|     2.53|     3.03|     9.65|
| AGO  | Angola     |   152.7 |   153.6 |  170.88 |   130.86|    20.6 |     0.86|     0.77|     3.88|    21.4 |    68.7 |
| AIA  | Anguilla   |    92.6 |    27.2 |    59.1 |    49.5 |    88.3 |    89.1 |   125.6 |    97.4 |   163.3 |   123.6 |
| ALA  | Finland    |   15.76 |   21.36 |   19.57 |    32.15|     8.28|    37.45|     7.23|    27.14|    31.37|      71 |


### Production Indices
Índices de produção agrícola que medem a variação no volume de produção agrícola ao longo do tempo. Fonte: FAO.

Tratamentos: dados faltantes, conversão de unidades, segmentação de dados.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/QI)

| Area Code | Area Code | Area      | Item Code | Item Code | Item       | Element C | oElement  | Unit     | Y1961 | Y1962 | Y1963 | Y1964 | Y1965 |
|-----------|-----------|-----------|-----------|-----------|------------|-----------|-----------|----------|-------|-------|-------|-------|-------|
| 2         | 4         | Afghanist | 541       | 01349.20  | Other ston | 5510      | Productio | nt       | 18100 | 18100 | 18100 | 22100 | 24400 |
| 2         | 4         | Afghanist | 463       | 01290.90  | Other vege | 5312      | Area harv | eha      | 68700 | 68700 | 68700 | 73700 | 79700 |
| 2         | 4         | Afghanist | 463       | 01290.90  | Other vege | 5419      | Yield     | 100 g/ha | 42402 | 44585 | 47249 | 46526 | 44856 |
| 2         | 4         | Afghanist | 463       | 01290.90  | Other vege | 5510      | Productio | nt       | 291300| 306300| 324600| 342900| 357500|
| 2         | 4         | Afghanist | 534       | 1345      | Peaches a  | 5312      | Area harv | eha      | 1810  | 1810  | 1810  | 1920  | 2020  |
| 2         | 4         | Afghanist | 534       | 1345      | Peaches a  | 5419      | Yield     | 100 g/ha | 66298 | 66298 | 66298 | 76563 | 80693 |


### PIB
Produto Interno Bruto de países, medido em dólares correntes, usado para avaliar o desempenho econômico. Fonte: Banco Mundial.

Tratamentos: dados faltantes.

#### Fonte: [WorldBank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)

| Country N  | aCountry C | oIndicator | NIndicator      | C           | 1960       | 1961       | 1962       | 1963       | 1964       | 1965       | 1966       |
|------------|------------|------------|-----------------|-------------|------------|------------|------------|------------|------------|------------|------------|
| Bahrain    | BHR        | GDP (curr  | eNY.GDP.MKTP.CD |             |            |            |            |            |            |            |
| Bahamas    | BHS        | GDP (curr  | eNY.GDP.M       | 169803921   | 190098039  | 2.12E+08   | 2.38E+08   | 266666666  | 300392156  | 3.4E+08    |
| Bosnia     | BIH        | GDP (curr  | eNY.GDP.MKTP.CD |             |            |            |            |            |            |            |
| Belarus    | BLR        | GDP (curr  | eNY.GDP.MKTP.CD |             |            |            |            |            |            |            |
| Belize     | BLZ        | GDP (curr  | eNY.GDP.M       | 28072478    | 029964999  | 931857591  | 833750113  | 736194586  | 140110040  | 144450044.4|
| Bermuda    | BMU        | GDP (curr  | eNY.GDP.M       | 84466652    | 589249985  | 194149984  | 396366650  | 6107566648 | 114339050  | 13417337   |
| Bolivia    | BOL        | GDP (curr  | eNY.GDP.M       | 3.73E+08    | 4.06E+08   | 443916666  | 4.78E+08   | 538583333  | 598333333  | 6.63E+08   |


### Fertilizantes por Nutrientes
Quantidade de fertilizantes usados por tipo de nutriente na agricultura. Fonte: FAO.

Tratamentos: dados faltantes, retirar dados úteis da tabela, conversão de unidades.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/RFN)

| 9  | 32 | Argentina | 3102 | Nutrient n | i | 5510 | Productio | nt   | 2100  | A  | Official da | 5000  | X  |
|----|----|-----------|------|------------|---|------|-----------|------|-------|----|-------------|-------|----|
| 9  | 32 | Argentina | 3102 | Nutrient n | i | 5610 | Import Qu | t    | 6290  | A  | Official da | 7073  | A  |
| 9  | 32 | Argentina | 3102 | Nutrient n | i | 5910 | Export Qu | at   |       |    |             |       |    |
| 9  | 32 | Argentina | 3102 | Nutrient n | i | 5157 | Agricultur| at   | 8390  | A  | Official da | 8605  | A  |
| 9  | 32 | Argentina | 3102 | Nutrient n | i | 5159 | Use per ar| kg/ha| 0.43  | E  |             | 0.43  | E  |


### Pesticidas
Uso de pesticidas agrícolas por categoria (herbicidas, inseticidas, etc.). Fonte: FAO.

Tratamentos: valores faltantes, segmentação de dados, conversão de unidades.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/#data/RP)

| 4  | 12 | Algeria  | 1320 | Herbicide  | s | 5157 | Agricultur | at   | 99.28  | E  | Estimated   | 129.54  | E  | Estimated  | 69.7  |
|----|----|----------|------|------------|---|------|------------|------|--------|----|-------------|---------|----|------------|-------|
| 4  | 12 | Algeria  | 1331 | Fungicide  | s | 5157 | Agricultur | at   | 3275.4 | E  | Estimated   | 3712.8  | E  | Estimated  | 1898.4|
| 4  | 12 | Algeria  | 1341 | Plant Grow | w | 5157 | Agricultur | at   | 1059.34| I  | Imputed v   | 1059.34 | I  | Imputed v  | 1059.34|
| 4  | 12 | Algeria  | 1355 | Other Pest |   | 5157 | Agricultur | at   | 121.53 | E  | Estimated   | 198.79  | E  | Estimated  | 140.39|
| 6  | 20 | Andorra  | 1357 | Pesticides |   | 5157 | Agricultur | at   | 14.12  | E  | Estimated   | 14.12   | E  | Estimated  | 14.12 |
| 6  | 20 | Andorra  | 1357 | Pesticides |   | 5159 | Use per ar | kg/ha| 14.12  | E  |             | 14.12   | E  |            | 14.12 |


### Emissões
O dataset contém dados de emissões de gases de efeito estufa na agricultura, abrangendo diversas atividades agrícolas e mais de 200 países desde 1961. Fonte: FAO.

Tratamentos: agrupamento de dados por elementos e países, dados nulos, conversão de unidades, segmentação dos dados necessários.

#### Fonte: [Faostat](https://www.fao.org/faostat/en/##data/GT)

| Area Code | Area Code (M49) | Area       | Item Code | Item             | Element Code | Element                          | Source Code | Source   | Unit | Y1961     |
|-----------|-----------------|------------|-----------|------------------|--------------|----------------------------------|-------------|----------|------|-----------|
| 2         | 004             | Afghanistan| 5064      | Crop Residues    | 7234         | Direct emissions (N2O)           | 3050        | FAOTIER1 | kt   | 876200    |
| 2         | 004             | Afghanistan| 5064      | Crop Residues    | 7230         | Emissions (N2O)                  | 3050        | FAOTIER1 | kt   | 1073400   |
| 2         | 004             | Afghanistan| 5064      | Crop Residues    | 723113       | Emissions (CO2eq) (AR5)          | 3050        | FAOTIER1 | kt   | 284451000 |
| 2         | 004             | Afghanistan| 5060      | Rice Cultivation | 724413       | Emissions (CO2eq) from CH4 (AR5) | 3050        | FAOTIER1 | kt   | 823200000 |


### Desastres Naturais/Tecnológicos
Dados sobre a ocorrência e impacto de desastres em geral, naturais e tecnológicos. Fonte: EM-DAT.

Utilidade: Realizar análises com a API da OpenAI para comprovar ou sustentar teses e hipóteses levantadas.

Tratamentos: segmentar os dados, identificação correta dos países.

#### Fonte: [Emdat]( https://public.emdat.be/data)

| DisNo.      | Historic | Classifica  | tDisaster G | Disaster Su  | Disaster T | yDisaster Su    | External ID | Event Nam         | ISO | Country      | Subregion | Region      | Location             | Origin   | Associated |
|-------------|----------|-------------|-------------|--------------|------------|-----------------|-------------|-------------------|-----|--------------|-----------|-------------|----------------------|----------|------------|
| 1900-0003-  | Yes      | nat-met-s   | tNatural    | Meteorolo    | Storm      | Tropical cyclone |             |                   | USA | United Sta   | Northern  | AAmericas   | Galveston (Texas)    | Avalanch |            |
| 1900-0005-  | Yes      | tec-ind-fir | -Technolog  | Industrial   | Fire (Indu)| sFire (Industrial)|             |                   | USA | United Sta   | Northern  | AAmericas   | Hoboken, New York,   | Explosion|            |
| 1900-0006-  | Yes      | nat-hyd-fl  | oNatural    | Hydrologi    | cFlood     | Flood (General)  |             |                   | JAM | Jamaica      | Latin Ame | rAmericas   | Saint James          |          |            |
| 1900-0007-  | Yes      | nat-bio-ep  | Natural     | Biological   | Epidemic   | Viral disease    | Gastroent   |                   | JAM | Jamaica      | Latin Ame | rAmericas   | Porus                |          |            |


## Hipóteses Levantadas:

- Baseando-se nos dados agrícolas, é possível ver se um país apresentou desenvolvimento significativo no período (PIB)?

- Há uma correlação maior entre produção agrícola e PIB nos países subdesenvolvidos/em desenvolvimento em relação aos países desenvolvidos?

- A produtividade por hectare de terra arável está aumentando ao longo do tempo, com destaque para os países emergentes.

- A variação na precipitação ao longo dos anos está correlacionada com mudanças nos índices de produção agrícola em regiões específicas.

-  O aumento no uso de fertilizantes e pesticidas apresenta uma correlação maior com a produção por hectare em países subdesenvolvidos e emergentes?


## Pré Processamento 
(@Bruno_Luiz)

## Contribuições
- #### Bruno:
	- Tratou os dados

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
