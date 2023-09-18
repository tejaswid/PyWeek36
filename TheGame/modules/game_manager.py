from modules.asteroid import Asteroid
from modules.utils import distance

import random


def spawn_asteroids(num_asteroids, player, batch, group):
    new_asteroids = []
    for i in range(num_asteroids):
        # spawn asteroids far away from the player
        asteroid_x = player.x
        asteroid_y = player.y
        while distance((asteroid_x, asteroid_y), (player.x, player.y)) < 100:
            asteroid_x = random.uniform(10, 990)
            asteroid_y = random.uniform(10, 990)

        # spawn asteroid
        new_asteroid = Asteroid(player.assets, batch=batch, group=group)
        # set initial properties
        new_asteroid.set_initial_properties(asteroid_x, asteroid_y)

        new_asteroids.append(new_asteroid)
    return new_asteroids
