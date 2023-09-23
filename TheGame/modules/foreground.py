import random
import pyglet
from modules.game_object import GameObject


class Foreground(GameObject):
    def __init__(self, game_assets, *args, **kwargs):

        if (random.randint(1, 3) < 2):
            images = [game_assets.image_assets["img_foreground_1"]]
        else:
            images = [game_assets.image_assets["img_foreground_2"]]
        
        anim = pyglet.image.Animation.from_image_sequence(images, duration=0.5, loop=True)
        super(Foreground, self).__init__(img=anim, *args, **kwargs)

        self.assets = game_assets
        self.type = "foreground"

        # movement
        self.speed = 0
        self.velocity = [0, 0]
        self.collision_radius = None
        self.max_health = 0
        self.current_health = self.max_health
        self.damage = None

    def update_object(self, dt):
        pass

    def handle_collision_with(self, other_object):
        pass
