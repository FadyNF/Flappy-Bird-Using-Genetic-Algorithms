import pygame as pg
import Classes.settings as s
import random
import math 

class Bird:
    def __init__(self, x, y, jump_force, gravity):
        self.x = x
        self.y = y
        self.width = s.BIRD_WIDTH
        self.height = s.BIRD_HEIGHT
        self.image = pg.transform.scale(pg.image.load("images/bird.png"), (self.width, self.height))

        # Movement Variables
        self.y_velocity = 0
        self.gravity = gravity
        self.jump_force = jump_force

        self.alive = True
        self.mask = pg.mask.from_surface(self.image)
        
        self.survival_time = 0
        self.obstacles_passed = 0
        self.fitness = 0

    def move(self, obstacles=None):
        if self.alive:
            # Update vertical velocity and position
            self.y_velocity += self.gravity
            self.y += self.y_velocity

            # AI-driven jump decision
            if obstacles and self.should_jump(obstacles):
                self.jump()

    def jump(self):
        # Make the bird jump upwards
        self.y_velocity = self.jump_force

    
    def should_jump(self, obstacles):
        if not obstacles:
            return False

        # Find the closest obstacle
        closest_obstacle = min(obstacles, key=lambda obs: obs.x - self.x)
        
        # Jump conditions
        distance_to_obstacle = closest_obstacle.x - self.x
        jump_condition = (
            # Jump if too close to the ground
            self.y > s.SCREEN_HEIGHT * 0.8 or 
            # Jump if obstacle is approaching and bird is in danger
            (distance_to_obstacle < 200 and 
             (self.y < closest_obstacle.y_top or 
              self.y > closest_obstacle.y_bottom))
        )
        
        return jump_condition
        
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_bounds(self, screen_height):
        if self.y > screen_height - self.height:
            self.y = screen_height - self.height
            self.y_velocity = 0
            self.alive = False
        elif self.y < 0:
            self.y = 0
            self.y_velocity = 0
            self.alive = False

    def reset(self, y=None, jump_force=None, gravity=None):
        """Reset the bird's position and parameters"""
        self.x = 100
        self.y = y if y is not None else random.randint(100, 300)
        self.y_velocity = 0
        self.gravity = gravity if gravity is not None else random.uniform(0.1, 0.5)
        self.jump_force = jump_force if jump_force is not None else random.uniform(-12, -5)
        self.alive = True
        self.survival_time = 0
        self.obstacles_passed = 0

    def increment_fitness(self):
        """Increment fitness metrics over time"""
        self.survival_time += 1
        self.fitness = self.obstacles_passed + self.survival_time * 0.1
        
    def pass_obstacle(self):
        """Increase the obstacle counter when a bird passes an obstacle"""
        self.obstacles_passed += 1

    def get_fitness(self):
        """Calculate fitness based on survival time and obstacles passed"""
        return self.fitness