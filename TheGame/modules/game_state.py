class GameState(object):
    """
    Class to store the current state of the game
    """
    def __init__(self) -> None:
        # dimensions of the stage
        self.stage_width = 1024
        self.stage_height = 1024

        # viewport size - this is the size of the window that we see
        self.viewport_width = 800
        self.viewport_height = 800
        self.viewport_x = self.stage_width // 2  # centre of the stage
        self.viewport_y = self.stage_height // 2  # centre of the stage
        self.viewport_margin = 50  # margin tp move the screen when player moves

        self.score = 0
        self.player_position = [0, 0]

        self.level = 1
    
    def reset_viewport(self):
        self.viewport_x = self.stage_width // 2
        self.viewport_y = self.stage_height // 2
    
    def update_viewport(self, x, y):
        self.viewport_x = x
        self.viewport_y = y

    def get_viewport(self):
        return self.viewport_x, self.viewport_y
