from functions import *
from tradingview_ta import *

setting = ReadSetting()

timeout = setting["timeout"]
timeframe = setting["interval"]
exchange = setting["exchange"]
symbolList = setting["symbolList"]
propertyList = setting["propertyList"]

print("fetching analysis objects....")
while True:
    try:
        analysis = get_multiple_analysis("CRYPTO", timeframe, symbolList, propertyList,timeout)
        break;
    except Exception as e:
        print("error raised." + e)
print("received analysis objects.")

symbolPerf:dict[str, dict] = {}
for symbol,ana in analysis.items():
    symbolPerf[symbol] = dict()
    indicators = ana.indicators
    for property in propertyList:
        symbolPerf[symbol][property] = indicators[property]

sortedSymbolPerf = dict(
    sorted(symbolPerf.items(),
           key=lambda item:item[1][propertyList[0]]*-1)
)
for (coinName, properties) in sortedSymbolPerf.items():
    print(coinName)
    for (property, value) in properties.items():
        print(f"\t{property}:{value}")
