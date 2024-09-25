"""Inicializa totas as funções de limpeza dos dados que estão dentro de ./clean"""

import pandas as tp
import sys
import os

sys.path.append(
	os.path.abspath(os.path.join(os.path.dirname(__file__), "../clean"))
)

import precipitacao
