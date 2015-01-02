#Homework 2 - Lasca

The PDF for the assignment can found in [`hw2.pdf`](hw2.pdf?raw=true).

This code was written using [PyCharm](https://www.jetbrains.com/pycharm/). I highly recommend it for fast and fun code development. It has a free community edition that should suffice for this exercise.

##Directory Structure

###[`/`](http://github.com/TechnionAI/Win14_15_HW2)
**Important notice** - Even though you are not submitting any of the files outside [`players`](players), you are encouraged to use the provided libraries. You can see examples of such usages in the provided players, and you can do exactly the same. Don't copy any of the provided files into your submission, you can assume all the files will be present with the latest version published here.

**Another notice** The `__init__.py` files are very important, and enable all libraries to be imported from any place, no matter their nesting. Very convenient.

[`.gitignore`](.gitignore) A git file, ignore it.

[`abstract.py`](abstract.py) Contains abstract classes you should inherit from.

[`gameconsts.py`](gameconsts.py) Pre-calculated structures you can use if you want to save running time for your player.

[`gameutils.py`](gameutils.py) Lasca-specific utilities.

[`hw2.pdf`](hw2.pdf) The homework assignment.

[`README.md`](README.md) This file.

[`run_game.py`](run_game.py) The game running engine. Please read this file's docs to understand how you should provide the arguments. This is the file you should run:
> python run_game.py [args]
>

This is the file we will run in the tournament, so make sure that all the imports you used work. You are not submitting any of the files outside of [`players`](players) directory; so make sure your players runs in a clean `git clone`. (You are only submitting only a directory inside players - your player).

[`utils.py`](utils.py) Generic utilities. Note that usage of threads in your code is prohibited (and will be enforced), so you can't use all the functions here.

___
###[`gui/`](gui/)
Gui library.
Notice that the gui is **not** interactive. To follow the game in gui mode, open the created `game.png` with your OS preview app, and watch it update on every move. Tip: make the window "always on top".

[`.gitignore`](.gitignore) A git file, ignore it.

[`gui/__init__.py`](gui/__init__.py) Defines the functions and constants accessible using `import gui`.

[`gui/Helvetica.ttf`](gui/Helvetica.ttf) The font used to draw the output png.

___

###[`players/`](players/)
Home for all players. Both given as example, and your own player.
Your submission should be a zip file containing the directory AI2_123_456. It should contain an `__init__.py` so we can import it. It should contain any 3rd party library that is not pip-installable inside the directory structure.
For example:
```
AI2_123_456.zip:
|- AI2_123_456
   |- __init__.py
   |- player1
     |- __init__.py
     |- ...
   |- player2
     |- __init__.py
     |- ...
   |- player3
     |- __init__.py
     |- ...
   |- competition_player
     |- __init__.py
     |- ...
   |- libs.txt
   |- AI_HW2.pdf
   |- readme.txt
   |- 3rd_party_lib
      |- __init__.py
      |-...
```

To verify that your competition player will not fail to run successfully at the tournament, this command should work in the terminal:
> python run_game.py 3 3 3 50 t AI2_123_456.competition_player simple_player
>

Any pip-installable library you used in your code should be listed in `libs.txt`. Can be empty. Example of this file's contents:
```
matplotlib
numpy
...
```

####[`players/interactive`](players/interactive)
The interactive player. Waits for input for every move. Always given an infinite time to run, no matter what the args to `run_game.py` are.

[`players/interactive/__init__.py`](players/interactive/__init__.py) The player's code.

####[`players/random_player`](players/random_player)
The random player. Chooses from the given moves randomly.

[`players/random_player/__init__.py`](players/random_player/__init__.py) The player's code.

####[`players/simple_player`](players/simple_player)
The minimax player. Manages its running time, and uses iterative deepening. **Understanding all of its code is essential**.

[`players/simple_player/__init__.py`](players/simple_player/__init__.py) The player's code.
