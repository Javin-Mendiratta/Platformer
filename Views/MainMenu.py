import arcade
import arcade.gui
import pathlib
from Views.Settings import Settings
from Util.Constants import Constants
from Util.Sounds import Sounds

sounds = Sounds()
const = Constants()

path_to_background = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Images" / "MainMenu"

class MainMenu(arcade.View):
       
    def __init__(self, nextView, current_frame = 0, currentPlayer = None):

        super().__init__()
        self.next_view = nextView
        self.bgm = sounds.MENU_BGM
        self.player = currentPlayer

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.animation_timer = 0
        self.animation_wait = 3

        self.text_timer = 0
        self.text_wait = 50
        self.show_text = True

        self.max_frames = 148
        self.current_frame = current_frame

        self.text = arcade.Text(
            "Press ENTER To Start",
            self.window.width / 2,
            self.window.height * (10/21),
            arcade.color.WHEAT,
            self.window.width / 25,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            bold = True
        )

        self.credits_text = arcade.Text(
            "By: Javin Mendiratta",
            (self.window.width * (76.5 / 90)) + (self.window.height * (1/25)),
            self.window.height * (1/25),
            arcade.color.WHITE,
            self.window.width / 90,
            font_name = "Kenney Future",
            anchor_x = "center",
            bold = True
        )

        self.background = arcade.load_texture(path_to_background / f"Background-{self.current_frame}.png")
        self.button_style = self.create_button_style()

        self.add_menu_buttons(["Settings", "Quit"])

    def add_menu_buttons(self, textList):
        buttons = []        

        y_margin = self.window.height * (7/8)
        x_margin = (1/8 - 1/10) * self.window.height

        settings_button = arcade.gui.UIFlatButton(x = x_margin, y = y_margin, text = textList[0], width = self.window.width/5, height=self.window.height/10, style = self.button_style)

        @settings_button.event("on_click")
        def on_click_settings(event):
            if(self.window.current_view == self):
                self.window.show_view(Settings(self))
                
        buttons.append(settings_button)

        y_margin = self.window.height * (7/8)
        x_margin = self.window.width - ((1/8 - 1/10) * self.window.height + self.window.width/5)

        quit_button = arcade.gui.UIFlatButton(x = x_margin, y = y_margin, text = textList[1], width = self.window.width/5, height=self.window.height/10, style = self.button_style)

        @quit_button.event("on_click")
        def on_click_quit(event):
            if(self.window.current_view == self):
                arcade.exit()

        buttons.append(quit_button)

        for button in buttons:
            self.manager.add(
                button
            )

    def on_show_view(self):
        self.manager.enable()
        self.background = arcade.load_texture(path_to_background / f"Background-{self.current_frame}.png")
        arcade.set_background_color(arcade.color.WHITE)
        if not self.player:
            self.player = self.bgm.play(volume = 0.3, loop = True)

    def on_hide_view(self):
        self.manager.disable()
    
    def on_key_press(self, key, modifiers):
        if key == const.FULL_SCREEN_KEY:
            self.window.set_fullscreen(not self.window.fullscreen)
            newView = MainMenu(self.next_view, current_frame = self.current_frame, currentPlayer = self.player)
            self.window.show_view(newView)
        elif key == arcade.key.ENTER:
            if(self.window.current_view == self):
                self.bgm.stop(self.player)
                self.window.show_view(self.next_view)
            

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        if self.show_text:
            self.text.draw()
        self.credits_text.draw()

        arcade.draw_text(
            "Platformer",
            self.window.width / 2,
            self.window.height * 10.5 / 12,
            arcade.color.BLACK,
            self.window.width / 30,
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
                self.current_frame = 0
            self.background = arcade.load_texture(path_to_background / f"Background-{self.current_frame}.png")

        self.text_timer += 1
        if self.text_timer == self.text_wait:
            self.show_text = not self.show_text
            self.text_timer = 0

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
        