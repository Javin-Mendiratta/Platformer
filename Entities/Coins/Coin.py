import arcade
import pathlib
import os.path
from Util.Constants import Constants

const = Constants()

#Path to Sprites
PATH_TO_COINS = pathlib.Path(__file__).resolve().parent.parent.parent / "Assets" / "Images" / "Coin"

class Coin(arcade.Sprite):
    def __init__(self, name, frames, waitTime: int = 4, scale: int = const.COIN_SCALING, pointVal: int = 10):
        super().__init__()

        # Used for image sequences
        self.cur_texture = 0
        self.scale = scale
        self.frames = frames
        self.wait_time = waitTime
        self.point_val = pointVal
        self.current_wait = 0

        self.path = PATH_TO_COINS

        # Load textures for walking
        self.spinning_set = []
        for i in range(self.frames):
            self.spinning_set.append(arcade.load_texture(self.path / f"{name}{i+1}.png"))

        self.texture = self.spinning_set[0]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        self.current_wait += 1
        if self.current_wait == self.wait_time:
            self.cur_texture += 1
            if self.cur_texture == self.frames:
                self.cur_texture = 0
            self.current_wait = 0
        self.texture = self.spinning_set[self.cur_texture]