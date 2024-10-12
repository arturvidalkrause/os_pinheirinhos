"""Módulo de teste para o a função de limpeza do dataset de temperatura"""

import unittest
import pandas as pd
import numpy as np
import os

# Ajusta o caminho do módulo para importação
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'clean')))

from temperatura import preprocessamento_temperatura

class TestPreprocessamentoTemperatura(unittest.TestCase):

    # Helper para criar um arquivo Parquet temporário
    def create_temp_parquet(self, df, file_name):
        temp_path = file_name
        df.to_parquet(temp_path, index=False)
        return temp_path

    # Helper para criar um arquivo de mapeamento temporário
    def create_temp_mapping_file(self, mapping, file_name):
        temp_path = file_name
        with open(temp_path, 'w') as f:
            for k, v in mapping.items():
                f.write(f"{k} {v}\n")
        return temp_path

    def setUp(self):
        # Cria DataFrame de exemplo
        data1 = {
            'Station_ID': ['ST001', 'ST002'],
            'Year': [1961, 1962],
            'Jan': [10, 15],
            'Feb': [12, 17],
            'Mar': [-99.99, 19],
            'Apr': [14, 21],
            'May': [15, 22],
            'Jun': [16, 23],
            'Jul': [17, 24],
            'Aug': [18, 25],
            'Sep': [19, 26],
            'Oct': [20, 27],
            'Nov': [21, 28],
            'Dec': [22, 29]
        }
        data2 = {
            'Station_ID': ['ST003', 'ST004'],
            'Year': [1963, 1964],
            'Jan': [11, 16],
            'Feb': [13, 18],
            'Mar': [-99.99, 20],
            'Apr': [15, 22],
            'May': [16, 23],
            'Jun': [17, 24],
            'Jul': [18, 25],
            'Aug': [19, 26],
            'Sep': [20, 27],
            'Oct': [21, 28],
            'Nov': [22, 29],
            'Dec': [23, 30]
        }
        self.df1 = pd.DataFrame(data1)
        self.df2 = pd.DataFrame(data2)

        # Cria arquivos Parquet temporários
        self.temp_path1 = self.create_temp_parquet(self.df1, 'temperatura_mes_a_mes1.parquet')
        self.temp_path2 = self.create_temp_parquet(self.df2, 'temperatura_mes_a_mes2.parquet')

        # Cria arquivo de mapeamento temporário
        self.mapping = {'ST': 'TestCountry'}
        self.temp_mapping_path = self.create_temp_mapping_file(self.mapping, 'Conversão_Station_id_para_Pais.txt')

        # Define caminho
        self.path = '.'

    def tearDown(self):
        # Remove arquivos temporários após o teste
        os.remove(self.temp_path1)
        os.remove(self.temp_path2)
        os.remove(self.temp_mapping_path)

    def test_preprocessamento_temperatura(self):
        # Chama a função
        df_result = preprocessamento_temperatura(self.path)

        # Verifica se o DataFrame resultante não está vazio
        self.assertFalse(df_result.empty)

        # Verifica se as colunas do DataFrame estão corretas
        expected_columns = ['ano', 'temperatura_media_anual(°C)', 'country_code']
        self.assertEqual(sorted(df_result.columns.tolist()), sorted(expected_columns))

        # Verifica se os valores estão arredondados corretamente
        self.assertTrue(np.allclose(df_result['temperatura_media_anual(°C)'], df_result['temperatura_media_anual(°C)'].round(2)))

if __name__ == "__main__":
    unittest.main()
