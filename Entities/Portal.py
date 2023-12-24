import arcade
import pathlib
import os.path
from Util.Constants import Constants

const = Constants()

#Path to Sprites
PATH_TO_PORTALS = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Sprites" / "Portal"

def load_texture_pair(fileName): 
    return [
        arcade.load_texture(fileName),
        arcade.load_texture(fileName, flipped_horizontally = True)
    ]

class Portal(arcade.Sprite):
    def __init__(self, scale: int = const.CHARACTER_SCALING, direction = const.LEFT_FACING, portal_type = "purple", id = None, pairedID = None):
        super().__init__()

        # Default to facing left
        self.direction = direction

        # Used for image sequences
        self.cur_texture = 0
        self.animation_timer = 0
        self.scale = scale
        self.can_teleport = False
        self.teleport_x = None
        self.teleport_y = None
        self.id = id
        self.paired_id = pairedID
        
        if portal_type == "green":
            self.can_teleport = True

        self.path_to_portal = PATH_TO_PORTALS / portal_type
        
        self.idle_set = []
        for i in range(8):
            self.idle_set.append(load_texture_pair(self.path_to_portal / f"Idle{i+1}.png"))

        # Load textures for walking
        '''self.running_set = []
        for i in range(runningFrames):
            self.running_set.append(load_texture_pair(main_path / f"Running{i+1}.png"))'''

        self.texture = self.idle_set[0][self.direction]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        self.animation_timer += 1
        if self.animation_timer >= 4:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.idle_set[self.cur_texture][self.direction]
            self.animation_timer = 0

