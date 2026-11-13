# HW 3: tennis_career package

This repository contains a Python package that retrieves the career matches of a specified tennis player from [tennisabstract.com](https://www.tennisabstract.com) and plots the player's age against the age difference with each opponent, similar to the graphic from the New York Times article ["Serena Williams Dominated Her Generation, Then the Next One, Too"](https://www.nytimes.com/interactive/2022/08/28/sports/tennis/serena-age-opponents.html) by Sara Ziegler and Leo Dominguez.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw02-2-lilyridley
```

## Usage

```python
from tennis_career import get_player_career, plot_age_gap

# Serena Williams data and plot
serena = get_player_career('serena williams')
plot_age_gap(serena)

# Rafael Nadal data and plot
rafael = get_player_career("Rafael Nadal")
plot_age_gap(rafael)

# An invalid name returns a meaningful error message
unknown_player = data_function("LilyRidley")
```

## Functions

- `get_player_career(player_name)`: takes a name in any of the forms `"serena williams"`, `"Serena Williams"` or `"SerenaWilliams"` and returns a DataFrame with one row per match: `date`, `tournament`, `surface`, `result`,
  `opponent`, `player_age`, `opp_age` and `age_diff` (player age minus opponent
  age, in years)
- `plot_age_gap(career_df)`: takes the DataFrame created by `get_player_career` and creates a scatter plot of the player's age (x-axis) against `age_diff` (y-axis), with matches won and lost in different colors

## Tests

The tests use mock career files and avoid hitting live servers. Run them from the repo folder with:

```bash
pip install -e .
pip install pytest
pytest -v
```