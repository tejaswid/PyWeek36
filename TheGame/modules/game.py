import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes

from modules.game_assets import GameAssets
from modules.player import Player
from modules.enemy import Enemy


def run():
    print(pyglet.version)

    # create the game window - size is 1000px x 1000px
    window = pyglet.window.Window(1000, 1000, "The game", resizable=False)

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()
    health_bar_batch = pyglet.graphics.Batch()

    # health_bar = shapes.Rectangle(
    #         x=10,#obj.x - obj.width // 2,
    #         y=100,#obj.y - obj.height // 2 + 50,
    #         width=200,
    #         height=50,
    #         color=(55, 55, 255, 255),
    #         batch=main_batch,
    #     )

    # groups - 0 drawn first, 10 drawn last
    groups = []
    for i in range(10):
        # groups.append(pyglet.graphics.OrderedGroup(i))  # used in older version
        groups.append(pyglet.graphics.Group(i))

    # load required assets
    assets = GameAssets()

    # list of all objects in the simulation
    game_objects = []

    # list of health bar objects
    health_bars = []

    # create an instance of a player
    player_1 = Player(assets, x=200, y=500, batch=main_batch, group=groups[5])
    enemy_1 = Enemy(assets, x=1000, y=500, batch=main_batch, group=groups[5])

    # change mouse cursor
    cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
    window.set_mouse_cursor(cursor)

    # drawing items on screen
    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        health_bar_batch.draw()

    # handle keyboard inputs
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.A:
            pass

    # handle mouse inputs
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            # create a bullet
            player_1.fire_bullet(x, y)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        player_1.update_rotation(x, y)

    # loads the main scene
    def load_main_scene():
        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)
        game_objects.append(enemy_1)

    def draw_health_bar(obj):
        if obj.type == "bullet":
            return

        # Draw a health bar for the game object
        health_bar_width = obj.width  # Adjust the width based on the object's sprite
        health_percentage = (
            (obj.current_health / obj.max_health) if obj.max_health > 0 else 0
        )
        health_bar_width *= health_percentage

        health_bar = shapes.Rectangle(
            x=obj.x - obj.width // 2,
            y=obj.y + obj.height // 2 + 10,
            width=health_bar_width,
            height=5,
            color=(55, 55, 255, 255),
            batch=health_bar_batch,
        )
        health_bars_to_add = [health_bar]
        health_bars.extend(health_bars_to_add)

    # update loop
    def update(dt):
        health_bars.clear()
        objects_to_add = []  # list of new objects to add
        # update positions, state of each object and
        # collect all children that each object may spawn
        for obj in game_objects:
            obj.update_object(dt)
            objects_to_add.extend(obj.child_objects)
            obj.child_objects = []  # clear the list

            # if object is an enemy, seek the player
            if obj.type == "enemy":
                obj.seek_player(player_1.x, player_1.y)

            # check collision with all other objects
            for other_obj in game_objects:
                if other_obj is not obj:
                    obj.handle_collision_with(other_obj)

        # add new objects
        game_objects.extend(objects_to_add)

        for obj in game_objects:
            if obj.dead:
                print("removing ", obj.type)
                obj.batch = None

        # remove dead objects
        game_objects[:] = [obj for obj in game_objects if not obj.dead]

        # draw health bar for all objects
        for obj in game_objects:
            draw_health_bar(obj)

    load_main_scene()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
