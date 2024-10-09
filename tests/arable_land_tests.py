import unittest
import pandas as pd
from io import StringIO
from arable_land import preprocessamento_arable_land

class TestPreprocessamentoArableLand(unittest.TestCase):

    def setUp(self):
        # CSV de exemplo para testar a função
        self.csv_data = """Country Name,Indicator Name,Indicator Code,Country Code,1960,1961,1962
                           Brazil,Arable land (% of land area),AG.LND.ARBL.ZS,BRA,10.5,10.6,NaN
                           World,Arable land (% of land area),AG.LND.ARBL.ZS,WLD,NaN,37.8,38.0
                        """
        self.path_mock = StringIO(self.csv_data)

    def test_preprocessamento_arable_land(self):
        # Usando StringIO para simular a leitura de um arquivo CSV
        df_result = preprocessamento_arable_land(self.path_mock)

        # Verificando se as colunas estão corretas
        expected_columns = ['ano', 'terras_araveis(%)', 'country_code']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verificando se a coluna 'ano' foi convertida corretamente para int
        self.assertTrue(pd.api.types.is_integer_dtype(df_result['ano']))

        # Verificando se o período está correto (de 1961 a 2022)
        self.assertTrue((df_result['ano'] >= 1961).all())
        self.assertTrue((df_result['ano'] <= 2022).all())

        # Verificando se os países estão corretos
        self.assertTrue('BRA' in df_result['country_code'].values)
        self.assertTrue('WLD' in df_result['country_code'].values)

        # Verificando se os valores estão arredondados corretamente
        self.assertEqual(df_result["terras_araveis(%)"].iloc[0], 10.600)

if __name__ == '__main__':
    unittest.main()