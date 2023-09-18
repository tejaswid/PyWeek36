from modules.asteroid import Asteroid
from modules.enemy import Enemy
from modules.powerup import Powerup
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


def spawn_enemies(num_enemies, player, batch, group):
    new_enemies = []
    for i in range(num_enemies):
        # spawn enemies far away from the player
        enemy_x = player.x
        enemy_y = player.y
        while distance((enemy_x, enemy_y), (player.x, player.y)) < 100:
            enemy_x = random.uniform(10, 990)
            enemy_y = random.uniform(10, 990)
        # spawn enemy
        new_enemy = Enemy(player.assets, x=enemy_x, y=enemy_y, batch=batch, group=group)

        new_enemies.append(new_enemy)
    return new_enemies


def spawn_powerups(num_powerups, player, batch, group):
    new_powerups = []
    for i in range(num_powerups):
        # spawn enemies far away from the player
        powerup_x = player.x
        powerup_y = player.y
        while distance((powerup_x, powerup_y), (player.x, player.y)) < 500:
            powerup_x = random.uniform(10, 990)
            powerup_y = random.uniform(10, 990)
        # spawn enemy
        new_powerup = Powerup(player.assets, x=powerup_x, y=powerup_y, batch=batch, group=group)

        new_powerups.append(new_powerup)
    return new_powerups