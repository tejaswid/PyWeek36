from modules.game_object import GameObject

class Boss(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_boss_3"]
        if game_state.level == 2:
            self.img = game_assets.image_assets["img_boss_2"]
        super(Boss, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.type = "boss"
        self.game_state = game_state

        # spawn
        self.rotation = 0
        # movement
        self.speed = 0
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 100
        # health
        self.max_health = 1000
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 40

        # parameters for boss movement
        self.movement_mode = "straight"
    
    def update_object(self, dt):
        pass

    def set_movement_mode(self, mode):
        self.movement_mode = mode

    
    def handle_collision_with(self, other_object):
        pass
        
