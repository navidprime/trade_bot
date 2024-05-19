import loguru,random

# base strategy class
class Strategy:
    def init(self, config):
        raise NotImplementedError()
    def call(self, indicators:list) -> int:
        raise NotImplementedError()

class RandomStrategy(Strategy):
    def init(self, config):
        self.buyChance = config["buyChance"] # 0-1
    def call(self, indicators: list) -> int:
        rsi = indicators["RSI"]
        r = random.random()

        action = -1
        if (r < self.buyChance):
            action = 1
        
        return action

# any indicator that gives signals based on comparsion(psar, ma cross, macd) can be used with this class.
class MAStrategy():
    def init(self, config):
        self.maFast = config["MA1"]
        self.maSlow = config["MA2"]

    def call(self, indicators: list) -> int:
        ma1 = indicators[self.maFast]
        ma2 = indicators[self.maSlow]
        
        signal = ma1 >= ma2
        
        loguru.logger.info(f"Criteria => signal:{signal}")
        
        action = -1
        if signal:
            action = 1
        
        return action