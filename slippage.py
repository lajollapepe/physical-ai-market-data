import databento as db
import pandas as pd

MULT = {"NG": 10000, "NVDA": 1, "SERV": 1}

def load(path, symbol=None):
    df = db.DBNStore.from_file(path).to_df()
    if symbol:
        df = df[df["symbol"] == symbol]
    return df.iloc[len(df)//2]  # one representative snapshot mid-window

def walk(row, name, order_usd):
    m = MULT[name]
    best_ask = row["ask_px_00"]
    spent = filled_units = 0.0

    for lvl in range(10):
        px = row[f"ask_px_0{lvl}"]
        sz = row[f"ask_sz_0{lvl}"]
        if px <= 0 or sz <= 0:
            continue
        level_value = px * sz * m
        take = min(level_value, order_usd - spent)
        spent += take
        filled_units += take / (px * m)
        if spent >= order_usd:
            break

    if filled_units == 0:
        return {"instrument": name, "note": "no fill"}

    avg_px = spent / (filled_units * m)
    slip_bps = (avg_px - best_ask) / best_ask * 10000
    return {
        "instrument": name,
        "order_$": order_usd,
        "best_ask": round(best_ask, 2),
        "avg_fill": round(avg_px, 2),
        "slippage_bps": round(slip_bps, 2),
        "filled_pct": round(min(spent / order_usd * 100, 100)),
    }

ORDER = 100_000
rows = [
    walk(load("data/ng_mbp10.dbn.zst", "NGQ26"), "NG", ORDER),
    walk(load("data/nvda_mbp10.dbn.zst"), "NVDA", ORDER),
    walk(load("data/serv_mbp10.dbn.zst"), "SERV", ORDER),
]
print()
print(pd.DataFrame(rows).to_string(index=False))