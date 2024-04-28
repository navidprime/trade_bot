from datetime import timezone
import loguru,random,datetime

class Strategy:
    def init(self, config):
        raise NotImplementedError()
    def call(self, indicators:list) -> int:
        raise NotImplementedError()

# example usage
class RandomStrategy(Strategy):
    def init(self, config):
        self.buyChance = config["buyChance"] # 0-1
    def call(self, indicators: list) -> int:
        print(f"rsi is {indicators['RSI']}")
        
        r = random.random()
        action = -1
        if (r < self.buyChance):
            action = 1
        return action

class MACDStrategy(Strategy):
    def init(self, config):
        self.ma = config["MA"]
    def call(self, indicators: list) -> int:
        macd_macd = indicators["MACD.macd"]
        macd_signal = indicators["MACD.signal"]
        ma = indicators[self.ma]
        close = indicators["close"]
        
        c1 = macd_macd <= 0 or macd_signal <= 0
        c2 = macd_macd-macd_signal >= 0
        c3 = close-ma >= 0
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria : {c1},{c2},{c3}")
        
        action = 0
        if c1 and c2 and c3:
            action = 1
        elif not c2 and not c3:
            action = -1
        
        return action

class TrendStrategy(Strategy):
    def init(self, config):
        self.adxLine = config["ADXLine"]
        self.ma = config["MA"]
    def call(self, indicators: list) -> int:
        adx = indicators["ADX"]
        
        macd_macd = indicators["MACD.macd"]
        macd_signal = indicators["MACD.signal"]
        
        sar = indicators["P.SAR"]
        
        ma = indicators[self.ma]
        
        close = indicators["close"]
        
        c1 = adx >= self.adxLine
        c2 = macd_macd >= macd_signal
        c3 = close >= sar
        c4 = close >= ma
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria : {c1},{c2},{c3},{c4}")
        
        action = 0
        if (c1):
            if (c2 and c3 and c4):
                action = 1
            elif (not c2 and not c3 and not c4):
                action = -1
        else:
            action = -1
        
        return action

class BBRSIStrategy(Strategy):
    def init(self, config):
        self.rsi = config["RSI"] # RSI7 or RSI (which is 14)
        self.rsi_overbought = config["RSIOverBought"]
        self.rsi_oversold = config["RSIOverSold"]
    
    def call(self, indicators: list) -> int:
        rsi = indicators[self.rsi]
        bbUpper = indicators["BB.upper"]
        bbLower = indicators["BB.lower"]
        close = indicators["close"]
        
        rsiOversold = rsi <= self.rsi_oversold
        rsiOverbought = rsi >= self.rsi_overbought
        
        bbOversold = close <= bbLower
        bbOverbought = close >= bbUpper
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria : rsiOversold:{rsiOversold},rsiOverbought:{rsiOverbought},\
            bbOversold:{bbOversold},bbOverbought:{bbOverbought}")
        
        action = 0
        if (rsiOverbought and bbOverbought):
            action = -1
        elif (rsiOversold and bbOversold):
            action = 1;
        
        return action