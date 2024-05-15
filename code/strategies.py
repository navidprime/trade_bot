import loguru,random

# base strategy class
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
        self.maFast = config["FastMA"]
        self.maSlow = config["SlowMA"]
    def call(self, indicators: list) -> int:
        macdM = indicators["MACD.macd"]
        macdS = indicators["MACD.signal"]
        
        maFast = indicators[self.maFast]
        maSlow = indicators[self.maSlow]
        
        macdHigherSignal = macdM >= macdS
        marketIsUptrend = maFast >= maSlow # use same ma for not using ema crosses
        
        loguru.logger.info(f"---- Criteria -> marketIsUptrend:{marketIsUptrend},macdHigherSignal:{macdHigherSignal}")
        
        action = -1
        if (marketIsUptrend and macdHigherSignal):
            action = 1
        
        return action

class SARStrategy(Strategy):
    def init(self, config):
        self.maFast = config["FastMA"]
        self.maSlow = config["SlowMA"]

    def call(self, indicators: list) -> int:
        maFast = indicators[self.maFast]
        maSlow = indicators[self.maSlow]
        
        sar = indicators["P.SAR"]
        close = indicators["close"]

        sarSatisfied = close >= sar
        marketIsUptrend = maFast >= maSlow
        
        loguru.logger.info(f"---- Criteria -> marketIsUptrend:{marketIsUptrend},sarSatisfied:{sarSatisfied}")
        
        action = -1
        if (marketIsUptrend and sarSatisfied):
            action = 1
        
        return action

class MAStrategy(Strategy):
    def init(self, config):
        self.maFast = config["FastMA"]
        self.maSlow = config["SlowMA"]

    def call(self, indicators: list) -> int:
        maFast = indicators[self.maFast]
        maSlow = indicators[self.maSlow]
        
        marketIsUptrend = maFast >= maSlow
        
        loguru.logger.info(f"---- Criteria -> marketIsUptrend:{marketIsUptrend}")
        
        action = -1
        if marketIsUptrend:
            action = 1
        
        return action

class MSAStrategy(Strategy):
    def init(self, config):
        self.ma = config["SlowMA"]

    def call(self, indicators: list) -> int:
        ma = indicators[self.ma]
        close = indicators["close"]

        macdM = indicators["MACD.macd"]
        macdS = indicators["MACD.signal"]

        sar = indicators["P.SAR"]
        
        marketIsUptrend = close >= ma
        macdIsSatisfied = macdM >= macdS
        sarIsSatisfied = close >= sar 
        
        loguru.logger.info(f"---- Criteria -> marketIsUptrend:{marketIsUptrend},macdIsSatisfied:{macdIsSatisfied},sarIsSatisfied:{sarIsSatisfied}")
        
        action = -1
        if marketIsUptrend:
            if macdIsSatisfied and sarIsSatisfied:
                action = 1
            elif not macdIsSatisfied and not sarIsSatisfied:
                action = -1
        
        return action