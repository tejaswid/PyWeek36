class GameState(object):
    """
    Class to store the current state of the game
    """
    def __init__(self) -> None:
        self.score = 0
        self.player_position = [0, 0]

        self.num_enemies = 0
        self.num_asteroids = 0
        self.num_powerups = 0        