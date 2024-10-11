import pandas as pd
import os

# Constructing a relative path based on the script's location
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'dados_sobre_estacoes_metereologicas.parquet')

# Loading the Parquet file into a pandas DataFrame
df = pd.read_parquet(file_path)

# Displaying the first few rows of the DataFrame
print(df.head())
