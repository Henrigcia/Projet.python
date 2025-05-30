import arcade
from GameView import *
import timeit
import pytest

def test_on_update(window :arcade.Window) -> None:
    gv = GameView()
    gv.load_level("maps/map3.txt")
    gv.setup()
    number = 1000
    res1 = timeit.timeit(lambda: gv.on_update(1/60), number=number)
   
    gv.load_level("maps/maptest3.txt")
    res2 = timeit.timeit(lambda: gv.on_update(1/60), number=number)
    print(res1 / number)
    print(res2 / number)
    gv.load_level("maps/map3.txt")
    res3 = timeit.timeit(lambda: gv.on_update(1/60), number=number)
    print(res3 / number)
    gv.load_level("maps/map4.txt")
    res4 = timeit.timeit(lambda: gv.on_update(1/60), number=number)
    print(res4 / number)
    gv.load_level("maps/map5.txt")
    res5 = timeit.timeit(lambda: gv.on_update(1/60), number=number)
    print(res5 / number)
    gv.load_level("maps/map6.txt")
    res6 = timeit.timeit(lambda: gv.on_update(1/60), number=number)
    print(res6 / number)
    
    

def test_load_level(window :arcade.Window) -> None:
    gv = GameView()
    number = 100
    re1 = timeit.timeit(lambda: gv.load_level("maps/map1.txt"), number=number)
    re2 = timeit.timeit(lambda: gv.load_level("maps/map2.txt"), number=number)
    re3 = timeit.timeit(lambda: gv.load_level("maps/map3.txt"), number=number)
    re4 = timeit.timeit(lambda: gv.load_level("maps/map5.txt"), number=number)
    re5 = timeit.timeit(lambda: gv.load_level("maps/map5.txt"), number=number)
    re6 = timeit.timeit(lambda: gv.load_level("maps/map6.txt"), number=number)
    
    res1 = timeit.timeit(lambda: gv.load_level("maps/mapupdate1.txt"), number=number)
    res2 = timeit.timeit(lambda: gv.load_level("maps/mapupdate2.txt"), number=number)
    res3 = timeit.timeit(lambda: gv.load_level("maps/mapupdate3.txt"), number=number)
    res4 = timeit.timeit(lambda: gv.load_level("maps/mapupdate5.txt"), number=number)
    res5 = timeit.timeit(lambda: gv.load_level("maps/mapupdate5.txt"), number=number)
    res6 = timeit.timeit(lambda: gv.load_level("maps/mapupdate6.txt"), number=number)
    print(re1 / number)
    print(re2 / number)
    print(re3 / number)
    print(re4 / number)
    print(re5 / number)
    print(re6 / number)
    print(res1 / number)
    print(res2 / number)
    print(res3 / number)
    print(res4 / number)
    print(res5 / number)
    print(res6 / number)




