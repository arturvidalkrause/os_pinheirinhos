"""Módulo de teste para o a função de limpeza do dataset de emissões"""

import unittest
import pandas as pd
import os
from io import StringIO

# Adiciona o diretório src ao sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from emissoes import preprocessamento_emissoes

class TestPreprocessamentoEmissoes(unittest.TestCase):

    # Helper para criar um arquivo CSV temporário
    def create_temp_csv(self, content):
        csv_data = StringIO(content)
        df = pd.read_csv(csv_data)
        temp_path = 'test_temp_emissoes.csv'
        df.to_csv(temp_path, index=False)
        return temp_path

    # Testa a função com um DataFrame contendo todas as colunas necessárias
    def test_all_columns_present(self):
        csv_content = """
        Entity,Code,Year,Annual CO₂ emissions
Brazil,BRA,1960,10.5
Brazil,BRA,1961,10.6
Brazil,BRA,1962,NaN
World,OWID_WRL,1960,NaN
World,OWID_WRL,1961,37.8
World,OWID_WRL,1962,38.0"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_emissoes(temp_path)
        os.remove(temp_path)

        expected_columns = ['ano', 'Annual CO₂ emissions', 'country_code']
        self.assertEqual(sorted(cleaned_data.columns.tolist()), sorted(expected_columns))

    # Testa a função para verificar se ela retorna um DataFrame não vazio
    def test_non_empty_dataframe(self):
        csv_content = """
        Entity,Code,Year,Annual CO₂ emissions
Brazil,BRA,1960,10.5
Brazil,BRA,1961,10.6
Brazil,BRA,1962,NaN
World,OWID_WRL,1960,NaN
World,OWID_WRL,1961,37.8
World,OWID_WRL,1962,38.0"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_emissoes(temp_path)
        os.remove(temp_path)

        self.assertFalse(cleaned_data.empty)

if __name__ == "__main__":
    unittest.main()