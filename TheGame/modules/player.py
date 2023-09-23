import math

from pyglet.window import key
from pyglet.window import mouse
from pyglet.image import Animation

from modules.game_object import GameObject
from modules.bullet import Bullet
from modules import utils
from modules.flame import Flame


class Player(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.default_sprite = game_assets.image_assets["img_player_ship"]
        super(Player, self).__init__(img=self.default_sprite, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "player"

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.mouse_handler = mouse.MouseStateHandler()
        self.event_handlers = [self, self.key_handler, self.mouse_handler]

        # movement
        self.speed = 120
        self.velocity = utils.random_velocity(self.speed)
        self.acceleration_magnitude = 500
        self.acceleration = [0, 0]
        # collision
        self.collision_radius = 5
        # health
        self.max_health = 500
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 30
        # damage caused by bullets spawned by this object
        self.bullet_damage = 20
        # update player position in game state
        self.game_state.player_position = [self.x, self.y]

        # arbitrary motion variables
        self.in_arbitrary_motion = False
        self.arbitrary_motion_time = 2
        self.arbitrary_motion_time_left = self.arbitrary_motion_time
        self.arbitrary_speed_factor = 5
        self.arbitrary_angular_velocity = 1000
        self.arbitrary_recover_speed = 10

        # powerup related variables
        self.powerup_sp_boosted_speed = self.speed + 600
        self.powerup_sp_original_speed = self.speed
        self.powerup_sp_max_time = 7
        self.powerup_sp_current_time = 0
        self.powerup_sp_active = False

        self.powerup_db_boosted_damage = self.bullet_damage * 1.5
        self.powerup_db_original_damage = self.bullet_damage
        self.powerup_db_max_time = 5
        self.powerup_db_current_time = 0
        self.powerup_db_active = False

        self.shield_max_health = 100
        self.shield_current_health = self.shield_max_health
        self.shield_active = False
        # self.shield_sprite = self.assets.image_assets["img_player_ship_with_shield"]

        self.shield_sprites = [self.assets.image_assets["img_player_ship_with_shield_s1"],
                               self.assets.image_assets["img_player_ship_with_shield_s2"],
                               self.assets.image_assets["img_player_ship_with_shield_s3"],
                               self.assets.image_assets["img_player_ship_with_shield_s4"],
                               self.assets.image_assets["img_player_ship_with_shield_s5"]]
        self.shield_animation = Animation.from_image_sequence(self.shield_sprites, duration=0.2, loop=True)

        # add flame
        self.flame = Flame(self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group)
        self.child_objects.append(self.flame)
        

    def update_object(self, dt):
        if not self.in_arbitrary_motion:
            self.acceleration = [0, 0]
            self.flame.set_long_flame_status(False)
            if self.key_handler[key.A]:
                self.update_velocity(dt)
                self.flame.set_long_flame_status(True)
            self.update_position(dt)
        else:
            self.move_arbitraryly(dt)

        self.game_state.player_position = [self.x, self.y]

        # handle powerup modes
        if self.powerup_db_active:
            self.powerup_db_current_time += dt
            self.check_powerup_db_status()
        
        if self.powerup_sp_active:
            self.powerup_sp_current_time += dt
            self.check_powerup_sp_status()

        self.flame.set_rotation(self.rotation)
        self.flame.set_position(self.x, self.y)
        

    # updates the position of the player
    def update_position(self, dt):
        self.x += self.velocity[0] * dt + 0.5 * self.acceleration[0] * dt**2
        self.y += self.velocity[1] * dt + 0.5 * self.acceleration[1] * dt**2

    # update rotation of the player based on mouse position
    def update_rotation(self, mouse_x, mouse_y):
        if self.in_arbitrary_motion:
            return
        # Note: - is required in the below code for ccw rotation. DO NOT REMOVE
        self.rotation = -math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))

    # update the velocity of the player - new velocity vector must be aligned with rotation
    def update_velocity(self, dt):
        self.velocity[0] += (
            self.acceleration_magnitude * math.cos(self.rotation * math.pi / 180) * dt
        )
        self.velocity[1] += (
            self.acceleration_magnitude * -math.sin(self.rotation * math.pi / 180) * dt
        )

        if self.velocity[0] > self.speed:
            self.velocity[0] = self.speed
        if self.velocity[0] < -self.speed:
            self.velocity[0] = -self.speed
        if self.velocity[1] > self.speed:
            self.velocity[1] = self.speed
        if self.velocity[1] < -self.speed:
            self.velocity[1] = -self.speed

    def initiate_arbitrary_motion(self):
        self.in_arbitrary_motion = True
        self.arbitrary_motion_time_left = self.arbitrary_motion_time
        self.velocity = utils.random_velocity(self.speed * self.arbitrary_speed_factor)

    def move_arbitraryly(self, dt):
        self.arbitrary_motion_time_left -= dt
        if self.arbitrary_motion_time_left <= 0:
            self.in_arbitrary_motion = False
            self.velocity = utils.random_velocity(self.arbitrary_recover_speed)
        else:
            self.update_position(dt)
            self.rotation += self.arbitrary_angular_velocity * dt

    def fire_bullet(self, target_x, target_y):
        bullet = Bullet(
            self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group
        )
        bullet.damage = self.bullet_damage
        bullet.set_rotation(target_x, target_y)
        bullet.set_velocity(target_x, target_y)
        bullet.set_type("player")
        self.child_objects.append(bullet)

    def fire_tracer(self, target_x, target_y):
        tracer = Bullet(
            self.assets, x=self.x, y=self.y, batch=self.batch, group=self.group
        )
        tracer.damage = 0
        tracer.set_rotation(target_x, target_y)
        tracer.set_velocity(target_x, target_y)
        tracer.set_type("tracer")
        self.child_objects.append(tracer)

    def activate_damage_boost(self):
        self.powerup_db_active = True
        self.bullet_damage = int(self.powerup_db_boosted_damage)

    def check_powerup_db_status(self):
        if self.powerup_db_current_time >= self.powerup_db_max_time:
            print("powerup_db expired")
            self.bullet_damage = self.powerup_db_original_damage
            self.powerup_db_current_time = 0
            self.powerup_db_active = False

    def activate_speed_boost(self):
        self.powerup_sp_active = True
        self.speed = self.powerup_sp_boosted_speed

    def check_powerup_sp_status(self):
        if self.powerup_sp_current_time >= self.powerup_sp_max_time:
            print("powerup_sp expired")
            self.speed = self.powerup_sp_original_speed
            self.powerup_sp_current_time = 0
            self.powerup_sp_active = False

    def add_shield_sprite(self):
        self.image = self.shield_animation

    def remove_shield_sprite(self):
        self.image = self.default_sprite

    def shield_up(self):
        self.shield_active = True
        self.add_shield_sprite()

    def handle_collision_with(self, other_object):
        # handle collision with enemy and asteroid
        if other_object.type in ["enemy", "asteroid"]:
            if self.has_collided_with(other_object):
                print("player collided with ", other_object.type)
                self.take_damage(other_object.damage)
                # enemy takes damage, needed to possibly overcome the framerate issue
                other_object.take_damage(self.damage)

        # handle collision with powerup
        if other_object.type == "powerup":
            if self.has_collided_with(other_object):
                other_object.dead = True
                print("player collided with powerup")
                if other_object.powerup_type == "health":
                    self.take_damage(-other_object.damage)
                elif other_object.powerup_type == "shield":
                    self.shield_up()
                elif other_object.powerup_type == "speed":
                    self.activate_speed_boost()
                elif other_object.powerup_type == "damage":
                    self.activate_damage_boost()

        # handle collision with dark matter
        if other_object.type == "dark_matter":
            if (
                self.has_collided_with(other_object)
                and self.in_arbitrary_motion is False
            ):
                print("player collided with dark matter")
                self.take_damage(other_object.damage)
                # deflect the player in an arbitrary direction and spin
                self.initiate_arbitrary_motion()

        # handle collision with bullet
        if other_object.type == "bullet" and other_object.bullet_type == "enemy":
            if self.has_collided_with(other_object):
                print("player collided with enemy bullet")
                self.take_damage(other_object.damage)
                other_object.dead = True

        # handle collision with boss
        if other_object.type == "boss":
            if self.has_collided_with(other_object):
                print("player collided with boss")
                self.take_damage(other_object.damage)
                other_object.take_damage(self.damage)
