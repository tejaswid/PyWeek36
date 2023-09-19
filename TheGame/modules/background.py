import pyglet
from modules.game_objects import GameObject


class Background(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        images = [
            game_assets.image_assets["img_bkg_1"],
            game_assets.image_assets["img_bkg_2"],
        ]
        anim = pyglet.image.Animation.from_image_sequence(
            images, duration=0.5, loop=True
        )

        super(Background, self).__init__(img=anim, *args, **kwargs)

        self.assets = game_assets
        self.type = "background"

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
