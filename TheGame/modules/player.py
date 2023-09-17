import math

from pyglet.window import key
from pyglet.window import mouse

from modules.game_objects import GameObject
from modules.bullet import Bullet

class Player(GameObject):

    def __init__(self, game_assets, *args, **kwargs):

        robot_image = game_assets.image_assets["img_player_ship"]
        super(Player, self).__init__(img=robot_image,*args, **kwargs)

        self.assets = game_assets
        self.type = "player"

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.event_handlers = [self, self.key_handler, self.mouse_handler]

        self.speed = 100
        self.velocity = [self.speed,0]
        self.acceleration_magnitude = 500
        self.acceleration = [0,0]


    def update_object(self, dt):
        self.acceleration = [0,0]
        if self.key_handler[key.A]:
            self.update_velocity(dt)
        self.update_position(dt)
        
    # updates the position of the player
    def update_position(self,dt):
        self.x += self.velocity[0] * dt + 0.5 * self.acceleration[0] * dt**2
        self.y += self.velocity[1] * dt + 0.5 * self.acceleration[1] * dt**2

    # update rotation of the player based on mouse position
    def update_rotation(self, mouse_x, mouse_y):
        self.rotation = math.atan2(mouse_y-self.y, mouse_x-self.x) * -180 / math.pi

    # update the velocity of the player - new velocity vector must be aligned with rotation
    def update_velocity(self, dt):
        self.velocity[0] += self.acceleration_magnitude * math.cos(self.rotation * math.pi / 180) * dt
        self.velocity[1] += self.acceleration_magnitude * -math.sin(self.rotation * math.pi / 180) * dt

        if self.velocity[0] > self.speed:
            self.velocity[0] = self.speed
        if self.velocity[0] < -self.speed:
            self.velocity[0] = -self.speed
        if self.velocity[1] > self.speed:
            self.velocity[1] = self.speed
        if self.velocity[1] < -self.speed:
            self.velocity[1] = -self.speed
    
    def fire_bullet(self):
        bullet = Bullet(self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group)
        self.child_objects.append(bullet)