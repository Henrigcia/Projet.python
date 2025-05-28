import arcade 
import os
from GameView import *


# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 750
WINDOW_TITLE = "Platformer"



def main() -> None:
    """Main function."""

    # Create the (unique) Window, setup our GameView, and launch
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gv = GameOverView(f"Welcome to the {WINDOW_TITLE} Game", True)
    window.show_view(gv)
    arcade.run()

if __name__ == "__main__":
    main()
    
