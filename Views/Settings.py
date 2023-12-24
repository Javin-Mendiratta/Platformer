import arcade
import arcade.gui
import pathlib
from Util.Constants import Constants

const = Constants()
path_to_background = pathlib.Path(__file__).resolve().parent.parent / "Assets" / "Images" / "MainMenu"

class Settings(arcade.View):
       
    def __init__(self, menuView):

        super().__init__()
        self.menu_view = menuView

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.animation_timer = 0
        self.animation_wait = 3
        self.max_frames = 148

        self.background = arcade.load_texture(path_to_background / f"Background-{self.menu_view.current_frame}.png")
        self.button_style = self.create_button_style()

        self.add_menu_buttons(["Back"])

    def add_menu_buttons(self, textList):

        y_margin = self.window.height * (7/8)
        x_margin = (1/8 - 1/10) * self.window.height
        back_button = arcade.gui.UIFlatButton(x = x_margin, y = y_margin, text = textList[0], width = self.window.width/5, height=self.window.height/10, style = self.button_style)
        
        @back_button.event("on_click")
        def on_click_back(event):
            if(self.window.current_view == self):
                self.window.show_view(self.menu_view)

        self.manager.add(
            back_button
        )

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.WHITE)
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_key_press(self, key, modifiers):
        if key == const.FULL_SCREEN_KEY:
            self.window.set_fullscreen(not self.window.fullscreen)
            newView = Settings(self.menu_view)
            self.window.show_view(newView)
            
    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        arcade.draw_text(
            "Settings",
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
            self.menu_view.current_frame += 1
            if self.menu_view.current_frame == self.max_frames:
                self.menu_view.current_frame = 0
            self.background = arcade.load_texture(path_to_background / f"Background-{self.menu_view.current_frame}.png")

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