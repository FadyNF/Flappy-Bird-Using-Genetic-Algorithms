import pygame as pg
import Classes.settings as s

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = s.BIRD_WIDTH
        self.height = s.BIRD_HEIGHT
        self.image = pg.transform.scale(pg.image.load("images/bird.png"), (self.width, self.height))

        # Movement Variables
        self.y_velocity = 0
        self.gravity = s.GRAVITY  # Gravity accelerates the bird downward
        self.jump_force = s.JUMP_FORCE  # Negative force for an upward jump
        self.max_fall_speed = s.MAX_FALL_SPEED  # Limit the maximum downward speed
        self.alive = True
        
        self.mask = pg.mask.from_surface(self.image)

    def move(self):
        if self.alive:
            # Apply gravity to the velocity
            self.y_velocity += self.gravity

            # Limit the maximum fall speed
            if self.y_velocity > self.max_fall_speed:
                self.y_velocity = self.max_fall_speed

            # Update the bird's position based on the velocity
            self.y += self.y_velocity

    def jump(self):
        # Set velocity to jump force when jumping
        self.y_velocity = self.jump_force

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_bounds(self, screen_height):
        # Check if bird is within screen bounds
        if self.y <= 0 or self.y >= screen_height - self.height:
            self.alive = False

