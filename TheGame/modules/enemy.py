from modules.game_object import GameObject
from modules import utils


class Enemy(GameObject):
    def __init__(self, game_assets, game_state, *args, **kwargs):
        self.img = game_assets.image_assets["img_enemy"]
        super(Enemy, self).__init__(img=self.img, *args, **kwargs)

        self.assets = game_assets
        self.game_state = game_state
        self.type = "enemy"

        # movement
        self.speed = 50
        self.velocity = [0, 0]
        # collision
        self.collision_radius = 10
        # health
        self.max_health = 100
        self.current_health = self.max_health
        # damage to other objects
        self.damage = 30
        # score
        self.score = 10
        # repulsion with other enemies
        self.repulsion_distance = 50
        self.repulsion_factor = 2
        
    def update_object(self, dt):
        # TODO add collision detection
        self.update_velocity()
        self.update_position(dt)

    def update_velocity(self):
        player_x = self.game_state.player_position[0]
        player_y = self.game_state.player_position[1]
        if player_x is not None and player_y is not None:
            # compute direction towards player
            self.velocity = utils.compute_velocity(
                self.speed, self.x, self.y, player_x, player_y
            )

    def update_position(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def handle_collision_with(self, other_object):
        # handle collision with bullet
        if other_object.type == "bullet":
            if self.has_collided_with(other_object):
                print("enemy collided with bullet")
                self.take_damage(other_object.damage)
                # remove bullet. again needed to possibly overcome the framerate issue
                other_object.dead = True
                # if I am dead, then I was killed by the player
                if self.dead:
                    self.died_by_player = True

        if other_object.type in ["player", "asteroid"]:
            if self.has_collided_with(other_object):
                print("enemy collided with ", other_object.type)
                self.take_damage(other_object.damage)
                # player takes damage, needed to possibly overcome the framerate issue
                other_object.take_damage(self.damage)


    def compute_repulsion(self, other_object):
        if other_object.type != "enemy":
            return
        
        # TODO: for now this updates the position, instead add velocity or force based control
        distance = utils.distance((self.x, self.y), (other_object.x, other_object.y))
        if distance < self.repulsion_distance:
            # add a repulsion effect to the objects
            old_self_x = self.x
            old_self_y = self.y
            old_other_object_x = other_object.x
            old_other_object_y = other_object.y

            self.x += (old_self_x - old_other_object_x) * self.repulsion_factor
            self.y += (old_self_y - old_other_object_y) * self.repulsion_factor

            other_object.x += (old_other_object_x - old_self_x) * other_object.repulsion_factor
            other_object.y += (old_other_object_y - old_self_y) * other_object.repulsion_factor