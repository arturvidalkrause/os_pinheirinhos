import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression

# Adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DATA_SET_PIB

PATH_DATASET_PIB: Path = Path(DATA_SET_PIB)

df = pd.read_parquet(DATA_SET_PIB, engine="pyarrow")

df["pib_log"] = np.log(df["PIB"])

fig_pib = px.choropleth(df,
						locations= "country_code",
						color="pib_log",
						hover_name="pais",
						hover_data={"PIB": True, "country_code": False, "pib_log": False},
						range_color=[20, 30],
						animation_frame="ano"
						)

fig_pib.show()