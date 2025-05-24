from __future__ import annotations
import arcade
import os
import sys
import math
import arcade.camera.camera_2d
from monster import *
import numpy

import yaml
from switch_gate import Switch, Gate
from portal import Portal

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

FIRST_MAP = "maps/map6.txt"                 # First level map file; the each next level is referenced in the map file itself

SYMBOLS = {

    "=": ":resources:images/tiles/grassMid.png",  # Wall
    "-": ":resources:/images/tiles/grassHalf_mid.png",  # Wall
    "x": ":resources:/images/tiles/boxCrate_double.png",  # Wall
    "*": ":resources:images/items/coinGold.png",  # Coin
    "o": ":resources:/images/enemies/slimePurple.png",  # Monster (slime)
    "S": "assets/Doeraene.png",  # Start
    "£": ":resources:/images/tiles/lava.png",  # No-go (lava)
    "v": "assets/kenney-voxel-items-png/kenney-extended-enemies-png/Bat.png",   #Bat
    "E": ":resources:/images/tiles/signExit.png", #Exit
    "|": ":resources:/images/tiles/stoneCenter_rounded.png", #Gate
    "P": "assets/purple-portal.png", #Portal
    #"^": ":resources:/images/tiles/leverLeft.png"     
}

platform_chars = {"=","-","x","£","E"}
up_chars = {"↑","U"}
down_chars = {"↓","D"}
left_chars = {"←","L"}
right_chars = {"→","R"}

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
    sprite_portal: arcade.SpriteList[arcade.Sprite]
    portals: arcade.SpriteList[arcade.Sprite]
    new_switch_list: arcade.SpriteList[arcade.Sprite]
    sprite_switch: arcade.SpriteList[arcade.Sprite]
    camera : arcade.camera.Camera2D
    sound : arcade.Sound
    sound_2 : arcade.Sound
    camera2 : arcade.camera.Camera2D                                            # Camera for coins


    player_sprite : arcade.Sprite                                               # Everything that relates to the player and weapons
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    player_sword: arcade.Sprite
    portal_list : list[Portal]
   
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
    connected_portal : arcade.Sprite
 

    next_map : str                                                              # Ref to the next level map
    sortie_list : arcade.SpriteList[arcade.Sprite]                               #Exit sign                                                       
    score : int
    flop: int
                                                                #Variable for the score
   


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
        self.flop = 0 

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
        self.switch_list = arcade.SpriteList(use_spatial_hash=True)
        self.new_switch_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprite_switch = arcade.SpriteList(use_spatial_hash=True)
        self.solid_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprite_portal = arcade.SpriteList(use_spatial_hash=True)
        self.portal_list = []
        self.portals = arcade.SpriteList(use_spatial_hash=True)
        
        

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
        
        self.i : float = 3.0
        self.arrow_list=arcade.SpriteList(use_spatial_hash=True)
        

        self.change_weapon = True                                               # Setup weapons
        self.weapon_active = False
        self.Vecteur=arcade.Vec3(0,0)
        self.Vecteur_sword=arcade.Vec2(0,0)
        self.connected_portal: arcade.Sprite = arcade.Sprite(
            "assets/purple-portal.png",
            scale = 0.4*0.2
        )
        

        
    def solid(self, gates:arcade.SpriteList)->None:
        self.solid_list = self.wall_list 
        for g in gates:
            self.solid_list.append(g)

    def load_level(self, filename):                             # This will initiate a new game level    

        self.monsters_list.clear()                              # Clears all sprites that will be loaded from the map
        self.wall_list.clear()
        self.lava_list.clear()
        self.sortie_list.clear()
        self.player_sprite_list.clear()
        self.platforme_list.clear()
        self.gate_list.clear()
        self.sprite_switch.clear()
        self.portals.clear()
        self.sprite_portal.clear()
        self.solid_list.clear()
        
      

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
       

       
                                                                        
        lines.reverse()                                         # Reverse line order (Arcade places (0,0) at the bottom)
        map_height = len(lines)
        

        self.switch_list = Switch.load_switchgates(filename)
        
        self.load_switches()

        for x in Switch.load_switchgates(filename):
            if x.switch_on:
                for i in x.switch_on:
                    if i.kind == Switch.Action.Kind.open_portal: 
                        p = Portal(0,0,0,0)
                        p.x = i.x
                        p.y = i.y
                        p.teleport_x = i.go_x
                        p.teleport_y = i.go_y
                        self.portal_list.append(p)
            if x.switch_off:
                for j in x.switch_off:
                    if j.kind == Switch.Action.Kind.open_portal:
                        p = Portal(0,0,0,0)
                        p.x = j.x
                        p.y = j.y
                        p.teleport_x = j.go_x
                        p.teleport_y = j.go_y
                        self.portal_list.append(p)
                

        

        ps_dict:    dict[tuple[int,int], arcade.Sprite] = {}    # Here we initialize an empty dict which will contain the coordinates of the platform symbols and coorspinding Sprite
        up_set:    set[tuple[int,int]] = set()                 # Here we will store the coordinates of each type of arrows 
        down_set:  set[tuple[int,int]] = set()
        left_set:  set[tuple[int,int]] = set()
        right_set: set[tuple[int,int]] = set()

        for row_index, line in enumerate(lines):                # Each line...
            for col_index, char in enumerate(line):             # ... read through each char 
                x = col_index * TILE_SIZE
                y = (map_height-row_index-1)*TILE_SIZE

                if char in up_chars:                             # Here we will add an arrow coordinates to the relevant set of arrows
                    up_set.add((col_index, row_index))
                if char in down_chars:
                    down_set.add((col_index, row_index)) 
                if char in left_chars:
                    left_set.add((col_index, row_index))
                if char in right_chars:
                    right_set.add((col_index, row_index))

                if char in SYMBOLS:                             # If any of the game symbols we will then create a new Sprite
                    texture = SYMBOLS[char]
                    center_x = self.coordinates_to_center_z(col_index)
                    center_y = self.coordinates_to_center_z(row_index)
                    s = arcade.Sprite(texture, scale=0.5)
                    s.center_x = center_x
                    s.center_y = center_y

                    if char in platform_chars and row_index != 0:    # Here it checks is a symbol that forms the platform and this is not the bottom line
                        ps_dict[(col_index, row_index)] = s          # Here it stores it in a dict the sprite and its coordinates (x,y) as the dict key
                    
                    if char == "S": 
                        
                        self.player_sprite = s
                        self.player_sprite.scale = 0.2 * 0.25
                                             # Spawnpoint  
                        self.start_x = s.center_x                   # Store start coordinates
                        self.start_y = s.center_y
                       

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

                    elif char == "P" :
                        s.scale = 0.4 * 0.2
                        self.sprite_portal.append(s) #add portal to portal list
                    
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
                            self.open_gate_list.append(s)

                    else :

                        self.wall_list.append(s)

                        
        
        
        # -----------------------------------------------------------------------------------
    

       
                        

        blocks: Platforms = Platforms(set(ps_dict.keys()))                 # Convert the dict keys into the set of points (x,y) and create Platforms object
        ups:    VSeries = VSeries(up_set)                                  # Create VSeries object for arrows up
        downs:  VSeries = VSeries(down_set)                                # Create VSeries object for arrows down
        lefts:  HSeries = HSeries(left_set)                                # Create HSeries object for arrows left
        rights: HSeries = HSeries(right_set)                               # Create HSeries object for arrows right

        blocks.build_islands()                                            # Build the list of the plaform blocks
        rights.build_islands()                                            # Build the list of the arrow-right series
        lefts.build_islands()                                             # Build the list of the arrow-left series
        ups.build_islands()                                               # Build the list of the arrow-up series
        downs.build_islands()                                             # Build the list of the arrow-down series

        for b in blocks.Islands:                                          # For each of the blocks

            if True:                                                      # TEMP only take 1st block: blocks.Islands.index(b) == 2:

                boundary_right: int = max([x for x,y in b])               # By default, the right boundary of a block is x of the rightmost cell
                boundary_left: int = min([x for x,y in b])                # By default, the left boundary of a block is x of the leftmost cell
                boundary_top: int = max([y for x,y in b])                 # By default, the top boundary of a block is y of the highest cell
                boundary_bottom: int = min([y for x,y in b])              # By default, the bottom boundary of a block is y of the lowest cell

                rights_no: int = 0                                        # Here we will track the number of attached arrows of each direction
                lefts_no: int = 0
                ups_no: int = 0                                        
                downs_no: int = 0

                for c in b:                                               # For each cell c in this block we will look for the attached arrows and update block boundaries if found

                    for a in rights.Islands:                              # Go through each arrow RIGHT 
                        if (c[0]+1, c[1]) in a:                            # If the cell to the right of c belongs to an arrow RIGHT...
                            boundary_right = max([x for x,y in a])           # ...update right boundary of the block to the x of the rightmost arrow cell
                            rights_no += 1                                   # increase attached arrows counter

                    for a in lefts.Islands:                               # Go through each arrow LEFT 
                        if (c[0]-1, c[1]) in a:                            # If the cell to the left of c belongs to an arrow LEFT...
                            boundary_left = min([x for x,y in a])            # ...update left boundary of the block to the x of the lefttmost arrow cell
                            lefts_no += 1                                    # increase attache arrows counter

                    for a in ups.Islands:                                 # Go through each arrow UP
                        if (c[0], c[1]+1) in a:                            # If the cell to the up of c belongs to an arrow UP...
                            boundary_top = max([y for x,y in a])            # ...update top boundary of the block to the y of the highest arrow cell
                            ups_no += 1                                    # increase attached arrows counter

                    for a in downs.Islands:                               # Go through each arrow DOWN 
                        if (c[0], c[1]-1) in a:                            # If the cell to the down of c belongs to an arrow DOWN...
                            boundary_bottom = min([y for x,y in a])          # ...update bottom boundary of the block to the y of the lowest arrow cell
                            downs_no += 1                                    # increase attached arrows counter

                if sum([rights_no, lefts_no, ups_no, downs_no]) != 0:      # If any movement at all is detected for this block...

                    if sum([rights_no, lefts_no]) != 0 and sum([ups_no, downs_no]) != 0:
                        self.fatal_error("Invalid map: plafform block cannot move both horizontally and vertically at the same time")
                    
                    if any([rights_no > 1, lefts_no > 1, ups_no > 1, downs_no > 1]):
                        self.fatal_error("Invalid map: plafform block cannot have more than one movemnent arrow attached")                    

                    if sum([rights_no, lefts_no]) != 0:                                # The block will move HORIZONTALLY
                        change_x: float = 1 if rights_no == 1 else -1 if lefts_no == 1 else 0           # ... set initial horizontal speed
                        pb: HBlock = HBlock(                                                          # Create a new HBlock object for this block with the screen movement boundaries
                            boundary_left * TILE_SIZE + TILE_SIZE/2, 
                            boundary_right * TILE_SIZE + TILE_SIZE/2)
                        for c in b:                                         # For each cell in this block...
                            s = ps_dict[c]                                  # ...get the corresponding sprite from dictionary using the tuple coordinates
                            s.change_x = change_x                           # Set initial horizontal speed
                            pb.add_platform(s)                              # Add the sprite to HBlock and recalculate individual boundaries for coherent movement
                            self.platforme_list.append(s)                   # Add the sprtite to the list of all platform block sprites for Arcade engine

                    if sum([ups_no, downs_no]) != 0:                                # The block will move VERTICALLY
                        change_y: float = 1 if ups_no == 1 else -1 if downs_no == 1 else 0           # ... set initial vertical speed
                        pb: VBlock = VBlock(                                                          # Create a new VBlock object for this block with the screen movement boundaries
                            boundary_bottom * TILE_SIZE + TILE_SIZE/2, 
                            boundary_top * TILE_SIZE + TILE_SIZE/2)
                        for c in b:                                         # For each cell in this block...
                            s = ps_dict[c]                                  # ...get the corresponding sprite from dictionary using the tuple coordinates
                            s.change_y = change_y                           # Set initial vertical speed
                            pb.add_platform(s)                              # Add the sprite to VBlock and recalculate individual boundaries for coherent movement
                            self.platforme_list.append(s)                   # Add the sprtite to the list of all platform block sprites for Arcade engine


        self.solid_list.extend(self.wall_list)
        for g in self.gate_list:
            self.solid_list.append(g)

        self.player_sprite_list.append(self.player_sprite)                      # Add player
        self.physics_engine = arcade.PhysicsEnginePlatformer(                   # Initialize physics
            self.player_sprite,
            walls=self.solid_list,
            gravity_constant=PLAYER_GRAVITY,
            platforms = self.platforme_list
        )
        self.physics_engine.disable_multi_jump()
        self.physics_engine.can_jump()
               
    def load_switches(self)->None:

        self.sprite_switch.clear()

        for a in self.switch_list:    
            a.appearance = Switch.switchdraw(a)
            a.appearance.center_x = self.coordinates_to_center_z(a.x)
            a.appearance.center_y = self.coordinates_to_center_z(a.y)  
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
            self.portals.draw()
           
                
           

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
        with self.camera2.activate():
            text2 = arcade.Text(f" Flops d'Emilie: {self.flop}", 0 ,64, font_size = 25)     #Function for the score
        text2.draw()


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
                    if self.weapon_active and self.toggle(a, self.player_sword):
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

        self.i += delta_time
        j=0
        if self.connected_portal in self.portals and self.i<2 and self.i>1:            
            for k in self.portal_list:
                if k.teleport_x == self.center_z_to_coordinates(self.connected_portal.center_x) and k.teleport_y == self.center_z_to_coordinates(self.connected_portal.center_y) and j==0:
                    print("step 1")
                    for s in self.sprite_portal:
                        if s.center_x == self.coordinates_to_center_z(k.x) and s.center_y == self.coordinates_to_center_z(k.y):
                            print("step 2")
                            print(f"{self.center_z_to_coordinates(s.center_x)},{self.center_z_to_coordinates(s.center_y)}")
                            self.portals.remove(s)
                            j += 1
                            
                
            self.portals.remove(self.connected_portal)
        
        

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
            self.player_sword.center_x = self.pointx + 20
            self.player_sword.center_y = self.pointy + 9
            
        elif self.angle_degrees<0:
            self.player_sword.center_x = self.pointx -20
        self.player_sword.center_y = self.pointy + 9
        

        for a in self.switch_list:
            Switch.update(a)
        
        #Bow

        self.player_bow.angle = self.angle_degrees - 45
       
        if self.angle_degrees>=0:
            self.player_bow.center_x = self.pointx + 18
            
        elif self.angle_degrees<0:
            self.player_bow.center_x = self.pointx -18
            
        self.player_bow.center_y = self.pointy +6

       
            

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
                    

        if self.player_sprite.center_y<-500:
            self.reset_game()
        
        for p in self.portals:
            if arcade.check_for_collision(self.player_sprite, p):
                for a in self.portal_list:
                    if (p.center_x-32)/64 == a.x and (p.center_y-32)/64 == a.y:
                        
                        self.player_sprite.center_x = self.coordinates_to_center_z(a.teleport_x)
                        self.player_sprite.center_y =self.coordinates_to_center_z(a.teleport_y)
                        self.i = 0

        if self.player_sprite.change_x * self.player_sprite.scale_x < 0 :
            self.player_sprite.scale_x *= -1
                   
                            




        
        

      
         
        
    #Switches
    
    
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

            if i.kind == Switch.Action.Kind.open_portal:
                portal = Portal(i.x,i.y,i.go_x,i.go_y)

                self.action_portal(portal)

                

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

            if j.kind == Switch.Action.Kind.open_portal:
                portal = Portal(j.x,j.y,j.go_x,j.go_y)
                
                self.action_portal(portal)

            if j.kind == Switch.Action.Kind.disable:
               
               switch.disabled = True

   
    def action_open(self, gate: Gate)->None:
        for g in self.gate_list: 
            if gate.x == self.center_z_to_coordinates(g.center_x) and gate.y == self.center_z_to_coordinates(g.center_y) :  #Converts center x and y to x and y coordinates (center_x-tilesize/2)/tilesize where tilesize = 64
                self.open_gate_list.append(g)
                self.gate_list.remove(g)
                self.solid_list.remove(g)
                
    
  
    def action_close(self, gate: Gate)->None:
        for g in self.open_gate_list:
            if gate.x == self.center_z_to_coordinates(g.center_x) and gate.y == self.center_z_to_coordinates(g.center_y) :
                self.gate_list.append(g)
                self.open_gate_list.remove(g)
                self.solid_list.append(g)
    
    def action_portal(self, portal: Portal)->None:
        connected: Portal
        for p in self.sprite_portal:
            if portal.x == self.center_z_to_coordinates(p.center_x) and portal.y == self.center_z_to_coordinates(p.center_y) :
                self.connected_portal.center_x = self.coordinates_to_center_z(portal.teleport_x) 
                self.connected_portal.center_y = self.coordinates_to_center_z(portal.teleport_y) 
                if self.connected_portal in self.portals or p in self.portals:
                    return
                else:
                    self.portals.append(self.connected_portal)
                    self.portals.append(p)

    @staticmethod
    def center_z_to_coordinates(z: float)->float:
        return (z-TILE_SIZE/2)/TILE_SIZE
    
    @staticmethod
    def coordinates_to_center_z(x: float)->float:
        return x*TILE_SIZE+TILE_SIZE/2
         

                
        
            

    
    
    
    



      
    
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
        self.flop += 1
        self.player_sprite.center_x = self.start_x                                      # Reset X
        self.player_sprite.center_y = self.start_y
        self.load_level(FIRST_MAP)                                  # Reset Y
        arcade.play_sound(self.sound_gameover)

    def fatal_error(self, error_message: str) -> None:
        print(f"ERROR: {error_message}")
        sys.exit(1) 
