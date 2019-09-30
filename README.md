# PyOnitama

This project was made for CS 5033 Machine Learning. It emulates the Onitama board game.

## Run Instructions

Use Python 3.6 or higher
```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

## Set Experiments and Agents

Place new agents in `src/agents`. See others as example. `BaseAgent` will act as a human player, but is also the base class for all agents

Place new experiments in `src/experiments`. See others as example. Make sure to set `blue_agent`, `red_agent`, and `do_render`. `game_ended()` will be called after every round with the final game state. Agents can be reassigned at any time (e.g. swapping `blue_agent` and `red_agent` every match)

Tell PyOnitama which experiment to use in `main.py` as the argument to the `Game` constructor. (Line 10 at time of writing)
