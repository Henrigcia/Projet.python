from __future__ import annotations
import os
import arcade
import math
import random
from maps import *
import yaml
from enum import Enum, StrEnum



class Portal(arcade.Sprite):

    x: int
    y: int
    teleport_x: int
    teleport_y: int
    connected: arcade.Sprite 

    def __init__(self, x: int, y: int ,a: int, b: int) -> None:
        self.x = x
        self.y = y
        self.teleport_x = a
        self.teleport_y = b
        
