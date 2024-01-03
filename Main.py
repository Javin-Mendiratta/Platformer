import arcade
import shelve
from Platformer import PreLevel
from Views.MainMenu import MainMenu
from Util.Constants import Constants

const = Constants()

def main():

    window = arcade.Window(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, const.SCREEN_TITLE)
    menu_view = MainMenu(PreLevel())
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()