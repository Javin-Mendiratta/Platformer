from Entities.Entity import Entity
from Util.Constants import Constants
import math
import arcade
import pathlib

const = Constants()
PATH_TO_SPRITE = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Sprites" / "Player"

def load_texture_pair(fileName): 
    return [
        arcade.load_texture(fileName),
        arcade.load_texture(fileName, flipped_horizontally = True)
    ]

class Player(Entity):
    def __init__(self):
        super().__init__("Player", runningFrames = 5, attackingFrames = 4)

        self.jumping = False
        self.ducking = False
        self.attacking = False
        self.attack_frame = 0
        self.isInvincible = False
        self.onMovingPlatform = False
        self.fall_timer = 0
        self.time_before_fall = 5

        self.hurt_set = []
        for i in range(2):
            self.hurt_set.append(load_texture_pair(PATH_TO_SPRITE / f"Hurt_{i+1}.png"))
        self.hurt_frame = 0

        self.idle_set = []
        for i in range(5):
            self.idle_set.append(load_texture_pair(PATH_TO_SPRITE / f"Idle{i+1}.png"))
        self.idle_frame = 0
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_direction == const.RIGHT_FACING:
            self.character_direction = const.LEFT_FACING
        elif self.change_x > 0 and self.character_direction == const.LEFT_FACING:
            self.character_direction = const.RIGHT_FACING

        if self.isInvincible:
            self.texture = self.hurt_set[self.hurt_frame][self.character_direction]
            self.hurt_frame += 1
            if self.hurt_frame == 2:
                self.hurt_frame = 0
            return

        if self.attacking:
            self.texture = self.attacking_set[math.floor(self.attack_frame)][self.character_direction]
            self.attack_frame += 0.25
            if self.attack_frame == 4:
                self.attack_frame = 0
                self.attacking = False
            return

        if self.change_y > 0:
            self.texture = self.jumping_pair[self.character_direction]
            return
        elif self.change_y < 0 and not self.onMovingPlatform:
            self.fall_timer += 1
            if self.fall_timer >= self.time_before_fall:
                self.texture = self.falling_pair[self.character_direction]
                return

        if self.change_y >= 0:
            self.fall_timer = 0

        if self.change_x == 0:
            if self.ducking:
                self.texture = self.ducking_pair[self.character_direction]
            else:
                self.texture = self.idle_set[math.floor(self.idle_frame)][self.character_direction]
                self.idle_frame += 0.1
                if self.idle_frame >= 4:
                    self.idle_frame = 0
            return
        else:
            self.cur_texture += 1
            if self.cur_texture > 4:
                self.cur_texture = 0
            self.texture = self.running_set[self.cur_texture][self.character_direction]
            return 