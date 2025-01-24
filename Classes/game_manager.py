import pygame as pg
from Classes.bird import Bird
from Classes.BirdGA import BirdGA
from Classes.obstacles import Obstacle
import Classes.settings as s
import random

class GameManager:
    def __init__(self):
        pg.init()
        # Define the full screen dimensions and then divide it into game and scoreboard parts
        self.main_surface = pg.display.set_mode((s.SCREEN_WIDTH + s.SCOREBOARD_WIDTH, s.SCREEN_HEIGHT))
        pg.display.set_caption("Flappy Bird AI")
        self.clock = pg.time.Clock()
        
        # Initialize scoreboard area as part of the same surface
        self.scoreboard_surface = pg.Surface((s.SCOREBOARD_WIDTH, s.SCREEN_HEIGHT))
        
        # Fonts
        self.title_font = pg.font.Font(None, 48)
        self.score_font = pg.font.Font(None, 36)
        
        # GA and game setup
        self.bird_ga = BirdGA(population_size=10, mutation_rate=0.1)
        self.birds = self.bird_ga.population
        
        self.running = True
        self.generation_scores = []
        self.current_generation = 0
        
        self.obstacles = []
        self.obstacle_timer = 0
        
        self.top_5_scores = []
        
        self.spawn_obstacle()
        
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    def update(self):
        # Remove dead birds
        self.birds = [bird for bird in self.birds if bird.alive]
        
        # End game if all birds are dead
        if not self.birds:
            self.reset_generation()
        
        # Move obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move()
            
            # Remove obstacles that are off screen
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
        
        # Spawn new obstacles more frequently
        self.obstacle_timer += 1
        if not self.obstacles or self.obstacle_timer >= 120:
            self.spawn_obstacle()
            self.obstacle_timer = 0
        
        # Move and check birds
        for bird in self.birds:
            bird.move(self.obstacles)
            bird.check_bounds(s.SCREEN_HEIGHT)
            bird.increment_fitness()  # Ensure fitness is incremented
            
            # Check collisions for each bird
            for obstacle in self.obstacles:
                if self.check_collision(bird, obstacle):
                    bird.alive = False
    
    def reset_generation(self):
        # Calculate best fitness in current generation
        best_fitness = max(bird.get_fitness() for bird in self.bird_ga.population)
        
        # Append the current generation number and the best fitness as a tuple
        self.generation_scores.append((self.current_generation, best_fitness))
        
        # Add the best fitness to the top_5_scores list
        self.add_to_top_5(best_fitness)

        self.current_generation += 1
        
        # Evolve population
        self.bird_ga.evolve()
        
        # Reset birds
        self.birds = self.bird_ga.population
        for bird in self.birds:
            bird.reset()
        
        # Clear obstacles
        self.obstacles.clear()
        self.obstacle_timer = 0


    
    def spawn_obstacle(self):
        x_position = s.SCREEN_WIDTH
        new_obstacle = Obstacle(x_position)
        self.obstacles.append(new_obstacle)
    
    def render(self):
        # Clear surfaces
        self.main_surface.fill(s.BG_COLOR)
        self.scoreboard_surface.fill((200, 200, 200))  # Light gray background
        
        # Render game on main surface
        for bird in self.birds:
            bird.render(self.main_surface)
        
        for obstacle in self.obstacles:
            obstacle.render(self.main_surface)
        
        # Render scoreboard
        self.render_scoreboard()
        
        # Draw the scoreboard to the right part of the screen
        self.main_surface.blit(self.scoreboard_surface, (s.SCREEN_WIDTH, 0))
        
        # Update the display
        pg.display.update()
    
    def add_to_top_5(self, fitness_score):
        """Add the new fitness score to the top 5 scores"""
        # Add the new score to the list
        self.top_5_scores.append(fitness_score)
        
        # Sort the list in descending order (highest fitness first)
        self.top_5_scores.sort(reverse=True)
        
        # Keep only the top 5 scores
        if len(self.top_5_scores) > 5:
            self.top_5_scores = self.top_5_scores[:5]

    
    
    def render_scoreboard(self):
        # Minimalistic background (light color or very subtle gradient)
        self.scoreboard_surface.fill((240, 240, 240))  # Light gray background
        
        # Title in simple, clear font with no decoration
        title = self.title_font.render("Top 5 Generation Scores", True, (0, 0, 0))  # Black text for contrast
        title_rect = title.get_rect(centerx=s.SCOREBOARD_WIDTH // 2, top=20)
        self.scoreboard_surface.blit(title, title_rect)
        
        # Sort the generation_scores by best fitness (highest first) and limit to top 5
        sorted_scores = sorted(self.generation_scores, key=lambda x: x[1], reverse=True)[:5]
        
        # Minimalistic rows with simple border and no shadows
        for i, (gen_num, score) in enumerate(sorted_scores, 1):
            # Define the color of the rows (light gray and white alternating)
            row_color = (255, 255, 255) if i % 2 == 0 else (230, 230, 230)
            
            # Create the row rectangle (simple border-radius for smooth edges)
            row_rect = pg.Rect(20, 80 + i * 50, s.SCOREBOARD_WIDTH - 40, 40)
            pg.draw.rect(self.scoreboard_surface, row_color, row_rect, border_radius=8)
            
            # Minimalist text (centered, no effects)
            gen_text = self.score_font.render(f"Gen {gen_num}", True, (0, 0, 0))  # Black text
            score_text = self.score_font.render(f"Best Fitness: {score:.2f}", True, (50, 50, 50))  # Dark gray text
            
            # Position text inside the row (left-aligned for generation, right-aligned for score)
            gen_text_rect = gen_text.get_rect(left=row_rect.left + 20, centery=row_rect.centery)
            score_text_rect = score_text.get_rect(right=row_rect.right - 20, centery=row_rect.centery)
            
            # Blit the text
            self.scoreboard_surface.blit(gen_text, gen_text_rect)
            self.scoreboard_surface.blit(score_text, score_text_rect)



    
    def check_collision(self, bird, obstacle):
        """Collision detection using rectangles"""
        bird_rect = pg.Rect(bird.x, bird.y, bird.width, bird.height)
        top_obstacle_rect = pg.Rect(obstacle.x, 0, obstacle.width, obstacle.y_top)
        bottom_obstacle_rect = pg.Rect(obstacle.x, obstacle.y_bottom, obstacle.width, s.SCREEN_HEIGHT - obstacle.y_bottom)
        
        return (bird_rect.colliderect(top_obstacle_rect) or 
                bird_rect.colliderect(bottom_obstacle_rect))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pg.quit()
