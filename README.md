# PyWeek36
Our game for PyWeek36, September 2023

## Requirements
- Pyglet

If using native pip then simply open a terminal and run the following from the repo.

```bash
cd <path_to_this_repo>
pip install -r requirements.txt
```

If using a conda/mamba environemnt, then make sure you have pip installed in it and then install requirements using pip.

Conda
```bash
conda create -n kadabra
conda activate kadabra
conda install python pip

cd <path_to_this_repo>
pip install -r requirements.txt
```

Mamba
```bash
mamba create -n kadabra
mamba activate kadabra
mamba install python pip

cd <path_to_this_repo>
pip install -r requirements.txt
```


## Running the game
```bash
cd <path_to_the_repo>
cd TheGame
python run_game.py
```

## Code structure

### Folders
- modules: Python files that implement individual components of the game.
- resources: All resources like images, sounds, etc.

### Files
- The main game is written in `game.py`. This is like the stage.   
- The `GameObject` class in `game_object.py` is the abstract class to define all individual objects in the game - player, enemy, asteroid, boss, powerup and dark matter.
- The `Spawner` class in `spawner.py` is the abstract class to spawm the above objects.
- Assets for each of these objects are defined in the `GameAssets` class in `game_assets.py`.  
- Utility functions are defined in `utils.py`.  
- The file `game_state.py` has behind the scenes management.

