import unittest
import pandas as pd
from io import StringIO
from producao import preprocessamento_producao

class TestPreprocessamentoPrecipitacao(unittest.TestCase):

    def setUp(self):
        # CSV de exemplo para testar a função
        self.csv_data = """code,name,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec
                           BRA,Brazil,200,180,150,120,90,60,40,80,130,160,170,190
                           ARG,Argentina,100,120,140,160,180,200,220,190,170,150,130,110
                           USA,United States,300,310,320,330,340,350,360,370,380,390,400,410
                           CAN,Canada,150,160,170,180,190,200,210,220,230,240,250,260
                        """
        self.path_mock = StringIO(self.csv_data)

    def test_preprocessamento_producao(self):
        # Usando StringIO para simular a leitura de um arquivo Excel (o formato do exemplo foi adaptado)
        df_result = preprocessamento_producao(self.path_mock)

        # Verifica se as colunas estão corretas após o processamento
        expected_columns = ['ano', 'country_code', 'precipitação_anual']
        self.assertListEqual(list(df_result.columns), expected_columns)

        # Verifica se o número de linhas está correto
        self.assertEqual(len(df_result), 16)  # 4 países com dados para 12 meses

        # Verifica se os valores estão arredondados corretamente
        self.assertAlmostEqual(df_result['precipitação_anual'].iloc[0], 1940.00)

        # Verifica se a coluna de ano foi extraída corretamente
        self.assertTrue(df_result['ano'].str.isnumeric().all())

if __name__ == '__main__':
    unittest.main()