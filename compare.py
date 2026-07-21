import databento as db
import pandas as pd

# contract multiplier: units represented by one contract/share
MULTIPLIER = {
    "NG Aug26": 10000,   # 1 Henry Hub contract = 10,000 MMBtu
    "NVDA": 1,
    "SERV": 1,
}

def load(path, symbol=None):
    df = db.DBNStore.from_file(path).to_df()
    if symbol:
        df = df[df["symbol"] == symbol]
    return df

def stats(df, name):
    bid, ask = df["bid_px_00"], df["ask_px_00"]
    ok = (bid > 0) & (ask > 0) & (ask > bid)

    if ok.sum() == 0:
        return {"instrument": name, "events": len(df), "note": "no valid quotes"}

    bid, ask = bid[ok], ask[ok]
    mid = (bid + ask) / 2
    spread = ask - bid
    m = MULTIPLIER[name]

    px = mid.median()
    bid_sz = df["bid_sz_00"][ok].median()
    ask_sz = df["ask_sz_00"][ok].median()

    return {
        "instrument": name,
        "events": len(df),
        "price": round(px, 2),
        "spread_bps": round(((spread / mid) * 10000).median(), 2),
        "bid_$": round(bid_sz * px * m),
        "ask_$": round(ask_sz * px * m),
    }

rows = [
    stats(load("data/ng_mbp1.dbn.zst", symbol="NGQ26"), "NG Aug26"),
    stats(load("data/nvda_mbp1.dbn.zst"), "NVDA"),
    stats(load("data/serv_mbp1.dbn.zst"), "SERV"),
]

table = pd.DataFrame(rows)
print()
print(table.to_string(index=False))
print()

table.to_csv("results_pass1.csv", index=False)
print("saved -> results_pass1.csv")