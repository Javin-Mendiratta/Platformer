import arcade
import arcade.gui
from Util.Constants import Constants
from Util.Sounds import Sounds

const = Constants()
sounds = Sounds()

class PauseScreen(arcade.View):
       
    def __init__(self, currentGame):

        super().__init__()
        self.current_game_view = currentGame

        self.pause_count = self.current_game_view.pause_count
        self.world = self.current_game_view.world
        self.level = self.current_game_view.level

        self.image = self.current_game_view.image
        self.background = None

        self.text_timer = 0
        self.text_wait = 50
        self.show_text = True
        self.text = arcade.Text(
            "Press ESCAPE To Resume",
            self.window.width / 2,
            self.window.height * (10/21),
            arcade.color.BLACK,
            self.window.width / 25,
            font_name = "Kenney Pixel Square",
            anchor_x = "center"
        )


    def on_show_view(self):
        arcade.set_background_color(arcade.color.AERO_BLUE)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if(self.window.current_view == self):
                arcade.play_sound(sounds.UNPAUSE_SOUND)
                arcade.pause(0.15)
                self.clear()
                self.window.show_view(self.current_game_view)

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, arcade.Texture(f"Background{self.world}{self.level}{self.pause_count}", self.image), alpha = 150)

        if self.show_text:
            self.text.draw()

        arcade.draw_text(
            "Paused",
            self.window.width / 2,
            self.window.height * 10.5 / 12,
            arcade.color.BLACK,
            self.window.width / 30,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            bold = True
        )

    def on_update(self, delta_time: float):
        arcade.Texture(f"Background{self.pause_count}", self.image)
        self.text_timer += 1
        if self.text_timer == self.text_wait:
            self.show_text = not self.show_text
            self.text_timer = 0