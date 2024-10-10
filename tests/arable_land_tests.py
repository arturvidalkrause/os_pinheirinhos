import unittest
import pandas as pd
from io import StringIO

import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from clean.arable_land import preprocessamento_arable_land

class TestPreprocessamentoArableLand(unittest.TestCase):

    def setUp(self):
        # CSV de exemplo para testar a função
        self.csv_data = """Country Name,Indicator Name,Indicator Code,Country Code,1960,1961,1962
                           Brazil,Arable land (% of land area),AG.LND.ARBL.ZS,BRA,10.5,10.6,NaN
                           World,Arable land (% of land area),AG.LND.ARBL.ZS,WLD,NaN,37.8,38.0
                        """
        self.path_mock = StringIO(self.csv_data)

    def test_preprocessamento_arable_land(self):
        # Usando StringIO para simulação de leitura do CSV
        df_result = preprocessamento_arable_land(self.path_mock)

        # Verificando se as colunas estão
        expected_columns = ['ano', 'terras_araveis(%)', 'country_code']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se a coluna 'ano' foi convertida para int
        self.assertTrue(pd.api.types.is_integer_dtype(df_result['ano']))

        # Verifica se o período está correto (de 1961 a 2022)
        self.assertTrue((df_result['ano'] >= 1961).all())
        self.assertTrue((df_result['ano'] <= 2022).all())

        # Verifica se os países estão corretos
        self.assertTrue('BRA' in df_result['country_code'].values)
        self.assertTrue('WLD' in df_result['country_code'].values)

        # Verifica se os valores estão arredondados corretamente
        self.assertEqual(df_result["terras_araveis(%)"].iloc[0], 10.600)

if __name__ == '__main__':
    unittest.main()