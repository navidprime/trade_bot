from strategies import *
from tradingview_ta import *
from datetime import timezone
import sys,json,datetime

def ReadSetting() -> dict:
    settingPath = sys.argv[1] # assuming it is running from interpreter
    
    with open(settingPath, "r") as f:
        content = json.load(f)
    
    return content

def ParseInterval(interval)-> float:
    if (interval=="1m"):
        return 60
    elif (interval == "5m"):
        return 5*60
    elif(interval=="15m"):
        return 15*60
    elif(interval=="1h"):
        return 60*60
    elif(interval=="4h"):
        return 4*60*60
    raise Exception()

def GetSleepTime(seconds:float) -> float:
    DELAY_SECONDS = 4
    while True:
        now_s = datetime.datetime.now(timezone.utc).timestamp()
        
        remaining = seconds-(now_s%seconds)
        remaining_delayed = remaining - DELAY_SECONDS
        if (remaining_delayed < 0):
            continue
        
        next_epoch = datetime.datetime.now() + datetime.timedelta(seconds=remaining_delayed)
        amount_seconds = (next_epoch-datetime.datetime.now()).total_seconds()
        return amount_seconds

def GetIndicators(taObject:TA_Handler) -> dict:
    return taObject.get_indicators()

def GetStrategy(strategyName:str, config:dict) -> Strategy:
    obj:Strategy = eval(strategyName+"()")
    obj.init(config)
    return obj
