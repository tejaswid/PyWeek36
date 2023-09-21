import math
import random

from modules import utils
from modules.game_object import GameObject
from modules.bullet import Bullet


class Boss(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_boss_3"]
        if game_state.level == 2:
            self.img = game_assets.image_assets["img_boss_2"]
        super(Boss, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.type = "boss"
        self.game_state = game_state

        # spawn
        self.rotation = 0
        # movement
        self.speed = 0
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 100
        # health
        self.max_health = 1000
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
        self.stand_and_fire_speed = 10  # speed of boss in this mode
        self.stand_and_fire_num_bullets = 10  # number of bullets to fire in a spiral
        self.stand_and_fire_bullet_cooldown = 0.4  # time between firing bullets
        self.stand_and_fire_bullet_timer = (
            self.stand_and_fire_bullet_cooldown
        )  # timer for firing bullets
        self.stand_and_fire_bullet_set = 0  # index of the fired set of bullets
        self.stand_and_fire_bullet_offset_per_set = math.radians(
            5
        )  # offset between each set of bullets

        self.fire_time = 5
        self.test_counter = 0

    def update_object(self, dt):
        self.time_since_last_mode_change += dt
        if self.time_since_last_mode_change > self.mode_change_interval:
            self.time_since_last_mode_change = 0  # reset timer
            self.current_movement_mode = random.choice(
                self.movement_modes
            )  # change mode
            self.mode_change_interval = random.randint(
                5, 10
            )  # change interval randomly

        if self.current_movement_mode == "stand_and_fire":
            self.stand_and_fire_bullets_in_spiral(dt)
        else:
            self.stand_and_fire_bullets_in_spiral(dt)

    def set_movement_mode(self, mode):
        self.movement_mode = mode

    def handle_collision_with(self, other_object):
        pass

    def fire_spiral_bullet(self, firing_angle):
        start_x = self.x + self.collision_radius * math.cos(firing_angle)
        start_y = self.y + self.collision_radius * math.sin(firing_angle)

        target_x = self.x + (self.collision_radius + 1) * math.cos(firing_angle)
        target_y = self.y + (self.collision_radius + 1) * math.sin(firing_angle)

        bullet = Bullet(
            self.assets, x=start_x, y=start_y, batch=self.batch, group=self.group
        )
        bullet.set_rotation(target_x, target_y)
        bullet.set_velocity(target_x, target_y)
        self.child_objects.append(bullet)

    def stand_and_fire_bullets_in_spiral(self, dt):
        # in this mode the boss is almost stationary and fires bullets in a spiral
        
        # fire bullets in a spiral
        self.stand_and_fire_bullet_timer += dt
        if self.stand_and_fire_bullet_timer > self.stand_and_fire_bullet_cooldown:
            self.stand_and_fire_bullet_timer = 0

            for i in range(self.stand_and_fire_num_bullets):
                firing_angle = (
                    i * 2 * math.pi / self.stand_and_fire_num_bullets
                    + self.stand_and_fire_bullet_set
                    * self.stand_and_fire_bullet_offset_per_set
                )
                self.fire_spiral_bullet(firing_angle)

            self.stand_and_fire_bullet_set += 1

            # small random velocity
            self.velocity = utils.random_velocity(self.stand_and_fire_speed)

        self.rotation = 0
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt