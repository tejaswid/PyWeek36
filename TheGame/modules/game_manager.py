from modules.asteroid import Asteroid
from modules.enemy import Enemy
from modules.powerup import Powerup
from modules.utils import distance

import random


def spawn_asteroids(num_asteroids, game_assets, game_state, batch, group):
    new_asteroids = []
    player_position = game_state.player_position
    for i in range(num_asteroids):
        # spawn asteroids far away from the player
        asteroid_x = player_position[0]
        asteroid_y = player_position[1]
        while distance((asteroid_x, asteroid_y), (player_position[0], player_position[1])) < 100:
            asteroid_x = random.uniform(10, 990)
            asteroid_y = random.uniform(10, 990)

        # spawn asteroid
        new_asteroid = Asteroid(game_assets, batch=batch, group=group)
        # set initial properties
        new_asteroid.set_initial_properties(asteroid_x, asteroid_y)

        new_asteroids.append(new_asteroid)
    return new_asteroids


def spawn_enemies(num_enemies, game_assets, game_state, batch, group):
    new_enemies = []
    player_position = game_state.player_position
    for i in range(num_enemies):
        # spawn enemies far away from the player
        enemy_x = player_position[0]
        enemy_y = player_position[1]
        while distance((enemy_x, enemy_y), (player_position[0], player_position[1])) < 100:
            enemy_x = random.uniform(10, 990)
            enemy_y = random.uniform(10, 990)
        # spawn enemy
        new_enemy = Enemy(game_assets, game_state, x=enemy_x, y=enemy_y, batch=batch, group=group)

        new_enemies.append(new_enemy)
    return new_enemies


def spawn_powerups(num_powerups, game_assets, game_state, batch, group):
    new_powerups = []
    player_position = game_state.player_position
    for i in range(num_powerups):
        # spawn enemies far away from the player
        powerup_x = player_position[0]
        powerup_y = player_position[1]
        while distance((powerup_x, powerup_y), (player_position[0], player_position[1])) < 300:
            powerup_x = random.uniform(10, 990)
            powerup_y = random.uniform(10, 990)
        # spawn enemy
        new_powerup = Powerup(game_assets, x=powerup_x, y=powerup_y, batch=batch, group=group)

        new_powerups.append(new_powerup)
    return new_powerups