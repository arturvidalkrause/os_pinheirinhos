import unittest
import pandas as pd
from io import StringIO
from temperatura import preprocessamento_temperatura

class TestPreprocessamentoTemperatura(unittest.TestCase):

    def setUp(self):
        # CSV de exemplo para testar a função
        self.data1 = """Station_ID,Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec
                        ST1,1961,25.0,-99.99,22.0,23.5,24.0,26.5,28.0,29.0,30.0,31.0,32.0,29.0
                        ST2,1961,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0
                     """
        self.data2 = """Station_ID,Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec
                        ST1,1962,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0,33.0,34.0,35.0
                        ST2,1962,-99.99,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0
                     """
        self.path_mock1 = StringIO(self.data1)
        self.path_mock2 = StringIO(self.data2)

        # Arquivos temporário para simular a leitura do parquet
        self.path_parquet1 = "temperatura_mes_a_mes1.parquet"
        self.path_parquet2 = "temperatura_mes_a_mes2.parquet"
        
        # Criando DataFrames e salvando como Parquet
        df1 = pd.read_csv(self.path_mock1)
        df2 = pd.read_csv(self.path_mock2)
        df1.to_parquet(self.path_parquet1, index=False)
        df2.to_parquet(self.path_parquet2, index=False)

    def test_preprocessamento_temperatura(self):
        # Chamando a função de pré-processamento
        path = "."  # Ajuste se necessário
        df_result = preprocessamento_temperatura(path)

        # Verifica se as colunas estão corretas após o processamento
        expected_columns = ['ano', 'country_code', 'temperatura_media_anual(°C)']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se o número de linhas está correto
        self.assertGreater(len(df_result), 0)  # Verifica se há dados

        # Verifica se a média anual foi calculada corretamente
        self.assertAlmostEqual(df_result['temperatura_media_anual(°C)'].iloc[0], 25.0, places=1)

        # Verifica se a coluna de ano foi extraída corretamente
        self.assertTrue(df_result['ano'].str.isnumeric().all())

    @classmethod
    def tearDownClass(cls):
        # Removendo arquivos temporários
        import os
        os.remove("temperatura_mes_a_mes1.parquet")
        os.remove("temperatura_mes_a_mes2.parquet")

if __name__ == '__main__':
    unittest.main()