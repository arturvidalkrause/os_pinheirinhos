"""Módulo de teste para o a função de limpeza do dataset de terras aráveis"""

import unittest
import pandas as pd
import os
from io import StringIO

# Adiciona o diretório src ao sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from arable_land import preprocessamento_arable_land

class TestPreprocessamentoArableLand(unittest.TestCase):

    def setUp(self):
        # Crie um diretório temporário e um arquivo CSV para o teste
        self.test_dir = 'test_dir'
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_content = """,,,,,,
        ,,,,,,
        ,,,,,,
        Country Name,Indicator Name,Indicator Code,Country Code,1960,1961,1962
Brazil,Arable land (% of land area),AG.LND.ARBL.ZS,BRA,10.5,10.6,NaN
World,Arable land (% of land area),AG.LND.ARBL.ZS,WLD,NaN,37.8,38.0
"""
        self.temp_path = os.path.join(self.test_dir, 'Arable_Land.csv')
        with open(self.temp_path, 'w') as f:
            f.write(self.csv_content)

    def tearDown(self):
        # Remove o arquivo temporário e o diretório após o teste
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_preprocessamento_arable_land(self):
        # Chama a função com o caminho do diretório temporário
        df_result = preprocessamento_arable_land(self.temp_path)

        # Verifica se as colunas estão corretas após o processamento
        expected_columns = ['ano', 'terras_araveis(%)', 'country_code']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se a coluna 'ano' foi convertida para int
        self.assertTrue(pd.api.types.is_integer_dtype(df_result['ano']))

        # Verifica se o período está correto (de 1961 a 2022)
        self.assertTrue((df_result['ano'] >= 1961).all())
        self.assertTrue((df_result['ano'] <= 2022).all())

        # Verifica se os países estão corretos
        self.assertIn('BRA', df_result['country_code'].values)
        self.assertIn('WLD', df_result['country_code'].values)

        # Verifica se os valores estão arredondados corretamente
        self.assertEqual(df_result["terras_araveis(%)"].iloc[0], 10.600)
        self.assertEqual(df_result["terras_araveis(%)"].iloc[1], 37.800)

if __name__ == '__main__':
    unittest.main()
