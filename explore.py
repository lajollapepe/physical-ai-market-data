import databento as db

data = db.DBNStore.from_file("data/ng_mbp1.dbn.zst")
df = data.to_df()

print("total rows:", len(df))
print("distinct symbols:", df["symbol"].nunique())
print()
print("busiest 15 symbols:")
print(df["symbol"].value_counts().head(15))