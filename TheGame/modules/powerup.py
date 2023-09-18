import random

from modules.game_objects import GameObject
import pyglet.clock


class Powerup(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        self.img = game_assets.image_assets["img_powerup"]
        self.max_time = 8

        super(Powerup, self).__init__(img=self.img, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, self.max_time)

        self.assets = game_assets
        self.type = "powerup"

        # spawn
        self.rotation = random.uniform(0, 360)
        # movement - only visual
        self.angular_velocity = random.uniform(-100, 100)    
        # collision
        self.collision_radius = 5
        # time left
        self.time_left = self.max_time


    def update_object(self, dt):
        # update rotation - just for visual effect
        self.rotation += self.angular_velocity * dt

        # update time left
        self.time_left -= dt

    def handle_collision_with(self, other_object):
        # handle collision with player
        if other_object.type == "player":
            if self.has_collided_with(other_object):
                self.dead = True
                print("powerup collided with player")
                other_object.take_damage(-20)   # give health to player
