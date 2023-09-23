# Dark Odyssey
Our game for PyWeek36, September 2023.

## Requirements
- Pyglet == 2.0.9

## Running the game
```bash
cd <path_to_the_repo>/Dark_Odyssey
python run_game.py
```

Checkout `README_dev.md` for developer instructions.

## About the Game
Voyage through the cosmos to unravel the mysteries of dark matter, all while facing formidable adversaries.

### Controls
Use the mouse to aim and rotate your spaceship.
Press 'A' to accelerate in the direction that the spaceship is pointing towards.

## To build the game yourself
### Setup
If using native pip then simply open a terminal and run the following from the repo.

```bash
cd <path_to_this_repo>/Dark_Odyssey
pip install -r requirements.txt
```

If using a conda/mamba environemnt, then make sure you have pip installed in it and then install requirements using pip.

Conda
```bash
conda create -n darkodyssey
conda activate darkodyssey
conda install python pip

cd <path_to_this_repo>/Dark_Odyssey
pip install -r requirements.txt
```

Mamba
```bash
mamba create -n darkodyssey
mamba activate darkodyssey
mamba install python pip

cd <path_to_this_repo>/Dark_Odyssey
pip install -r requirements.txt
```

### Code structure

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

## Credits
- Game Design, Programming, Artwork: ballipilla, ele-phant-astic, pillitoka, dark knight  
- Sounds: freesound.org. Individual licences are mentioned next to the specific files  
- Music: Patreon Goal Reward Loops - Track10 - Layer_04.wav Track by Abstraction (http://abstractionmusic.bandcamp.com/)  

## License
This work (apart from files mentioned specifically) is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.