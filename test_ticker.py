import os
import databento as db
from dotenv import load_dotenv

load_dotenv()
client = db.Historical(os.environ["DATABENTO_API_KEY"])

# ---- CHANGE ONLY THIS LINE ----
TICKER = "SERV"
# -------------------------------

params = dict(
    dataset="XNAS.ITCH",
    symbols=TICKER,
    schema="mbp-1",
    start="2026-07-16T15:00",
    end="2026-07-16T15:10",
)

print("testing:", TICKER)
print("cost:", client.metadata.get_cost(**params))

data = client.timeseries.get_range(**params)
df = data.to_df()
print("rows:", len(df))

if len(df) == 0:
    print("-> nothing came back. Not on Nasdaq, or wrong ticker.")
elif len(df) < 5000:
    print("-> THIN. Good candidate.")
elif len(df) < 30000:
    print("-> moderate. Usable.")
else:
    print("-> too liquid. Try a smaller company.")

if len(df) > 0:
    path = "data/" + TICKER.lower() + "_mbp1.dbn.zst"
    data.to_file(path)
    print("saved to", path)