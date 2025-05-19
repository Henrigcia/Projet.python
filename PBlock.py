# This module implements blocks of platforms (individual sptites) that move together coherently
# The base class PBlock implements the core structure
# HBlock and VBlock classes are then derived to implement horizonatally and vertically moving blocks respectively

import arcade

class PBlock:

    boundary_low : float                                          # Right boundary for the entire block
    boundary_high : float                                         # Left boundary for the entire block

    d_a : float                                                   # The distance from the LEFTMOST platform to the left boundary
    d_b : float                                                   # The distance from the RIGHTMOST platform to the right boun

    platform_list : arcade.SpriteList[arcade.Sprite]              # The list of platfroms that form the block

    def __init__(self, boundary_low : float, boundary_high : float) -> None:

        self.boundary_low, self.boundary_high = boundary_low, boundary_high                 # Initialize the block boundaries
        self.d_a, self.d_b = boundary_high - boundary_low, boundary_high - boundary_low     # Initialize the distances to max values 
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)                           # Create the platforms list (empty at start)


# This method will add a new plaform sprite to the block and recalculate the distances and individual platforms boundaries
    def add_platform(self, s : arcade.Sprite) -> None:                                          

        self.platform_list.append(s)                                                                 # The baseline: append a new platform sprite to the list


# This class will implement horizontally moving block of plaforms
class HBlock(PBlock):

    def add_platform(self, s : arcade.Sprite) -> None:                                          

        super().add_platform(s)                                                                # First, call the superior

        self.d_a = min(self.d_a, s.center_x - self.boundary_low)                               # Recacluate the distance from the LEFTMOST platform to the left boundary (update if the distance from the newly added platform is less than the current distance)
        self.d_b = min(self.d_b, self.boundary_high - s.center_x)                              # Recacluate the distance from the RIGHTMOST platform to the right boundary (update if the distance from the newly added platform is less than the current distance)

        for s in self.platform_list:                                                           # Update each individual platform sprite boundaries based on the new distances to the block boundaries so all of them move coherently over the same distance
            s.boundary_left = s.center_x - self.d_a
            s.boundary_right = s.center_x + self.d_b


# This clas will implement vertically moving block of platforms
class VBlock(PBlock):

    def add_platform(self, s : arcade.Sprite) -> None:                                          

        super().add_platform(s)                                                                # First, call the superior

        self.d_a = min(self.d_a, s.center_y - self.boundary_low)                               # Recacluate the distance from the LOWEST platform to the bottom boundary (update if the distance from the newly added platform is less than the current distance)
        self.d_b = min(self.d_b, self.boundary_high - s.center_y)                              # Recacluate the distance from the HIGHEST platform to the top boundary (update if the distance from the newly added platform is less than the current distance)

        for s in self.platform_list:                                                           # Update each individual platform sprite boundaries based on the new distances to the block boundaries so all of them move coherently over the same distance
            s.boundary_bottom = s.center_y - self.d_a
            s.boundary_top = s.center_y + self.d_b






    


 