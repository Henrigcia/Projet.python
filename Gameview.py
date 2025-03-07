import arcade
import os

PLAYER_MOVEMENT_SPEED = 8
PLAYER_GRAVITY = 1
PLAYER_JUMP_SPEED = 18

SYMBOLS = {

    "=": ":resources:images/tiles/grassMid.png",  # Wall
    "-": ":resources:/images/tiles/grassHalf_mid.png",  # Wall
    "x": ":resources:/images/tiles/boxCrate_double.png",  # Wall
    "*": ":resources:images/items/coinGold.png",  # Coin
    "o": ":resources:/images/enemies/slimeBlue.png",  # Monster (slime)
    "S": ":resources:/images/animated_characters/robot/robot_idle.png",  # Start
    "£": ":resources:/images/tiles/lava.png",  # No-go (lava)
}

class GameView(arcade.View):
    """Main in-game view."""
    physics_engine: arcade.PhysicsEnginePlatformer
    player_sprite: arcade.Sprite
    wall_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    blob_list: arcade.SpriteList[arcade.Sprite]
    lava_list: arcade.SpriteList[arcade.Sprite]
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    camera: arcade.camera.Camera2D
    sound : arcade.Sound
    sound_2 : arcade.Sound

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()
        self.right_pressed = False
        self.left_pressed = False
        self.sound=arcade.Sound(":resources:sounds/coin1.wav")
        self.sound_2=arcade.Sound(":resources:sounds/jump1.wav" )

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.DARK_RED
        
        # Setup our game
        self.setup()


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )
        self.physics_engine.disable_multi_jump()
        self.physics_engine.can_jump()
        self.camera = arcade.camera.Camera2D()

    def load_map(self, filename="maps/map1.txt"):
        """Charge la carte depuis un fichier texte et place les objets sur la scène."""
        
        # Vérifie si le fichier existe
        if not os.path.exists(filename):
            print(f"Erreur : Le fichier {filename} est introuvable !")
            return  

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        lines = lines[3:-1]

        lines.reverse()  # Reverse line order (Arcade places (0,0) at the bottom)

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):  # Reads through the caracters 
                if char in SYMBOLS:
                    TILE_SIZE = 64
                    texture = SYMBOLS[char]
                    sprite = arcade.Sprite(texture, scale=0.5)
                    sprite.center_x = col_index * TILE_SIZE + TILE_SIZE / 2
                    sprite.center_y = row_index * TILE_SIZE + TILE_SIZE / 2

                    if char == "S":  
                        self.player_sprite = sprite  # Spawnpoint  
                    elif char == "*":  
                        self.coin_list.append(sprite)  # add a coin
                    elif char == "o":  
                        self.blob_list.append(sprite)  # add a slime monster
                    elif char == "£":  
                        self.lava_list.append(sprite)  # add lava
                    else:  
                        self.wall_list.append(sprite)  # add a wall


                        
    def setup(self) -> None:   
        """Set up the game here."""
        
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.blob_list = arcade.SpriteList(use_spatial_hash=True)
        self.lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_sprite_list = arcade.SpriteList(use_spatial_hash=True)

        self.load_map("maps/map1.txt")
        
        self.player_sprite_list.append(self.player_sprite)








    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.lava_list.draw()
            self.blob_list.draw()
            self.coin_list.draw()
            self.player_sprite_list.draw()
            #some_sprite_list.draw_hit_boxes()

    def update_movement(self):
        speed =0
        if self.right_pressed and not self.left_pressed:
            speed = +PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            speed = -PLAYER_MOVEMENT_SPEED
        else: 
            speed = 0
        self.player_sprite.change_x = speed


    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                # start moving to the right
                self.right_pressed = True
            case arcade.key.LEFT:
                # start moving to the left
                self.left_pressed = True
            case arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                   
                    # jump by giving an initial vertical speed
                    arcade.play_sound(self.sound_2)
                
        self.update_movement() 
        """Movement update after pressing a key"""

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                self.right_pressed = False
            case arcade.key.LEFT:
                self.left_pressed = False
        self.update_movement()
            
    
    
            

            
            

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances"", or "ticks"."""
        
        self.physics_engine.update()
        self.camera.position = self.player_sprite.position

        coins_to_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_to_hit:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.sound)

