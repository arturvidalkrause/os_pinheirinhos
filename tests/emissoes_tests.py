import unittest
import pandas as pd
from io import StringIO
from emissoes import preprocessamento_emissoes

class TestPreprocessamentoEmissoes(unittest.TestCase):

    def setUp(self):
        # CSV de exemplo para testar a função
        self.csv_data = """Entity,Code,Year,Annual CO2 emissions
                           Brazil,BRA,1960,NaN
                           Brazil,BRA,1961,100.0
                           Brazil,BRA,1962,110.0
                           World,OWID_WRL,1961,NaN
                           World,OWID_WRL,1962,30000.0
                           Kosovo,OWID_KOS,1961,NaN
                        """
        self.path_mock = StringIO(self.csv_data)

    def test_preprocessamento_emissoes(self):
        # Usando StringIO para simulação de leitura do CSV
        df_result = preprocessamento_emissoes(self.path_mock)

        # Verifica se as colunas foram renomeadas corretamente
        expected_columns = ['country_code', 'ano', 'Annual CO2 emissions']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se a coluna 'ano' foi convertida para int
        self.assertTrue(pd.api.types.is_integer_dtype(df_result['ano']))

        # Verifica se o período está correto (de 1961 a 2022)
        self.assertTrue((df_result['ano'] >= 1961).all())
        self.assertTrue((df_result['ano'] <= 2022).all())

        # Verifica se o total global foi renomeado de 'OWID_WRL' para 'WLD'
        self.assertIn('WLD', df_result['country_code'].unique())

        # Verifica se o Kosovo foi renomeado de 'OWID_KOS' para 'XKX'
        self.assertIn('XKX', df_result['country_code'].unique())

        # Verifica se as linhas com 'country_code' NaN foram removidas
        self.assertFalse(df_result['country_code'].isna().any())

if __name__ == '__main__':
    unittest.main()
