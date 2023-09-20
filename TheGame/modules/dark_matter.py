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
        self.collision_radius = 30
        # damage to other objects
        self.damage = 40

    def update_object(self, dt):
        pass

    def handle_collision_with(self, other_object):
        # handle collision with player
        if other_object.type == "player":
            if self.has_collided_with(other_object) and not other_object.in_arbitrary_motion:
                print("dark matter collided with player")
                other_object.take_damage(self.damage)
                other_object.initiate_circular_motion(self.collision_radius, self.x, self.y)
            pass

        # if enemy touches it, nothing happens
        if other_object.type == "enemy":
            pass
        # if bullet touches it, it deflects around it in a circle
        if other_object.type == "bullet":
            if self.has_collided_with(other_object) and not other_object.in_circular_motion:
                print("dark matter collided with bullet")
                other_object.initiate_circular_motion(self.collision_radius, self.x, self.y)
        # if asteroid or powerup touches it, it dies
        if other_object.type in ["asteroid", "powerup"]:
            if self.has_collided_with(other_object):
                print("dark matter collided with ", other_object.type)
                other_object.dead = True