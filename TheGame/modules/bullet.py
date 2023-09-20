import math

from pyglet.window import key
from pyglet.window import mouse
from pyglet import clock

from modules.game_object import GameObject
from modules import utils


class Bullet(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        self.img = game_assets.image_assets["img_bullet"]
        super(Bullet, self).__init__(img=self.img, *args, **kwargs)
        clock.schedule_once(
            self.die, 0.5
        )  # schedule the bullet to die after 0.5 seconds

        self.assets = game_assets
        self.type = "bullet"

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.event_handlers = [self, self.key_handler, self.mouse_handler]

        # spawn
        self.rotation = 0
        # movement
        self.speed = 500
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 5
        # health
        self.max_health = 100
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 20

    def set_rotation(self, target_x, target_y):
        # Note: - is required in the below code for ccw rotation. DO NOT REMOVE
        self.rotation = -math.degrees(math.atan2(target_y - self.y, target_x - self.x))

    # compute the velocity of the bullet
    def set_velocity(self, target_x, target_y):
        self.velocity = utils.compute_velocity(
            self.speed, self.x, self.y, target_x, target_y
        )

    def update_object(self, dt):
        # TODO add collision detection
        self.update_position(dt)

    # update the position of the bullet based on the current velocity
    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def handle_collision_with(self, other_object):
        # handle collision with enemy
        if other_object.type in ["enemy", "asteroid"]:
            if self.has_collided_with(other_object):
                print("bullet collided with ", other_object.type)
                # remove bullet
                self.dead = True
                # reduce health of enemy. This is needed to possibly overcome the framerate problem
                other_object.take_damage(self.damage)
                # if the other object is dead, increase the score
                if other_object.dead:
                    other_object.died_by_player = True
