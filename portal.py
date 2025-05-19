from __future__ import annotations
import os
import arcade
import math
import random
from maps import *
import yaml
from enum import Enum, StrEnum



class Portal:
    teleport_x: int
    teleport_y: int
    
    


    def __init__(self, x: int, y: int ,a: bool)->None:
        self.x = x
        self.y = y
    
        
