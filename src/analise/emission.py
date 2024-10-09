import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_EMISSION


PATH_DATASET_EMISSION: Path = Path(DATA_SET_EMISSION)

df: pd.DataFrame = pd.read_csv(PATH_DATASET_EMISSION)

fig = px.choropleth(df, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])
fig.show()