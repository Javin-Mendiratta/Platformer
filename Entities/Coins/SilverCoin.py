from Entities.Coins.Coin import Coin

class SilverCoin(Coin):
    def __init__(self, pointVal: int = 10):
        super().__init__("Silver", 5, pointVal = pointVal)