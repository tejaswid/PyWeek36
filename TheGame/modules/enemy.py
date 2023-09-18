import math

from modules.game_objects import GameObject
from modules import utils

class Enemy(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        
        self.img = game_assets.image_assets["img_enemy"]
        super(Enemy, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.type = "enemy"

        # movement
        self.speed = 50
        self.player_x = None
        self.player_y = None
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 5
        # health
        self.max_health = 100
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 30

    def seek_player(self, player_x, player_y):
        self.player_x = player_x
        self.player_y = player_y

    def update_object(self, dt):
        # TODO add collision detection
        self.update_velocity()
        self.update_position(dt)

    def update_velocity(self):
        if self.player_x is not None and self.player_y is not None:
            # compute direction towards player
            self.velocity = utils.compute_velocity(self.speed, self.x, self.y, self.player_x, self.player_y)

    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def handle_collision_with(self, other_object):
        # handle collision with bullet
        if other_object.type == "bullet":
            if self.has_collided_with(other_object):
                print("enemy collided with bullet")
                self.take_damage(other_object.damage)
                # remove bullet. again needed to possibly overcome the framerate issue
                other_object.dead = True

        if other_object.type in ["player", "asteroid"]:
            if self.has_collided_with(other_object):
                print("enemy collided with ", other_object.type)
                self.take_damage(other_object.damage)
                # player takes damage, needed to possibly overcome the framerate issue
                other_object.take_damage(self.damage)
        