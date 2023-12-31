import math
import random

from pyglet.image import Animation

from modules import utils
from modules.game_object import GameObject
from modules.bullet import Bullet


class Boss(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.boss_1_sprites = [
            game_assets.image_assets["img_boss_1_s1"],
            game_assets.image_assets["img_boss_1_s2"],
            game_assets.image_assets["img_boss_1_s3"],
            game_assets.image_assets["img_boss_1_s4"],
        ]
        self.boss_1_animation = Animation.from_image_sequence(
            self.boss_1_sprites, duration=0.3, loop=True
        )
        self.default_sprite = self.boss_1_animation

        if game_state.level == 2:
            self.boss_2_sprites = [
                game_assets.image_assets["img_boss_2_s1"],
                game_assets.image_assets["img_boss_2_s2"],
            ]
            self.boss_2_animation = Animation.from_image_sequence(
                self.boss_2_sprites, duration=0.3, loop=True
            )
            self.default_sprite = self.boss_2_animation

        super(Boss, self).__init__(img=self.default_sprite, *args, **kwargs)

        self.assets = game_assets
        self.type = "boss"
        self.game_state = game_state

        # spawn
        self.rotation = 0
        # movement
        self.speed = 0
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 50
        # health
        self.max_health = 1500
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 40

        # parameters for boss movement
        self.movement_modes = [
            "stand_and_fire",
            "seek_player",
            "seek_dark_matter",
            "teleport",
            "dash_to_player",
            "temporary_shield",
        ]
        self.current_movement_mode = "seek_player"
        self.time_since_last_mode_change = 0
        self.mode_change_interval = 5

        # parameters for stand and fire bullets in spiral mode
        self.sf_speed = 10  # speed of boss in this mode
        self.sf_bullet_speed = 600  # speed of bullets fired in this mode
        self.sf_num_bullets = 10  # number of bullets to fire in a spiral
        self.sf_bullet_cooldown = 0.3  # time between firing bullets
        self.sf_bullet_timer = self.sf_bullet_cooldown  # timer for firing bullets
        self.sf_bullet_set = 0  # index of the fired set of bullets
        self.sf_bullet_offset = math.radians(5)  # offset between each set of bullets

        # parameters for seek player mode
        self.sp_speed = 80  # speed of boss in this mode
        self.sp_bullet_speed = 800  # speed of bullets fired in this mode
        self.sp_bullet_cooldown = 3  # time between firing bullets
        self.sp_bullet_timer = self.sf_bullet_cooldown  # timer for firing bullets

        # parameters for temporary shield mode
        self.shield_max_health = 100
        self.shield_current_health = self.shield_max_health
        self.shield_active = False

        self.boss_1_shield_sprites = [
            game_assets.image_assets["img_boss_1_with_shield_s1"],
            game_assets.image_assets["img_boss_1_with_shield_s2"],
            game_assets.image_assets["img_boss_1_with_shield_s3"],
        ]
        self.boss_1_shield_animation = Animation.from_image_sequence(
            self.boss_1_shield_sprites, duration=0.3, loop=True
        )
        self.shield_sprite = self.boss_1_shield_animation

        self.boss_2_shield_sprites = [
            game_assets.image_assets["img_boss_2_with_shield_s1"],
            game_assets.image_assets["img_boss_2_with_shield_s2"],
        ]
        self.boss_2_shield_animation = Animation.from_image_sequence(
            self.boss_2_shield_sprites, duration=0.3, loop=True
        )
        if game_state.level == 2:
            self.shield_sprite = self.boss_2_shield_animation

        self.bullet_boss_1_1_sprites = [
            game_assets.image_assets["img_bullet_boss_1_s1"],
            game_assets.image_assets["img_bullet_boss_1_s2"],
        ]
        self.bullet_boss_2_1_sprites = [
            game_assets.image_assets["img_bullet_boss_3_s1"],
            game_assets.image_assets["img_bullet_boss_3_s2"],
            game_assets.image_assets["img_bullet_boss_3_s3"],
            game_assets.image_assets["img_bullet_boss_3_s4"],
            game_assets.image_assets["img_bullet_boss_3_s5"],
            game_assets.image_assets["img_bullet_boss_3_s6"],
            game_assets.image_assets["img_bullet_boss_3_s7"],
        ]
        if game_state.level == 1:
            self.boss_bullet_1_animation = Animation.from_image_sequence(
                self.bullet_boss_1_1_sprites, duration=0.3, loop=True
            )
        else:
            self.boss_bullet_1_animation = Animation.from_image_sequence(
                self.bullet_boss_2_1_sprites, duration=0.3, loop=True
            )

        self.bullet_boss_1_2_sprites = [
            game_assets.image_assets["img_bullet_boss_4_s1"],
            game_assets.image_assets["img_bullet_boss_4_s2"],
        ]
        self.bullet_boss_2_2_sprites = [
            game_assets.image_assets["img_bullet_boss_2_s1"],
            game_assets.image_assets["img_bullet_boss_2_s2"],
        ]

        if game_state.level == 1:
            self.boss_bullet_2_animation = Animation.from_image_sequence(
                self.bullet_boss_1_2_sprites, duration=0.3, loop=True
            )
        else:
            self.boss_bullet_2_animation = Animation.from_image_sequence(
                self.bullet_boss_2_2_sprites, duration=0.3, loop=True
            )

        # parameters for dash to player mode
        self.dash_start_x = self.x
        self.dash_start_y = self.y
        self.dash_speed = 500
        self.dash_max_distance = 200
        self.dash_current_distance = 0

        # parameters for seek dark matter mode
        self.sdm_closest_dm_x = None
        self.sdm_closest_dm_y = None
        self.sdm_closest_dm_index = None
        self.sdm_speed = 100

    def update_object(self, dt):
        self.time_since_last_mode_change += dt
        if self.time_since_last_mode_change > self.mode_change_interval:
            self.time_since_last_mode_change = 0  # reset timer
            self.current_movement_mode = random.choice(self.movement_modes)
            self.mode_change_interval = random.randint(5, 10)
            self.dash_current_distance = 0

        if self.current_movement_mode == "stand_and_fire":
            self.stand_and_fire_bullets_in_spiral(dt)
        elif self.current_movement_mode == "seek_player":
            self.seek_player(dt)
        elif self.current_movement_mode == "teleport":
            self.teleport()
        elif self.current_movement_mode == "temporary_shield":
            self.temporary_shield()
        elif self.current_movement_mode == "dash_to_player":
            self.dash_to_player(dt)
        elif self.current_movement_mode == "seek_dark_matter":
            self.seek_dark_matter(dt)
        else:
            self.seek_player(dt)

    def set_movement_mode(self, mode):
        self.movement_mode = mode

    def fire_bullet(self, target_x, target_y):
        bullet = Bullet(
            self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group
        )
        bullet.image = self.boss_bullet_2_animation
        bullet.set_rotation(target_x, target_y)
        bullet.set_velocity(target_x, target_y, self.sp_bullet_speed)
        bullet.collision_radius = 20
        self.child_objects.append(bullet)
        self.assets.sound_assets["snd_bullet_fire"].play()

    def fire_spiral_bullet(self, firing_angle):
        start_x = self.x + self.collision_radius * math.cos(firing_angle)
        start_y = self.y + self.collision_radius * math.sin(firing_angle)

        target_x = self.x + (self.collision_radius + 1) * math.cos(firing_angle)
        target_y = self.y + (self.collision_radius + 1) * math.sin(firing_angle)

        bullet = Bullet(
            self.assets, x=start_x, y=start_y, batch=self.batch, group=self.group
        )
        bullet.image = self.boss_bullet_1_animation
        bullet.set_type("boss")
        bullet.set_rotation(target_x, target_y)
        bullet.set_velocity(target_x, target_y, self.sf_bullet_speed)
        bullet.collision_radius = 20
        self.child_objects.append(bullet)
        self.assets.sound_assets["snd_bullet_fire"].play()

    def stand_and_fire_bullets_in_spiral(self, dt):
        # fire bullets in a spiral
        self.sf_bullet_timer += dt
        if self.sf_bullet_timer > self.sf_bullet_cooldown:
            self.sf_bullet_timer = 0

            for i in range(self.sf_num_bullets):
                firing_angle = (
                    i * 2 * math.pi / self.sf_num_bullets
                    + self.sf_bullet_set * self.sf_bullet_offset
                )
                self.fire_spiral_bullet(firing_angle)

            self.sf_bullet_set += 1
            # small random velocity
            self.velocity = utils.random_velocity(self.sf_speed)

        self.rotation = 0
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def seek_player(self, dt):
        # in this mode the boss seeks the player and fires bullets at the player
        player_x = self.game_state.player_position[0]
        player_y = self.game_state.player_position[1]

        if player_x is None or player_y is None:
            return

        # compute direction towards player
        self.velocity = utils.compute_velocity(
            self.sp_speed, self.x, self.y, player_x, player_y
        )
        # self.rotation = -math.degrees(math.atan2(player_y - self.y, player_x - self.x))
        self.rotation = 0
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

        # fire bullets at the player
        self.sp_bullet_timer += dt
        if self.sp_bullet_timer >= self.sp_bullet_cooldown:
            self.sp_bullet_timer = 0
            self.fire_bullet(player_x, player_y)

    def teleport(self):
        # TODO if possible stay invisible for a while
        # teleport to a random location
        self.x = random.randint(0, self.game_state.stage_width)
        self.y = random.randint(0, self.game_state.stage_height)
        self.mode_change_interval = random.randint(5, 10)
        self.current_movement_mode = "seek_player"

    def add_shield_sprite(self):
        self.image = self.shield_sprite

    def remove_shield_sprite(self):
        self.image = self.default_sprite

    def temporary_shield(self):
        self.shield_active = True
        self.add_shield_sprite()

    def dash_to_player(self, dt):
        if self.dash_current_distance == 0:
            self.dash_start_x = self.x
            self.dash_start_y = self.y

            player_x = self.game_state.player_position[0]
            player_y = self.game_state.player_position[1]

            if player_x is None or player_y is None:
                return

            self.velocity = utils.compute_velocity(
                self.dash_speed,
                self.dash_start_x,
                self.dash_start_y,
                player_x,
                player_y,
            )

            # self.rotation = -math.degrees(
            #     math.atan2(player_y - self.y, player_x - self.x)
            # )
            # boss looks odd when rotating
            self.rotation = 0

            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt

            self.dash_current_distance = utils.distance(
                (self.dash_start_x, self.dash_start_y), (self.x, self.y)
            )
        else:
            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt
            self.dash_current_distance = utils.distance(
                (self.dash_start_x, self.dash_start_y), (self.x, self.y)
            )
            if self.dash_current_distance >= self.dash_max_distance:
                self.dash_current_distance = 0
                self.current_movement_mode = "seek_player"
                self.mode_change_interval = random.randint(5, 10)

    def find_closest_dark_matter(self):
        closest_distance = 99999999
        for i, dm_position in enumerate(self.game_state.dark_matter_positions):
            distance_to_dm = utils.distance((self.x, self.y), dm_position)
            if distance_to_dm < closest_distance:
                closest_distance = distance_to_dm
                self.sdm_closest_dm_x = dm_position[0]
                self.sdm_closest_dm_y = dm_position[1]
                self.sdm_closest_dm_index = i

    def seek_dark_matter(self, dt):
        # seeks the closest dark matter and replaces it at another place
        if self.sdm_closest_dm_x is None or self.sdm_closest_dm_y is None:
            self.find_closest_dark_matter()
            # move towards the closest dark matter
            self.velocity = utils.compute_velocity(
                self.sdm_speed,
                self.x,
                self.y,
                self.sdm_closest_dm_x,
                self.sdm_closest_dm_y,
            )

            # self.rotation = -math.degrees(
            #     math.atan2(
            #         self.sdm_closest_dm_y - self.y,
            #         self.sdm_closest_dm_x - self.x,
            #     )
            # )
            self.rotation = 0
            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt
        else:
            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt

    def handle_collision_with(self, other_object):
        # handle collision with bullet
        if other_object.type == "bullet" and other_object.bullet_type == "player":
            if self.has_collided_with(other_object):
                # #print("boss collided with player bullet")
                self.assets.sound_assets["snd_bullet_hit"].play()
                self.take_damage(other_object.damage)
                # if I am dead, then I was killed by the player
                if self.dead:
                    self.died_by_player = True
        # handle collision with player, enemy and other asteroids
        if other_object.type == "player":
            if self.has_collided_with(other_object):
                # #print("boss collided with player")
                self.assets.sound_assets["snd_collision"].play()
                self.take_damage(other_object.damage)
                other_object.take_damage(self.damage)
        if (
            other_object.type == "dark_matter"
            and self.current_movement_mode == "seek_dark_matter"
        ):
            if self.has_collided_with(other_object):
                # #print("boss collided with dark matter")
                other_object.dead = True
                self.game_state.dark_matter_positions.pop(self.sdm_closest_dm_index)
                self.sdm_closest_dm_x = None
                self.sdm_closest_dm_y = None
                self.sdm_closest_dm_index = None
