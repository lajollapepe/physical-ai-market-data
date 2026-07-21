\# Physical AI Market Data — Pass 1



A liquidity comparison across the physical AI supply chain, built with

\[Databento](https://databento.com) market data.



\## Thesis



Physical AI is a supply chain before it is a sector. A humanoid robot or an

autonomous delivery fleet is the visible end of a chain that begins with power

generation, runs through industrial metals and silicon, and terminates in

deployed hardware. Public markets price these layers in separate places —

energy futures, semiconductor equities, small-cap robotics names — so a trader

taking a view on physical AI is implicitly trading all three. This basket takes

one instrument from each layer: natural gas for the power, NVDA for the

compute, and SERV for a deployed robot fleet. The thesis explains why these

instruments were selected; everything below is about the data structure they

exhibit, not about whether the thesis is right.



\## Method



| | |

|---|---|

| Window | 2026-07-16, 15:00–15:10 UTC |

| Schema | `mbp-1` (top of book) |

| Datasets | `GLBX.MDP3` (CME Globex), `XNAS.ITCH` (Nasdaq) |

| Total data cost | \~$0.035 |



Natural gas was requested with parent symbology (`NG.FUT`), which returns every

outright contract month \*\*plus every calendar spread\*\*. Spreads were filtered

out and the front month identified as the most active remaining outright —

`NGQ26` (August 2026). Identifying it by activity rather than a hardcoded

expiry calendar means the script still works next month.



\## Results



| Instrument | Events | Price | Spread (bps) | Bid notional | Ask notional |

|---|---:|---:|---:|---:|---:|

| NG Aug26 | 16,628 | $2.83 | 3.53 | $311,355 | $367,965 |

| NVDA | 101,721 | $206.30 | 0.97 | $15,472 | $19,392 |

| SERV | 957 | $5.49 | 18.23 | $3,936 | $3,294 |



\## Findings



\### 1. Dollar spreads are meaningless across instruments



NVDA's spread is $0.020 and natural gas is $0.001 — twenty times tighter in

dollar terms. Normalized to basis points the ranking \*\*reverses\*\*: NVDA at

0.97 bps against NG's 3.53 bps, roughly 3.6× tighter.



Any cross-asset comparison that skips normalization reaches the wrong

conclusion.



\### 2. Raw size is not comparable either



One Henry Hub contract represents 10,000 MMBtu; one NVDA share represents one

share. Comparing a size of 11 against 75 is meaningless until both are

converted to notional — at which point natural gas shows roughly \*\*20× more

capital\*\* resting at the top of book.



\### 3. Natural gas trades at the minimum tick



NG's median spread of $0.001 is the contract's minimum price increment. The

spread cannot narrow further.



When price competition is exhausted, the only remaining edge is \*\*queue

position\*\* — visible only in MBO (L3) data. A concrete, data-derived reason to

move beyond top of book.



\### 4. Thin names need depth most, and cost least



SERV shows $3,936 at the top of book. A $50,000 order covers roughly 8% of the

displayed size, so the quoted price describes almost none of the trade.



| Instrument | Data cost | Top-of-book notional | Depth needed? |

|---|---:|---:|---|

| NG Aug26 | $0.0259 | $311,355 | Moderate |

| NVDA | $0.0091 | $15,472 | Moderate |

| SERV | $0.0001 | $3,936 | \*\*High\*\* |



Natural gas data costs roughly 300× more than SERV data, yet SERV is where

top-of-book is most misleading. \*\*The instruments that most require deeper

data are the cheapest ones to buy it for.\*\*



\## Schema selection



| If you need to... | Use | Why |

|---|---|---|

| Backtest a daily signal | `ohlcv-1d` | Bars are sufficient and cheapest |

| Measure quoted spread | `mbp-1` | Best bid/offer only |

| Size an order in a thin name | `mbp-10` | Top of book covers too little |

| Model queue position | `mbo` | Only L3 shows individual orders |



Information flows one way. MBO aggregates down into any of the others; OHLCV

cannot be expanded back up.



\## Limitations



`XNAS.ITCH` covers Nasdaq only. NVDA and SERV trade across roughly 15 US

venues, so these figures are one venue's view, not the consolidated market.



A single ten-minute window on one day. No claim is made about stability across

sessions.



Medians rather than means, since quote data contains outliers around auctions

and reprices.



\## Reproduce



```bash

python -m venv .venv

.venv\\Scripts\\Activate.ps1

pip install -U databento python-dotenv pandas



python fetch.py          # natural gas

python build.py          # front month + NVDA

python test\_ticker.py    # SERV

python compare.py        # results table

```



\## Roadmap



| Pass | Schema | Adds |

|---|---|---|

| 1 | `mbp-1` | Spread and top-of-book comparison ✅ |

| 2 | `mbp-10` | Depth — how much size sits behind the quote |

| 3 | `mbo` | Order-by-order — book reconstruction, queue position |



Same three instruments each pass. Only the resolution changes.

