import pyglet
from modules.game_object import GameObject

class DarkMatter(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_dark_matter_invisible"]
        super(DarkMatter, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "dark_matter"

        # collision
        self.collision_radius = 30
        # damage to other objects
        self.damage = 40
        self.rotation = 0
        self.revealed = False
        # self.reveal()

    def update_object(self, dt):
        self.rotation += 10 * dt

    def reveal(self):
        # images = [self.assets.image_assets["img_dark_matter_revealed_1"],
        #           self.assets.image_assets["img_dark_matter_revealed_2"]]
        # anim = pyglet.image.Animation.from_image_sequence(
        #     images, duration=0.5, loop=True
        # )
        # self.image = anim

        if not self.revealed:
            self.image = self.assets.image_assets["img_dark_matter_revealed_3"]
            self.game_state.revealed_dark_matter += 1
        self.revealed = True

    def handle_collision_with(self, other_object):
        # handle collision with player
        if other_object.type == "player":
            if self.has_collided_with(other_object) and not other_object.in_arbitrary_motion:
                #print("dark matter collided with player")
                other_object.take_damage(self.damage)
                other_object.initiate_arbitrary_motion()
            pass

        # if enemy touches it, nothing happens
        if other_object.type == "enemy":
            pass
        # if player bullet touches it, it deflects around it in a circle
        if other_object.type == "bullet":
            if other_object.bullet_type == "player":
                if self.has_collided_with(other_object) and not other_object.in_circular_motion:
                    #print("dark matter collided with player bullet")
                    other_object.initiate_circular_motion(self.collision_radius, self.x, self.y)
            if other_object.bullet_type == "tracer":
                if self.has_collided_with(other_object):
                    #print("dark matter collided with tracer bullet")
                    other_object.dead = True
                    self.reveal()
        # if asteroid or powerup touches it, it dies
        if other_object.type in ["asteroid", "powerup"]:
            if self.has_collided_with(other_object):
                #print("dark matter collided with ", other_object.type)
                other_object.dead = True
        if other_object.type == "boss" and other_object.current_movement_mode == "seek_dark_matter":
            if self.has_collided_with(other_object):
                #print("dark matter collided with boss")
                self.dead = True
                if other_object.sdm_closest_dm_index is None:
                    #print("dark matter object already removed")
                    pass
                else:
                    self.game_state.dark_matter_positions.pop(other_object.sdm_closest_dm_index)
                other_object.sdm_closest_dm_x = None
                other_object.sdm_closest_dm_y = None
                other_object.sdm_closest_dm_index = None