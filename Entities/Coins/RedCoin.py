from Entities.Coins.Coin import Coin

class RedCoin(Coin):
    def __init__(self, pointVal: int = 50):
        super().__init__("Red", 5, pointVal = pointVal)