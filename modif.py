import arcade
import os
import math
import arcade.camera.camera_2d
from monster import *





PLAYER_MOVEMENT_SPEED = 5
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_SPEED = 12

CAMERA_PAN_SPEED = 0.5
GRID_PIXEL_SIZE = 90



ARROW_GRAVITY = 10
ARROW_SPEED = 12

FIRST_MAP = "maps/map1.txt"                 # First level map file; the each next level is referenced in the map file itself

SYMBOLS = {

    "=": ":resources:images/tiles/grassMid.png",  # Wall
    "-": ":resources:/images/tiles/grassHalf_mid.png",  # Wall
    "x": ":resources:/images/tiles/boxCrate_double.png",  # Wall
    "*": ":resources:images/items/coinGold.png",  # Coin
    "o": ":resources:/images/enemies/slimeBlue.png",  # Monster (slime)
    "S": ":resources:/images/animated_characters/robot/robot_idle.png",  # Start
    "£": ":resources:/images/tiles/lava.png",  # No-go (lava)
    "v": "assets/kenney-voxel-items-png/kenney-extended-enemies-png/bat.png",   #Bat
    "E": ":resources:/images/tiles/signExit.png", #The sign exit
}



class GameView(arcade.View):                                                    # The main game class that ihertits View

    physics_engine: arcade.PhysicsEnginePlatformer
  
    wall_list : arcade.SpriteList[arcade.Sprite]
    lava_list: arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    monsters_list : arcade.SpriteList[Monster]                                  # List of monsters (blobs and bats)

    camera : arcade.camera.Camera2D
    sound : arcade.Sound
    sound_2 : arcade.Sound
    camera2 : arcade.camera.Camera2D                                            # Camera for coins


    player_sprite : arcade.Sprite                                               # Everything that relates to the player and weapons
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    player_sword: arcade.Sprite
   
    sword_list: arcade.SpriteList[arcade.Sprite]
    player_bow: arcade.Sprite
    
    bow_list: arcade.SpriteList[arcade.Sprite]
    arrow_list: arcade.SpriteList[arcade.Sprite]
    arrow: arcade.Sprite
    Vecteur: arcade.Vec3
    Vector_arrow: arcade.Vec2= arcade.Vec2(0,0)
    change_weapon: bool
    weapon_active: bool
    arrow_active: bool = False
    arrow_speed_vec : arcade.Vec2 = arcade.Vec2(0,0)

    next_map : str                                                              # Ref to the next level map
    sortie_list : arcade.SpriteList[arcade.Sprite]                               #Exit sign                                                       
    score : int                                                                 #Variable for the score
   


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

#        self.sortie = arcade.Sprite(":resources:/images/tiles/signExit.png") #Init. for the sign

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.LIGHT_BLUE
        
        self.setup()                                                                        # Setup our game for the first time

        self.load_level(FIRST_MAP)


        self.camera = arcade.camera.Camera2D()
        self.camera2 = arcade.camera.Camera2D()
        self.angle_degrees = 0.0
        
        max_x = GRID_PIXEL_SIZE * self.width 
        max_y = GRID_PIXEL_SIZE * self.height 




    def setup(self) -> None:
        
        self.player_sprite_list = arcade.SpriteList(use_spatial_hash=True)      # Create all lists
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)               
        self.lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.monsters_list = arcade.SpriteList(use_spatial_hash=True)
        self.sortie_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sword: arcade.Sprite = arcade.Sprite(                       # Setup sword
            "assets/kenney-voxel-items-png/sword_silver.png",
            scale=0.5 * 0.7
            )
        self.sword_list = arcade.SpriteList(use_spatial_hash=True)
        self.sword_list.append(self.player_sword)
        

        self.player_bow: arcade.Sprite = arcade.Sprite(                         # Setup bow
            "assets/kenney-voxel-items-png/bowArrow.png",
            scale=0.5 * 0.7
            )
        self.bow_list = arcade.SpriteList(use_spatial_hash=True)
        self.bow_list.append(self.player_bow)
        

        self.arrow_list=arcade.SpriteList(use_spatial_hash=True)
        

        self.change_weapon = True                                               # Setup weapons
        self.weapon_active = False
        self.Vecteur=arcade.Vec3(0,0)
        self.Vecteur_sword=arcade.Vec2(0,0)


    def load_level(self, filename):                             # This will initiate a new game level    

        self.monsters_list.clear()                              # Clears all sprites that will be loaded from the map
        self.wall_list.clear()
        self.lava_list.clear()
        self.sortie_list.clear()
        self.player_sprite_list.clear()
 
        # Vérifie si le fichier existe
        if not os.path.exists(filename):
            print(f"Erreur : Le fichier {filename} est introuvable !")       # TO-DO: handle correctly if file doesn't exixt
            return  

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
                                                                # TO-DO: to handle incorrect files, e.g. no 3rd line, etc

        self.next_map = lines[2].split(":")[-1].strip()         # The 3rd line in the file will have the reference to the next level, e.g. "next-map: map2.txt"

        lines = lines[4:-1]                                     # Ignore first 3 lines and the very last one for the map

        lines.reverse()                                         # Reverse line order (Arcade places (0,0) at the bottom)

        map_height = len(lines)
        tile_size = 64

        TILE_SIZE = 64 

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):  # Reads through the caracters 
                x = col_index * tile_size
                y = (map_height - row_index - 1) * tile_size # Flip y axis
                if char in SYMBOLS:

                    texture = SYMBOLS[char]
                    center_x = col_index * TILE_SIZE + TILE_SIZE / 2
                    center_y = row_index * TILE_SIZE + TILE_SIZE / 2
                    s = arcade.Sprite(texture, scale=0.5)
                    s.center_x = center_x
                    s.center_y = center_y

                    if char == "S":  
                        self.player_sprite = s                  # Spawnpoint  
                        self.start_x = x                        # Store start coordinates
                        self.start_y = y 

                    elif char == "*":  
                        self.coin_list.append(s)                # add a coin to coins list

                    elif char == "o":  
                        b = Blob(texture, scale=0.5)            # add Blob monster to monsters list
                        b.center_x = center_x
                        b.center_y = center_y
                        b.change_x = BLOB_MOVEMENT_SPEED        # Blob moves only horizonally
                        b.change_y = 0                     
                        self.monsters_list.append(b)

                    elif char == "v" :
                        v = Bat(texture, scale=0.5)            # add Bat monster to monsters list
                        v.center_x = center_x
                        v.center_y = center_y         
                        v.change_x = BAT_MOVEMENT_SPEED_X
                        v.change_y = BAT_MOVEMENT_SPEED_Y          
                        v.fix_center_x = center_x
                        v.fix_center_y = center_y
                        v.area_x = BAT_AREA_X
                        v.area_y = BAT_AREA_Y
                        v.frames = 0
                        # v.distort_movement(1)                   
                        self.monsters_list.append(v)
                    
                    elif char == "£":                          # add Lava to lava list
                        self.lava_list.append(s) 
                    elif char == "E":
                        self.sortie_list.append(s)             # add Exit to the list
                        
                    else:  
                        self.wall_list.append(s)               # add a wall to walls list

        self.player_sprite_list.append(self.player_sprite)                      # Add player
        self.physics_engine = arcade.PhysicsEnginePlatformer(                   # Initialize physics
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )
        self.physics_engine.disable_multi_jump()
        self.physics_engine.can_jump()
               


    def on_draw(self) -> None:                                                  # Render the sreen
        self.clear()                                                            # always start with self.clear()
        with self.camera.activate():

            self.sortie_list.draw()
            self.wall_list.draw()
            self.lava_list.draw()
            self.monsters_list.draw()
            self.coin_list.draw()
            self.player_sprite_list.draw()
            if self.weapon_active and self.change_weapon:   
                self.sword_list.draw()
                self.arrow_active = False
            if self.weapon_active and not self.change_weapon:
                self.bow_list.draw()
            if self.arrow_active: 
                self.arrow_list.draw()   
              
                
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

        arrow_tbd = arcade.Sprite(                              # Setup arrow to be drawn
            "assets/kenney-voxel-items-png/arrow.png",
            scale= 0.5 * 0.7
        )
        self.Vecteur = self.camera.unproject((x,y))
        self.angle = math.atan2((self.Vecteur[0]-self.player_sprite.center_x),(self.Vecteur[1]-self.player_sprite.center_y))
        self.angle_degrees = math.degrees(self.angle)
        self.Vecteur_sword=arcade.Vec2(self.Vecteur[0] - self.player_sprite.center_x,self.Vecteur[1] - self.player_sprite.center_y)      
        self.Vecteur_sword = self.Vecteur_sword.normalize()*16
        arrow_tbd.center_x = self.player_bow.center_x
        arrow_tbd.center_y = self.player_bow.center_y          
        self.Vector_arrow = self.Vecteur_sword.normalize()*ARROW_SPEED
        arrow_tbd.change_x = self.Vector_arrow.x
        arrow_tbd.change_y = self.Vector_arrow.y
        arrow_tbd.angle = self.player_bow.angle

        match button: 
            case arcade.MOUSE_BUTTON_LEFT:
                self.weapon_active = True
                if self.change_weapon == False:
                    self.arrow_list.append(arrow_tbd)
                    self.arrow_active = True
            case arcade.MOUSE_BUTTON_RIGHT:
                self.change_weapon = not self.change_weapon

                
       
                
         
           
            
    
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a key on the mouse"""

        match button: 
            case arcade.MOUSE_BUTTON_LEFT:
                self.weapon_active = False
            case arcade.MOUSE_BUTTON_RIGHT:
                self.mouse_press = False

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances"", or "ticks"."""

         # Monsters movement
        for m in self.monsters_list:  
            m.move_monster(self.wall_list)

        

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
           self.reset_game()

        # Check if exit the level            
        if arcade.check_for_collision_with_list(self.player_sprite, self.sortie_list):
            self.load_level(self.next_map)  
        
                                     
        for arrow in self.arrow_list:
            if arcade.check_for_collision_with_list(arrow, self.wall_list):
                arrow.remove_from_sprite_lists()
            

        #Check monsters hit
        hits = arcade.check_for_collision_with_list(self.player_sword, self.monsters_list)
        for h in hits:
            if self.weapon_active and self.change_weapon:
                h.kill_monster()

        if arcade.check_for_collision_with_list(self.player_sprite, self.monsters_list):
            self.reset_game()
        
        for a in self.arrow_list:                                                           # Monster killed by arrows
            hits = arcade.check_for_collision_with_list(a, self.monsters_list)
            for h in hits:
               if self.arrow_active:
                    h.kill_monster()
        
                    
        
        
            

            
            
                            
 
        # if arcade.check_for_collision_with_list(self.player_sword, self.blob_list) and self.sword_active:
        #     self.blob_list.remove(Blob)
        #     arcade.play_sound(self.sound_blob)
        
        # #Kills the bat
        # for bat in self.bat_list :
        #     if arcade.check_for_collision_with_list(self.player_sword, self.bat_list) and self.sword_active :
        #         bat.remove_from_sprite_lists()

        #         arcade.play_sound(self.sound_blob)


        # #Checks if the player hits the bat
        # if arcade.check_for_collision_with_list(self.player_sprite, self.bat_list):
        #     self.score = 0
        #     self.player_sprite.center_x = self.start_x  # Reset X
        #     self.player_sprite.center_y = self.start_y -150 # Reset Y
        #     arcade.play_sound(self.sound_gameover)
            

 
       
        #Sword
       
        self.pointx: float
        self.pointy: float
        self.pointx = self.player_sprite.center_x + self.Vecteur_sword[0]
        self.pointy = self.player_sprite.center_y + self.Vecteur_sword[1]  
        
        self.player_sword.angle = self.angle_degrees - 45         
        if self.angle_degrees>=0:
            self.player_sword.center_x = self.pointx + 15
            
        elif self.angle_degrees<0:
            self.player_sword.center_x = self.pointx -15
        self.player_sword.center_y = self.pointy -20

        #Bow

        self.player_bow.angle = self.angle_degrees - 45
       
        if self.angle_degrees>=0:
            self.player_bow.center_x = self.pointx + 15
            
        elif self.angle_degrees<0:
            self.player_bow.center_x = self.pointx -15
            
        self.player_bow.center_y = self.pointy -25

       
            

        #Arrow
        for arrow in self.arrow_list: 
            arrow.change_y -= ARROW_GRAVITY * delta_time
            
            arrow_speed_vec = arcade.Vec2(arrow.change_x, arrow.change_y)
            arrow_speed_vec = arrow_speed_vec.normalize()
            arrow.radians = math.atan2(arrow_speed_vec[0], arrow_speed_vec[1]) - math.pi/4

            arrow.update()
         
        


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
    
    def reset_game(self):                                                               # This method will end and reset the game to the starting position

        self.score = 0
        self.player_sprite.center_x = self.start_x                                      # Reset X
        self.player_sprite.center_y = self.start_y -150                                 # Reset Y
        arcade.play_sound(self.sound_gameover)