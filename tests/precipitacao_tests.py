import unittest
import pandas as pd
import os

# Ajusta o caminho do módulo para importação
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from precipitacao import preprocessamento_precipitacao

class TestPreprocessamentoPrecipitacao(unittest.TestCase):

    # Helper para criar um arquivo Excel temporário
    def create_temp_excel(self, df, file_name='test_temp_precipitacao.xlsx'):
        temp_path = file_name
        df.to_excel(temp_path, index=False)
        return temp_path

    # Testa a função com um DataFrame contendo todas as colunas necessárias
    def test_all_columns_present(self):
        data = {
            'code': ['BRA', 'WLD'],
            'name': ['Brazil', 'World'],
            '2021-01': [100, 200],
            '2021-02': [110, 210],
            '2022-01': [120, 220]
        }
        df = pd.DataFrame(data)
        temp_path = self.create_temp_excel(df)
        cleaned_data = preprocessamento_precipitacao(temp_path)
        os.remove(temp_path)

        expected_columns = ['ano', 'country_code', 'precipitação_anual']
        self.assertEqual(sorted(cleaned_data.columns.tolist()), sorted(expected_columns))

    # Testa a função para verificar se ela retorna um DataFrame não vazio
    def test_non_empty_dataframe(self):
        data = {
            'code': ['BRA', 'WLD'],
            'name': ['Brazil', 'World'],
            '2021-01': [100, 200],
            '2021-02': [110, 210],
            '2022-01': [120, 220]
        }
        df = pd.DataFrame(data)
        temp_path = self.create_temp_excel(df)
        cleaned_data = preprocessamento_precipitacao(temp_path)
        os.remove(temp_path)

        self.assertFalse(cleaned_data.empty)

if __name__ == "__main__":
    unittest.main()
