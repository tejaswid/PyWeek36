from modules.enemy import Enemy
from modules.spawner import Spawner

class EnemySpawner(Spawner):
    def __init__(self, game_assets, game_state, batch, group, *args, **kwargs):
        super().__init__(game_assets, game_state, batch, group, *args, **kwargs)

        self.spawn_interval = 5
        self.time_since_last_spawn = self.spawn_interval
        self.max_num_objects = 15
        self.spawn_at_start = True

        self.dist_from_player = 150
        self.game_object = Enemy
        self.spawn_bounds_type = "stage"