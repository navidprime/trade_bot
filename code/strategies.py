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

class BRIStrategy(Strategy):
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

class MAMStrategy(Strategy):
    def init(self, config):
        self.fastma = config["FastMA"]
        self.slowma = config["SlowMA"]
        self.adxline = config["ADXLine"]
    
    def call(self, indicators: list) -> int:
        fast = indicators[self.fastma]
        slow = indicators[self.slowma]
        adx = indicators["ADX"]
        momentum = indicators["Mom"]
        
        trendSatisfied = True if fast > slow else False
        momentumSatisfied = True if momentum > 0 else False
        adxSatisfied = True if adx > self.adxline else False
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\tadxSatisfied:{adxSatisfied},trendSatisfied:{trendSatisfied},momentumSatisfied:{momentumSatisfied}")
        
        action = 0
        if (adxSatisfied):
            if (trendSatisfied and momentumSatisfied):
                action = 1
            elif (not trendSatisfied and not momentumSatisfied):
                action = -1
        else:
            action = -1
        
        return action

class PoldStrategy(Strategy):
    def init(self, config):
        self.ma1 = config["FastMA"]
        self.ma2 = config["SlowMA"]
    
    def call(self, indicators: list) -> int:
        
        ma1 = indicators[self.ma1]
        ma2 = indicators[self.ma2]
        
        macdm = indicators["MACD.macd"]
        macds = indicators["MACD.signal"]
        
        sar = indicators["P.SAR"]
        close = indicators["close"]
        
        trendSatisfied = ma1 >= ma2
        macdSatisfied = macdm >= macds
        sarSatisfied = close >= sar
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\sarSatisfied:{sarSatisfied},trendSatisfied:{trendSatisfied},\n\
macdSatisfied:{macdSatisfied}")
        
        action = 0 
        if trendSatisfied:
            if macdSatisfied and sarSatisfied:
                action = 1
            elif not macdSatisfied and not sarSatisfied:
                action = -1
        else:
            action = -1
        
        return action

class PoldV2Strategy(Strategy):
    def init(self, config):
        self.ma1 = config["FastMA"]
        self.ma2 = config["SlowMA"]
        self.ma = config["MiddleMA"]
    
    def call(self, indicators: list) -> int:
        
        ma1 = indicators[self.ma1]
        ma2 = indicators[self.ma2]
        
        macdm = indicators["MACD.macd"]
        macds = indicators["MACD.signal"]
        
        ma = indicators[self.ma]
        close = indicators["close"]
        
        trendSatisfied = ma1 >= ma2
        maSatisfied = close >= ma
        macdSatisfied = macdm >= macds
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\
\maSatisfied:{maSatisfied},trendSatisfied:{trendSatisfied},macdSatisfied:{macdSatisfied}")
        
        action = 0 
        if trendSatisfied and maSatisfied and macdSatisfied:
            action = 1
        else:
            action = -1
        
        return action

class AdvancedStrategy(Strategy):
    def init(self, config):
        self.ma1 = config["FastMA"]
        self.ma2 = config["SlowMA"]
        self.mas1 = config["ShortMA"]
        self.mas2 = config["LongMA"]
        
        self.rsi = config["RSI"]
        self.rsiBought = config["RSIOverBought"]
        self.rsiSold = config["RSIOverSold"]
    
    def call(self, indicators: list) -> int:
        
        ma1 = indicators[self.ma1]
        ma2 = indicators[self.ma2]
        
        mas1 = indicators[self.mas1]
        mas2 = indicators[self.mas2]
        
        rsi = indicators[self.rsi]
        
        trendSatisfied = ma1 >= ma2
        masSatisfied = mas1 >= mas2
        rsiBuySatisfied = rsi <= self.rsiSold
        rsiSellSatisfied = rsi >= self.rsiBought
        
        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\t\
trendSatisfied:{trendSatisfied},masSatisfied:{masSatisfied},\
\trsiBuySatisfied:{rsiBuySatisfied},rsiSellSatisfied:{rsiSellSatisfied}")
        
        action = 0 
        if trendSatisfied and masSatisfied and not rsiSellSatisfied:
            action = 1
        else:
            action = -1
        
        return action

class SarStrategy(Strategy):
    def init(self, config):
        self.ma1 = config["FastMA"]
        self.ma2 = config["SlowMA"]
    def call(self, indicators: list) -> int:
        
        fastm = indicators[self.ma1]
        slowm = indicators[self.ma2]

        sar = indicators["P.SAR"]
        close = indicators["close"]

        trendSatisfied = fastm >= slowm
        sarSatisfied = close >= sar

        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\t\
trendSatisfied:{trendSatisfied},sarSatisfied:{sarSatisfied}")
        
        action = 0
        if sarSatisfied and trendSatisfied:
            action = 1
        else:
            action = -1
        
        return action

class SarStochStrategy(Strategy):
    def init(self, config):
        self.ma1 = config["FastMA"]
        self.ma2 = config["SlowMA"]
    def call(self, indicators: list) -> int:
        
        fastm = indicators[self.ma1]
        slowm = indicators[self.ma2]

        sar = indicators["P.SAR"]
        close = indicators["close"]

        stochk = indicators["Stoch.K"]

        trendSatisfied = fastm >= slowm
        sarSatisfied = close >= sar
        stochkSatisfied = stochk >= 50

        utcTime = datetime.datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        
        loguru.logger.info(f"{utcTime} - criteria :\n\t\
trendSatisfied:{trendSatisfied},sarSatisfied:{sarSatisfied},stochkSatisfied:{stochkSatisfied}")
        
        action = 0
        if sarSatisfied:
            if stochkSatisfied and sarSatisfied:
                action = 1
            elif not stochkSatisfied and not sarSatisfied:
                action = -1
        else:
            action = -1
        
        return action