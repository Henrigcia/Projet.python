import arcade
import math
import random

BLOB_MOVEMENT_SPEED = 0.5
BLOB_SIZE = 40

BAT_AREA_X = 150                            # Bat "home area", 1/2 of rectangle x
BAT_AREA_Y = 100                            # Bat "home area", 1/2 of rectangle y
BAT_MOVEMENT_SPEED_X = 2                    # Intital velocity x
BAT_MOVEMENT_SPEED_Y = 1                    # Intital velocity y
BAT_SPEED_CHANGE_SCALE = 0.1                # Change factor for velocity value  (0-1)
BAT_ANGLE_CHANGE_SCALE = 20                 # Change facfor for velocity direction in GRAD
BAT_FRAMES = 60                             # Frequency to distort velocity vector (each xxx frames)
BAT_SIZE = 30



class Monster(arcade.Sprite):                                                   # The base level class that describes all game monsters behavoirs

    def move_monster(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:       # The default defintion of a Monster movement. This method will be overriden for each particular Monster subclass (Blob, Bat) to make its movemnent unique
        self.center_x += self.change_x                                          # We need to pass the walls list as the movement rules can be dependent on collision with walls
        self.center_y += self.change_y 
        if self.scale_x*self.change_x > 0:
            self.scale_x*= -1
    
    def kill_monster(self) -> None:                                                      # This method will define what happens when the player kills the monster
        self.remove_from_sprite_lists()                                           # Will remove this monster from all lists and sound
        arcade.play_sound(arcade.Sound(":resources:/sounds/explosion1.wav"))
  

class Blob(Monster):                                                            # Blob is a subclass of Monster to describe blob monster

    def move_monster(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:       # This method overrides and extends the rules of movement for Blob monster
        super().move_monster(wall_list)                                         # First, we inoke the default movement

        if arcade.check_for_collision_with_list(self, wall_list):               #Check if with the changes the blob touches the wall 
            self.change_x = - self.change_x   #Invert speed
            self.scale_x *= -1                #Change looking direction 
              

        if self.change_x > 0:                                                   # Logic for Blobs stop right side
            self.center_x += BLOB_SIZE                                              # Move temporarily 1 BLOB_SIZE RIGHT 
            self.center_y -= 1                                                      # and 1 pix down
            if not arcade.check_for_collision_with_list(self, wall_list):           # Check if no longer supported by wall
                self.change_x = - self.change_x                                         # Invert speed
                self.scale_x *=-1                                                       # Mirrow image   
            self.center_x -= BLOB_SIZE                                             # restore x
            self.center_y += 1                                                     # restore y

        elif self.change_x < 0:                                                 # Logic for Blobs stop left side
                self.center_x -= BLOB_SIZE                                          # Move temporarily 1 BLOB_SIZE LEFT
                self.center_y -= 1                                                  # and 1 pix down
                if not arcade.check_for_collision_with_list(self, wall_list):       # Check if no longer supported by wall
                        self.change_x = - self.change_x                                 # Invert speed
                        self.scale_x *=-1                                                # Mirrow image                              
                self.center_x += BLOB_SIZE                                          # restore x
                self.center_y += 1                                                  # restore y
            

class Bat(Monster):                                                             # Bat is a subclass of Monster to describe bat monster

    fix_center_x : float
    fix_center_y : float
    area_x : float
    area_y : float
    frames : int 

    def distort_movement(self, scale: float, angle: float) -> None:                                                 # Will distort velocity within the given scale and angle and recalculate Vx and Vy

        angle_dir = math.atan(self.change_y / self.change_x)
        velocity = math.sqrt(self.change_x**2 + self.change_y**2)
        velocity += velocity * random.uniform(-1,1) * scale                                               # Random velocity change within the given scale
        angle_adj = math.radians(random.uniform(-angle, angle))                                           # Random direction change for the velocity vector wuthin the given angle
        self.change_x =   velocity * math.cos(angle_dir + angle_adj)                                      # Recalculate Vx
        self.change_y =   velocity * math.sin(angle_dir + angle_adj)                                      # Recalculate Vy
        

    def move_monster(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:       # This method overrides and extends the rules of movement for Bat monster
        super().move_monster(wall_list)                                         # First, we inoke the default movement

        self.frames += 1                                                             # Increase frame count
        if self.frames == BAT_FRAMES:                                                # When count runs out randomize volcity vector and reset count
            self.distort_movement(BAT_SPEED_CHANGE_SCALE, BAT_ANGLE_CHANGE_SCALE)
            self.frames = 0

        current_x = self.center_x - self.fix_center_x
        current_y = self.center_y - self.fix_center_y
        if abs(current_x) > abs(self.area_x) :
            self.change_x = - self.change_x                                         # Invert speed  on the x axis                                                         
        if abs(current_y) > abs(self.area_y):
            self.change_y = - self.change_y                                         # Invert speed on the y axis
                                                         

