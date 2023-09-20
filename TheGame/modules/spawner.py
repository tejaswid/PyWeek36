import random
from modules import utils


class Spawner(object):
    def __init__(self, game_assets, game_state, batch, group, *args, **kwargs):
        self.assets = game_assets
        self.game_state = game_state

        self.spawn_interval = 0
        self.time_since_last_spawn = 0
        self.spawn_at_start = True

        self.max_num_objects = 0

        self.dist_from_player = 0
        self.game_object = None

        self.spawned_objects = []

        self.batch = batch
        self.group = group

        self.spawn_margin = 10

        self.spawn_bounds_type = "viewport"
        self.grid_cells = 1

    def get_num_to_spawn(self):
        return self.max_num_objects - len(self.spawned_objects)

    def get_spawn_bounds(self):
        if self.spawn_bounds_type == "viewport":
            viewport_x, viewport_y = self.game_state.get_viewport()
            min_x = viewport_x - self.game_state.viewport_width//2 + self.spawn_margin
            max_x = viewport_x + self.game_state.viewport_width//2 - self.spawn_margin
            min_y = viewport_y - self.game_state.viewport_height//2 + self.spawn_margin
            max_y = viewport_y + self.game_state.viewport_height//2 - self.spawn_margin
            return min_x, max_x, min_y, max_y
        elif self.spawn_bounds_type == "stage":
            min_x = 0 + self.spawn_margin
            max_x = self.game_state.stage_width - self.spawn_margin
            min_y = 0 + self.spawn_margin
            max_y = self.game_state.stage_height - self.spawn_margin
            return min_x, max_x, min_y, max_y
        else:
            raise ValueError("Invalid spawn bounds type")

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
                min_x, max_x, min_y, max_y = self.get_spawn_bounds()

                grid_width = (max_x - min_x) // self.grid_cells
                grid_height = (max_y - min_y) // self.grid_cells

                # convert linear index i to grid index xi, yi
                xi = i % self.grid_cells
                yi = i // self.grid_cells

                object_x = random.uniform(min_x + xi * grid_width, min_x + (xi + 1) * grid_width)
                object_y = random.uniform(min_y + yi * grid_height, min_y + (yi + 1) * grid_height)

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
        if self.spawn_at_start:
            self.time_since_last_spawn = self.spawn_interval
        else:
            self.time_since_last_spawn = 0
            

    def remove(self, obj):
        self.spawned_objects.remove(obj)
