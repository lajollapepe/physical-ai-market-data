import os
from pathlib import Path
import databento as db
from dotenv import load_dotenv

load_dotenv()
client = db.Historical(os.environ["DATABENTO_API_KEY"])
Path("data").mkdir(exist_ok=True)

# --- 1. find the front month in the NG data we already have ---
ng = db.DBNStore.from_file("data/ng_mbp1.dbn.zst").to_df()

outrights = ng[~ng["symbol"].str.contains("-")]
front = outrights["symbol"].value_counts().index[0]

print("outright contracts:", outrights["symbol"].nunique())
print("front month:", front)
print("front month rows:", (ng["symbol"] == front).sum())

# --- 2. fetch NVDA ---
params = dict(
    dataset="XNAS.ITCH",
    symbols="NVDA",
    schema="mbp-1",
    start="2026-07-16T15:00",
    end="2026-07-16T15:10",
)

print("\nNVDA estimated cost:", client.metadata.get_cost(**params))

data = client.timeseries.get_range(**params)
data.to_file("data/nvda_mbp1.dbn.zst")

nvda = data.to_df()
print("NVDA rows:", len(nvda))