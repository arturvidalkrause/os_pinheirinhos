import unittest
import pandas as pd
from io import StringIO

import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from clean.fertilizantes import preprocessamento_fertilizantes

class TestPreprocessamentoFertilizantes(unittest.TestCase):

    def setUp(self):
        # CSV de exemplo para testar a função
        self.csv_data = """Area,Element Code,Item Code,Element,Unit,Y1960,Y1961,Y1962,Area Code,Area Code (M49)
                           Brazil,5157,101,Usage,tonnes,NaN,100.5,105.0,76,123
                           World,5157,101,Usage,tonnes,NaN,50000.0,51000.0,OWID_WRL,123
                           Kosovo,5157,101,Usage,tonnes,NaN,30.0,35.0,OWID_KOS,123
                           Brazil,1234,102,Other,tonnes,NaN,NaN,NaN,76,123
                        """
        self.path_mock = StringIO(self.csv_data)

    def test_preprocessamento_fertilizantes(self):
        # Usando StringIO para simular a leitura de um arquivo CSV
        df_result = preprocessamento_fertilizantes(self.path_mock)

        # Verifica se as colunas estão corretas após o processamento
        expected_columns = ['ano', 'uso_total_de_fertilizantes(t)', 'country_code']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se a coluna 'ano' foi convertida para int
        self.assertTrue(pd.api.types.is_integer_dtype(df_result['ano']))

        # Verifica se o período está correto (de 1961 a 2022)
        self.assertTrue((df_result['ano'] >= 1961).all())
        self.assertTrue((df_result['ano'] <= 2022).all())

        # Verifica se os países foram corretamente filtrados e codificados
        self.assertIn('BRA', df_result['country_code'].unique())
        self.assertIn('WLD', df_result['country_code'].unique())
        self.assertIn('XKX', df_result['country_code'].unique())

        # Verifica se os valores estão arredondados corretamente
        self.assertEqual(df_result["uso_total_de_fertilizantes(t)"].iloc[0], 100.50)

        # Verifica se os anos faltantes foram preenchidos corretamente
        unique_years = df_result['ano'].nunique()
        self.assertEqual(unique_years, 62)  # Anos de 1961 a 2022

if __name__ == '__main__':
    unittest.main()