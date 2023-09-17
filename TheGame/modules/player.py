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

        self.mouse_x = 1000
        self.mouse_y = 500


    def update_object(self, dt):
        if self.key_handler[key.LEFT]:
            self.rotation -= 10 * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += 10 * dt
        self.update_position(dt)
        

    # updates the position of the player
    def update_position(self,dt):
        self.x += 1
        self.y += 1

    # update rotation of the player based on mouse position
    def update_rotation(self, mouse_x, mouse_y):
        self.rotation = math.atan2(mouse_y-self.y, mouse_x-self.x) * -180 / math.pi