"""Inicializa totas as funções de limpeza dos dados que estão dentro de ./clean"""

import sys
import os

sys.path.append(
	os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)

import precipitacao
import temperatura
import pib
import arable_land
import emissoes
import producao
import fertilizantes
import pesticidas

# Diretório das tabelas a serem tratadas
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")
path_brutos = os.path.join(path_data, "brutos")
path_limpos = os.path.join(path_data, "limpos")

# limpeza dos dados de temperatura
temperatura_data = temperatura.preprocessamento_temperatura(path_brutos)
temperatura_data.to_parquet(os.path.join(path_limpos, 'temperatura.parquet'), engine="pyarrow", index=False)

# limpeza dos dados de pib
pib_data = pib.preprocessamento_PIB(path_brutos)
pib_data.to_parquet(os.path.join(path_limpos, 'PIB.parquet'), engine="pyarrow", index=False)

# # limpeza dos dados de terra arável
arable_land_data = arable_land.preprocessamento_arable_land(path_brutos)
arable_land_data.to_parquet(os.path.join(path_limpos, 'terras_araveis.parquet'), engine="pyarrow", index=False)

# # limpeza dos dados de emissões
emissoes_data = emissoes.preprocessamento_emissoes(path_brutos)
emissoes_data.to_parquet(os.path.join(path_limpos, 'emissoes_co2.parquet'), engine="pyarrow", index=False)

# # limpeza dos dados de produção
producao_data = producao.preprocessamento_producao(path_brutos)
producao_data.to_parquet(os.path.join(path_limpos, 'producao_total_e_area.parquet'), engine="pyarrow", index=False)

# # limpeza dos dados de precipitacao
precipitacao_data = precipitacao.preprocessamento_precipitacao(path_brutos)
precipitacao_data.to_parquet(os.path.join(path_limpos, 'precipitacao_anual.parquet'), engine="pyarrow", index=False)

# # limpeza dos dados de fertilizantes
fertilizantes_data = fertilizantes.preprocessamento_fertilizantes(path_brutos)
fertilizantes_data.to_parquet(os.path.join(path_limpos, 'fertilizantes_total.parquet'), engine="pyarrow", index=False)

# # limpeza dos dados de fertilizantes
fertilizantes_data = pesticidas.preprocessamento_pesticidas(path_brutos)
fertilizantes_data.to_parquet(os.path.join(path_limpos, 'pesticidas_total.parquet'), engine="pyarrow", index=False)