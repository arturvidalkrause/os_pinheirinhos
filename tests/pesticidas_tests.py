"""Módulo de teste para o a função de limpeza do dataset de pesticidas"""

import unittest
import pandas as pd
import os
from io import StringIO

# Adiciona o diretório src ao sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from pesticidas import preprocessamento_pesticidas

class TestPreprocessamentoPesticidas(unittest.TestCase):

    # Helper para criar um arquivo CSV temporário
    def create_temp_csv(self, content):
        csv_data = StringIO(content)
        df = pd.read_csv(csv_data)
        temp_path = 'test_temp_pesticidas.csv'
        df.to_csv(temp_path, index=False)
        return temp_path

    # Testa a função com um DataFrame contendo todas as colunas necessárias
    def test_all_columns_present(self):
        csv_content = """Area,Element Code,Item Code,Element,Unit,Y1961,Y1962,Y1963
Brazil,5157,1357,Total Pesticide Use,t,100,110,120
Brazil,5157,1357,Total Pesticide Use,t,200,210,220
World,5157,1357,Total Pesticide Use,t,300,310,320
World,5157,1357,Total Pesticide Use,t,400,410,420"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_pesticidas(temp_path)
        os.remove(temp_path)

        expected_columns = ['ano', 'uso_total_de_fertilizantes(t)', 'country_code']
        self.assertEqual(sorted(cleaned_data.columns.tolist()), sorted(expected_columns))

    # Testa a função para verificar se ela retorna um DataFrame não vazio
    def test_non_empty_dataframe(self):
        csv_content = """Area,Element Code,Item Code,Element,Unit,Y1961,Y1962,Y1963
Brazil,5157,1357,Total Pesticide Use,t,100,110,120
Brazil,5157,1357,Total Pesticide Use,t,200,210,220
World,5157,1357,Total Pesticide Use,t,300,310,320
World,5157,1357,Total Pesticide Use,t,400,410,420"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_pesticidas(temp_path)
        os.remove(temp_path)

        self.assertFalse(cleaned_data.empty)

if __name__ == "__main__":
    unittest.main()
