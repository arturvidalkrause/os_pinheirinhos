import unittest
import pandas as pd
import os

# Ajusta o caminho do módulo para importação
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from pib import preprocessamento_PIB

class TestPreprocessamentoPIB(unittest.TestCase):

    # Helper para criar um arquivo CSV temporário
    def create_temp_csv(self, content):
        temp_path = 'test_temp_pib.csv'
        with open(temp_path, 'w') as f:
            f.write(content)
        return temp_path

    # Testa a função com um DataFrame contendo todas as colunas necessárias
    def test_all_columns_present(self):
        csv_content = """Country Name,Indicator Name,Indicator Code,Country Code,1960,1961,1962
Brazil,GDP (current US$),NY.GDP.MKTP.CD,BRA,500,550,600
World,GDP (current US$),NY.GDP.MKTP.CD,WLD,1000,1100,1200"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_PIB(temp_path)
        os.remove(temp_path)

        expected_columns = ['ano', 'PIB', 'country_code']
        self.assertEqual(sorted(cleaned_data.columns.tolist()), sorted(expected_columns))

    # Testa a função para verificar se ela retorna um DataFrame não vazio
    def test_non_empty_dataframe(self):
        csv_content = """Country Name,Indicator Name,Indicator Code,Country Code,1960,1961,1962
Brazil,GDP (current US$),NY.GDP.MKTP.CD,BRA,500,550,600
World,GDP (current US$),NY.GDP.MKTP.CD,WLD,1000,1100,1200"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_PIB(temp_path)
        os.remove(temp_path)

        self.assertFalse(cleaned_data.empty)

if __name__ == "__main__":
    unittest.main()