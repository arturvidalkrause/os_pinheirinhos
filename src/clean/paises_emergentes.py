import pandas as pd
import pyarrow
from pathlib import Path

# Criando o dataset a partir da imagem fornecida
data = {
    'country_code': ['África do Sul', 'Brasil', 'China', 'Filipinas', 'Índia', 'Indonésia', 'Malásia', 'México', 'Tailândia', 'Turquia'],
    'Habitantes': ['60,4 mi', '216,4 mi', '1.410,7 mi', '117,3 mi', '1.428,6 mi', '277,5 mi', '34,3 mi', '128,5 mi', '71,8 mi', '85,3 mi'],
    'Renda per capita': [6750, 9070, 13400, 4230, 2540, 4870, 11970, 12100, 7180, 11650],
    'Índice de Desenvolvimento Humano': [0.717, 0.760, 0.788, 0.710, 0.644, 0.713, 0.807, 0.781, 0.803, 0.855],
    'Índice de Ativos Humanos': [84.7, 93.6, 97.0, 84.1, 79.7, 84.3, 89.1, 92.9, 93.5, 97.0]
}

# Criar um DataFrame do pandas
df = pd.DataFrame(data)

# Certifique-se de que o diretório existe
output_dir = Path('C:/Users/guguo/OneDrive/Área de Trabalho/FGV/LP/trabalho_a1/os_pinheirinhos/data/limpos')
output_dir.mkdir(parents=True, exist_ok=True)

# Especificar o caminho completo do arquivo, incluindo o nome do arquivo Parquet
file_path = output_dir / 'paises_emergentes.parquet'

# Salvando o DataFrame como um arquivo Parquet
df.to_parquet(file_path, engine='pyarrow')

file_path
