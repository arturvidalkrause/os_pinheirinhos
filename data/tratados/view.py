import pandas as pd
import os

def load_parquet_file():
    """
    Loads a Parquet file into a pandas DataFrame.

    This function constructs a relative path to the Parquet file based on the location
    of the script and loads the file into a pandas DataFrame. It assumes the Parquet file
    is located in the same directory as the script.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the contents of the Parquet file.
    """
    # Constructing a relative path based on the script's location
    current_dir = os.path.dirname(__file__)  # Get the directory of the current script
    file_path = os.path.join(current_dir, 'dados_sobre_estacoes_metereologicas.parquet')  # Construct the relative path

    # Loading the Parquet file into a pandas DataFrame
    df = pd.read_parquet(file_path)

    return df


if __name__ == "__main__":
    # Load and display the first few rows of the Parquet file
    df = load_parquet_file()
    print(df.head())