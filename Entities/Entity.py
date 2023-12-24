import arcade
import pathlib
import os.path
from Util.Constants import Constants

const = Constants()

#Path to Sprites
PATH_TO_SPRITES = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Sprites"

def load_texture_pair(fileName): 
    return [
        arcade.load_texture(fileName),
        arcade.load_texture(fileName, flipped_horizontally = True)
    ]

class Entity(arcade.Sprite):
    def __init__(self, name, runningFrames, attackingFrames = 0, scale: int = const.CHARACTER_SCALING):
        super().__init__()

        # Default to facing right
        self.character_direction = const.RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = scale

        main_path = PATH_TO_SPRITES / name

        self.idle_pair = load_texture_pair(main_path / "Idle.png")
        if os.path.isfile(main_path / "Jumping.png"):
            self.jumping_pair = load_texture_pair(main_path / "Jumping.png")
        if os.path.isfile(main_path / "Ducking.png"):
            self.ducking_pair = load_texture_pair(main_path / "Ducking.png")
        if os.path.isfile(main_path / "Falling.png"):
            self.falling_pair = load_texture_pair(main_path / "Falling.png")
        if os.path.isfile(main_path / "Hit.png"):
            self.hit_pair = load_texture_pair(main_path / "Hit.png")
        if os.path.isfile(main_path / "Attack.png"):
            self.attack_pair = load_texture_pair(main_path / "Attack.png")
        
        self.attacking_set = []
        if os.path.isfile(main_path / "Casting1.png"):
            for i in range(attackingFrames):
                self.attacking_set.append(load_texture_pair(main_path / f"Casting{i+1}.png"))

        # Load textures for walking
        self.running_set = []
        for i in range(runningFrames):
            self.running_set.append(load_texture_pair(main_path / f"Running{i+1}.png"))

        self.texture = self.idle_pair[0]
        self.hit_box = self.texture.hit_box_points

