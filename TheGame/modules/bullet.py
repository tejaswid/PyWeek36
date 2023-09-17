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
        self.velocity = [0, 0]

        self.rotation = 0

    def set_rotation(self, target_x, target_y):
        # Note: - is required in the below code for ccw rotation. DO NOT REMOVE
        self.rotation = -math.degrees(math.atan2(target_y-self.y, target_x-self.x))

    # compute the velocity of the bullet
    def set_velocity(self, target_x, target_y):
        self.velocity = [0,0]
        
        # compute direction towards target
        dir_x = target_x - self.x
        dir_y = target_y - self.y
        mag = math.sqrt(dir_x**2 + dir_y**2)

        if mag != 0:
            dir_x /= mag
            dir_y /= mag

        # set velocity
        self.velocity[0] = dir_x * self.speed
        self.velocity[1] = dir_y * self.speed

    def update_object(self, dt):
        # TODO add collision detection
        self.update_position(dt)

    # update the position of the bullet based on the current velocity
    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
