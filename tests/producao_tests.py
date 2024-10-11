import unittest
import pandas as pd
import os
from io import StringIO

# Adiciona o diretório src ao sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from producao import preprocessamento_producao

class TestPreprocessamentoProducao(unittest.TestCase):

    # Helper para criar um arquivo CSV temporário
    def create_temp_csv(self, content):
        csv_data = StringIO(content)
        df = pd.read_csv(csv_data)
        temp_path = 'test_temp_producao.csv'
        df.to_csv(temp_path, index=False)
        return temp_path

    # Teste a função com um DataFrame contendo todas as colunas necessárias
    def test_all_columns_present(self):
        csv_content = """Area,Item,Element,Unit,Y1961,Y1962,Y1963
Brazil,Wheat,Area harvested,ha,100,110,120
Brazil,Wheat,Production,t,1000,1050,1100
Brazil,Rice,Area harvested,ha,200,210,220
Brazil,Rice,Production,t,1500,1550,1600"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_producao(temp_path)
        os.remove(temp_path)

        expected_columns = ['ano', 'producao_total(t)', 'area_total_de_producao(ha)', 'country_code']
        self.assertEqual(sorted(cleaned_data.columns.tolist()), sorted(expected_columns))

    # Teste a função para verificar se ela retorna um DataFrame não vazio
    def test_non_empty_dataframe(self):
        csv_content = """Area,Item,Element,Unit,Y1961,Y1962,Y1963
Brazil,Wheat,Area harvested,ha,100,110,120
Brazil,Wheat,Production,t,1000,1050,1100
Brazil,Rice,Area harvested,ha,200,210,220
Brazil,Rice,Production,t,1500,1550,1600"""
        
        temp_path = self.create_temp_csv(csv_content)
        cleaned_data = preprocessamento_producao(temp_path)
        os.remove(temp_path)

        self.assertFalse(cleaned_data.empty)

if __name__ == "__main__":
    unittest.main()
