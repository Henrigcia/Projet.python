# This module impments blocks of platforms (individual sptites) that move together coherently
import arcade

class PBlock:
    boundary_right : int                                        # Right boundary for the entire block
    boundary_left : int                                         # Left boundary for the entire block
    d_a : int                                                   # The distance from the LEFTMOST platform to the left boundary
    d_b : int                                                   # The distance from the RIGHTMOST platform to the right boundary

    platform_list : arcade.SpriteList[arcade.Sprite]            # The list of platfroms that form the block

    def __init__(self, boundary_left : int, boundary_right : int) -> None:
        self.boundary_right, self.boundary_left = boundary_right, boundary_left
        self.d_a, self.d_b = boundary_right - boundary_left, boundary_right - boundary_left     # Initialize the distances 
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)                           # Create the platforms list (empty at start)
        
    def add_platform(self, s : arcade.Sprite) -> None:                                          # Add another platform to the block
        self.platform_list.append(s)
        self.d_b = int(min(self.d_b, self.boundary_right - s.center_x))                              # Recacluate the distance from the RIGHTMOST platform to the right boundary (update if the distance from the newlz added platform is less than the current distance)
        self.d_a = int(min(self.d_a, s.center_x - self.boundary_left))                               # Recacluate the distance from the LEFTMOST platform to the left boundary (update if the distance from the newlz added platform is less than the current distance)

        for s in self.platform_list:                                                            # Update each indivisual platform boundaries based on the new distances to the block boundaries so all of themm move coherently
            s.boundary_left = s.center_x - self.d_a
            s.boundary_right = s.center_x + self.d_b

    


 