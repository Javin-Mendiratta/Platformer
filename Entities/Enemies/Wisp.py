from Entities.Enemies.Enemy import Enemy

class Wisp(Enemy):
    def __init__(self):
        super().__init__("Wisp", runningFrames = 6, scale = 1.2)
        self.health = 50
        self.max_health = 50
        self.isHit = False
        self.type = "Wisp"