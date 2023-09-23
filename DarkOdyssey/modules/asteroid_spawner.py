from modules.asteroid import Asteroid
from modules.spawner import Spawner

class AsteroidSpawner(Spawner):
    def __init__(self, game_assets, game_state, batch, group, **kwargs):
        super().__init__(game_assets, game_state, batch, group, **kwargs)

        self.spawn_interval = 3
        self.time_since_last_spawn = self.spawn_interval
        self.max_num_objects = 5
        self.spawn_at_start = True

        self.dist_from_player = 100
        self.game_object = Asteroid
        self.spawn_bounds_type = "viewport"