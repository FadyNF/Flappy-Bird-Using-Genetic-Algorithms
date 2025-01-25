# Flappy Bird AI with Genetic Algorithm

## Overview
This project implements a Flappy Bird game where the birds are controlled by a Genetic Algorithm (GA). The goal is to evolve a population of birds to successfully navigate randomly generated obstacles over generations.

Key Features:
- **Genetic Algorithm**:
  - Selection, crossover, and mutation operations to evolve the bird population.
  - Fitness function based on survival time and obstacles passed.
- **Dynamic Gameplay**:
  - Randomly generated obstacles with configurable gap sizes and speeds.
  - Simple but effective collision detection.
- **Extensibility**:
  - Modular design for easy integration of new features, such as neural networks or enhanced visualizations.

---

## Project Structure
- **`bird.py`**: Defines the `Bird` class, which handles movement, jumping, and collision logic.
- **`BirdGA.py`**: Implements the Genetic Algorithm for evolving the bird population.
- **`obstacles.py`**: Contains the `Obstacle` class to manage pipes (gap positioning, movement, and rendering).
- **`main.py`**: The entry point of the project, responsible for running the game loop, integrating classes, and managing gameplay.

---

## How to Run
1. Run the game:
   ```bash
   python main.py
   ```
2. Watch as the birds evolve over generations to play the game better.

---

## Customization
- **Obstacle Settings**:
  Modify `Classes/settings.py` to adjust obstacle speed, gap size, and other parameters.
- **GA Settings**:
  In `BirdGA.py`, tweak `population_size`, `mutation_rate`, or the fitness function to experiment with different evolution strategies.

---

## Future Enhancements
- Integrate neural networks for birds' decision-making.
- Add visual indicators of bird fitness and generation statistics.
- Implement a leaderboard to track high-performing configurations.
