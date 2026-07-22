import os
import databento as db
from dotenv import load_dotenv

load_dotenv()
client = db.Historical(os.environ["DATABENTO_API_KEY"])

jobs = [
    ("ng_mbp10",   "GLBX.MDP3", "NG.FUT", "parent"),
    ("nvda_mbp10", "XNAS.ITCH", "NVDA",   "raw_symbol"),
    ("serv_mbp10", "XNAS.ITCH", "SERV",   "raw_symbol"),
]

for name, dataset, symbols, stype in jobs:
    params = dict(
        dataset=dataset,
        symbols=symbols,
        stype_in=stype,
        schema="mbp-10",
        start="2026-07-16T15:00",
        end="2026-07-16T15:10",
    )
    cost = client.metadata.get_cost(**params)
    print(f"{name}: estimated ${cost:.4f}")

    data = client.timeseries.get_range(**params)
    data.to_file(f"data/{name}.dbn.zst")
    print(f"  saved data/{name}.dbn.zst")