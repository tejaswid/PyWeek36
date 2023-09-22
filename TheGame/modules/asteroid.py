import random

from modules.game_object import GameObject
from modules import utils


class Asteroid(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        images = [game_assets.image_assets["img_asteroid"],
                  game_assets.image_assets["img_asteroid_2"]]
                  
        super(Asteroid, self).__init__(img=random.choice(images), *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "asteroid"

        # spawn
        self.rotation = random.uniform(0, 360)
        # movement
        self.speed = random.uniform(5, 30)
        self.velocity = utils.random_velocity(self.speed)
        self.angular_velocity = random.uniform(-100, 100)
        # collision
        self.collision_radius = 15
        # health
        self.max_health = 50
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 2
        # score
        self.score = 5

    def update_object(self, dt):
        self.update_velocity()
        self.update_position(dt)

    def update_velocity(self):
        pass

    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.rotation += self.angular_velocity * dt

    def handle_collision_with(self, other_object):
        # handle collision with bullet
        if other_object.type == "bullet" and other_object.bullet_type == "player":
            if self.has_collided_with(other_object):
                print("asteroid collided with player bullet")
                self.take_damage(other_object.damage)
                # if I am dead, then I was killed by the player
                if self.dead:
                    self.died_by_player = True

        # handle collision with player, enemy and other asteroids
        if other_object.type in ["player", "enemy", "asteroid"]:
            if self.has_collided_with(other_object):
                print("asteroid collided with player")
                self.take_damage(other_object.damage)
                other_object.take_damage(self.damage)

        if other_object.type == "dark_matter":
            if self.has_collided_with(other_object):
                print("asteroid collided with dark_matter")
                # remove asteroid
                self.dead = True
