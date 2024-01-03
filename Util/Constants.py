import arcade

class Constants:

    def __init__(self):

        #Window Attributes
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 650
        self.SCREEN_TITLE = "Platformer"

        #Scaling
        self.TILE_SCALING = 1
        self.COIN_SCALING = 1
        self.SPRITE_PIXEL_SIZE = 128
        self.GRID_PIXEL_SIZE = self.SPRITE_PIXEL_SIZE * self.TILE_SCALING
        self.CHARACTER_SCALING = 1.5
        self.ENEMY_SCALING = 1

        #Magic Attack Constants
        self.SPELL_SCALING = 1
        self.SPELL_CAST_SPEED = 20
        self.SPELL_SPEED = 8
        self.SPELL_DAMAGE = 25

        #Physics Constants
        self.PLAYER_MOVEMENT_SPEED = 10
        self.GRAVITY = 0.7
        self.PLAYER_JUMP_SPEED = 14
        self.PLAYER_DOUBLE_JUMP_SPEED = 10

        #View Values
        self.LEFT_VIEWPORT_MARGIN = 200
        self.RIGHT_VIEWPORT_MARGIN = 200
        self.BOTTOM_VIEWPORT_MARGIN = 150
        self.TOP_VIEWPORT_MARGIN = 100

        #Constants used to track if the player is facing left or right
        self.RIGHT_FACING = 0
        self.LEFT_FACING = 1

        #Player Starting Pos
        self.PLAYER_START_X = 64
        self.PLAYER_START_Y = 225

        #Layer Names
        self.LAYER_NAME_PLATFORMS = "Platforms"
        self.LAYER_NAME_COINS = "Coins"
        self.LAYER_NAME_BACKGROUND = "Background"
        self.LAYER_NAME_PROPS = "Props"
        self.LAYER_NAME_PLAYER = "Player"
        self.LAYER_NAME_ENEMIES = "Enemies"
        self.LAYER_NAME_SPELLS = "Spells"
        self.LAYER_NAME_GOAL = "Goal"
        self.LAYER_NAME_GROUND = "Ground"
        self.LAYER_NAME_PORTALS = "Portals"

        #Full Screen Key
        self.FULL_SCREEN_KEY = arcade.key.F11

        #Invincibility Frames
        self.INVINCIBLE_TIME = 15
        self.MAX_LEVEL = 2
        self.MAX_WORLD = 1