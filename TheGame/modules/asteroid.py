import math
import random

from modules.game_objects import GameObject
from modules import utils

class Asteroid(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        
        self.img = game_assets.image_assets["img_asteroid"]
        super(Asteroid, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.type = "asteroid"

        # movement
        self.speed = 0
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 5
        # health
        self.max_health = 50
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 2

    def set_initial_properties(self, x, y):
        # spawn pose
        self.x = x
        self.y = y
        self.rotation = random.uniform(0, 360)
        # spawn random linear movement
        self.speed = random.uniform(5, 30)
        self.velocity = utils.random_velocity(self.speed)
        # spawn random angular movement
        self.angular_velocity = random.uniform(-100, 100)

    def update_object(self, dt):
        self.update_velocity()
        self.update_position(dt)

    def update_velocity(self):
        pass

    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.rotation += self.angular_velocity * dt
        print(self.rotation)

    def handle_collision_with(self, other_object):
        # handle collision with bullet
        if other_object.type == "bullet":
            if self.has_collided_with(other_object):
                print("asteroid collided with bullet")
                self.take_damage(other_object.damage)
        # handle collision with player, enemy and other asteroids
        if other_object.type in ["player", "enemy", "asteroid"]:
            if self.has_collided_with(other_object):
                print("asteroid collided with player")
                self.take_damage(other_object.damage)
                other_object.take_damage(self.damage)
        