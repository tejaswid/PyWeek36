import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes


from modules.game_assets import GameAssets
from modules.player import Player
from modules.background import Background
from modules.game_state import GameState

from modules.powerup_spawner import PowerupSpawner
from modules.asteroid_spawner import AsteroidSpawner
from modules.enemy_spawner import EnemySpawner
from modules.dark_matter_spawner import DarkMatterSpawner
from modules.boss_spawner import BossSpawner


def run():
    print(pyglet.version)

    game_state = GameState()

    # create the game window - size is 1000px x 1000px
    window = pyglet.window.Window(
        width=game_state.viewport_width,
        height=game_state.viewport_height,
        caption="The game",
        resizable=False,
    )

    # Store objects in a batch to load them efficiently
    gui_batch = pyglet.graphics.Batch()
    main_batch = pyglet.graphics.Batch()

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

    # spawners
    asteroid_spawner = AsteroidSpawner(assets, game_state, main_batch, groups[5])
    enemy_spawner = EnemySpawner(assets, game_state, main_batch, groups[5])
    powerup_spawner = PowerupSpawner(assets, game_state, main_batch, groups[5])
    dark_matter_spawner = DarkMatterSpawner(assets, game_state, main_batch, groups[4])
    boss_spawner = BossSpawner(assets, game_state, main_batch, groups[3])

    # score
    score_label = None
    score = 0

    # change mouse cursor
    cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
    window.set_mouse_cursor(cursor)

    def window_to_world(x, y):
        return (
            x + game_state.viewport_x - game_state.viewport_width // 2,
            y + game_state.viewport_y - game_state.viewport_height // 2,
        )

    def world_to_window(x, y):
        return (
            x - game_state.viewport_x + game_state.viewport_width // 2,
            y - game_state.viewport_y + game_state.viewport_height // 2,
        )

    def get_camera_bottom_left():
        return (-window.view[12], -window.view[13])

    def get_camera_centre():
        camera_bl_x, camera_bl_y = get_camera_bottom_left()
        print(" camera bottom left: {}, {}".format(camera_bl_x, camera_bl_y))
        return (
            camera_bl_x + game_state.viewport_width // 2,
            camera_bl_y + game_state.viewport_height // 2,
        )

    def reset_camera():
        # get current corner of the camera
        camera_bl_x, camera_bl_y = get_camera_bottom_left()
        # compute difference between current corner and desired corner
        diff_x = (game_state.viewport_x - game_state.viewport_width // 2) - camera_bl_x
        diff_y = (game_state.viewport_y - game_state.viewport_height // 2) - camera_bl_y
        # translate the camera by the difference
        window.view = window.view.translate((-diff_x, -diff_y, 0))

    # drawing items on screen
    @window.event
    def on_draw():
        window.clear()

        gui_batch.draw()
        main_batch.draw()
        

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
        game_state.background_sprite = Background(
            assets,
            level=1,
            x=game_state.stage_width // 2,
            y=game_state.stage_height // 2,
            batch=main_batch,
            group=groups[0],
        )

        # spawn the player
        player_1 = Player(
            assets, game_state, x=700, y=700, batch=main_batch, group=groups[5]
        )

        # reset the view_port
        game_state.reset_viewport()
        # reset the camera
        reset_camera()

        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)

    # loads the second scene
    def load_stage_2():
        # create an instance of the background centred on the stage
        game_state.background_sprite = Background(
            assets,
            level=2,
            x=game_state.stage_width // 2,
            y=game_state.stage_height // 2,
            batch=main_batch,
            group=groups[0],
        )

        # spawn the player
        player_1 = Player(
            assets, game_state, x=200, y=200, batch=main_batch, group=groups[5]
        )

        # reset the view_port
        game_state.reset_viewport()

        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)
        # window.view = window.view.translate(
        #     (-game_state.viewport_x + game_state.viewport_width // 2, -game_state.viewport_y + game_state.viewport_height // 2, 0)
        # )

        # reset the camera
        reset_camera()

    def draw_health_bar(obj):
        if obj.type in ["bullet", "dark_matter"]:
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
            batch=main_batch,
        )
        # the health bars need to be added to a list so that the objects do not go out of scope.
        # this is because rendering using batch needs the objects to be in scope during the draw call.
        health_bars_to_add = [health_bar]
        health_bars.extend(health_bars_to_add)

        damage_label = obj.draw_damage_label(main_batch)
        if damage_label is not None:
            damage_labels_to_add = [damage_label]
            frames_persistent = 25
            damage_labels.append(tuple((damage_labels_to_add, frames_persistent)))

    def handle_out_of_bounds(obj):
        # if object is an asteroid or bullet, remove it if it goes out of bounds
        if obj.type in ["asteroid", "bullet"]:
            if (
                (obj.x + obj.width // 2) < 0
                or (obj.x - obj.width // 2) > game_state.stage_width
                or (obj.y + obj.height // 2) < 0
                or (obj.y - obj.height // 2) > game_state.stage_height
            ):
                obj.dead = True

        # if object is a player or enemy, bounce it back if it goes out of bounds
        if obj.type in ["player", "enemy"]:
            if (obj.x - obj.width // 2) <= 0:
                obj.velocity[0] = -obj.velocity[0]
                obj.x = obj.width // 2

            if (obj.x + obj.width // 2) >= game_state.stage_width:
                obj.velocity[0] = -obj.velocity[0]
                obj.x = game_state.stage_width - obj.width // 2

            if (obj.y - obj.height // 2) <= 0:
                obj.velocity[1] = -obj.velocity[1]
                obj.y = obj.height // 2

            if (obj.y + obj.height // 2) >= game_state.stage_height:
                obj.velocity[1] = -obj.velocity[1]
                obj.y = game_state.stage_height - obj.height // 2

    def update_viewport():
        diff_x = 0
        diff_y = 0
        player_position = game_state.player_position

        new_viewport_x, new_viewport_y = game_state.get_viewport()

        if (
            player_position[0]
            > game_state.viewport_x
            + game_state.viewport_width // 2
            - game_state.viewport_margin
        ):
            diff_x = (
                int(player_position[0])
                - game_state.viewport_x
                - game_state.viewport_width // 2
                + game_state.viewport_margin
            )
            # move the viewport to the right
            new_viewport_x = min(
                game_state.stage_width - game_state.viewport_width // 2,
                game_state.viewport_x + diff_x,
            )
            if (
                new_viewport_x
                == game_state.stage_width - game_state.viewport_width // 2
            ):
                diff_x = 0

        if (
            player_position[0]
            < game_state.viewport_x
            - game_state.viewport_width // 2
            + game_state.viewport_margin
        ):
            diff_x = -(
                game_state.viewport_x
                - game_state.viewport_width // 2
                + game_state.viewport_margin
                - int(player_position[0])
            )
            # move the viewport to the left
            new_viewport_x = max(
                game_state.viewport_width // 2, game_state.viewport_x + diff_x
            )
            if new_viewport_x == game_state.viewport_width // 2:
                diff_x = 0

        if (
            player_position[1]
            > game_state.viewport_y
            + game_state.viewport_height // 2
            - game_state.viewport_margin
        ):
            diff_y = (
                int(player_position[1])
                - game_state.viewport_y
                - game_state.viewport_height // 2
                + game_state.viewport_margin
            )
            # move the viewport up
            new_viewport_y = min(
                game_state.stage_height - game_state.viewport_height // 2,
                game_state.viewport_y + diff_y,
            )
            if (
                new_viewport_y
                == game_state.stage_height - game_state.viewport_height // 2
            ):
                diff_y = 0

        if (
            player_position[1]
            < game_state.viewport_y
            - game_state.viewport_height // 2
            + game_state.viewport_margin
        ):
            diff_y = -(
                game_state.viewport_y
                - game_state.viewport_height // 2
                + game_state.viewport_margin
                - int(player_position[1])
            )
            # move the viewport down
            new_viewport_y = max(
                game_state.viewport_height // 2,
                game_state.viewport_y + diff_y,
            )
            if new_viewport_y == game_state.viewport_height // 2:
                diff_y = 0
        # update viewport of the state
        game_state.update_viewport(new_viewport_x, new_viewport_y)

        # translate the window by the difference
        window.view = window.view.translate((-diff_x, -diff_y, 0))

    def reset_spawners():
        asteroid_spawner.reset()
        enemy_spawner.reset()
        powerup_spawner.reset()
        dark_matter_spawner.reset()
        boss_spawner.reset()

    def remove_non_essential_objects():
        for obj in game_objects:
            obj.dead = True
            obj.batch = None
            obj.child_objects = []  # clear the list
        game_objects.clear()

        game_state.background_sprite.batch = None

    def handle_level_change():
        # if change_level
        if game_state.level == 0:
            load_stage_1()
            game_state.level = 1
        elif game_state.level == 1:
            # check if the level has to change based on the score
            if score > game_state.score_level_2:
                print("changing level")

                # remove all objects
                remove_non_essential_objects()
                # reset spawners
                reset_spawners()

                load_stage_2()
                game_state.level = 2

    # update loop
    def update(dt):
        handle_level_change()

        health_bars.clear()
        objects_to_add = []  # list of new objects to add

        # update viewport
        update_viewport()

        # spawn asteroids if necessary
        objects_to_add.extend(asteroid_spawner.spawn(dt))
        # spawn enemies if required
        objects_to_add.extend(enemy_spawner.spawn(dt))
        # spawn powerups if required
        objects_to_add.extend(powerup_spawner.spawn(dt))
        # spawn dark matter if required
        objects_to_add.extend(dark_matter_spawner.spawn(dt))
        # spawn boss if required
        objects_to_add.extend(boss_spawner.spawn(dt))

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
                    asteroid_spawner.remove(obj)
                # if it is an enemy remove it from the list of enemies
                if obj.type == "enemy":
                    if obj.died_by_player:
                        score += obj.score  # increase score
                    enemy_spawner.remove(obj)
                # if it is a powerup remove it from the list of powerups
                if obj.type == "powerup":
                    powerup_spawner.remove(obj)
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
            x=game_state.viewport_x + game_state.viewport_width // 2 - 10,
            y=game_state.viewport_y + game_state.viewport_height // 2 - 10,
            anchor_x="right",
            anchor_y="top",
            batch=gui_batch,
            group=groups[0],
        )

    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
