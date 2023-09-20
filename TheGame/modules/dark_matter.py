import pyglet

from modules.game_object import GameObject

class DarkMatter(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_dark_matter"]
        super(DarkMatter, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "dark_matter"

        # collision
        self.collision_radius = 10

    def update_object(self, dt):
        pass

    def handle_collision_with(self, other_object):
        # handle collision with player
        if other_object.type == "player":
            # if self.has_collided_with(other_object):
            #     self.dead = True
            #     print("dark matter collided with player")
            #     other_object.take_damage(-20)   # give health to player
            pass

        # if enemy touches it, nothing happens
        if other_object.type == "enemy":
            pass
        # if bullet touches it, it deflects around it in a circle
        if other_object.type == "bullet":
            # need to implement it
            pass
        # if asteroid or powerup touches it, it dies
        if other_object.type in ["asteroid", "powerup"]:
            if self.has_collided_with(other_object):
                print("dark matter collided with asteroid")
                other_object.dead = True