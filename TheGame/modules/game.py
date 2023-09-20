import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes

from modules import game_manager
from modules.game_assets import GameAssets
from modules.player import Player
from modules.background import Background
from modules.game_state import GameState

def run():
    print(pyglet.version)

    # actual stage size
    stage_width = 1024
    stage_height = 1024

    # viewport size - this is the size of the window that we see
    viewport_width = 800
    viewport_height = 800
    viewport_x = stage_width // 2  # centre of the stage
    viewport_y = stage_height // 2  # centre of the stage
    viewport_margin = 50  # margin tp move the screen when player moves

    # create the game window - size is 1000px x 1000px
    window = pyglet.window.Window(
        width=viewport_width,
        height=viewport_height,
        caption="The game",
        resizable=False,
    )

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()
    health_bar_batch = pyglet.graphics.Batch()
    damage_label_batch = pyglet.graphics.Batch()
    gui_batch = pyglet.graphics.Batch()

    game_state = GameState()


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

    # score
    score_label = None
    score = 0

    # level
    level = 0
    change_level = True

    # change mouse cursor
    cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
    window.set_mouse_cursor(cursor)

    def window_to_world(x, y):
        return (
            x + viewport_x - viewport_width // 2,
            y + viewport_y - viewport_height // 2,
        )

    def world_to_window(x, y):
        return (
            x - viewport_x + viewport_width // 2,
            y - viewport_y + viewport_height // 2,
        )

    def reset_viewport():
        nonlocal viewport_x
        nonlocal viewport_y
        viewport_x = stage_width // 2
        viewport_y = stage_height // 2

    def get_camera_bottom_left():
        return (-window.view[12], -window.view[13])

    def get_camera_centre():
        camera_bl_x, camera_bl_y = get_camera_bottom_left()
        print(" camera bottom left: {}, {}".format(camera_bl_x, camera_bl_y))
        return (camera_bl_x + viewport_width // 2, camera_bl_y + viewport_height // 2)

    def reset_camera():
        # get current corner of the camera
        camera_bl_x, camera_bl_y = get_camera_bottom_left()
        # compute difference between current corner and desired corner
        diff_x = (viewport_x - viewport_width // 2) - camera_bl_x
        diff_y = (viewport_y - viewport_height // 2) - camera_bl_y
        # translate the camera by the difference
        window.view = window.view.translate((-diff_x, -diff_y, 0))

    # drawing items on screen
    @window.event
    def on_draw():
        window.clear()

        gui_batch.draw()
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
        # Note: x and y are in window coordinate frame
        # convert to world coordinate frame
        x, y = window_to_world(x, y)
        if button == mouse.LEFT:
            for obj in game_objects:
                if obj.type == "player":
                    obj.fire_bullet(x, y)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        # Note: x and y are in window coordinate frame
        # convert to world coordinate frame
        x, y = window_to_world(x, y)
        for obj in game_objects:
            if obj.type == "player":
                obj.update_rotation(x, y)

    # loads the main scene
    def load_stage_1():
        # create an instance of the background centred on the stage
        _ = Background(
            assets,
            level=1,
            x=stage_width // 2,
            y=stage_height // 2,
            batch=gui_batch,
            group=groups[0],
        )

        # spawn the player
        player_1 = Player(assets, game_state, x=700, y=700, batch=main_batch, group=groups[5])

        # reset the view_port
        reset_viewport()
        # reset the camera
        reset_camera()

        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)
        

    # loads the second scene
    def load_stage_2():
        # create an instance of the background centred on the stage
        _ = Background(
            assets,
            level=2,
            x=stage_width // 2,
            y=stage_height // 2,
            batch=gui_batch,
            group=groups[0],
        )

        # spawn the player
        player_1 = Player(assets, game_state, x=200, y=200, batch=main_batch, group=groups[5])

        # reset the view_port
        reset_viewport()

        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)
        # window.view = window.view.translate(
        #     (-viewport_x + viewport_width // 2, -viewport_y + viewport_height // 2, 0)
        # )

        # reset the camera
        reset_camera()

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
                or (obj.x - obj.width // 2) > stage_width
                or (obj.y + obj.height // 2) < 0
                or (obj.y - obj.height // 2) > stage_height
            ):
                obj.dead = True

        # if object is a player or enemy, bounce it back if it goes out of bounds
        if obj.type in ["player", "enemy"]:
            if (obj.x - obj.width // 2) <= 0:
                obj.velocity[0] = -obj.velocity[0]
                obj.x = obj.width // 2

            if (obj.x + obj.width // 2) >= stage_width:
                obj.velocity[0] = -obj.velocity[0]
                obj.x = stage_width - obj.width // 2

            if (obj.y - obj.height // 2) <= 0:
                obj.velocity[1] = -obj.velocity[1]
                obj.y = obj.height // 2

            if (obj.y + obj.height // 2) >= stage_height:
                obj.velocity[1] = -obj.velocity[1]
                obj.y = stage_height - obj.height // 2

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
                num_max_asteroids - len(asteroids), assets, game_state, main_batch, groups[5]
            )
            asteroids.extend(new_asteroids)
            objects_to_add.extend(new_asteroids)

            if level == 2:
                print("new_asteroids: ", len(new_asteroids))
                print("asteroids: ", len(asteroids))

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
                num_max_enemies - len(enemies), assets, game_state, main_batch, groups[5]
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
                num_max_powerups - len(powerups), assets, game_state, main_batch, groups[5]
            )
            powerups.extend(new_powerups)
            objects_to_add.extend(new_powerups)
            print("spawned powerup")

    def update_viewport():
        nonlocal viewport_x
        nonlocal viewport_y

        diff_x = 0
        diff_y = 0
        player_position = game_state.player_position

        if player_position[0] > viewport_x + viewport_width // 2 - viewport_margin:
            diff_x = (
                int(player_position[0]) - viewport_x - viewport_width // 2 + viewport_margin
            )
            # move the viewport to the right
            viewport_x = min(stage_width - viewport_width // 2, viewport_x + diff_x)
            if viewport_x == stage_width - viewport_width // 2:
                diff_x = 0

        if player_position[0] < viewport_x - viewport_width // 2 + viewport_margin:
            diff_x = -(
                viewport_x - viewport_width // 2 + viewport_margin - int(player_position[0])
            )
            # move the viewport to the left
            viewport_x = max(viewport_width // 2, viewport_x + diff_x)
            if viewport_x == viewport_width // 2:
                diff_x = 0

        if player_position[1] > viewport_y + viewport_height // 2 - viewport_margin:
            diff_y = (
                int(player_position[1]) - viewport_y - viewport_height // 2 + viewport_margin
            )
            # move the viewport up
            viewport_y = min(
                stage_height - viewport_height // 2,
                viewport_y + diff_y,
            )
            if viewport_y == stage_height - viewport_height // 2:
                diff_y = 0

        if player_position[1] < viewport_y - viewport_height // 2 + viewport_margin:
            diff_y = -(
                viewport_y - viewport_height // 2 + viewport_margin - int(player_position[1])
            )
            # move the viewport down
            viewport_y = max(
                viewport_height // 2,
                viewport_y + diff_y,
            )
            if viewport_y == viewport_height // 2:
                diff_y = 0
        # translate the window by the difference
        window.view = window.view.translate((-diff_x, -diff_y, 0))

    def reset_spawners():
        nonlocal time_since_last_asteroid_spawn
        nonlocal time_since_last_enemy_spawn
        nonlocal time_since_last_powerup_spawn

        time_since_last_asteroid_spawn = asteroid_spawn_interval
        time_since_last_enemy_spawn = enemy_spawn_interval
        time_since_last_powerup_spawn = 0

        asteroids.clear()
        enemies.clear()
        powerups.clear()

    def remove_non_essential_objects():
        for obj in game_objects:
            obj.dead = True
            obj.batch = None
            obj.child_objects = []  # clear the list
        game_objects.clear()

    def handle_level_change():
        nonlocal level
        nonlocal change_level

        # if change_level
        if level == 0:
            load_stage_1()
            level = 1
        elif level == 1:
            # check if the level has to change based on the score
            if score > 10:
                print("changing level")

                # remove all objects
                remove_non_essential_objects()
                # reset spawners
                reset_spawners()

                load_stage_2()
                level = 2

    # update loop
    def update(dt):
        handle_level_change()

        health_bars.clear()
        objects_to_add = []  # list of new objects to add

        # update viewport
        update_viewport()

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

            # if object is an enemy
            if obj.type == "enemy":
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
            x=viewport_x + viewport_width // 2 - 10,
            y=viewport_y + viewport_height // 2 - 10,
            anchor_x="right",
            anchor_y="top",
            batch=gui_batch,
            group=groups[0],
        )


    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
