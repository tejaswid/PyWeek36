from modules.dark_matter import DarkMatter
from modules.spawner import Spawner

class DarkMatterSpawner(Spawner):
    def __init__(self, game_assets, game_state, batch, group, **kwargs):
        super().__init__(game_assets, game_state, batch, group, **kwargs)

        self.spawn_interval = 0
        self.time_since_last_spawn = self.spawn_interval
        self.max_num_objects = 4
        self.spawn_at_start = True

        self.dist_from_player = 10
        self.game_object = DarkMatter
        self.spawn_bounds_type = "stage"
        self.grid_cells = 2
        