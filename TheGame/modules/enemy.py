import math

from modules.game_objects import GameObject

class Enemy(GameObject):
    def __init__(self, game_assets, *args, **kwargs):
        
        enemy_image = game_assets.image_assets["img_enemy"]
        super(Enemy, self).__init__(img=enemy_image, *args, **kwargs)

        self.assets = game_assets
        self.type = "enemy"

        self.speed = 50
        self.player_x = None
        self.player_y = None

        self.velocity = [0, 0]

    def seek_player(self, player_x, player_y):
        self.player_x = player_x
        self.player_y = player_y

    def update_object(self, dt):
        # TODO add collision detection
        self.update_velocity()
        self.update_position(dt)

    def update_velocity(self):
        if self.player_x is not None and self.player_y is not None:
            # compute direction towards player
            dir_x = self.player_x - self.x
            dir_y = self.player_y - self.y
            mag = math.sqrt(dir_x**2 + dir_y**2)

            if mag != 0:
                dir_x /= mag
                dir_y /= mag

            # set velocity
            self.velocity[0] = dir_x * self.speed
            self.velocity[1] = dir_y * self.speed

    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt