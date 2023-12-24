import arcade
import arcade.gui
import pathlib
from Util.Constants import Constants
from Util.Sounds import Sounds

const = Constants()
sounds = Sounds()

path_to_background = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Images" / "GameOver" 

class GameOverView(arcade.View):

    def __init__(self, menuView):

        super().__init__()
        self.menu_view = menuView
        self.animation_timer = 0
        self.animation_wait = 10
        self.max_frames = 4
        self.current_frame = 1

        self.bgm = sounds.GAME_OVER_BGM
        self.player = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = arcade.load_texture(path_to_background / f"Background{self.current_frame}.png")
        self.button_style = self.create_button_style()

        self.add_buttons(["Menu", "Quit"])

    def add_buttons(self, text):

        buttons = []

        menu_button = arcade.gui.UIFlatButton(
            x = self.window.width * 1/9,
            y = self.window.height * 1/4,
            text = text[0], 
            width = self.window.width / 3, 
            height = self.window.height / 6, 
            style = self.button_style
        )

        buttons.append(menu_button)

        quit_button = arcade.gui.UIFlatButton(
            x = self.window.width * 5/9,
            y = self.window.height * 1/4,
            text = text[1], 
            width = self.window.width / 3, 
            height = self.window.height / 6, 
            style = self.button_style
        )

        buttons.append(quit_button)

        @menu_button.event("on_click")
        def on_click_button(event):
            if(self.window.current_view == self):
                self.window.show_view(self.menu_view)

        @quit_button.event("on_click")
        def on_click_button(event):
            if(self.window.current_view == self):
                arcade.exit()

        for button in buttons:
            self.manager.add(button)
        

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.BLACK)
        if not self.player:
            self.player = self.bgm.play(volume = 0.7, loop = True)
    
    def on_hide_view(self):
        self.manager.disable()
        self.bgm.stop(self.player)

    def on_key_press(self, key, modifiers):
        if key == const.FULL_SCREEN_KEY:
            self.window.set_fullscreen(not self.window.fullscreen)
            newView = GameOverView(self.menu_view)
            self.window.show_view(newView)
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        arcade.draw_text(
            "GAME OVER",
            self.window.width / 2,
            self.window.height * 8 / 12,
            arcade.color.WHITE,
            self.window.width / 15,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            bold = True
        )
    
        self.manager.draw()

    def on_update(self, delta_time: float):
        self.animation_timer += 1
        if self.animation_timer == self.animation_wait:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame == self.max_frames:
                self.current_frame = 1
            self.background = arcade.load_texture(path_to_background / f"Background{self.current_frame}.png")

    def create_button_style(self):
        return {
        "font_name": "Kenney Blocks",
        "font_size": self.window.width / 50,
        "font_color": arcade.color.BLACK,
        "border_width": 3,
        "border_color": None,
        "bg_color": arcade.color.BABY_PINK,

        # used if button is pressed
        "bg_color_pressed": arcade.color.BLACK,
        "border_color_pressed": arcade.color.BLACK,  # also used when hovered
        "font_color_pressed": arcade.color.BABY_PINK,
    }