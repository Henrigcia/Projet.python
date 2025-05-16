from abc import abstractmethod

class Arrows:
    arrows_up : set[tuple[int, int] ] = set()
    #arrows_down : set[tuple[int, int] ] = set()
    #arrows_left : set[tuple[int, int] ] = set()
    #arrows_right : set[tuple[int, int] ] = set()

    def __init__(self,  arrows_up : set[tuple[int, int] ]):
        self.arrows_up = arrows_up
    def lecture(self):
        empty_list : list[tuple[int, int]] = []
        



        
