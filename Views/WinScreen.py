import arcade
import arcade.gui
import pathlib
from Util.Constants import Constants
from Util.Sounds import Sounds

const = Constants()
sounds = Sounds()

class WinScreen(arcade.View):

    def __init__(self, menuView):

        super().__init__()
        self.menu_view = menuView

        self.bgm = sounds.WIN_BGM
        self.player = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        path_to_background = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Images" / "Victory" / "Background.webp"
        self.background = arcade.load_texture(path_to_background)
        self.button_style = self.create_button_style()

        self.add_buttons(["Menu", "Quit"])

    def add_buttons(self, text):

        buttons = []

        menu_button = arcade.gui.UIFlatButton(
            x = self.window.width * (1/9),
            y = self.window.height * 2 / 12,
            text = text[0], 
            width = self.window.width/3, 
            height=self.window.height/6, 
            style = self.button_style
        )

        buttons.append(menu_button)

        quit_button = arcade.gui.UIFlatButton(
            x = self.window.width * (5/9),
            y = self.window.height * 2 / 12,
            text = text[1], 
            width = self.window.width/3, 
            height=self.window.height/6, 
            style = self.button_style
        )

        buttons.append(quit_button)

        @menu_button.event("on_click")
        def on_click_button(event):
            self.window.show_view(self.menu_view)

        @quit_button.event("on_click")
        def on_click_button(event):
            arcade.exit()

        for button in buttons:
            self.manager.add(button)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.WHITE)
        if not self.player:
            self.player = self.bgm.play(volume = 0.7, loop = True)

    def on_hide_view(self):
        self.manager.disable()
        self.bgm.stop(self.player)

    def on_key_press(self, key, modifiers):
        if key == const.FULL_SCREEN_KEY:
            self.window.set_fullscreen(not self.window.fullscreen)
            newView = WinScreen(self.menu_view)
            self.window.show_view(newView)
        elif key == arcade.key.ENTER:
            if self.window.current_view == self:
                self.window.show_view(self.menu_view)
    
    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        arcade.draw_text(
            "You Win!",
            self.window.width / 2,
            self.window.height * 8 / 12,
            arcade.color.LIGHT_BLUE,
            self.window.width / 15,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            bold = True
        )

        self.manager.draw()
    
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