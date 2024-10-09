import unittest
import pandas as pd
from io import StringIO
from pib import preprocessamento_PIB

class TestPreprocessamentoPIB(unittest.TestCase):

    def setUp(self):
        # Criando um CSV de exemplo para testar
        self.csv_data = """Country Name,Indicator Name,1960,1961,1962,1963,Indicator Code,Country Code
                           Brazil,PIB (current US$),NaN,500.5,505.0,510.0,NY.GDP.MKTP.CD,BRA
                           World,PIB (current US$),NaN,10000.0,10500.0,11000.0,NY.GDP.MKTP.CD,WLD
                           Kosovo,PIB (current US$),NaN,200.0,210.0,220.0,NY.GDP.MKTP.CD,OWID_KOS
                           Brazil,Other Indicator,NaN,NaN,NaN,NaN,OTHER_CODE,BRA
                        """
        self.path_mock = StringIO(self.csv_data)

    def test_preprocessamento_PIB(self):
        # Usando StringIO para simular a leitura de um arquivo CSV
        df_result = preprocessamento_PIB(self.path_mock)

        # Verifica se as colunas estão corretas após o processamento
        expected_columns = ['ano', 'PIB', 'country_code']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se o número de linhas está correto após filtragem
        self.assertEqual(len(df_result), 6)

        # Verifica se os valores estão arredondados corretamente
        self.assertEqual(df_result['PIB'].iloc[0], 500.5)

        # Verifica se o período está correto (de 1961 a 2022)
        self.assertTrue(df_result['ano'].between(1961, 2022).all())

if __name__ == '__main__':
    unittest.main()
