from modules.boss import Boss
from modules.spawner import Spawner

class BossSpawner(Spawner):
    def __init__(self, game_assets, game_state, batch, group, *args, **kwargs):
        super().__init__(game_assets, game_state, batch, group, *args, **kwargs)

        self.spawn_interval = 0
        self.time_since_last_spawn = self.spawn_interval
        self.max_num_objects = 1
        self.spawn_at_start = False

        self.dist_from_player = 100
        self.game_object = Boss
        self.spawn_bounds_type = "viewport"