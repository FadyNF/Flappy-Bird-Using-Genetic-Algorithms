import pygame as pg
import random
import Classes.settings as s

class Obstacle:
    def __init__(self, x_position):
        self.width = s.OBSTACLE_WIDTH
        self.height = s.SCREEN_HEIGHT
        self.x = x_position
        
        # Randomly select the position for the top obstacle
        self.y_top = random.randint(s.MIN_GAP_Y, s.MAX_GAP_Y)
        
        # Randomly determine the size of the gap between obstacles
        self.gap_size = random.randint(s.MIN_GAP_HEIGHT, s.MAX_GAP_HEIGHT)
        
        # Ensure the bottom of the top obstacle is well above the bottom obstacle
        self.y_bottom = self.y_top + self.gap_size
        
        # Set the speed and color of the obstacles
        self.speed = s.OBSTACLE_SPEED
        self.color = s.OBSTACLE_COLOR

    def move(self):
        # Move the obstacle leftward across the screen
        self.x -= self.speed

    def render(self, screen):
        # Draw the top part of the obstacle (above the gap)
        pg.draw.rect(screen, self.color, (self.x, 0, self.width, self.y_top))
        
        # Draw the bottom part of the obstacle (below the gap)
        pg.draw.rect(screen, self.color, (self.x, self.y_bottom, self.width, s.SCREEN_HEIGHT - self.y_bottom))

    def is_off_screen(self):    
        # Return True if the obstacle has moved off the screen
        return self.x + self.width < 0
