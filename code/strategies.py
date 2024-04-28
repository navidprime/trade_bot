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
        
        macdOrSignalLowerThanZero = macd_macd <= 0 or macd_signal <= 0
        macdMacdHighThanSignal = macd_macd-macd_signal >= 0
        confirmUpTrend = close-ma >= 0
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\tmacdOrSignalLowerThanZero:{macdOrSignalLowerThanZero},macdMacdHighThanSignal:{macdMacdHighThanSignal}\n\
\tconfirmUpTrend:{confirmUpTrend}")
        
        action = 0
        if macdOrSignalLowerThanZero and macdMacdHighThanSignal and confirmUpTrend:
            action = 1
        elif not macdMacdHighThanSignal and not confirmUpTrend:
            action = -1
        
        return action

class TrendStrategy(Strategy):
    def init(self, config):
        self.adxLine = config["ADXLine"]
        self.ma = config["MA"]
        
        self.last_action = None
    def call(self, indicators: list) -> int:
        adx = indicators["ADX"]
        
        macd_macd = indicators["MACD.macd"]
        macd_signal = indicators["MACD.signal"]
        
        sar = indicators["P.SAR"]
        
        ma = indicators[self.ma]
        
        close = indicators["close"]
        
        adxSatisfied = adx >= self.adxLine
        macdIsBuy = macd_macd >= macd_signal
        sarSatisfied = close >= sar
        maSatisfied = close >= ma
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\tadxSatisfied:{adxSatisfied},macdIsBuy:{macdIsBuy},\n\
\tsarSatisfied:{sarSatisfied},maSatisfied:{maSatisfied}")
        
        action = 0
        if (adxSatisfied or self.last_action == 1):
            if (macdIsBuy and sarSatisfied and maSatisfied):
                action = 1
                self.last_action = 1
            elif (not macdIsBuy and not sarSatisfied and not maSatisfied):
                action = -1
                self.last_action = -1
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
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\trsiOversold:{rsiOversold},rsiOverbought:{rsiOverbought},\n\
\tbbOversold:{bbOversold},bbOverbought:{bbOverbought}")
        
        action = 0
        if (rsiOverbought and bbOverbought):
            action = -1
        elif (rsiOversold and bbOversold):
            action = 1;
        
        return action

class MAADXStrategy(Strategy):
    def init(self, config):
        self.maList = config["MAList"]
        self.adxline = config["ADXLine"]
    def call(self, indicators: list) -> int:
        raise NotImplementedError() # i am not sure about this strategy if works fine or not
        adx = indicators["ADX"]
        close = indicators["close"]
        
        maRating = 0
        for ma in self.maList:
            maRating += close - indicators[ma]
        
        adxSatisfied = adx >= self.adxline
        maSatisfied = maRating >= 0
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\tadxSatisfied:{adxSatisfied},maRating:{maRating}")
        
        action = 0
        if (adxSatisfied and maSatisfied):
            action = 1
        else:
            action = -1
        
        return action