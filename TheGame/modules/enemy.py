import math
import random

from pyglet.image import Animation

from modules.game_object import GameObject
from modules.bullet import Bullet
from modules import utils


class Enemy(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        default_sprite = game_assets.image_assets["img_enemy"]
        super(Enemy, self).__init__(img=default_sprite, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "enemy"

        # movement
        self.speed = 50
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 10
        # health
        self.max_health = 100
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 30
        # score
        self.score = 10
        # repulsion with other enemies
        self.repulsion_distance = 50
        self.repulsion_factor = 2

        self.enemy_types = ["seeker", "shooter", "spear"]
        self.enemy_type = random.choice(self.enemy_types)
        self.update_sprite()

        # parameters for shooter
        self.shooter_bullet_cooldown = 3
        self.shooter_bullet_timer = 0
        self.shooter_bullet_speed = 100
        self.shooter_bullet_radius = 10

        # parameters for spear
        self.spear_speed = 600
        self.spear_activation_distance = 300
        self.spear_active = False
        self.spear_start_x = self.x
        self.spear_start_y = self.y
        self.spear_max_distance = 500
        self.spear_current_distance = 0
        self.spear_cooldown = 2
        self.spear_timer = 0

    def update_sprite(self):
        if self.enemy_type == "seeker":
            # self.image = self.assets.image_assets["img_enemy_seeker"]
            self.enemy_seeker_sprites = [self.assets.image_assets["img_enemy_seeker_s1"],
                               self.assets.image_assets["img_enemy_seeker_s2"],
                               self.assets.image_assets["img_enemy_seeker_s1"],
                               self.assets.image_assets["img_enemy_seeker_s3"]]
            self.enemy_seeker_animation = Animation.from_image_sequence(self.enemy_seeker_sprites, duration=0.3, loop=True)
            self.image = self.enemy_seeker_animation
        elif self.enemy_type == "shooter":
            self.enemy_shooter_sprites = [self.assets.image_assets["img_enemy_shooter_s1"],
                               self.assets.image_assets["img_enemy_shooter_s2"],
                               self.assets.image_assets["img_enemy_shooter_s3"],
                               self.assets.image_assets["img_enemy_shooter_s4"],
                               self.assets.image_assets["img_enemy_shooter_s5"]]
            self.enemy_shooter_animation = Animation.from_image_sequence(self.enemy_shooter_sprites, duration=0.3, loop=True)
            self.image = self.enemy_shooter_animation
        elif self.enemy_type == "spear":
            self.image = self.assets.image_assets["img_enemy_spear"]
        else:
            self.image = self.assets.image_assets["img_enemy"]

    def update_object(self, dt):
        if self.enemy_type == "seeker":
            self.seek_player(dt)
        elif self.enemy_type == "shooter":
            self.shooter(dt)
        elif self.enemy_type == "spear":
            self.spear(dt)
        else:
            self.seek_player(dt)

    def seek_player(self, dt):
        # compute velocity towards player
        player_x = self.game_state.player_position[0]
        player_y = self.game_state.player_position[1]
        if player_x is not None and player_y is not None:
            # compute direction towards player
            self.velocity = utils.compute_velocity(
                self.speed, self.x, self.y, player_x, player_y
            )

        # update position
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.rotation = -math.degrees(math.atan2(player_y - self.y, player_x - self.x))

    def shooter(self, dt):
        # random motion and fire a single bullet towards player
        self.shooter_bullet_timer += dt
        if self.shooter_bullet_timer > self.shooter_bullet_cooldown:
            self.shooter_bullet_timer = 0

            # shoot bullet towards player
            player_x = self.game_state.player_position[0]
            player_y = self.game_state.player_position[1]
            if player_x is not None and player_y is not None:
                bullet = Bullet(
                    self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group
                )
                bullet.set_type("enemy")
                bullet.set_rotation(player_x, player_y)
                bullet.set_velocity(player_x, player_y, self.shooter_bullet_speed)
                bullet.collision_radius = self.shooter_bullet_radius
                self.child_objects.append(bullet)

            # small random velocity
            self.velocity = utils.random_velocity(self.speed)

        player_x = self.game_state.player_position[0]
        player_y = self.game_state.player_position[1]
        if player_x is not None and player_y is not None:
            self.rotation = -math.degrees(
                math.atan2(player_y - self.y, player_x - self.x)
            )
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def spear(self, dt):
        if self.spear_timer < self.spear_cooldown and not self.spear_active:
            self.spear_timer += dt
            return

        # stay still and if player comes close, dash towards player
        if not self.spear_active:
            # check if the player is close enough to activate the spear
            player_x = self.game_state.player_position[0]
            player_y = self.game_state.player_position[1]

            if player_x is None or player_y is None:
                return

            # compute distance to player
            distance = utils.distance((self.x, self.y), (player_x, player_y))
            # activate spear
            if distance < self.spear_activation_distance:
                self.spear_active = True
                self.spear_start_x = self.x
                self.spear_start_y = self.y
                self.spear_current_distance = 0
                self.velocity = utils.compute_velocity(
                    self.spear_speed,
                    self.spear_start_x,
                    self.spear_start_y,
                    player_x,
                    player_y,
                )
            self.rotation = -math.degrees(
                math.atan2(player_y - self.y, player_x - self.x)
            )

        else:
            if self.spear_current_distance >= self.spear_max_distance:
                self.spear_active = False
                self.spear_current_distance = 0
                self.velocity = [0, 0]
                self.spear_timer = 0
                return

        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.spear_current_distance += utils.distance(
            (self.spear_start_x, self.spear_start_y), (self.x, self.y)
        )

    def compute_repulsion(self, other_object):
        if other_object.type != "enemy":
            return

        # TODO: for now this updates the position, instead add velocity or force based control
        distance = utils.distance((self.x, self.y), (other_object.x, other_object.y))
        if distance < self.repulsion_distance:
            # add a repulsion effect to the objects
            old_self_x = self.x
            old_self_y = self.y
            old_other_object_x = other_object.x
            old_other_object_y = other_object.y

            self.x += (old_self_x - old_other_object_x) * self.repulsion_factor
            self.y += (old_self_y - old_other_object_y) * self.repulsion_factor

            other_object.x += (
                old_other_object_x - old_self_x
            ) * other_object.repulsion_factor
            other_object.y += (
                old_other_object_y - old_self_y
            ) * other_object.repulsion_factor

    def handle_collision_with(self, other_object):
        # handle collision with bullet
        if other_object.type == "bullet" and other_object.bullet_type == "player":
            if self.has_collided_with(other_object):
                print("enemy collided with player bullet")
                self.take_damage(other_object.damage)
                # remove bullet. again needed to possibly overcome the framerate issue
                other_object.dead = True
                # if I am dead, then I was killed by the player
                if self.dead:
                    self.died_by_player = True

        if other_object.type in ["player", "asteroid"]:
            if self.has_collided_with(other_object):
                print("enemy collided with ", other_object.type)
                self.take_damage(other_object.damage)
                # player takes damage, needed to possibly overcome the framerate issue
                other_object.take_damage(self.damage)
