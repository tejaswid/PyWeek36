import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes


from modules.game_assets import GameAssets
from modules.player import Player
from modules.background import Background
from modules.foreground import Foreground
from modules.game_state import GameState
from modules.story import Story

from modules.powerup_spawner import PowerupSpawner
from modules.asteroid_spawner import AsteroidSpawner
from modules.enemy_spawner import EnemySpawner
from modules.dark_matter_spawner import DarkMatterSpawner
from modules.boss_spawner import BossSpawner


def run():
    print(pyglet.version)

    game_state = GameState()

    # create the game window
    window = pyglet.window.Window(
        width=game_state.viewport_width,
        height=game_state.viewport_height,
        caption="The game",
        resizable=False,
    )

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()

    # groups - 0 drawn first, 10 drawn last
    groups = []
    for i in range(10):
        # groups.append(pyglet.graphics.OrderedGroup(i))  # used in older version
        groups.append(pyglet.graphics.Group(i))

    # load required assets
    assets = GameAssets()

    # background music score
    background_music = assets.sound_assets["snd_default_bkg"]
    boss_bgm = assets.sound_assets["snd_boss_bkg"]
    p = pyglet.media.Player()
    p.queue(background_music)
    p.queue(boss_bgm)
    p.queue(background_music)
    p.loop = True
    p.play()

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
        main_batch.draw()

    # handle keyboard inputs
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.A:
            pass
        if game_state.level in [-1, 0, 0.5]:
            if symbol == key.SPACE:
                game_state.change_level = True
            return
        if game_state.level in [3, 4]:
            if symbol == key.R:
                game_state.change_level = True
            return

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

        if button == mouse.RIGHT:
            for obj in game_objects:
                if obj.type == "player":
                    obj.fire_tracer(x, y)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        # Note: x and y are in window coordinate frame
        # convert to world coordinate frame
        x, y = window_to_world(x, y)
        for obj in game_objects:
            if obj.type == "player":
                obj.update_rotation(x, y)

    def load_screen(level_name):
        name_to_id = {
            "title": -1,
            "instructions": 0.5,
            "won": 3,
            "game_over": 4,
        }

        game_state.background_sprite = Background(
            assets,
            level=name_to_id[level_name],
            x=game_state.stage_width // 2,
            y=game_state.stage_height // 2,
            batch=main_batch,
            group=groups[0],
        )
        # reset the view_port
        game_state.reset_viewport()
        # reset the camera
        reset_camera()



    def load_story():
        # create an instance of the background centred on the stage
        game_state.background_sprite = Background(
            assets,
            level=0,
            x=game_state.stage_width // 2,
            y=game_state.stage_height // 2,
            batch=main_batch,
            group=groups[0],
        )

        story_object = Story(
            assets,
            game_state,
            x=game_state.stage_width // 2,
            y=game_state.viewport_y - game_state.viewport_height // 2 - 200,
            batch=main_batch,
            group=groups[9],
        )

        game_objects.append(story_object)

        # reset the view_port
        game_state.reset_viewport()
        # reset the camera
        reset_camera()

    # loads the first stage
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

        # create some forground neublae
        fg_1 = Foreground(assets, x=300, y=500, batch=main_batch, group=groups[8])
        fg_2 = Foreground(assets, x=1800, y=1700, batch=main_batch, group=groups[8])
        game_objects.append(fg_1)
        game_objects.append(fg_2)

        # spawn the player
        player_1 = Player(
            assets, game_state, x=700, y=700, batch=main_batch, group=groups[5]
        )

        # spawn dark matter
        dark_matter_objects = dark_matter_spawner.spawn(0.1)
        for obj in dark_matter_objects:
            game_state.dark_matter_positions.append((obj.x, obj.y))

        # reset the view_port
        game_state.reset_viewport()
        # reset the camera
        reset_camera()

        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)
        game_objects.extend(dark_matter_objects)

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

        # create some forground neublae
        fg_1 = Foreground(assets, x=500, y=300, batch=main_batch, group=groups[8])
        fg_2 = Foreground(assets, x=1000, y=1200, batch=main_batch, group=groups[8])
        game_objects.append(fg_1)
        game_objects.append(fg_2)

        # spawn the player
        player_1 = Player(
            assets, game_state, x=200, y=200, batch=main_batch, group=groups[5]
        )

        # spawn dark matter
        dark_matter_objects = dark_matter_spawner.spawn(0.1)
        if len(game_state.dark_matter_positions) > 0:
            raise RuntimeError("dark matter positions not empty")

        for obj in dark_matter_objects:
            game_state.dark_matter_positions.append((obj.x, obj.y))

        # reset the view_port
        game_state.reset_viewport()

        # player was already created before
        window.push_handlers(player_1.key_handler)
        window.push_handlers(player_1.mouse_handler)
        game_objects.append(player_1)
        game_objects.extend(dark_matter_objects)

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

        if obj.type == "story":
            if obj.y >= 1.5 * game_state.viewport_height:
                obj.dead = True
                game_objects.remove(obj)

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
        game_state.dark_matter_positions.clear()
        game_state.revealed_dark_matter = 0
        boss_spawner.reset()


    def remove_non_essential_objects():
        for obj in game_objects:
            obj.dead = True
            obj.batch = None
            obj.child_objects = []  # clear the list
        game_objects.clear()

        game_state.background_sprite.batch = None

    def check_dark_matter_reveal_status_and_spawn_boss():
        if (
            game_state.revealed_dark_matter == len(game_state.dark_matter_positions)
            and game_state.should_spawn_boss
        ):
            print("revealed all dark matter. changing level")
            print("revealed dark matter: ", game_state.revealed_dark_matter)
            print("total dark matter: ", len(game_state.dark_matter_positions))
            game_state.should_spawn_boss = False
            game_objects.extend(boss_spawner.spawn(0.1))
            p.next_source()
            p.loop = True
            
    def handle_level_change():
        if game_state.level == -2:
            load_screen("title")
            game_state.level = -1

        if game_state.level == -1:
            if game_state.change_level:
                remove_non_essential_objects()
                reset_spawners()
                load_story()
                game_state.level = 0
                game_state.change_level = False

        if game_state.level == 0:
            if game_state.change_level:
                remove_non_essential_objects()
                reset_spawners()
                load_screen("instructions")
                game_state.level = 0.5
                game_state.change_level = False

        elif game_state.level == 0.5:
            if game_state.change_level:
                remove_non_essential_objects()
                reset_spawners()
                load_stage_1()
                game_state.level = 1
                game_state.change_level = False
                game_state.should_spawn_boss = True

        elif game_state.level == 1:
            check_dark_matter_reveal_status_and_spawn_boss()
            if game_state.change_level:
                # remove all objects
                remove_non_essential_objects()
                # reset spawners
                reset_spawners()
                load_stage_2()
                game_state.level = 2
                game_state.change_level = False
                game_state.should_spawn_boss = True                
                p.next_source()

        elif game_state.level == 2:
            check_dark_matter_reveal_status_and_spawn_boss()
            if game_state.change_level:
                # remove all objects
                remove_non_essential_objects()
                # reset spawners
                reset_spawners()
                if game_state.game_won:
                    print("game won")
                    load_screen("won")
                    game_state.level = 3
                else:
                    print("game over")
                    load_screen("game_over")
                    game_state.level = 4
                game_state.change_level = False
                game_state.should_spawn_boss = False
                damage_labels.clear()
                nonlocal score_label
                score_label.batch = None
                score_label.delete()
                score_label = None

        elif game_state.level == 3 or game_state.level == 4:
            if game_state.change_level:
                # remove all objects
                remove_non_essential_objects()
                # reset spawners
                reset_spawners()
                game_state.change_level = True
                game_state.level = 0.5
                game_state.should_spawn_boss = True

    # update loop
    def update(dt):
        handle_level_change()
        health_bars.clear()

        # return early for these levels
        if game_state.level == -1:
            return
        elif game_state.level == 0:
            for obj in game_objects:
                obj.update_object(dt)
            return
        elif game_state.level == 0.5:
            return
        elif game_state.level == 3:
            return
        elif game_state.level == 4:
            return

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
        new_dark_matter_objects = dark_matter_spawner.spawn(dt)
        if len(new_dark_matter_objects) > 0:
            print("adding dark matter")
            print(game_state.dark_matter_positions)
        for obj in new_dark_matter_objects:
            game_state.dark_matter_positions.append((obj.x, obj.y))
        objects_to_add.extend(new_dark_matter_objects)

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
                elif obj.type == "enemy":
                    if obj.died_by_player:
                        score += obj.score  # increase score
                    enemy_spawner.remove(obj)
                # if it is a powerup remove it from the list of powerups
                elif obj.type == "powerup":
                    powerup_spawner.remove(obj)
                # if player is dead, game over
                elif obj.type == "player":
                    game_state.level = 2
                    game_state.change_level = True
                    game_state.game_won = False
                    game_state.revealed_dark_matter = 0
                    game_state.dark_matter_positions.clear()                    
                elif obj.type == "dark_matter":
                    dark_matter_spawner.remove(obj)
                elif obj.type == "boss":
                    boss_spawner.remove(obj)
                    game_state.revealed_dark_matter = 0
                    game_state.dark_matter_positions.clear()
                    game_state.change_level = True
                    if game_state.level == 2:
                        game_state.game_won = True

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
            batch=main_batch,
            group=groups[9],
        )

    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
