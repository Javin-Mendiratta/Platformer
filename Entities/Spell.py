import arcade
import pathlib
import os.path
from Util.Constants import Constants

const = Constants()

#Path to Sprites
PATH_TO_SPRITES = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Sprites" / "Player"

def load_texture_pair(fileName): 
    return [
        arcade.load_texture(fileName),
        arcade.load_texture(fileName, flipped_horizontally = True)
    ]

class Spell(arcade.Sprite):
    def __init__(self, direction: int):
        super().__init__()

        # Default to facing right
        self.character_direction = direction

        # Used for image sequences
        self.cur_texture = 0
        self.animation_timer = 0
        self.scale = const.SPELL_SCALING

        main_path = PATH_TO_SPRITES

        # Load textures for magic
        self.magic_set = []
        for i in range(4):
            self.magic_set.append(load_texture_pair(main_path / f"Magical_Orbs_Spell{i+1}.png"))

        self.texture = self.magic_set[self.cur_texture][self.character_direction]
        self.hit_box = self.texture.hit_box_points
        
    def update_animation(self, delta_time: float = 1 / 60):
        self.animation_timer += 1
        if self.animation_timer > 3:
            self.cur_texture += 1
            if self.cur_texture > 3:
                self.cur_texture = 0
            self.texture = self.magic_set[self.cur_texture][self.character_direction]
            self.animation_timer = 0

