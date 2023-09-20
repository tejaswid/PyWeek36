class GameState(object):
    """
    Class to store the current state of the game
    """
    def __init__(self) -> None:
        # dimensions of the stage
        self.stage_width = 1024
        self.stage_height = 1024

        

        self.score = 0
        self.player_position = [0, 0]

        self.num_enemies = 0
        self.num_asteroids = 0
        self.num_powerups = 0        