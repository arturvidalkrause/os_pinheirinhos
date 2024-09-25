# Dados

## Formatação:
**Area:** Brazil  
**Item:** Precipitação  
**Elemento:** Verão  
**Unidade:** mm  
**Anos:** 1961 – 2022  

## Bases de dados:

### Temperatura
1. [ ] Dividir por 100 e trocar os -9999 por NaN.
2. [ ] Substituir `Stations_ID` pelo nome do país (2 primeiras letras).
3. [ ] Temperatura média (por estações e ano todo) (maybe API OPENAI).

### Precipitação
1. [ ] Substituir valores vazios por NaN.
2. [ ] Trocar os cabeçalhos por mês.
3. [ ] Precipitação total (por estações e ano todo) (maybe API OPENAI).

### Produção (por produto)
1. [ ] Dropar colunas **Area Code**, **Item Code**, **Element Code**.
2. [ ] Agrupar em Agricultura e Pecuária.

### Emissões
1. [ ] Dropar colunas **Area Code**, **Item Code**, **Element Code**, **Source Code**, **Source**, **Y####F**, **Y####N**
2. [ ] Criar linhas total emissions CO2eq

### PIB
1. [ ] Dropar colunas **Country Code** e **Indicator Code**

### Fertilizantes
1. [ ] Dropar colunas **Area Code**, **Item Code**, **Element Code**, **Y####N**
2. [ ] Ficar apenas com linhas "Agricultural Use" e "Use por area of cropland"

### Desastres naturais
1. [ ] Analizar o que fazer com ela (Está muito mal formatada)

### Terra arável
1. [ ] Tirar as 4 primeiras linhas
2. [ ] Dropar colunas **Country Code**, **Indicator Code** e **1960**


### Pesticidas
1. [ ] Dropar colunas **Area Code**, **Item Code**, **Element Code**, **Y####F**, **Y####N**
2. [ ] Ficar apenas com linhas Pesticides (total), ["Agricultural Use" and "Use per area of cropland"]

