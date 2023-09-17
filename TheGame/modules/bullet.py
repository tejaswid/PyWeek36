import math

from pyglet.window import key
from pyglet.window import mouse

from modules.game_objects import GameObject

class Bullet(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        
        bullet_image = game_assets.image_assets["img_bullet"]
        super(Bullet, self).__init__(img=bullet_image, *args, **kwargs)

        self.assets = game_assets
        self.type = "bullet"

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.event_handlers = [self, self.key_handler, self.mouse_handler]

        self.speed = 500

    def update_object(self, dt):
        # TODO add collision detection

        self.update_velocity(dt)
        self.update_position(dt)

    # compute the velocity of the bullet
    def update_velocity(self, dt):
        pass

    # update the position of the bullet based on the velocity
    def update_position(self, dt):
        pass