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

# macd and ma crossover based strategy:
# enter trade when:
#   - market is in a uptrend
#   - macd(or signal) is under zero line
#   - macd cross above the signal line
# exit trade when:
#   - macd crosses below signal line
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
        marketIsUptrend = maFast >= maSlow
        
        loguru.logger.info(f"---- Criteria -> marketIsUptrend:{marketIsUptrend},macdHigherSignal:{macdHigherSignal}")
        
        action = 0
        if marketIsUptrend:
            if macdHigherSignal:
                action = 1
            elif not macdHigherSignal:
                action = -1
        else:
            action = -1
        
        return action

# like MACDStrategy, but works with parabolic sar
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
        
        action = 0
        if marketIsUptrend:
            if sarSatisfied:
                action = 1
            elif not sarSatisfied:
                action = -1
        else:
            action = -1
        
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
        
        action = 0
        if marketIsUptrend:
            action = 1
        else:
            action = -1
        
        return action