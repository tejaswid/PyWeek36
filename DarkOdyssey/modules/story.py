from modules.game_object import GameObject


class Story(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        image = game_assets.image_assets["img_story"]
                  
        super(Story, self).__init__(img=image, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "story"

        # spawn
        self.rotation = 0
        # movement
        self.speed = 30

    def update_object(self, dt):
        self.y += self.speed * dt
        if self.y > 1024:
            self.speed = 0

    def handle_collision_with(self, other_object):
        pass
