import math

from pyglet.window import key
from pyglet.window import mouse

from modules.game_objects import GameObject

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

        self.speed = 1
        self.velocity = [self.speed,self.speed]


    def update_object(self, dt):
        if self.key_handler[key.A]:
            self.speed = 3 # small boost
            self.update_velocity()
        if self.key_handler[key.RIGHT]:
            self.rotation += 10 * dt
        self.update_position(dt)
        

    # updates the position of the player
    def update_position(self,dt):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    # update rotation of the player based on mouse position
    def update_rotation(self, mouse_x, mouse_y):
        self.rotation = math.atan2(mouse_y-self.y, mouse_x-self.x) * -180 / math.pi

    # update the velocity of the player - new velocity vector must be aligned with rotation
    def update_velocity(self):
        self.velocity[0] = math.cos(self.rotation * math.pi / 180)
        self.velocity[1] = -math.sin(self.rotation * math.pi / 180)