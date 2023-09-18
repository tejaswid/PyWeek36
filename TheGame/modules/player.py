import math

from pyglet.window import key
from pyglet.window import mouse

from modules.game_objects import GameObject
from modules.bullet import Bullet
from modules import utils


class Player(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        self.img = game_assets.image_assets["img_player_ship"]
        super(Player, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.type = "player"

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.event_handlers = [self, self.key_handler, self.mouse_handler]

        # movement
        self.speed = 80
        self.max_speed = 200
        self.velocity = [self.speed, 0]
        self.acceleration_magnitude = 0
        self.max_acceleration = 50000
        # self.acceleration = [0, 0]
        self.acceleration_time = 3  # in seconds
        self.acceleration_time_elapsed = 0

        # collision
        self.collision_radius = 5
        # health
        self.max_health = 100
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 30

    def update_object(self, dt):
        # self.acceleration = [0, 0]
        if self.key_handler[key.A]:
            self.update_acceleration_magnitude(dt, "increase")
        if self.key_handler[key.D]:
            self.update_acceleration_magnitude(dt, "decrease")

        self.update_acceleration()
        self.update_velocity(dt)
        self.update_position(dt)

        print(self.velocity)

    # updates the position of the player
    def update_position(self, dt):
        self.x += self.velocity[0] * dt + 0.5 * self.acceleration_magnitude * dt**2
        self.y += self.velocity[1] * dt + 0.5 * self.acceleration_magnitude * dt**2

    # update rotation of the player based on mouse position
    def update_rotation(self, mouse_x, mouse_y):
        # Note: - is required in the below code for ccw rotation. DO NOT REMOVE
        self.rotation = -math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))

    def update_acceleration_magnitude(self, dt, state):
        if state == "increase":
            # increase acceleration magnitude for certain time
            if self.acceleration_time_elapsed < self.acceleration_time:
                self.acceleration_time_elapsed += dt
                self.acceleration_magnitude = min(self.acceleration_magnitude + 10000 * dt, self.max_acceleration)
            else:
                self.acceleration_time_elapsed = 0
                self.acceleration_magnitude = 0
        elif state == "decrease":
            # decrease acceleration magnitude for certain time
            if self.acceleration_time_elapsed < self.acceleration_time:
                self.acceleration_time_elapsed += dt
                self.acceleration_magnitude = max(self.acceleration_magnitude - 10000 * dt, -self.max_acceleration)
            else:
                self.acceleration_time_elapsed = 0
                self.acceleration_magnitude = 0

    def update_acceleration(self):
        # self.acceleration[0] = self.acceleration_magnitude * math.cos(math.radians(self.rotation))
        # self.acceleration[1] = self.acceleration_magnitude * -math.sin(math.radians(self.rotation))
        pass

    # update the velocity of the player - new velocity vector must be aligned with rotation
    def update_velocity(self, dt):
        self.velocity[0] = math.cos(math.radians(self.rotation)) * (self.speed + self.acceleration_magnitude * dt)
        self.velocity[1] = -math.sin(math.radians(self.rotation)) * (self.speed + self.acceleration_magnitude * dt)

        # self.velocity[0] = max(-self.max_speed, min(self.max_speed, self.velocity[0] + self.acceleration_magnitude * dt))
        # self.velocity[1] = max(-self.max_speed, min(self.max_speed, self.velocity[1] + self.acceleration_magnitude * dt))

    def fire_bullet(self, target_x, target_y):
        bullet = Bullet(
            self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group
        )
        bullet.set_rotation(target_x, target_y)
        bullet.set_velocity(target_x, target_y)
        self.child_objects.append(bullet)

    def handle_collision_with(self, other_object):
        # handle collision with enemy
        if other_object.type in ["enemy", "asteroid"]:
            if self.has_collided_with(other_object):
                print("player collided with ", other_object.type)
                self.take_damage(other_object.damage)
                # enemy takes damage, needed to possibly overcome the framerate issue
                other_object.take_damage(self.damage)
