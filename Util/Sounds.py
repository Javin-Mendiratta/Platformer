import arcade
import pathlib

PATH_TO_SOUND_EFFECTS = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Sounds" / "Sound Effects"
PATH_TO_SONGS = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Sounds" / "BGM"

class Sounds:
    
    def __init__(self):

        self.COIN_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Coin.wav")
        )
        self.PLAYER_JUMP_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Jump.wav")
        )
        self.GOAL_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Goal.wav")
        )
        self.SPELL_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Spell.wav")
        )
        self.HIT_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Hit.wav")
        )
        self.HURT_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Character_Hurt.mp3")
        )
        self.GAME_OVER_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Game_Over.mp3")
        )
        self.WISP_DEATH_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Wisp_Death.mp3")
        )
        self.PAUSE_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Pause.mp3")
        )
        self.UNPAUSE_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Unpause.mp3")
        )
        self.LEVEL_START_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Level_Start.wav")
        )
        self.TELEPORT_SOUND = arcade.load_sound(
            str(PATH_TO_SOUND_EFFECTS / "Teleport.mp3")
        )

        self.MENU_BGM = arcade.Sound(PATH_TO_SONGS / "MENU_BGM.mp3" )
        self.GAME_BGM = arcade.Sound(PATH_TO_SONGS / "GAME_BGM.mp3")
        self.WIN_BGM = arcade.Sound(PATH_TO_SONGS / "VICTORY_BGM.mp3")
        self.GAME_OVER_BGM = arcade.Sound(PATH_TO_SONGS / "GAMEOVER_BGM.mp3")