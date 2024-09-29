"""Inicializa totas as funções de limpeza dos dados que estão dentro de ./clean"""

import pandas as tp
import sys
import os

sys.path.append(
	os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)

# Importando os arquivos de limpeza
import precipitacao
import temperatura
import pib
import arable_land
import emissoes

# Diretório das tabelas a serem tratadas
path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")
path_brutos = os.path.join(path_data, "brutos")
path_limpos = os.path.join(path_data, "limpos")

# limpeza dos dados de temperatura
temperatura_data = temperatura.preprocessamento_temperatura(path_brutos)
temperatura_data.to_csv(os.path.join(path_limpos, 'temperatura.csv'))

# limpeza dos dados de pib
pib_data = pib.preprocessamento_PIB(path_brutos)
pib_data.to_csv(os.path.join(path_limpos, 'PIB.csv'))

# limpeza dos dados de terra arável
arable_land_data = arable_land.preprocessamento_arable_land(path_brutos)
arable_land_data.to_csv(os.path.join(path_limpos, 'terras_araveis.csv'))

# limpeza dos dados de emissões
emissoes_data = emissoes.preprocessamento_emissoes(path_brutos)
emissoes_data.to_csv(os.path.join(path_limpos, 'emissoes_co2eq.csv'))