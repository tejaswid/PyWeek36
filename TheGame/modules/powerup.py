import random

from modules.game_object import GameObject
import pyglet.clock


class Powerup(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_powerup"]
        self.max_time = 8

        super(Powerup, self).__init__(img=self.img, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, self.max_time)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "powerup"

        # spawn
        self.rotation = random.uniform(0, 360)
        # movement - only visual
        self.angular_velocity = random.uniform(-100, 100)
        # collision
        self.collision_radius = 20
        # time left
        self.time_left = self.max_time
        # negative damage = positive health
        self.damage = -20

        self.powerup_types = ["health", "shield", "speed", "damage"]
        self.powerup_type = random.choice(self.powerup_types)
        self.update_sprite()
        # self.assets.sound_assets["snd_powerup_spawn"].play()

    def update_sprite(self):
        if self.powerup_type == "health":
            self.image = self.assets.image_assets["img_powerup_health"]
        elif self.powerup_type == "shield":
            self.image = self.assets.image_assets["img_powerup_shield"]
        elif self.powerup_type == "speed":
            self.image = self.assets.image_assets["img_powerup_speed"]
        elif self.powerup_type == "damage":
            self.image = self.assets.image_assets["img_powerup_damage"]

    def update_object(self, dt):
        # update rotation - just for visual effect
        self.rotation += self.angular_velocity * dt
        # update time left
        self.time_left -= dt

    def handle_collision_with(self, other_object):
        # handle collision with player
        if other_object.type == "player":
            if self.has_collided_with(other_object):
                self.assets.sound_assets["snd_powerup_pickup"].play()
                self.dead = True
                print("powerup collided with player")
                if self.powerup_type == "health":
                    other_object.take_damage(-20)  # give health to player
                elif self.powerup_type == "shield":
                    other_object.shield_up()
                elif self.powerup_type == "speed":
                    other_object.activate_speed_boost()
                elif self.powerup_type == "damage":
                    other_object.activate_damage_boost()

        if other_object.type == "dark_matter":
            if self.has_collided_with(other_object):
                print("powerup collided with dark matter")
                self.dead = True
