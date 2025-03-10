# RPGtest

This is a simply pygame generated using GPT o1, really meant to serve as a capability test. Can be downloaded in run in users pygame application.

# Fantasy JRPG Battle

## Overview
Fantasy JRPG Battle is a simple role-playing game (RPG) battle system developed using Python and Pygame. Players control a team of fantasy-inspired characters—including a Warrior, Mage, Healer, and Thief—as they engage in a strategic battle against a powerful boss character.

## Features

- **Character Classes:** Each character has distinct attributes:
  - Warrior: High HP and physical attack.
  - Mage: Powerful magic attacks.
  - Healer: Supports the team by healing.
  - Thief: Agile attacker with chance-based powerful moves.
  - Boss: A formidable opponent with substantial HP and attack power.

- **Game Mechanics:**
  - Turn-based combat with action selection.
  - Dynamic damage calculation considering attack type (physical or magical).
  - Unique animations for character actions.
  - Randomized damage calculation for variability.

- **Visuals:**
  - Programmatically generated character sprites.
  - Custom animations for each character action.
  - Dynamic health bars and turn order display.

- **Game States:**
  - STATE_TURN_START
  - STATE_PLAYER_CHOICE
  - STATE_TARGET_SELECTION
  - STATE_ANIMATION
  - STATE_NEXT_TURN
  - STATE_VICTORY
  - STATE_GAME_OVER

## Installation & Requirements

### Prerequisites
- Python 3.x
- Pygame library

Install dependencies using pip:
```bash
pip install pygame
```

## Running the Game
Execute the script from the command line:
```bash
python3 rpg_test.py
```

## Controls
- **Menu Navigation:**
  - Number keys (`1`, `2`) to quickly select actions.
  - Arrow keys (`UP`, `DOWN`) to navigate menu options.
  - `ENTER` to select an option.
  - Mouse click also supported for menu interaction.

## Game Flow
- Each round, the turn order is recalculated based on character speed.
- Players choose actions from available moves per character.
- Animations illustrate attack, healing, and special moves clearly.
- Game continues until either the boss or all player characters are defeated.

## Customization
You can adjust character attributes, create new moves, or customize the animations directly within the Python file:
- Character stats and moves can be edited under the "Character Classes & Stats" and "Moves Data & Action Class" sections.
- Animations and visuals can be customized within the "Sprite Generation Functions" and "Animation Classes" sections.

## Future Enhancements
- Additional characters and enemy types.
- Expanded set of animations and effects.
- Enhanced graphical assets and background images.
- Implement experience and leveling systems.

## Dependencies
- Python 3
- Pygame

## License
This project is licensed under the MIT License. Feel free to modify and redistribute with attribution.

---
Enjoy exploring and battling in your own fantasy JRPG adventure!
