import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes

from modules import game_manager
from modules.game_assets import GameAssets
from modules.player import Player
from modules.background import Background


def run():
    print(pyglet.version)

    # create the game window - size is 1000px x 1000px
    window = pyglet.window.Window(1000, 1000, "The game", resizable=False)

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()
    health_bar_batch = pyglet.graphics.Batch()
    damage_label_batch = pyglet.graphics.Batch()

    # groups - 0 drawn first, 10 drawn last
    groups = []
    for i in range(10):
        # groups.append(pyglet.graphics.OrderedGroup(i))  # used in older version
        groups.append(pyglet.graphics.Group(i))

    # load required assets
    assets = GameAssets()

    # list of all interactive objects in the simulation
    game_objects = []

    # list of health bar objects
    health_bars = []

    # list of damage labels
    damage_labels = []

    # list of asteroids
    asteroids = []
    num_max_asteroids = 5
    asteroid_spawn_interval = 5  # in seconds
    time_since_last_asteroid_spawn = (
        asteroid_spawn_interval  # time since last spawn in seconds
    )

    # list of enemies
    enemies = []
    num_max_enemies = 4
    enemy_spawn_interval = 5  # in seconds
    time_since_last_enemy_spawn = (
        enemy_spawn_interval  # time since last spawn in seconds
    )

    # list of powerups
    powerups = []
    num_max_powerups = 1
    powerup_spawn_interval = 10  # in seconds
    time_since_last_powerup_spawn = 0  # time since last spawn in seconds

    # create an instance of the background
    _ = Background(
        assets,
        x=window.width // 2,
        y=window.height // 2,
        batch=main_batch,
        group=groups[0],
    )

    # create an instance of a player
    player_1 = Player(assets, x=200, y=500, batch=main_batch, group=groups[5])

    # score
    score_label = None
    score = 0

    # change mouse cursor
    cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
    window.set_mouse_cursor(cursor)

    # drawing items on screen
    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        health_bar_batch.draw()
        damage_label_batch.draw()

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

    def draw_health_bar(obj):
        if obj.type == "bullet":
            return

        # Draw a health bar for the game object
        health_bar_width = obj.width  # Adjust the width based on the object's sprite
        health_percentage = 1.0
        health_bar_color = (55, 55, 255, 255)

        # if it is a poweup then calculate the health bar width based on the time left
        if obj.type == "powerup":
            health_percentage = (
                (obj.time_left / obj.max_time) if obj.max_time > 0 else 0
            )
            health_bar_color = (55, 255, 55, 255)
        else:
            health_percentage = (
                (obj.current_health / obj.max_health) if obj.max_health > 0 else 0
            )

        health_bar_width *= health_percentage

        health_bar = shapes.Rectangle(
            x=obj.x - obj.width // 2,
            y=obj.y + obj.height // 2 + 10,
            width=health_bar_width,
            height=5,
            color=health_bar_color,
            batch=health_bar_batch,
        )
        # the health bars need to be added to a list so that the objects do not go out of scope.
        # this is because rendering using batch needs the objects to be in scope during the draw call.
        health_bars_to_add = [health_bar]
        health_bars.extend(health_bars_to_add)

        damage_label = obj.draw_damage_label(damage_label_batch)
        if damage_label is not None:
            damage_labels_to_add = [damage_label]
            frames_persistent = 25
            damage_labels.append(tuple((damage_labels_to_add, frames_persistent)))

    def handle_out_of_bounds(obj):
        # if object is an asteroid or bullet, remove it if it goes out of bounds
        if obj.type in ["asteroid", "bullet"]:
            if (
                (obj.x + obj.width // 2) < 0
                or (obj.x - obj.width // 2) > window.width
                or (obj.y + obj.height // 2) < 0
                or (obj.y - obj.height // 2) > window.height
            ):
                obj.dead = True

        # if object is a player or enemy, bounce it back if it goes out of bounds
        if obj.type in ["player", "enemy"]:
            if (obj.x - obj.width // 2) <= 0:
                obj.velocity[0] = -obj.velocity[0]
                obj.x = obj.width // 2

            if (obj.x + obj.width // 2) >= window.width:
                obj.velocity[0] = -obj.velocity[0]
                obj.x = window.width - obj.width // 2

            if (obj.y - obj.height // 2) <= 0:
                obj.velocity[1] = -obj.velocity[1]
                obj.y = obj.height // 2

            if (obj.y + obj.height // 2) >= window.height:
                obj.velocity[1] = -obj.velocity[1]
                obj.y = window.height - obj.height // 2

    def spawn_asteroids(objects_to_add, dt):
        # spawn asteroids if necessary
        nonlocal time_since_last_asteroid_spawn
        time_since_last_asteroid_spawn += dt
        if (
            time_since_last_asteroid_spawn > asteroid_spawn_interval
            and len(asteroids) < num_max_asteroids
        ):
            time_since_last_asteroid_spawn = 0
            new_asteroids = game_manager.spawn_asteroids(
                num_max_asteroids - len(asteroids), player_1, main_batch, groups[5]
            )
            asteroids.extend(new_asteroids)
            objects_to_add.extend(new_asteroids)

    def spawn_enemies(objects_to_add, dt):
        # spawn enemies if necessary
        nonlocal time_since_last_enemy_spawn
        time_since_last_enemy_spawn += dt
        if (
            time_since_last_enemy_spawn > enemy_spawn_interval
            and len(enemies) < num_max_enemies
        ):
            time_since_last_enemy_spawn = 0
            new_enemies = game_manager.spawn_enemies(
                num_max_enemies - len(enemies), player_1, main_batch, groups[5]
            )
            enemies.extend(new_enemies)
            objects_to_add.extend(new_enemies)

    def spawn_powerups(objects_to_add, dt):
        # spawn powerups if necessary
        nonlocal time_since_last_powerup_spawn
        time_since_last_powerup_spawn += dt
        if (
            time_since_last_powerup_spawn > powerup_spawn_interval
            and len(powerups) < num_max_powerups
        ):
            time_since_last_powerup_spawn = 0
            new_powerups = game_manager.spawn_powerups(
                num_max_powerups - len(powerups), player_1, main_batch, groups[5]
            )
            powerups.extend(new_powerups)
            objects_to_add.extend(new_powerups)
            print("spawned powerup")

    # update loop
    def update(dt):
        health_bars.clear()
        objects_to_add = []  # list of new objects to add

        # spawn asteroids if necessary
        spawn_asteroids(objects_to_add, dt)

        # spawn enemies if required
        spawn_enemies(objects_to_add, dt)

        # spawn powerups if required
        spawn_powerups(objects_to_add, dt)

        # update positions, state of each object and
        # collect all children that each object may spawn
        for obj in game_objects:
            obj.update_object(dt)
            objects_to_add.extend(obj.child_objects)
            obj.child_objects = []  # clear the list

            # handle out of bounds
            handle_out_of_bounds(obj)

            # if object is an enemy, seek the player
            if obj.type == "enemy":
                obj.seek_player(player_1.x, player_1.y)

                # avoid other enemies
                for other_obj in game_objects:
                    if other_obj is not obj and other_obj.type == "enemy":
                        obj.compute_repulsion(other_obj)

            # check collision with all other objects
            for other_obj in game_objects:
                if other_obj is not obj:
                    obj.handle_collision_with(other_obj)

        # add new objects
        game_objects.extend(objects_to_add)

        # handle dead objects
        nonlocal score
        for obj in game_objects:
            if obj.dead:
                print("removing ", obj.type)
                obj.batch = None
                # if it is an asteroid remove it from the list of asteroids
                if obj.type == "asteroid":
                    if obj.died_by_player:
                        score += obj.score  # increase score
                    asteroids.remove(obj)
                # if it is an enemy remove it from the list of enemies
                if obj.type == "enemy":
                    if obj.died_by_player:
                        score += obj.score  # increase score
                    enemies.remove(obj)
                # if it is a powerup remove it from the list of powerups
                if obj.type == "powerup":
                    powerups.remove(obj)
                # if player is dead, game over
                if obj.type == "player":
                    print("Game over")
                    pyglet.app.exit()

        # remove dead objects from game_objects
        game_objects[:] = [obj for obj in game_objects if not obj.dead]

        # clean up damage labels
        if len(damage_labels) > 0:
            # damage_labels_new = damage_labels
            for i in range(len(damage_labels)):
                damage_labels[i] = (damage_labels[i][0], damage_labels[i][1] - 1)
            # remove damage labels that have expired
            damage_labels[:] = [obj for obj in damage_labels if obj[1] > 0]

        # draw health bar for all objects
        for obj in game_objects:
            draw_health_bar(obj)

        # draw score on the screen at top right
        nonlocal score_label
        score_label = pyglet.text.Label(
            "Score: " + str(score),
            font_name="Arial",
            font_size=20,
            x=window.width - 10,
            y=window.height - 10,
            anchor_x="right",
            anchor_y="top",
            batch=main_batch,
            group=groups[5],
        )

    load_main_scene()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
