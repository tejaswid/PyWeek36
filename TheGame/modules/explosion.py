import pyglet
from modules.game_object import GameObject
from pyglet import clock


class Explosion(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        images = [
            game_assets.image_assets["img_explosion_1"],
            game_assets.image_assets["img_explosion_2"],
            game_assets.image_assets["img_explosion_3"],
            game_assets.image_assets["img_explosion_4"],
            game_assets.image_assets["img_explosion_5"],
            game_assets.image_assets["img_explosion_6"],
            game_assets.image_assets["img_explosion_7"],
        ]
            
        anim = pyglet.image.Animation.from_image_sequence(
            images, duration=0.3, loop=True
        )

        super(Explosion, self).__init__(img=anim, *args, **kwargs)
        clock.schedule_once(
            self.die, 2
        )

        self.assets = game_assets
        self.type = "explosion"

        # movement
        self.speed = 0
        self.velocity = [0, 0]
        self.collision_radius = None
        self.max_health = None
        self.current_health = self.max_health
        self.damage = None

    def update_object(self, dt):
        pass

    def handle_collision_with(self, other_object):
        pass
