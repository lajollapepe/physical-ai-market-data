import os
from pathlib import Path
import databento as db
from dotenv import load_dotenv

load_dotenv()
key = os.environ["DATABENTO_API_KEY"]
print("key loaded:", key[:6] + "..." + key[-4:])

client = db.Historical(key)
Path("data").mkdir(exist_ok=True)

params = dict(
    dataset="GLBX.MDP3",
    symbols="NG.FUT",
    stype_in="parent",
    schema="mbp-1",
    start="2026-07-16T15:00",
    end="2026-07-16T15:10",
)

print("estimated cost:", client.metadata.get_cost(**params))

data = client.timeseries.get_range(**params)
data.to_file("data/ng_mbp1.dbn.zst")

df = data.to_df()
print(df.head())
print("rows:", len(df))