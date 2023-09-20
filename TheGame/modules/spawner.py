import random
from modules import utils
from modules.game_object import GameObject


class Spawner(object):
    def __init__(self, game_assets, game_state, batch, group, *args, **kwargs):
        self.assets = game_assets
        self.game_state = game_state

        self.spawn_interval = 0
        self.time_since_last_spawn = 0

        self.max_num_objects = 0

        self.dist_from_player = 0
        self.game_object = None

        self.spawned_objects = []

        self.batch = batch
        self.group = group

    def get_num_to_spawn(self):
        return self.max_num_objects - len(self.spawned_objects)

    def spawn(self, dt):
        self.time_since_last_spawn += dt

        if (
            self.time_since_last_spawn > self.spawn_interval
            and len(self.spawned_objects) < self.max_num_objects
        ):
            self.time_since_last_spawn = 0
            new_objects = self.create_new_objects()
            self.spawned_objects.extend(new_objects)
            return new_objects
        return []

    def create_new_objects(self):
        new_objects = []
        player_posiiton = self.game_state.player_position

        num_to_spawn = self.get_num_to_spawn()
        for i in range(num_to_spawn):
            # spawn objects far away from the player
            object_x = player_posiiton[0]
            object_y = player_posiiton[1]
            while (
                utils.distance(
                    (object_x, object_y), (player_posiiton[0], player_posiiton[1])
                )
                < self.dist_from_player
            ):
                object_x = random.uniform(10, 990)
                object_y = random.uniform(10, 990)

            # spawn object
            new_object = self.game_object(
                self.assets,
                self.game_state,
                x=object_x,
                y=object_y,
                batch=self.batch,
                group=self.group,
            )

            new_objects.append(new_object)
        return new_objects

    def reset(self):
        self.spawned_objects = []
        self.time_since_last_spawn = 0

    def remove(self, obj):
        self.spawned_objects.remove(obj)
