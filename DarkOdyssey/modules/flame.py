import math

from pyglet.image import Animation

from modules.game_object import GameObject
from modules import utils


class Flame(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        self.short_flame_sprites = [game_assets.image_assets["img_player_ship_flame_s1"],game_assets.image_assets["img_player_ship_flame_s2"]]
        self.default_flame_animation = Animation.from_image_sequence(self.short_flame_sprites, duration=0.2, loop=True)

        self.long_flame_sprites = [game_assets.image_assets["img_player_ship_long_flame_s1"],game_assets.image_assets["img_player_ship_long_flame_s2"]]
        self.long_flame_animation = Animation.from_image_sequence(self.long_flame_sprites, duration=0.2, loop=True)

        self.img = self.default_flame_animation
        super(Flame, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.type = "flame"

        # spawn
        self.rotation = 0

        # health
        self.max_health = 0 ## check if this is the correct way to turn off health bar
        self.current_health = self.max_health

        # normal or long flame
        self.long_flame = False

    
    def set_rotation(self, angle):
        # the player's angle is set to the flame
        self.rotation = angle

    def set_position(self, player_x, player_y):
        # compute flame position from player position
        if(self.long_flame):
            L = 45
        else:
            L = 30
        self.x = player_x-L*math.cos(self.rotation*math.pi/180)
        self.y = player_y-L*math.sin(-self.rotation*math.pi/180)

    def update_object(self, dt):
        self.check_long_flame_status()
        # self.update_position(dt)

    def check_long_flame_status(self):
        if(self.long_flame):
            self.image = self.long_flame_animation
        else:
            self.image = self.default_flame_animation

    def set_long_flame_status(self, status):
        self.long_flame = status

    def handle_collision_with(self, other_object):
        # handle collision with enemy
        pass
            
