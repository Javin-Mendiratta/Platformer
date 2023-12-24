from Entities.Coins.Coin import Coin

class GoldCoin(Coin):
    def __init__(self, pointVal: int = 25):
        super().__init__("Gold", 5, pointVal = pointVal)