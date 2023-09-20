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
            self.die, 6
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

        # parameters for circular motion
        self.in_circular_motion = False
        self.delta = 0
        self.theta = 0
        self.circle_radius = 0
        self.velocity_delta = 20
        self.prev_velocity_x = 0
        self.prev_velocity_y = 0

    def set_rotation(self, target_x, target_y):
        # Note: - is required in the below code for ccw rotation. DO NOT REMOVE
        self.rotation = -math.degrees(math.atan2(target_y - self.y, target_x - self.x))

    # compute the velocity of the bullet
    def set_velocity(self, target_x, target_y):
        self.velocity = utils.compute_velocity(
            self.speed, self.x, self.y, target_x, target_y
        )

    def update_object(self, dt):
        if not self.in_circular_motion:
            self.update_position(dt)
        else:
            self.move_along_circle(dt)

    # update the position of the bullet based on the current velocity
    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def initate_circular_motion(self, radius, centre_x, centre_y):
        self.in_circular_motion = True
        self.theta = math.atan2(self.y - centre_y, self.x - centre_x)
        self.delta = 0
        self.prev_velocity_x = self.velocity[0]
        self.prev_velocity_y = self.velocity[1]
        self.circle_radius = radius
        self.circle_centre_x = centre_x
        self.circle_centre_y = centre_y

    def move_along_circle(self, dt):
        if self.in_circular_motion:
            if self.delta < math.pi:
                self.x = self.circle_centre_x + self.circle_radius * math.cos(self.theta + self.delta)
                self.y = self.circle_centre_y + self.circle_radius * math.sin(self.theta + self.delta)
                self.delta += self.velocity_delta * dt
            else:
                self.velocity[0] = self.prev_velocity_x
                self.velocity[1] = self.prev_velocity_y
                self.in_circular_motion = False
                self.x = self.x + 1.5 * self.velocity[0] * dt
                self.y = self.y + 1.5 * self.velocity[1] * dt

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
        if other_object.type == "dark_matter":
            if self.has_collided_with(other_object) and not self.in_circular_motion:
                print("bullet collided with dark_matter")
                self.initate_circular_motion(other_object.collision_radius, other_object.x, other_object.y)
