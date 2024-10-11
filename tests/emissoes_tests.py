import unittest
import pandas as pd
import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from clean.emissoes import preprocessamento_emissoes

class TestPreprocessamentoEmissoes(unittest.TestCase):

    def setUp(self):
        # Crie um arquivo temporário CSV para o teste
        self.csv_path = 'test_annual_co2_emissions.csv'
        with open(self.csv_path, 'w') as f:
            f.write("""Entity,Code,Year,Annual CO2 emissions (tonnes)
Brazil,BRA,1960,10.5
Brazil,BRA,1961,10.6
Brazil,BRA,1962,NaN
World,OWID_WRL,1960,NaN
World,OWID_WRL,1961,37.8
World,OWID_WRL,1962,38.0
""")

    def tearDown(self):
        # Remova o arquivo temporário após o teste
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

    def test_preprocessamento_emissoes(self):
        # Passe o caminho completo do arquivo de teste
        df_result = preprocessamento_emissoes(os.path.dirname(os.path.abspath(self.csv_path)))

        # Verifique se as colunas estão corretas
        expected_columns = ['ano', 'Annual CO2 emissions (tonnes)', 'country_code']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se a coluna 'ano' foi convertida para int
        self.assertTrue(pd.api.types.is_integer_dtype(df_result['ano']))

        # Verifique se o período está correto (de 1961 a 2022)
        self.assertTrue((df_result['ano'] >= 1961).all())
        self.assertTrue((df_result['ano'] <= 2022).all())

        # Verifique se os países estão corretos
        self.assertIn('BRA', df_result['country_code'].values)
        self.assertIn('WLD', df_result['country_code'].values)

        # Verifique se os valores estão arredondados corretamente
        self.assertEqual(df_result["Annual CO2 emissions (tonnes)"].iloc[0], 10.6)
        self.assertEqual(df_result["Annual CO2 emissions (tonnes)"].iloc[1], 37.8)

if __name__ == '__main__':
    unittest.main()
