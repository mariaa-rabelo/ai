# Zero Point One Game

Zero Point One is a strategic board game played between two players or a player and an AI. This implementation provides an interactive experience with multiple game modes, including Human vs. Human, Human vs. AI, and AI vs. AI.

# Compilation and Execution

- This program runs using python and uses the terminal to give feedback to the user, with the option of running in PyGame for Human vs Human gameplay, meaning you need to have python and pygame installed to use it.

- To play with AI, open the source code in a terminal, and run the commands below, then follow the instructions.
```
> cd src/AI
> python .\__main__.py
```

- To play Human vs Human using PyGame, you need to run the commands below, taking into account the first player to play is Red, you should press the piece you wish to move, and you will see the possible moves you can do highlighted in green. Then click inside one of the valid squares to move your piece there.
```
> pip install pygame        ## to install pygame on Windows
> cd src/PyGame
> python .\__main__.py
```

## Features

- Different game modes to play:
  - Human vs. Human (HvH)
  - Human vs. AI (HvAI)
  - AI vs. AI (AIvAI)
- Graphical user interface using Pygame
- Intelligent AI using Iterative Deepening the Minimax algorithm with Alpha-Beta pruning

## Contributors
- Maria Rabelo up202000130
- Máximo Brandão 202108887
- Edoardo Tonet 202311494
