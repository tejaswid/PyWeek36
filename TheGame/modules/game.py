import pyglet

from modules.game_assets import GameAssets
from modules.player import Player

def run():
    print(pyglet.version)

    # create the game window - size is 1000px x 1000px
    window = pyglet.window.Window(1000, 1000, "The game", resizable=False)

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()

    # groups - 0 drawn first, 10 drawn last
    groups = []
    for i in range(10):
        #groups.append(pyglet.graphics.OrderedGroup(i))  # used in older version
        groups.append(pyglet.graphics.Group(i))

    # load required assets
    assets = GameAssets()

    # list of all objects in the simulation
    game_objects = []

    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()


    # loads the main scene
    def load_main_scene():
        # create an instance of a player
        player_1 = Player(assets, x=200, y=500, batch=main_batch, group=groups[5])
        game_objects.append(player_1)
    

    # update loop
    def update(dt):
        objects_to_add = []     # list of new objects to add
        # update positions, state of each object and
        # collect all children that each object may spawn
        for obj in game_objects:
            obj.update_object(dt)
            objects_to_add.extend(obj.child_objects)
            obj.child_objects = []  # clear the list

        # add new objects
        game_objects.extend(objects_to_add)


    load_main_scene()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()