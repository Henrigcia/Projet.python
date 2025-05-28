from __future__ import annotations
import os
import arcade

import math
import random
from maps import *
import yaml
from enum import Enum, StrEnum

SWITCH_OFF = arcade.Sprite(":resources:/images/tiles/leverLeft.png",
                           scale = 0.7 * 0.8)
SWITCH_ON = arcade.Sprite(":resources:/images/tiles/leverRight.png",
                           scale = 0.7 * 0.8)




class Gate:
    x: int
    y: int 
    active: bool
    def __init__(self, x: int, y: int ,a: bool) -> None:
        self.x = x
        self.y = y
        self.active = a

        
    def open(self) -> None:
        self.active = not self.active
    



class Switch(arcade.Sprite):
    x: int
    y: int
    appearance: arcade.Sprite
    status: bool = False
    disabled: bool = False

    class Action:
        class Kind(StrEnum):
            open_gate = "open-gate"
            close_gate = "close-gate"
            open_portal = "open-portal"
            disable = "disable"
        kind: Kind
        x: int
        y: int
        go_x: int
        go_y: int

    switch_on: list[Action] | None 
    switch_off: list[Action] | None 
    last_hit: float = 0
    
   

    

    def update(self, delta_time: float = 1 / 60) -> None:
        self.last_hit += delta_time
        
        super().update(delta_time)
    
    def change_gate(self, gate: Gate) -> None:
        gate.active = not gate.active

                
    @staticmethod
    def switchdraw(switch: Switch) -> arcade.Sprite:
        if switch.status:
            return arcade.Sprite(":resources:/images/tiles/leverRight.png",
                           scale = 0.7 * 0.8)
        else:
            return arcade.Sprite(":resources:/images/tiles/leverLeft.png",
                           scale = 0.7 * 0.8)
    
    
    
    

    @staticmethod
    def load_switchgates(filename: str) -> list[Switch]:

        if not os.path.exists(filename):

            raise ValueError(f"Error : The file {filename} doesn't exist !")       # TO-DO: handle correctly if file doesn't exist

        s = ""
        with open(filename, "r", encoding="utf-8") as file:
            for line in file.readlines():
                s += line

        arr = s.split("---", 2)
        m = yaml.safe_load(arr[0])
        switchlist = []
        if "switches" in m:
            
            for i in m["switches"]:
                
                new_switch: Switch = Switch()

                new_switch.x = i["x"]
                new_switch.y = i["y"]

                
                if "state" in i:
                    new_switch.status = True

                if "switch_on" in i:
                    new_switch.switch_on = []
                    for a in i["switch_on"]:
                        action = Switch.Action()
                        action.kind = a["action"]

                        if action.kind == Switch.Action.Kind.open_gate:
                            
                            action.x = a["x"]
                            action.y = a["y"]
                        elif action.kind == Switch.Action.Kind.close_gate:
                            action.x = a["x"]
                            action.y = a["y"]
                        elif action.kind == Switch.Action.Kind.open_portal:
                            action.x = a["x"]
                            action.y = a["y"]
                            action.go_x = a["go_x"]
                            action.go_y = a["go_y"]

                        new_switch.switch_on.append(action)
                else: new_switch.switch_on = None
                    
                
                if "switch_off" in i:
                    new_switch.switch_off = []
                    for a in i["switch_off"]:
                        action = Switch.Action()
                        action.kind = a["action"]

                        if action.kind == Switch.Action.Kind.open_gate:
                            action.x = a["x"]
                            action.y = a["y"]
                        elif action.kind == Switch.Action.Kind.close_gate:
                            action.x = a["x"]
                            action.y = a["y"]
                        elif action.kind == Switch.Action.Kind.open_portal:
                            action.x = a["x"]
                            action.y = a["y"]
                            action.go_x = a["go_x"]
                            action.go_y = a["go_y"]

                        new_switch.switch_off.append(action)
                else: new_switch.switch_off = None
                
                if new_switch in switchlist:
                    print("new_switch already in switchlist")
                    None
                else: 
                    switchlist.append(new_switch)

        
        return switchlist
                                  
                        
                        

                        
                        
                        
                        
                        
                        
                        
                        
                        
                            


                        


                    



                    

        

    
    

   
