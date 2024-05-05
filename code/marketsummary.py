from functions import *
from tradingview_ta import *

setting = ReadSetting()

timeframe = setting["interval"]
exchange = setting["exchange"]
symbolList = setting["symbolList"]

analysis = get_multiple_analysis("CRYPTO", timeframe, symbolList, ["ROC", "average_volume_10d_calc"])

symbol_perf = {}
for symbol,ana in analysis.items():
    maRec = ana.indicators["Recommend.MA"]
    oscRec = ana.indicators["Recommend.Other"]
    sumRec = ana.indicators["Recommend.All"]
    symbol_perf[symbol] = (oscRec,maRec,sumRec, ana.indicators["ROC"],ana.indicators["average_volume_10d_calc"]*ana.indicators["close"])

sorted_sp = dict(
    sorted(symbol_perf.items(),
           key=lambda item:item[1][2])
)
print(f"{"SYMBOL":<30} {"OSCILLATORS":<20} {"MA":<20} {"SUMMARY":<20} {"ROC(9)":<20} {"Vol10d*Close":<20}")
for symbol, recs in sorted_sp.items():
    print(f"{symbol:<30} {round(recs[0],2):<20} {round(recs[1],2):<20} {round(recs[2],2):<20} {round(recs[3],2):<20} {round(recs[4],2):<20}")