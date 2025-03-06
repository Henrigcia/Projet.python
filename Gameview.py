import arcade

PLAYER_MOVEMENT_SPEED = 8
PLAYER_GRAVITY = 1
PLAYER_JUMP_SPEED = 18


class GameView(arcade.View):
    """Main in-game view."""
    physics_engine: arcade.PhysicsEnginePlatformer
    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    camera: arcade.camera.Camera2D

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )
        self.camera = arcade.camera.Camera2D()

    def setup(self) -> None:
        """Set up the game here."""
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=64,
            center_y=128
        )

        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        x :int =0
        while x < (1280-64):
            wall=arcade.Sprite(
            ":resources:images/tiles/grassMid.png",
            center_x=x,
            center_y=32,
            scale=0.5
            )
            self.wall_list.append(wall)
            x+=64
        for x in [256,512,768]:
            wall=arcade.Sprite(
            ":resources:images/tiles/boxCrate_double.png",
            center_x=x,
            center_y=96,
            scale=0.5
            )
            self.wall_list.append(wall)

        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        x=128
        while x < 1250 :
            coin=arcade.Sprite(
            ":resources:images/items/coinGold.png",
            center_x=x,
            center_y=96,
            scale=0.5
            )
            self.coin_list.append(coin)
            x+=256









    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coin_list.draw()

            #some_sprite_list.draw_hit_boxes()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                # start moving to the right
                self.player_sprite.change_x = +PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT:
                # start moving to the left
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            case arcade.key.UP:
                # jump by giving an initial vertical speed
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        match key:
            case arcade.key.RIGHT | arcade.key.LEFT:
                # stop lateral movement
                self.player_sprite.change_x = 0

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        self.physics_engine.update()
        self.camera.position = self.player_sprite.position

        coins_to_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_to_hit:
            coin.remove_from_sprite_lists()
