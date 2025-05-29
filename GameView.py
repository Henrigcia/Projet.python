from __future__ import annotations
import arcade
import os
import sys
import math
import arcade.camera.camera_2d
from monster import *

import yaml
from switch_gate import Switch, Gate
from portal import Portal
from PBlock import *
from ConnectedCells import *
from typing import cast

PLAYER_MOVEMENT_SPEED = 5
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_SPEED = 12

CAMERA_PAN_SPEED = 0.5
GRID_PIXEL_SIZE = 90
TILE_SIZE = 64

ARROW_GRAVITY = 10
ARROW_SPEED = 12

MAX_DEATHS = 100                            # Maximal amount of deaths before game over 

FIRST_MAP = "maps/map1.txt"                 # First level map file; the each next level is referenced in the map file itself
GAME_COMPLETE = "end"

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
}

platform_chars = {"=","-","x","£","E"}                                          # Caracters that form the platform
up_chars = {"↑"}                                                                # Every possible arrow for the mouvement
down_chars = {"↓"}
left_chars = {"←"}
right_chars = {"→"}

class GameView(arcade.View):                                                    # The main game class that ihertits View

    physics_engine: arcade.PhysicsEnginePlatformer
  
    wall_list : arcade.SpriteList[arcade.Sprite]                                # The bloc of walls such as grass
    lava_list: arcade.SpriteList[arcade.Sprite]                                 # List of all the lava
    coin_list : arcade.SpriteList[arcade.Sprite]                                # List of coins
    monsters_list : arcade.SpriteList[Monster]                                  # List of monsters (blobs and bats)
    platforme_list : arcade.SpriteList[arcade.Sprite]                           # Platform list
    gate_list : arcade.SpriteList[arcade.Sprite]                                # List of gate
    open_gate_list : arcade.SpriteList[arcade.Sprite]                           # Only the opened invisible gates
    switch_list: list[Switch]                                                   # List of switches
    solid_list: arcade.SpriteList[arcade.Sprite]                                # List of solid blocks (walls + gates)
    sprite_portal: arcade.SpriteList[Portal]                                    # SpriteList of portals
    portals: arcade.SpriteList[arcade.Sprite]                                   # Spritelist of activated visible portals
    new_switch_list: arcade.SpriteList[arcade.Sprite]                           # List of switches
    sprite_switch: arcade.SpriteList[arcade.Sprite]                             # Spritelist of the switches
    portal_list : list[Portal]                                                  # List of portals for teleportation
    switch: Switch                                                              # Switch
    current_portal: Portal                                                      # Needed to check which portal you are going through

    camera : arcade.camera.Camera2D                                             # Creation of the camera
    sound : arcade.Sound                                                        # Sound 1
    sound_2 : arcade.Sound                                                      # Sound 2
    camera2 : arcade.camera.Camera2D                                            # Camera for score and number of deaths

    player_sprite : arcade.Sprite                                               # Everything that relates to the player and weapons
    player_sprite_list : arcade.SpriteList[arcade.Sprite]                       # List of the player sprite
    player_sword: arcade.Sprite                                                 # Weapon sword of the player
    sword_list: arcade.SpriteList[arcade.Sprite]                                # List of sword
    player_bow: arcade.Sprite                                                   # Second weapon bow of the player
    bow_list: arcade.SpriteList[arcade.Sprite]                                  # List of bow
    arrow: arcade.Sprite                                                        # Arrows 
    arrow_list: arcade.SpriteList[arcade.Sprite]                                # Arrows list

    Vecteur: arcade.Vec3                                                         # All the mathematical components
    Vector_arrow: arcade.Vec2= arcade.Vec2(0,0)
    change_weapon: bool                                                          
    weapon_active: bool
    arrow_active: bool = False
    arrow_speed_vec : arcade.Vec2 = arcade.Vec2(0,0)                             
    
    current_map : str                                                           # Current map file name
    next_map : str                                                              # Ref to the next level map
    score : int                                                                 # Variable for the score 
    pass_score : int                                                            # Score needed to pass Exit
    deaths: int                                                                 # Numbers of deaths   
    sortie_list : arcade.SpriteList[arcade.Sprite]                              # Exit sign                                                       

                                                                
    def __init__(self) -> None:
                                                                                
        super().__init__()                                                      # Magical incantion: initialize the Arcade view

        self.right_pressed = False
        self.left_pressed = False
        self.sound_coin = arcade.Sound(":resources:sounds/coin1.wav")            # Initialitze all the sounds used in the main game
        self.sound_jump = arcade.Sound(":resources:sounds/jump1.wav" )
        self.sound_blob = arcade.Sound(":resources:/sounds/explosion1.wav")
        self.sound_gameover = arcade.Sound("assets/Doeraene-game-over-sound.wav")   
        self.score = 0
        self.deaths = 0 

        self.background_color = arcade.csscolor.LIGHT_BLUE                           # Choose a nice comfy background color
        
        self.setup()                                                                 # Setup our game for the first time

        self.load_level(FIRST_MAP)                                                   # Loads the first file from its name

        self.camera = arcade.camera.Camera2D()                                       # Initialize the 2 camera used 
        self.camera2 = arcade.camera.Camera2D()
        self.angle_degrees = 0.0
    # Here we set up all our lists and the game --------------------------
    def setup(self) -> None:
        
        self.player_sprite_list = arcade.SpriteList(use_spatial_hash=True)      # Create all lists used for decoration and interaction in the main game
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)               
        self.lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.monsters_list = arcade.SpriteList(use_spatial_hash=True)
        self.sortie_list = arcade.SpriteList(use_spatial_hash=True)
        self.platforme_list = arcade.SpriteList(use_spatial_hash=True)
        self.gate_list = arcade.SpriteList(use_spatial_hash=True)
        self.open_gate_list = arcade.SpriteList(use_spatial_hash=True)

        self.new_switch_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprite_switch = arcade.SpriteList(use_spatial_hash=True)
        self.solid_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprite_portal = arcade.SpriteList(use_spatial_hash=True)
        self.portal_list = []
        self.portals = arcade.SpriteList(use_spatial_hash=True)
        self.current_portal = Portal(0,0,0,0)
        
        self.player_sword: arcade.Sprite = arcade.Sprite(                       # Setup sword
            "assets/kenney-voxel-items-png/sword_silver.png",
            scale=0.5 * 0.7
            )
        self.sword_list = arcade.SpriteList(use_spatial_hash=True)
        self.sword_list.append(self.player_sword)
        
        
        self.text_coins_true: bool = False
        self.j: float = 3
        self.player_bow: arcade.Sprite = arcade.Sprite(                         # Setup bow
            "assets/kenney-voxel-items-png/bowArrow.png",
            scale=0.5 * 0.7
            )
        self.bow_list = arcade.SpriteList(use_spatial_hash=True)
        self.bow_list.append(self.player_bow)
        
        self.i : float = 3.0
        self.arrow_list=arcade.SpriteList(use_spatial_hash=True)                # Setup the arrows
        

        self.change_weapon = True                                               # Setup weapons
        self.weapon_active = False
        self.Vecteur=arcade.Vec3(0,0)
        self.Vecteur_sword=arcade.Vec2(0,0)
     

    # Logic for solid gates -----------------------  
    def solid(self, gates:arcade.SpriteList) -> None:
        self.solid_list = self.wall_list 
        for g in gates:
            self.solid_list.append(g)
    # Loading level from the map -----------------
    def load_level(self, filename:str) -> None:                             # This will initiate a new game level    

        self.current_map = filename                                         # Note down map file 

        self.monsters_list.clear()                                          # Clears all sprites that will be loaded from the map
        self.wall_list.clear()
        self.lava_list.clear()
        self.coin_list.clear()                      
        self.sortie_list.clear()
        self.player_sprite_list.clear()
        self.platforme_list.clear()
        self.gate_list.clear()
        self.sprite_switch.clear()
        self.portals.clear()
        self.sprite_portal.clear()
        self.solid_list.clear()  
        self.pass_score = 0                                                 # Initialize the passe score for changing level and the normal score 
        self.score = 0

        if not os.path.exists(filename):
            self.fatal_error(f"The file {filename} not found")              # Handle the error when the file is missing
   
        st: str = ""
    
        with open(filename, "r", encoding="utf-8") as file:                 # Here we iterate over the lines in the file
            for line in file.readlines():
                st += line

        arr: list[str] = st.split("---", 1)                                 # It is used to split the line in two distinct object
        m = yaml.safe_load(arr[0])
        self.next_map = m["next-map"]

        lines: list[str] = arr[1].splitlines()
        lines.reverse()                                                     # Reverse line order (Arcade places (0,0) at the bottom)
        # Switches lecture and logic ----------------------
        self.switch_list = Switch.load_switchgates(filename)                # Loading the switches from the map 
        self.load_switches()

        for x in Switch.load_switchgates(filename):                         # TO comment correctly
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
        # sprites creation -------------------------------
        ps_dict:   dict[tuple[int,int], arcade.Sprite] = {}    # Here we initialize an empty dict which will contain the coordinates of the platform symbols and coorspinding Sprite
        up_set:    set[tuple[int,int]] = set()                 # Here we will store the coordinates of each type of arrows 
        down_set:  set[tuple[int,int]] = set()
        left_set:  set[tuple[int,int]] = set()
        right_set: set[tuple[int,int]] = set()

        for row_index, line in enumerate(lines):                # Each line...
            for col_index, char in enumerate(line):             # ... read through each char 

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
                        self.player_sprite.scale = (0.05, 0.05)     # Spawnpoint  
                        self.start_x = s.center_x                   # Store start coordinates
                        self.start_y = s.center_y
                       
                    elif char == "*":  
                        self.coin_list.append(s)                    # add a coin to coins list
                        self.pass_score += 1            

                    elif char == "o":  
                        mb = Blob(texture, scale=0.5)            # add Blob monster to monsters list
                        mb.center_x = center_x
                        mb.center_y = center_y
                        mb.change_x = BLOB_MOVEMENT_SPEED        # Blob moves only horizonally
                        mb.change_y = 0                     
                        self.monsters_list.append(mb)

                    elif char == "v" :
                        v = Bat(texture, scale=0.5)            # add Bat monster to monsters list
                        v.center_x = center_x
                        v.center_y = center_y         
                        v.change_x = BAT_MOVEMENT_SPEED_X      # Creates the y and x mouvement
                        v.change_y = BAT_MOVEMENT_SPEED_Y          
                        v.fix_center_x = center_x
                        v.fix_center_y = center_y
                        v.area_x = BAT_AREA_X                  # Creates the limit of the bat  
                        v.area_y = BAT_AREA_Y
                        v.frames = 0              
                        self.monsters_list.append(v)

                    elif char == "P" :
                        s.scale = (0.08, 0.08)
                        s.__class__ = Portal
                        self.sprite_portal.append(cast(Portal,s))            #add portal to portal list
                    
                    elif char == "£":                                         # add Lava to lava list
                        self.lava_list.append(s) 

                    elif char == "E":
                        self.sortie_list.append(s)                          # add Exit to the list
                    
                    elif char == "|":
                        g_active: bool = False
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

        # ----------------------------------------------------------------------------------- Platform Blocks ----------------------------------------------
   
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

            if True:                                                      

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
                        hb: HBlock = HBlock(                                                          # Create a new HBlock object for this block with the screen movement boundaries
                            boundary_left * TILE_SIZE + TILE_SIZE/2, 
                            boundary_right * TILE_SIZE + TILE_SIZE/2)
                        for c in b:                                         # For each cell in this block...
                            s = ps_dict[c]                                  # ...get the corresponding sprite from dictionary using the tuple coordinates
                            s.change_x = change_x                           # Set initial horizontal speed
                            hb.add_platform(s)                              # Add the sprite to HBlock and recalculate individual boundaries for coherent movement
                            self.platforme_list.append(s)                   # Add the sprtite to the list of all platform block sprites for Arcade engine
                            if s in self.wall_list:                         # Remove from the static walls list to avoid double update()
                                self.wall_list.remove(s)

                    if sum([ups_no, downs_no]) != 0:                                # The block will move VERTICALLY
                        change_y: float = 1 if ups_no == 1 else -1 if downs_no == 1 else 0           # ... set initial vertical speed
                        vb: VBlock = VBlock(                                                          # Create a new VBlock object for this block with the screen movement boundaries
                            boundary_bottom * TILE_SIZE + TILE_SIZE/2, 
                            boundary_top * TILE_SIZE + TILE_SIZE/2)
                        for c in b:                                         # For each cell in this block...
                            s = ps_dict[c]                                  # ...get the corresponding sprite from dictionary using the tuple coordinates
                            s.change_y = change_y                           # Set initial vertical speed
                            vb.add_platform(s)                              # Add the sprite to VBlock and recalculate individual boundaries for coherent movement
                            self.platforme_list.append(s)                   # Add the sprtite to the list of all platform block sprites for Arcade engine
                            if s in self.wall_list:                         # Remove from the static walls list to avoid double update()
                                self.wall_list.remove(s)
                               
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.solid_list.extend(self.wall_list)
        for g in self.gate_list:
            self.solid_list.append(g)

        self.text_coins = arcade.Text(f"Not enough coins to pass this level. You need: {self.pass_score-self.score} more coin(s)",self.window.width/2,self.window.height/4, font_size = 24, color=arcade.color.RED_DEVIL,font_name="arial", anchor_x="center",anchor_y="baseline")

        self.player_sprite_list.append(self.player_sprite)                      # Add player
        self.physics_engine = arcade.PhysicsEnginePlatformer(                   # Initialize physics
            self.player_sprite,
            walls = self.solid_list,
            gravity_constant=PLAYER_GRAVITY,
            platforms = self.platforme_list
        )
        self.physics_engine.disable_multi_jump()
        self.physics_engine.can_jump()
        
    # Logic for loading -----------           
    def load_switches(self) -> None:

        self.sprite_switch.clear()

        for a in self.switch_list:    
            a.appearance = Switch.switchdraw(a)
            a.appearance.center_x = self.coordinates_to_center_z(a.x)
            a.appearance.center_y = self.coordinates_to_center_z(a.y)  
            self.sprite_switch.append(a.appearance)
    
    # Draws all the sprite ------
    def on_draw(self) -> None:                                                  # Render the sreen
        self.clear()
                                                                    # always start with self.clear()
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

            if self.weapon_active and self.change_weapon:                       # Checks if the weapon is active then draw
                self.sword_list.draw()
                self.arrow_active = False
            if self.weapon_active and not self.change_weapon:
                self.bow_list.draw()
            if self.arrow_active: 
                self.arrow_list.draw()   

        if self.text_coins_true and self.j<2: 
            self.text_coins.draw()                    #Message when player tries to exit with not enough coins
             

        with self.camera2.activate():
            text = arcade.Text(f"Score: {self.score}/{self.pass_score}", 5 ,5, font_size = 16, color=arcade.color.DARK_BLUE_GRAY)     #Function for the score
        text.draw()

        if self.deaths >= 0:
            with self.camera2.activate():
                text2 = arcade.Text(f"Number of deaths: {self.deaths}", 5 ,30, font_size = 16, color=arcade.color.DARK_RED)     #Function for the deaths
            text2.draw()
    # Player's movement -------------
    def update_movement(self) -> None:
        speed = 0
        if self.right_pressed and not self.left_pressed:
            speed = +PLAYER_MOVEMENT_SPEED       
            
        elif self.left_pressed and not self.right_pressed:
            speed = -PLAYER_MOVEMENT_SPEED
        
        else: 
            speed = 0
        self.player_sprite.change_x = speed

    # Active when the key is pressed ------------------------
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:                                              # start moving to the right
                                                                               
                self.right_pressed = True
                
            case arcade.key.LEFT:                                               # start moving to the left
                                                                                
                self.left_pressed = True
                
            case arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                   
                                                                                
                    arcade.play_sound(self.sound_jump)                          # jump by giving an initial vertical speed
                 
        self.update_movement()                                                  # Updates the movement
        """Movement update after pressing a key"""
    # Active when the key is released ------------------------
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                self.right_pressed = False
            case arcade.key.LEFT:
                self.left_pressed = False
        self.update_movement()                                                  # Updates the movement
    # Same as before but with clicking ------------------------------------------
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
                        a.update()
                        self.load_switches()
                    
            case arcade.MOUSE_BUTTON_RIGHT:
                self.change_weapon = not self.change_weapon 
            
            
    # Same as before but with clicking --------------------------------------------
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a key on the mouse"""

        match button: 
            case arcade.MOUSE_BUTTON_LEFT:
                self.weapon_active = False
            case arcade.MOUSE_BUTTON_RIGHT:
                self.mouse_press = False

    def on_update(self, delta_time: float) -> None:

        # Monsters movement -----------------------------------
        for m in self.monsters_list:  
            m.move_monster(self.wall_list)

        
        #Portals dissapear after teleportaing (with delat time delay for visual purposes)
        self.i += delta_time
        if self.i<2 and self.i>1:
            for w in self.portals:
                print(hasattr(w, "connected"))
                if hasattr(w, "connected") and self.current_portal.x == self.center_z_to_coordinates(w.center_x) and self.current_portal.y == self.center_z_to_coordinates(w.center_y):
                    self.portals.remove(w)
                    self.portals.remove(w.connected)

        # Camera and physics update -----------------
        self.physics_engine.update()
        self.pan_camera_to_player(CAMERA_PAN_SPEED)

        # Collect coin(s) ------------------------------------
        coins_to_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)    # Checks the collision with coins
        for coin in coins_to_hit:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.sound_coin)
            self.score += 1                                                                        # Adds +1 to the score with new coin
        
        # Check lavas hit -------------------------------------
        rect2 = self.player_sprite.rect                                                     # Creates a rectangle around the player so that it can check the collisions with lava and exit
        rect2 = rect2.scale(1)                                                            # Custom size of the rectangle
        for p in self.lava_list:
            if rect2.overlaps(p.rect):                                                      # Checks the collision between the rectangle and the sprite 
                self.on_player_dead()

        # Check if Exit hit ---------------------------------- 
        self.j += delta_time
        for o in self.sortie_list:
            if arcade.check_for_collision(self.player_sprite, o) and self.score>=self.pass_score:
                if self.next_map == GAME_COMPLETE:
                    self.on_game_complete()                                                 # If game is over
                else:
                    self.load_level(self.next_map)                  # Otherwise load next level
            elif arcade.check_for_collision(self.player_sprite, o) and self.score<self.pass_score:
                print("touch exit")
                self.text_coins_true = True
                self.j = 0
                

        #Checks when the player fells of the map ------------     
        if self.player_sprite.center_y<-500:
            self.on_player_dead()
                 
        # Sword ---------------------------------------------
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
            
        # Check monsters hit ---------------------------------
        hits = arcade.check_for_collision_with_list(self.player_sword, self.monsters_list)
        for h in hits:
            if self.weapon_active and self.change_weapon:
                h.kill_monster()

        if arcade.check_for_collision_with_list(self.player_sprite, self.monsters_list):
            self.on_player_dead()
        
        # Switches update------------------------------------------
        for a in self.switch_list:
            Switch.update(a)
        
        # Bow -----------------------------------------------
        self.player_bow.angle = self.angle_degrees - 45
       
        if self.angle_degrees>=0:
            self.player_bow.center_x = self.pointx + 18
            
        elif self.angle_degrees<0:
            self.player_bow.center_x = self.pointx -18
            
        self.player_bow.center_y = self.pointy +6
  
        # Arrows and arrows hit --------------------------------------------
        for arrow in self.arrow_list: 
            arrow.change_y -= ARROW_GRAVITY * delta_time
            arrow_speed_vec = arcade.Vec2(arrow.change_x, arrow.change_y)
            arrow_speed_vec = arrow_speed_vec.normalize()
            arrow.radians = math.atan2(arrow_speed_vec[0], arrow_speed_vec[1]) - math.pi/4
            arrow.update()
            if arcade.check_for_collision_with_list(arrow, self.wall_list):                 # Arrow hits wall
                arrow.remove_from_sprite_lists()
            if arcade.check_for_collision_with_list(arrow, self.platforme_list):                 # Arrow hits wall
                arrow.remove_from_sprite_lists()
            if arcade.check_for_collision_with_list(arrow, self.sprite_switch):             # Arrow hits player
                arrow.remove_from_sprite_lists()
            hits = arcade.check_for_collision_with_list(arrow, self.monsters_list)          # Arrow hits monsters
            for h in hits:
               if self.arrow_active:
                    h.kill_monster() 
            for s in self.switch_list:
                if self.toggle(s, arrow):
                    s.update()
                    self.load_switches()    

        # Teleportation of player trhough portal ------------------------------------------
        for u in self.portals:
            if arcade.check_for_collision(self.player_sprite, u):
                for pl in self.portal_list:
                    if self.center_z_to_coordinates(u.center_x) == pl.x and self.center_z_to_coordinates(u.center_y) == pl.y:
                        self.current_portal = pl
                        self.player_sprite.center_x = self.coordinates_to_center_z(pl.teleport_x)
                        self.player_sprite.center_y = self.coordinates_to_center_z(pl.teleport_y)
                        self.i = 0 # stopwatch to remove the portals starts


        # Sprite faces moving direction -----------------------------
        if self.player_sprite.change_x * self.player_sprite.scale_x < 0 :  
            self.player_sprite.scale_x *= -1    
        
    # Switches and its logic ---------------------------------------

    # Called when sword, bow or arrow hits switch
    def toggle(self, switch: Switch, player: arcade.Sprite) -> bool:

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
        
    # If toggle switched it on
    def switch_action_on(self, switch: Switch) -> None:

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

    # If toggle switched it off
    def switch_action_off(self, switch: Switch) -> None:
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

    # Gate logic ---------------------------
    def action_open(self, gate: Gate) -> None:
        for g in self.gate_list: 
            if gate.x == self.center_z_to_coordinates(g.center_x) and gate.y == self.center_z_to_coordinates(g.center_y) :  #Converts center x and y to x and y coordinates (center_x-tilesize/2)/tilesize where tilesize = 64
                self.open_gate_list.append(g) # Adds it to a list of "invisible" gates
                self.gate_list.remove(g)    #  Removes it from visible gates
                self.solid_list.remove(g)   # Removes it from collision blocks
                
    
  
    def action_close(self, gate: Gate) -> None:
        for g in self.open_gate_list:
            if gate.x == self.center_z_to_coordinates(g.center_x) and gate.y == self.center_z_to_coordinates(g.center_y) :
                self.gate_list.append(g) #Same as open, but opposite
                self.open_gate_list.remove(g)
                self.solid_list.append(g)

    #Portal logic----------------------------
    def action_portal(self, portal: Portal) -> None:
        
        for p in self.sprite_portal:
            if portal.x == self.center_z_to_coordinates(p.center_x) and portal.y == self.center_z_to_coordinates(p.center_y) :
                portal.connected =  arcade.Sprite(      #Spawns the arrival portal (Which is only an image, no collision with the player)
                "assets/purple-portal.png",
                scale = 0.4*0.2
                )
                portal.connected.center_x = self.coordinates_to_center_z(portal.teleport_x) 
                portal.connected.center_y = self.coordinates_to_center_z(portal.teleport_y) 

                if portal.connected in self.portals:
                    print("connected already in portals")
                    return
                
                if  p in self.portals:
                    print("p already in portals")
                    return
                
                 # Adds start portal and arrival image to the list portals
                self.portals.append(portal.connected)
                p.connected = portal.connected
                self.portals.append(p)
                print("portal and connected added to portals")

    #Functions to go from sprite coordinates to x,y map coordinate and the other way around
    @staticmethod
    def center_z_to_coordinates(z: float) -> float:
        return (z-TILE_SIZE/2)/TILE_SIZE
    
    @staticmethod
    def coordinates_to_center_z(x: float) -> float:
        return x*TILE_SIZE+TILE_SIZE/2
    

    # Camera logic for mouvement ----------------------------------------    
    def pan_camera_to_player(self, panning_fraction: float = 2.0) -> None:
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player_sprite.position,
            self.window.delta_time,
            panning_fraction,

            )
    # Player's death and map reload logic ----------------------------------------
    def on_player_dead(self) -> None:                                                               # This method will end and reset the game to the starting position
        arcade.play_sound(self.sound_gameover)
        self.deaths += 1
        if self.deaths > MAX_DEATHS:
            game_over_view = GameOverView(f"You are Dead {MAX_DEATHS+1} Times", True)
            self.window.show_view(game_over_view)
        self.player_sprite.center_x = self.start_x                                      # Reset X
        self.player_sprite.center_y = self.start_y                                      # Reset Y                                 


    def on_game_complete(self) -> None:
        game_over_view = GameOverView(f"Congratulations, Game is Over", False)
        self.window.show_view(game_over_view)        
    
    def fatal_error(self, error_message: str) -> None:
        print(f"ERROR: {error_message}")
        sys.exit(1) 



# This class implements the start and end screen
class GameOverView(arcade.View):

    msg: str
    restart_game: bool
    
    def __init__(self, msg: str, restart_game: bool) -> None:
        super().__init__()
        self.msg = msg
        self.restart_game = restart_game

    def on_show(self) -> None:
        arcade.set_background_color(arcade.color.RED)

    def on_draw(self) -> None:
        self.clear() 
        arcade.draw_text(self.msg, self.window.width / 2, self.window.height / 2, arcade.color.DARK_BROWN, font_size=50, anchor_x="center")
        arcade.draw_text("Click to "+("start the new game" if self.restart_game else "quit"), self.window.width / 2, self.window.height / 2-75, arcade.color.SEA_GREEN, font_size=50, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:

        if not self.restart_game:
            arcade.close_window()
            sys.exit()                        
        else:
            gv = GameView()                      # (Re-) start the game
            self.window.show_view(gv)