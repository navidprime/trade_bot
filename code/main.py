from functions import *
from coinex import CoinexClient
import loguru,time,traceback

loguru.logger.add("data/logs.log", format="{message}", level="INFO")

setting = ReadSetting()

exchange = CoinexClient(
    setting["accessID"],
    setting["secretKey"],
    setting["timeout"]
)

strategy:Strategy = GetStrategy(setting["strategy"],setting["strategySetting"])

taObject = TA_Handler(
    symbol=setting["symbol"],
    exchange=setting["exchange"],
    screener=setting["screener"],
    interval=setting["interval"],
    timeout=setting["timeout"]
)
interval = ParseInterval(setting["interval"])

MAXTRIES = 3
tries = 0
while tries < MAXTRIES:
    try:
        indicators = GetIndicators(taObject)
        
        action = strategy.call(indicators)
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        if action != 0:
            orderType = "buy" if action==1 else "sell"
            result = exchange.place_market_order2(type=orderType, 
                                                market=setting["symbol"],
                                                percentage=1
                                                )
            loguru.logger.info(f"{utcTime} - Action : {orderType}\n\tResult : "+result["message"])
        else:
            loguru.logger.info(f"{utcTime} - Action : neutral")
            
        t = GetSleepTime(interval)
        print(f"sleeping for {round(t/60,2)}m")
        time.sleep(t)
        
        tries = 0
    except Exception:
        loguru.logger.error(traceback.format_exc())
        tries += 1