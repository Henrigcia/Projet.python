import arcade
import os
import math
import arcade.camera.camera_2d




PLAYER_MOVEMENT_SPEED = 8
PLAYER_GRAVITY = 1
PLAYER_JUMP_SPEED = 18
CAMERA_PAN_SPEED = 0.5
GRID_PIXEL_SIZE = 90
BLOB_MOVEMENT_SPEED = 1
BLOB_SIZE = 40
BAT_MOVEMENT_SPEED = 1
BAT_SIZE = 30


SYMBOLS = {

    "=": ":resources:images/tiles/grassMid.png",  # Wall
    "-": ":resources:/images/tiles/grassHalf_mid.png",  # Wall
    "x": ":resources:/images/tiles/boxCrate_double.png",  # Wall
    "*": ":resources:images/items/coinGold.png",  # Coin
    "o": ":resources:/images/enemies/slimeBlue.png",  # Monster (slime)
    "S": ":resources:/images/animated_characters/robot/robot_idle.png",  # Start
    "£": ":resources:/images/tiles/lava.png",  # No-go (lava)
    "v": "assets/kenney-voxel-items-png/kenney-extended-enemies-png/bat.png"   #Bat
}
  
class GameView(arcade.View):
    """Main in-game view."""
    physics_engine: arcade.PhysicsEnginePlatformer
    player_sprite : arcade.Sprite
    wall_list : arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    blob_list : arcade.SpriteList[arcade.Sprite]
    bat_list : arcade.SpriteList[arcade.Sprite]       #Sprite for the bat
    lava_list: arcade.SpriteList[arcade.Sprite]
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    camera : arcade.camera.Camera2D
    sound : arcade.Sound
    sound_2 : arcade.Sound
    camera2 : arcade.camera.Camera2D
    #Camera for coins
    player_sword: arcade.Sprite
    sword_active: bool
    sword_list: arcade.SpriteList[arcade.Sprite]
    Vecteur: arcade.Vec3
    sortie : arcade.Sprite
    next_map : str
    #Map
    score : int       
    #Variable for the score
    bat : arcade.Sprite
    #Variable for the bat


    

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()
        self.right_pressed = False
        self.left_pressed = False
        self.sound_coin = arcade.Sound(":resources:sounds/coin1.wav")
        self.sound_jump = arcade.Sound(":resources:sounds/jump1.wav" )
        self.sound_blob = arcade.Sound(":resources:/sounds/explosion1.wav")
        self.sound_gameover = arcade.Sound(":resources:/sounds/gameover5.wav")
        self.score = 0
        #Initialisation for the score
        #self.next_map = "gr"
        self.sortie = arcade.Sprite(":resources:/images/tiles/signExit.png") 

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.LIGHT_BLUE
        
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
        self.camera2 = arcade.camera.Camera2D()
        

        max_x = GRID_PIXEL_SIZE * self.width 
        max_y = GRID_PIXEL_SIZE * self.height 

        self.Vecteur=arcade.Vec3(0,0)

        

    def load_map(self, filename="maps/map1.txt"):
        self.wall_list.append(self.sortie)
        """Charge la carte depuis un fichier texte et place les objets sur la scène."""
        # Vérifie si le fichier existe
        if not os.path.exists(filename):
            print(f"Erreur : Le fichier {filename} est introuvable !")
            return  

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            


        #lines = lines[2:-1]

        #lmap = lines[0]
        # next-map: 
        #lmap.split(" ", 1)



        #lines = lines[2:]

        lines.reverse()  # Reverse line order (Arcade places (0,0) at the bottom)


        map_height = len(lines)
        tile_size = 64

        

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):  # Reads through the caracters 
                x = col_index * tile_size
                y = (map_height - row_index - 1) * tile_size # Flip y axis
                if char in SYMBOLS:
                    TILE_SIZE = 64
                    texture = SYMBOLS[char]
                    sprite = arcade.Sprite(texture, scale=0.5)
                    sprite.center_x = col_index * TILE_SIZE + TILE_SIZE / 2
                    sprite.center_y = row_index * TILE_SIZE + TILE_SIZE / 2

                    if char == "S":  
                        self.player_sprite = sprite  # Spawnpoint  
                        self.start_x = x  # Store start coordinates
                        self.start_y = y 
                    elif char == "v" :
                        self.bat_list.append(sprite)    #adds a bat 
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
        self.bat_list = arcade.SpriteList(use_spatial_hash=True)


        self.load_map("maps/map1.txt")
        
        self.player_sprite_list.append(self.player_sprite)

        blob : arcade.Sprite          #Get all blobs moving
        for blob in self.blob_list:         
            blob.change_x  = BLOB_MOVEMENT_SPEED

        self.player_sword: arcade.Sprite = arcade.Sprite(
            "assets/kenney-voxel-items-png/sword_silver.png",
            scale=0.5 * 0.7
            )
        
        self.sword_active = False
        self.sword_list = arcade.SpriteList(use_spatial_hash=True)
        self.sword_list.append(self.player_sword)

        bat : arcade.Sprite
        for bat in self.bat_list:
            bat.change_x = BAT_MOVEMENT_SPEED    #Makes the bat moove




    def on_draw(self) -> None:
        """Render the screen."""
        self.clear()                                    # always start with self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.lava_list.draw()
            self.blob_list.draw()
            self.coin_list.draw()
            self.player_sprite_list.draw()
            self.bat_list.draw()
            if self.sword_active:   
                self.sword_list.draw()
        with self.camera2.activate():
            text = arcade.Text(f" Score : {self.score}", 0 ,0, font_size = 25)     #Function for the score
        text.draw()


    def update_movement(self):
        speed = 0
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
                    arcade.play_sound(self.sound_jump)
                
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

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a key on the mouse"""
        self.Vecteur = self.camera.unproject((x,y))

        self.angle = math.atan2((self.Vecteur[0]-self.player_sprite.center_x),(self.Vecteur[1]-self.player_sprite.center_y))
        
        self.angle_degrees = math.degrees(self.angle)
        self.player_sword.angle = self.angle_degrees - 45

        match button: 
            case arcade.MOUSE_BUTTON_LEFT:
                self.sword_active = True
            case arcade.MOUSE_BUTTON_RIGHT:
                self.mouse_press = True 
    
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a key on the mouse"""

        match button: 
            case arcade.MOUSE_BUTTON_LEFT:
                self.sword_active = False
            case arcade.MOUSE_BUTTON_RIGHT:
                self.mouse_press = False

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances"", or "ticks"."""

        # Blobs movement
        for blob in self.blob_list:  
            blob.center_x += blob.change_x
            if blob.scale_x*blob.change_x > 0:
                blob.scale_x*= -1   
            if arcade.check_for_collision_with_list(blob, self.wall_list):  #Check if with the changes the blob touches the wall 
                blob.change_x = - blob.change_x   #Invert speed
                blob.scale_x *= -1                #Change looking direction   
            if blob.change_x > 0:             # Logic for Blobs stop right side
                blob.center_x += BLOB_SIZE      # Move temporarily 1 BLOB_SIZE RIGHT 
                blob.center_y -= 1              # and 1 pix down
                if not arcade.check_for_collision_with_list(blob, self.wall_list):  # Check if no longer supported by wall
                    blob.change_x = - blob.change_x   
                    blob.scale_x *=-1           
                blob.center_x -= BLOB_SIZE      # restore x
                blob.center_y += 1              # restore y
            elif blob.change_x < 0:          # Logic for Blobs stop left side
                blob.center_x -= BLOB_SIZE      # Move temporarily 1 BLOB_SIZE LEFT
                blob.center_y -= 1              # and 1 pix down
                if not arcade.check_for_collision_with_list(blob, self.wall_list):  # Check if no longer supported by wall
                    blob.change_x = - blob.change_x 
                    blob.scale_x *=-1                                              
                blob.center_x += BLOB_SIZE      # restore x
                blob.center_y += 1              # restore y
                #Bat mouvement
        for bat in self.bat_list:
            bat.center_x += bat.change_x  
            
            
                     
                
            

        
        


                
        #Player's movement
        self.physics_engine.update()

        self.pan_camera_to_player(CAMERA_PAN_SPEED)

        #Collect coin(s)
        coins_to_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_to_hit:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.sound_coin)
            self.score += 1

        
        #Check lavas hit
        if arcade.check_for_collision_with_list(self.player_sprite, self.lava_list):
            self.score = 0
            self.player_sprite.center_x = self.start_x  # Reset X
            self.player_sprite.center_y = self.start_y -150 # Reset Y
            arcade.play_sound(self.sound_gameover)
            
        
        #Check blobs hit
        if arcade.check_for_collision_with_list(self.player_sprite, self.blob_list):
            self.score = 0
            self.player_sprite.center_x = self.start_x  # Reset X
            self.player_sprite.center_y = self.start_y -150 # Reset Y
            arcade.play_sound(self.sound_gameover)

        if arcade.check_for_collision_with_list(self.player_sword, self.blob_list) and self.sword_active:
            self.blob_list.remove(blob)
            arcade.play_sound(self.sound_blob)
        #Kills the bat
        for bat in self.bat_list :
            if arcade.check_for_collision_with_list(self.player_sword, self.bat_list) and self.sword_active :
                bat.remove_from_sprite_lists()

                arcade.play_sound(self.sound_blob)


        #Checks if the player hits the bat
        if arcade.check_for_collision_with_list(self.player_sprite, self.bat_list):
            self.score = 0
            self.player_sprite.center_x = self.start_x  # Reset X
            self.player_sprite.center_y = self.start_y -150 # Reset Y
            arcade.play_sound(self.sound_gameover)
            

        
       
        #Sword
        Vecteur_sword=arcade.Vec2(self.Vecteur[0] - self.player_sprite.center_x,self.Vecteur[1] - self.player_sprite.center_y)
       
        Vecteur_sword = Vecteur_sword.normalize()*16
        self.pointx: float
        self.pointy: float
        self.pointx = self.player_sprite.center_x + Vecteur_sword[0]
        self.pointy = self.player_sprite.center_y + Vecteur_sword[1]           
        self.player_sword.center_x = self.pointx  
        self.player_sword.center_y = self.pointy -15

        #if arcade.check_for_collision_with_list(self.player_sprite, self.wall_list) :
            #self.load_map(self.next_map )

            

            
            
            

            
         
            



  
                

    def pan_camera_to_player(self, panning_fraction: float = 2.0):
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player_sprite.position,
            self.window.delta_time,
            panning_fraction,

            )
        #self.camera.position = arcade.camera.grips.constrain_xy(self.camera.view_data, self.camera_bounds)
