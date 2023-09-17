import math

from modules.game_objects import GameObject

class Player(GameObject):

    def __init__(self, game_assets, *args, **kwargs):

        robot_image = game_assets.image_assets["img_player_ship"]
        super(Player, self).__init__(img=robot_image,*args, **kwargs)

        self.assets = game_assets
        self.type = "player"


    def update_object(self, dt):
        self.update_position(dt)
        

    # updates the position of the robot based on its wheel velocities - differential drive kinematics
    def update_position(self,dt):
        self.x += 1
        self.y += 1