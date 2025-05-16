from __future__ import annotations
import arcade
import os
import math
import arcade.camera.camera_2d
from monster import *

import yaml
from switch_gate import Switch, Gate

from PBlock import *
from ConnectedCells import *



PLAYER_MOVEMENT_SPEED = 5
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_SPEED = 12

CAMERA_PAN_SPEED = 0.5
GRID_PIXEL_SIZE = 90
TILE_SIZE = 64 


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
    "v": "assets/kenney-voxel-items-png/kenney-extended-enemies-png/bee_fly.png",   #Bat
    "E": ":resources:/images/tiles/signExit.png", #Exit
    "|": ":resources:/images/tiles/stoneCenter_rounded.png", #Gate
}

platform_chars = {"=","-","x","£","E","^"}
up_chars = {"↑"}
down_chars = {"↓"}
left_chars = {"←"}
right_chars = {"→"}

class GameView(arcade.View):                                                    # The main game class that ihertits View

    physics_engine: arcade.PhysicsEnginePlatformer
  
    wall_list : arcade.SpriteList[arcade.Sprite]
    lava_list: arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    monsters_list : arcade.SpriteList[Monster]                                  # List of monsters (blobs and bats)
    platforme_list : arcade.SpriteList[arcade.Sprite]
    gate_list : arcade.SpriteList[arcade.Sprite]
    open_gate_list : arcade.SpriteList[arcade.Sprite]
    switch_list: arcade.SpriteList[Switch]
    solid_list: arcade.SpriteList[arcade.Sprite]
    #new_switch_list: arcade.SpriteList[arcade.Sprite]
    sprite_switch: arcade.SpriteList[arcade.Sprite]
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
    switch: Switch
 

    next_map : str                                                              # Ref to the next level map
    sortie_list : arcade.SpriteList[arcade.Sprite]                               #Exit sign                                                       
    score : int
    tile_size: int = 64                                                                 #Variable for the score
   


                                                                #Variable for the score
   
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
        self.platforme_list = arcade.SpriteList(use_spatial_hash=True)
        self.gate_list = arcade.SpriteList(use_spatial_hash=True)
        self.open_gate_list = arcade.SpriteList(use_spatial_hash=True)
        #self.switch_list = arcade.SpriteList(use_spatial_hash=True)
        #self.new_switch_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprite_switch = arcade.SpriteList(use_spatial_hash=True)
        self.solid_list = arcade.SpriteList(use_spatial_hash=True)
        

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

        

        
    #def solid(self, gates:arcade.SpriteList)->None:
     #   self.solid_list = self.wall_list 
      #  for g in gates:
       #     self.solid_list.append(g)

    def load_level(self, filename):                             # This will initiate a new game level    

        self.monsters_list.clear()                              # Clears all sprites that will be loaded from the map
        self.wall_list.clear()
        self.lava_list.clear()
        self.sortie_list.clear()
        self.player_sprite_list.clear()
        self.platforme_list.clear()
        self.gate_list.clear()
        self.sprite_switch.clear()
      
 
        # Vérifie si le fichier existe
        if not os.path.exists(filename):
            print(f"Erreur : Le fichier {filename} est introuvable !")       # TO-DO: handle correctly if file doesn't exist
            return  

        s = ""
        
        with open(filename, "r", encoding="utf-8") as file:
            for line in file.readlines():
                s += line

        arr = s.split("---", 1)
        m = yaml.safe_load(arr[0])

        self.next_map = m["next-map"]
        
        lines = arr[1].splitlines()
        lines.reverse()

       
                                                                        # TO-DO: to handle incorrect files, e.g. no 3rd line, etc
        self.next_map = lines[2].split(":")[-1].strip()         # The 3rd line in the file will have the reference to the next level, e.g. "next-map: map2.txt"
                                            # Ignore first 3 lines and the very last one for the map
        lines.reverse()                                         # Reverse line order (Arcade places (0,0) at the bottom)
        map_height = len(lines)
        

        self.switch_list = Switch.load_switchgates(filename)

        self.load_switches()
            

        
        ps_dict = {}                                            # Here we initialize an empty dict which will contain the coordinates of the platform symbols
        up_dict = {}
        down_dict = {}
        left_dict = {}
        right_dict = {}

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):  # Reads through the caracters 

                x = col_index * self.tile_size
                y = (map_height - row_index - 1) * self.tile_size # Flip y axis  

                if char in SYMBOLS:

                    texture = SYMBOLS[char]
                    center_x = col_index * self.tile_size + self.tile_size / 2
                    center_y = row_index * self.tile_size + self.tile_size / 2
                    s = arcade.Sprite(texture, scale=0.5)
                    s.center_x = center_x
                    s.center_y = center_y

                    if char in platform_chars and row_index != 0:                       # Here it checks is a symbol that forms the platform
                        ps_dict[(col_index, row_index)] = s          # Here it stores it in a dict the sprite and its coordinates (x,y) as the dict key
                    
                    if char in up_chars:
                        up_dict[(col_index, row_index)] = char     
                    if char in down_chars:
                       down_dict[(col_index, row_index)] = char  
                    if char in left_chars:
                        left_dict[(col_index, row_index)] = char  
                    if char in right_chars:
                        right_dict[(col_index, row_index)] = char  

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
                        self.monsters_list.append(v)
                    
                    elif char == "£":                          # add Lava to lava list
                        self.lava_list.append(s) 
                    elif char == "E":
                        self.sortie_list.append(s)             # add Exit to the list
                    elif char == "|":
                        g_active = False
                        if "gates" in m:
                            for gate in m["gates"]:
                                if gate["x"] == col_index and gate["y"] == row_index:
                                    g_active = gate["state"] == "open"
                        if not g_active:
                            self.gate_list.append(s)
                        else:
                            print("default opened gate")
                            self.open_gate_list.append(s)
                    else:
                        self.wall_list.append(s)              
        
        # -----------------------------------------------------------------------------------
    

        #self.solid(self.gate_list)
        for gate in self.gate_list:
            gate.hit_box = arcade.hitbox.RotatableHitBox(
                 gate.texture.hit_box_points
            )
                        

        print("The dictoinary of platform sprites read from the file:")
        print(ps_dict)
        print("The dictoinary of parrows read from the file:")
        print(up_dict)

        blocks: list[list[tuple[int, int]]] = Platforms(set(ps_dict.keys())).get_islands()          # Convert the dict keys into the set of points (row, col) and detect the platforms

        for b in blocks:                        # For each of the "islands" of plaform-type blocks
            pb = PBlock(1, 1280)                # Create a new PBlock and TEMP make it to move across entire screen
            if blocks.index(b) == 2:                    # TEMP only take 3rd block
                for c in b:                         # For each cell in the "island"
                    s = ps_dict[c]                  # Get the corresponding srite from dictionary using the coordinates tuple
                    s.change_x = 1
                    pb.add_platform(s)              # Add the srite to PBlock
                    self.platforme_list.append(s)   # Add the srtite to the list of all plaform block sprites

        self.player_sprite_list.append(self.player_sprite)                      # Add player
        self.physics_engine = arcade.PhysicsEnginePlatformer(                   # Initialize physics
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY,
            platforms = self.platforme_list
        )
        self.physics_engine.disable_multi_jump()
        self.physics_engine.can_jump()
               
    def load_switches(self)->None:

        self.sprite_switch.clear()

        for a in self.switch_list:    
            a.appearance = Switch.switchdraw(a)
            a.appearance.center_x = a.x * self.tile_size + self.tile_size/2
            a.appearance.center_y =  a.y * self.tile_size + self.tile_size/1.9  #using 1.9 to correct positional error 
            self.sprite_switch.append(a.appearance)
        

           
       
            



        
        

    def on_draw(self) -> None:                                                  # Render the sreen
        self.clear()                                                            # always start with self.clear()
        with self.camera.activate():
            self.platforme_list.draw()
            self.sortie_list.draw()
            self.wall_list.draw()
            self.lava_list.draw()
            self.monsters_list.draw()
            self.coin_list.draw()
            self.player_sprite_list.draw()
            self.gate_list.draw()
            self.sprite_switch.draw()
           
                

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
                for a in self.switch_list:
                    if self.weapon_active and self.change_weapon and self.toggle(a, self.player_sword):
                        print("Doerane")
                        a.update()
                        self.load_switches()
                    
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
            if arcade.check_for_collision_with_list(arrow, self.sprite_switch):
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
        for a in self.switch_list:
            Switch.update(a)

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

        

        for a in self.arrow_list:                                                           
            for s in self.switch_list:
                if self.toggle(s, a):
                    s.update()
                    self.load_switches()
                    #if gate in self.gate_list:
                    #self.gate_list.remove(gate)
                    
                            




        
        

      
         
        
    #Switches!!

    
    def toggle(self, switch: Switch, player: arcade.Sprite)->bool:

        if switch.last_hit < 0.4:
            
            return False
        
        if switch.disabled:
           
            return False
        
        if arcade.check_for_collision(player, switch.appearance):
            switch.status = not switch.status
            switch.last_hit = 0
            if switch.status:
                self.switch_action_on(switch)
            else: 
                self.switch_action_off(switch)

            return True
        else: 
            return False 
        
    
    def switch_action_on(self, switch: Switch)->None:
        if switch.switch_on is None:
            return
        
        for i in switch.switch_on:

            if i.kind == Switch.Action.Kind.open_gate:
                gate = Gate(i.x,i.y,True)  
                self.action_open(gate)

            if i.kind == Switch.Action.Kind.close_gate:
                gate = Gate(i.x,i.y,False)
                self.action_close(gate)

            if i.kind == Switch.Action.Kind.disable:
                
                switch.disabled = True

    def switch_action_off(self, switch: Switch)->None:
        if switch.switch_off is None:
            return
        for j in switch.switch_off:
            if j.kind == Switch.Action.Kind.open_gate:
                gate = Gate(j.x,j.y,True)  
                self.action_open(gate)
            if j.kind == Switch.Action.Kind.close_gate:
                gate = Gate(j.x,j.y,False)
                self.action_close(gate)

            if j.kind == Switch.Action.Kind.disable:
               
               switch.disabled = True

   
    def action_open(self, gate: Gate)->None:
        for g in self.gate_list: 
            if gate.x == (g.center_x-32)/64 and gate.y == (g.center_y-32)/64 :  #Converts center x and y to x and y coordinates (center_x-tilesize/2)/tilesize where tilesize = 64
                self.open_gate_list.append(g)
                self.gate_list.remove(g)
               # self.solid(self.gate_list)
    
  
    def action_close(self, gate: Gate)->None:
        for g in self.open_gate_list:
            if gate.x == (g.center_x-32)/64 and gate.y == (g.center_y-32)/64 :
                self.gate_list.append(g)
                self.open_gate_list.remove(g)
               # self.solid(self.gate_list)
        
            

    
    
    
    





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