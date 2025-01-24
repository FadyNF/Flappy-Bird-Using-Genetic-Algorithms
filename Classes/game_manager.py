import pygame as pg
from Classes.bird import Bird
from Classes.obstacles import Obstacle
import Classes.settings as s

class GameManager:
    def __init__(self):
        # Initialize pygame
        pg.init()
        # Set up the game screen
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        pg.display.set_caption("Flappy Bird AI")
        # Set up the game clock
        self.clock = pg.time.Clock()
        # Create a bird instance
        self.bird = Bird(100, 300)
        # Game state variables
        self.running = True
        self.game_over = False
        # Set up the font for game over text
        self.font = pg.font.Font(None, 74)
        
        self.obstacles = []
        self.obstacle_timer = 0
        
    def handle_events(self):
        # Handle user input events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                
            if not self.game_over and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.bird.jump()
        
    def update(self):
        # Update game state
        if not self.game_over:
            self.bird.move()
            self.bird.check_bounds(s.SCREEN_HEIGHT)
            if not self.bird.alive:
                self.game_over = True
                
            for obstacle in self.obstacles:
                obstacle.move()
                if self.check_collision(obstacle):
                    self.game_over = True
                
            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.x > -s.OBSTACLE_WIDTH]
            
            self.obstacle_timer += 1
            if self.obstacle_timer > 60:
                self.spawn_obstacle()
                self.obstacle_timer = 0
                
                        
    def spawn_obstacle(self):
        x_position = s.SCREEN_WIDTH
        new_obstacle = Obstacle(x_position)
        self.obstacles.append(new_obstacle)
        
        
    def render(self):
        # Render the game screen
        self.screen.fill(s.BG_COLOR)
        if self.game_over:
            # Display game over text
            game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (150, 300))
            
        else:
            self.bird.render(self.screen)
            
            for obstacle in self.obstacles:
                obstacle.render(self.screen)
        
        pg.display.update()
    
    def check_collision(self, obstacle):
        
        # Create masks for the obstacle's top and bottom parts
        top_mask = pg.mask.Mask((obstacle.width, obstacle.y_top), fill=True)
        bottom_mask = pg.mask.Mask((obstacle.width, s.SCREEN_HEIGHT - obstacle.y_bottom), fill=True)

        # Calculate offsets between the bird and the obstacle's top and bottom masks
        offset_top = (obstacle.x - self.bird.x, 0 - self.bird.y)
        offset_bottom = (obstacle.x - self.bird.x, obstacle.y_bottom - self.bird.y)

        # Check for overlap between the bird's mask and the obstacle masks
        collision_top = self.bird.mask.overlap(top_mask, offset_top)
        collision_bottom = self.bird.mask.overlap(bottom_mask, offset_bottom)

        # If either overlaps, return True (collision detected)
        return collision_top or collision_bottom


    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
            
        pg.quit()