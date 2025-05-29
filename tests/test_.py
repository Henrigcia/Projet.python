import arcade
import pytest
from GameView import GameView


def test_sword(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    ORIGINAL_NUMBER_OF_BLOBS = len(view.monsters_list)
    #initial position


    window.test(60)

    view.on_mouse_press(0,0,arcade.MOUSE_BUTTON_LEFT,0)
    #Verifies the sword comes out
    assert view.change_weapon == True, "Activated bow, not sword"
    #Verifies the placement of the sword
    assert view.player_sprite.center_x>=view.player_sword.center_x -20,  "Sword to the right of the player"

    window.test(20)

    view.on_mouse_press(0,500,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(20)

    view.on_mouse_press(500,500,arcade.MOUSE_BUTTON_LEFT,0)
    #Verifies the placement of the sword
    assert view.player_sprite.center_x<=view.player_sword.center_x +40,  "Sword to the left of the player"

    window.test(20)

    view.on_mouse_press(500,0,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(20)

    view.on_mouse_release(500,0,arcade.MOUSE_BUTTON_LEFT,0)

    #Verifies the sword is deactivated
    assert view.weapon_active == False, "Sword is still active"

    #Teleports near a blob
    view.player_sprite.center_x= 5*64
    view.player_sprite.center_y = 4*64

    window.test(60)

    view.on_mouse_press(10*64,5*64,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(80)

    #Verifies blob was killed 
    assert len(view.monsters_list) == ORIGINAL_NUMBER_OF_BLOBS -1, "Blob wasn't killed"


   

INITIAL_COIN_COUNT = 1

def test_collect_coins(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    # Make sure we have the amount of coins we expect at the start
    assert len(view.coin_list) == INITIAL_COIN_COUNT

    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)

    # Let the game run for 1 second
    window.test(20)

    # We should have collected the first coin
    assert len(view.coin_list) == INITIAL_COIN_COUNT - 1

    view.on_key_release(arcade.key.RIGHT, 0)

    window.test(50)


    


def test_bow(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    ORIGINAL_NUMBER_OF_BLOBS = len(view.monsters_list)
    #initial position


    window.test(60)

    view.on_mouse_press(0,0,arcade.MOUSE_BUTTON_RIGHT,0)

    view.on_mouse_press(0,0,arcade.MOUSE_BUTTON_LEFT,0)

    assert view.change_weapon==False,  "Switch in weapon didn't work"

    assert view.player_sprite.center_x<=view.player_bow.center_x -18,  "Bow to the right of the player"

    window.test(20)

    view.on_mouse_press(0,500,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(20)

    view.on_mouse_press(500,500,arcade.MOUSE_BUTTON_LEFT,0)

    assert view.player_sprite.center_x<=view.player_bow.center_x +40,  "Bow to the left of the player"

    window.test(20)

    view.on_mouse_press(500,0,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(20)

    view.on_mouse_release(500,0,arcade.MOUSE_BUTTON_LEFT,0)

    assert view.weapon_active == False, "Bow is still active"

    view.player_sprite.center_x= 5*64
    view.player_sprite.center_y = 4*64

    window.test(60)

    view.on_mouse_press(10*64,5*64,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(80)

    assert len(view.monsters_list) == ORIGINAL_NUMBER_OF_BLOBS -1, "Blob wasn't killed"

    #Tests whether or not arrows dissapeared after collision, shoots in the wall

    view.on_mouse_press(view.player_sprite.center_x + 3*64,view.player_sprite.center_y + 5*64,arcade.MOUSE_BUTTON_LEFT,0)
    window.test(10)
    view.on_mouse_press(view.player_sprite.center_x + 3*64,view.player_sprite.center_y + 5*64,arcade.MOUSE_BUTTON_LEFT,0)
    window.test(10)
    view.on_mouse_press(view.player_sprite.center_x + 3*64,view.player_sprite.center_y + 5*64,arcade.MOUSE_BUTTON_LEFT,0)
    view.on_mouse_release(0,0,arcade.MOUSE_BUTTON_LEFT,0)
    window.test(100)

    assert len(view.arrow_list) == 1, "Arrows did not dissapear"

def test_switchgates(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    assert len(view.gate_list) == 1, "Wrong number of starting gates"

    view.player_sprite.center_x = 32
    view.player_sprite.center_y = 5*64

    window.test(60)
    view.on_mouse_press(5*64, 5*64, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(30)
    view.on_mouse_release(0,0,arcade.MOUSE_BUTTON_LEFT,0)
    
    window.test(30)

    assert len(view.open_gate_list) == 1, "Gate did not dissapear"

    view.on_mouse_press(0,0,arcade.MOUSE_BUTTON_RIGHT,0)

    assert view.change_weapon == False, "Did not change weapon"

    view.on_mouse_press(380, 10*64, arcade.MOUSE_BUTTON_LEFT, 0)

    window.test(10)

    view.on_mouse_release(0,0,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(250)

    assert len(view.open_gate_list) == 0, "Gate did not appear"

def test_switchportals(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    assert len(view.portals) == 0, "Wrong number of starting visible portals"

    view.player_sprite.center_x = 64*7.5
    view.player_sprite.center_y = 64

    window.test(30)

    view.on_mouse_press(10*64, 64, arcade.MOUSE_BUTTON_LEFT, 0)

    window.test(30)

    assert len(view.portals) == 2, "Portals did not appear correctly"

    view.on_mouse_release(0,0,arcade.MOUSE_BUTTON_LEFT,0)

    window.test(20)


    view.on_key_press(arcade.key.RIGHT, 0)

    window.test(55)

    view.on_key_release(arcade.key.RIGHT, 0)

    assert view.player_sprite.center_x > 14*64, "Player did not teleport"

    window.test(10)

    view.on_key_press(arcade.key.LEFT, 0)

    window.test(50)

    view.on_key_release(arcade.key.RIGHT, 0)

    assert view.player_sprite.center_x > 13*64, "Player managed to teleport back"
    
    window.test(30)

def test_exit(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    view.player_sprite.center_x = 64*16
    view.player_sprite.center_y = 64

    window.test(60)

    view.on_key_press(arcade.key.RIGHT, 0)

    window.test(30)

    view.on_key_release(arcade.key.RIGHT, 0)

    window.test(60)

    #Checks that the exit sign is disabled before having enough coins
    
    assert view.current_map == "maps/map1.txt", "Exit worked without coins"

    #Teleport back to the start

    view.player_sprite.center_x = 64
    view.player_sprite.center_y = 64

    window.test(60)

    view.on_key_press(arcade.key.RIGHT, 0)

   
    window.test(20)

    # Collect the coin
    assert len(view.coin_list) == INITIAL_COIN_COUNT - 1

    view.on_key_release(arcade.key.RIGHT, 0)

    window.test(30)

    #Go back to the exit sign
    view.player_sprite.center_x = 64*16
    view.player_sprite.center_y = 64

    window.test(60)

    view.on_key_press(arcade.key.RIGHT, 0)

    window.test(60)
    #Checks that the sign worked
    assert view.current_map == "maps/map2.txt", "Exit sign didn't work"

def test_die(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    #Die to bats -------------
   
    #teleport to dying platform
    view.player_sprite.center_x = 64*15
    view.player_sprite.center_y = 6*64
    #wait 5 seconds
    window.test(100)
    assert view.deaths >0, "Did not die to bats"

    #Die to blobs -----------------
    #teleport to dying platform
    view.player_sprite.center_x= 5*64
    view.player_sprite.center_y = 4*64
    window.test(250)
    assert view.deaths>1, "Did not die to blob"

    #Die of falling -----------------
    #Run to edge and fall
    view.on_key_press(arcade.key.LEFT,0)
    window.test(80)
    view.on_key_release(arcade.key.LEFT,0)
    assert view.deaths>2, "Did not die to falling"

    #Die of Lava -------------------

    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(60)

    assert view.deaths>3, "Did not die to lava"

    view.on_key_release(arcade.key.RIGHT, 0)

    window.test(50)

def test_platforms(window: arcade.Window)->None:
    view = GameView()
    window.show_view(view)

    #Teleports player on platform
    view.player_sprite.center_x= 14*64
    view.player_sprite.center_y = 4*64

    window.test(50)
    #Checks that it moved left, and the player stayed on it
    assert view.player_sprite.center_x > 13*64, "Platform did not move"
    assert view.player_sprite.center_y >= 4*64, "Player fell off"

    window.test(140)
    #Checks that the platform went the other way around
    assert view.player_sprite.center_x < 15*64, "Platform did not go back left"
    assert view.player_sprite.center_y >= 4*64, "Player fell off"
















