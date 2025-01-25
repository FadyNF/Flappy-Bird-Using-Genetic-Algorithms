import pygame as pg
import random
import Classes.settings as s

# Collision Detection between the bird and an obstacle
def check_collision(bird, obstacle):
    """
    Checks if the bird collides with any obstacle or the ground.
    Returns True if a collision is detected, False otherwise.
    """
    bird_rect = pg.Rect(bird.x, bird.y, bird.width, bird.height)
    top_obstacle_rect = pg.Rect(obstacle.x, 0, obstacle.width, obstacle.y_top)
    bottom_obstacle_rect = pg.Rect(obstacle.x, obstacle.y_bottom, obstacle.width, s.SCREEN_HEIGHT - obstacle.y_bottom)
    
    return (bird_rect.colliderect(top_obstacle_rect) or 
            bird_rect.colliderect(bottom_obstacle_rect))

# Randomization function to initialize bird parameters
def randomize_bird_params():
    """
    Randomly initializes bird parameters: y-position, jump force, and gravity.
    """
    position_y = random.uniform(100, 300)
    jump_force = random.uniform(-12, -5)
    gravity = random.uniform(0.1, 0.5)
    return position_y, jump_force, gravity

# Function to keep bird's parameters within reasonable bounds
def bounds_check(value, min_val, max_val):
    """
    Ensures that a given value stays within the specified bounds.
    """
    return max(min_val, min(value, max_val))

# Fitness function (example)
def calculate_fitness(bird, survival_time, obstacles_passed):
    """
    Calculates the fitness of the bird based on survival time and obstacles passed.
    """
    return survival_time * obstacles_passed
