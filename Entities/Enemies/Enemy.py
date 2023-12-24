from Entities.Entity import Entity
from Util.Constants import Constants

const = Constants()

class Enemy(Entity):
    def __init__(self, name, runningFrames, scale: int = const.ENEMY_SCALING):
        super().__init__(name, runningFrames, scale = scale)
        self.should_update_walk = 0
        self.health = 0
        self.isHit = False
        self.HitPlayer = False
        self.hit_timer = 0
        self.hit_player_timer = 0
        self.hit_max = 10

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_direction == const.LEFT_FACING:
            self.character_direction = const.RIGHT_FACING
        elif self.change_x > 0 and self.character_direction == const.RIGHT_FACING:
            self.character_direction = const.LEFT_FACING

        if self.HitPlayer:
            self.texture = self.attack_pair[self.character_direction]
            self.hit_player_timer += 1
            if self.hit_player_timer == self.hit_max:
                self.hit_player_timer = 0
                self.HitPlayer = False
            return

        if self.isHit:
            self.texture = self.hit_pair[self.character_direction]
            self.hit_timer += 1
            if self.hit_timer == self.hit_max:
                self.hit_timer = 0
                self.isHit = False
            return

        if self.change_x == 0:
            self.texture = self.idle_pair[self.character_direction]
            return

        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 5:
                self.cur_texture = 0
            self.texture = self.running_set[self.cur_texture][self.character_direction]
            self.should_update_walk = 0
            return
        
        self.should_update_walk +=1