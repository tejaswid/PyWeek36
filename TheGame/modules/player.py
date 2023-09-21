import math

from pyglet.window import key
from pyglet.window import mouse

from modules.game_object import GameObject
from modules.bullet import Bullet
from modules import utils


class Player(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_player_ship"]
        super(Player, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "player"

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.event_handlers = [self, self.key_handler, self.mouse_handler]

        # movement
        self.speed = 80
        self.velocity = utils.random_velocity(self.speed)
        self.acceleration_magnitude = 500
        self.acceleration = [0, 0]
        # collision
        self.collision_radius = 5
        # health
        self.max_health = 100
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 30
        # update player position in game state
        self.game_state.player_position = [self.x, self.y]

        # arbitrary motion variables
        self.in_arbitrary_motion = False
        self.arbitrary_motion_time = 2
        self.arbitrary_motion_time_left = self.arbitrary_motion_time
        self.arbitrary_speed_factor = 5
        self.arbitrary_angular_velocity = 1000
        self.arbitrary_recover_speed = 10

    def update_object(self, dt):
        if not self.in_arbitrary_motion:
            self.acceleration = [0, 0]
            if self.key_handler[key.A]:
                self.update_velocity(dt)
            self.update_position(dt)
        else:
            self.move_arbitraryly(dt)

        self.game_state.player_position = [self.x, self.y]

    # updates the position of the player
    def update_position(self, dt):
        self.x += self.velocity[0] * dt + 0.5 * self.acceleration[0] * dt**2
        self.y += self.velocity[1] * dt + 0.5 * self.acceleration[1] * dt**2

    # update rotation of the player based on mouse position
    def update_rotation(self, mouse_x, mouse_y):
        if self.in_arbitrary_motion:
            return
        
        # Note: - is required in the below code for ccw rotation. DO NOT REMOVE
        self.rotation = -math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))

    # update the velocity of the player - new velocity vector must be aligned with rotation
    def update_velocity(self, dt):
        self.velocity[0] += (
            self.acceleration_magnitude * math.cos(self.rotation * math.pi / 180) * dt
        )
        self.velocity[1] += (
            self.acceleration_magnitude * -math.sin(self.rotation * math.pi / 180) * dt
        )

        if self.velocity[0] > self.speed:
            self.velocity[0] = self.speed
        if self.velocity[0] < -self.speed:
            self.velocity[0] = -self.speed
        if self.velocity[1] > self.speed:
            self.velocity[1] = self.speed
        if self.velocity[1] < -self.speed:
            self.velocity[1] = -self.speed

    def initiate_arbitrary_motion(self):
        self.in_arbitrary_motion = True
        self.arbitrary_motion_time_left = self.arbitrary_motion_time
        self.velocity = utils.random_velocity(self.speed * self.arbitrary_speed_factor)
    
    def move_arbitraryly(self, dt):
        self.arbitrary_motion_time_left -= dt
        if self.arbitrary_motion_time_left <= 0:
            self.in_arbitrary_motion = False
            self.velocity = utils.random_velocity(self.arbitrary_recover_speed)
        else:
            self.update_position(dt)
            self.rotation += self.arbitrary_angular_velocity * dt

    def fire_bullet(self, target_x, target_y):
        bullet = Bullet(
            self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group
        )
        bullet.set_rotation(target_x, target_y)
        bullet.set_velocity(target_x, target_y)
        bullet.fired_by_player = True
        self.child_objects.append(bullet)

    def handle_collision_with(self, other_object):
        # handle collision with enemy and asteroid
        if other_object.type in ["enemy", "asteroid"]:
            if self.has_collided_with(other_object):
                print("player collided with ", other_object.type)
                self.take_damage(other_object.damage)
                # enemy takes damage, needed to possibly overcome the framerate issue
                other_object.take_damage(self.damage)
        # handle collision with powerup
        if other_object.type == "powerup":
            if self.has_collided_with(other_object):
                other_object.dead = True
                print("player collided with powerup")
                self.take_damage(-other_object.damage)
        # handle collision with dark matter
        if other_object.type == "dark_matter":
            if self.has_collided_with(other_object) and self.in_arbitrary_motion is False:
                print("player collided with dark matter")
                self.take_damage(other_object.damage)
                # deflect the player in an arbitrary direction and spin
                self.initiate_arbitrary_motion()