import databento as db
import pandas as pd

MULT = {"NG": 10000, "NVDA": 1, "SERV": 1}

def load(path, symbol=None):
    df = db.DBNStore.from_file(path).to_df()
    if symbol:
        df = df[df["symbol"] == symbol]
    return df

def depth(df, name):
    m = MULT[name]
    row = {"instrument": name}
    total = 0
    for lvl in range(10):
        sz = df[f"bid_sz_0{lvl}"] if lvl < 10 else None
        px = df[f"bid_px_0{lvl}"]
        sz = df[f"bid_sz_0{lvl}"]
        notional = (sz * px * m)
        valid = px > 0
        med = notional[valid].median()
        total += med if med == med else 0
        if lvl in (0, 4, 9):
            row[f"L{lvl+1}_$"] = round(med) if med == med else 0
    row["bid_10lvl_$"] = round(total)
    return row

rows = [
    depth(load("data/ng_mbp10.dbn.zst", "NGQ26"), "NG"),
    depth(load("data/nvda_mbp10.dbn.zst"), "NVDA"),
    depth(load("data/serv_mbp10.dbn.zst"), "SERV"),
]

out = pd.DataFrame(rows)
print()
print(out.to_string(index=False))
print()
out.to_csv("results_pass2.csv", index=False)
print("saved -> results_pass2.csv")