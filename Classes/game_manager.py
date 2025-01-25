import pygame as pg
from Classes.BirdGA import BirdGA
from Classes.obstacles import Obstacle
import Classes.settings as s

class GameManager:
    def __init__(self):
        """
        Initializes the game manager, sets up the game window,
        fonts, and initializes the population of birds.
        """
        pg.init()
        # Define the full screen dimensions and then divide it into game and scoreboard parts
        self.main_surface = pg.display.set_mode((s.SCREEN_WIDTH + s.SCOREBOARD_WIDTH, s.SCREEN_HEIGHT))
        pg.display.set_caption("Flappy Bird AI")
        self.clock = pg.time.Clock()
        
        # Initialize scoreboard area as part of the same surface
        self.scoreboard_surface = pg.Surface((s.SCOREBOARD_WIDTH, s.SCREEN_HEIGHT))
        
        # Fonts for title and score
        self.title_font = pg.font.Font(None, 48)
        self.score_font = pg.font.Font(None, 36)
        
        # Genetic Algorithm setup: initializing bird population and other game parameters
        self.bird_ga = BirdGA(population_size=10, mutation_rate=0.1)
        self.birds = self.bird_ga.population
        
        self.running = True
        self.generation_scores = []
        self.current_generation = 0
        
        self.obstacles = []
        self.obstacle_timer = 0
        
        self.top_5_scores = []
        
        # Initial obstacle spawn
        self.spawn_obstacle()
        
    def handle_events(self):
        """Handles events like quitting the game."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    def update(self):
        """Updates the game state: moves obstacles, handles birds, and checks for collisions."""
        # Remove dead birds from the population
        self.birds = [bird for bird in self.birds if bird.alive]
        
        # End the game if all birds are dead
        if not self.birds:
            self.reset_generation()
        
        # Move obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move()
            
            # Remove obstacles that are off the screen
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
        
        # Spawn new obstacles after a certain interval
        self.obstacle_timer += 1
        if not self.obstacles or self.obstacle_timer >= 120:
            self.spawn_obstacle()
            self.obstacle_timer = 0
        
        # Move and update each bird
        for bird in self.birds:
            bird.move(self.obstacles)
            bird.check_bounds(s.SCREEN_HEIGHT)
            bird.increment_fitness()  # Increment fitness to reward bird's performance
            
            # Check for collisions between birds and obstacles
            for obstacle in self.obstacles:
                if self.check_collision(bird, obstacle):
                    bird.alive = False
    
    def reset_generation(self):
        """Resets the game for the next generation of birds."""
        # Get the best fitness score from the current generation
        best_fitness = max(bird.get_fitness() for bird in self.bird_ga.population)
        
        # Record the best fitness score along with the current generation number
        self.generation_scores.append((self.current_generation, best_fitness))
        
        # Add the best fitness score to the top 5 list
        self.add_to_top_5(best_fitness)

        self.current_generation += 1
        
        # Evolve the population of birds based on genetic algorithm
        self.bird_ga.evolve()
        
        # Reset all birds to prepare for the next generation
        self.birds = self.bird_ga.population
        for bird in self.birds:
            bird.reset()
        
        # Clear any obstacles from the screen
        self.obstacles.clear()
        self.obstacle_timer = 0

    def spawn_obstacle(self):
        """Spawns a new obstacle at the right edge of the screen."""
        x_position = s.SCREEN_WIDTH
        new_obstacle = Obstacle(x_position)
        self.obstacles.append(new_obstacle)
    
    def render(self):
        """Renders the game state: birds, obstacles, and scoreboard to the screen."""
        # Clear both the game and scoreboard surfaces
        self.main_surface.fill(s.BG_COLOR)
        self.scoreboard_surface.fill(s.BG_COLOR)
        
        # Render all birds
        for bird in self.birds:
            bird.render(self.main_surface)
        
        # Render all obstacles
        for obstacle in self.obstacles:
            obstacle.render(self.main_surface)
        
        # Render the scoreboard
        self.render_scoreboard()
        
        # Draw the scoreboard to the right of the screen
        self.main_surface.blit(self.scoreboard_surface, (s.SCREEN_WIDTH, 0))
        
        # Draw a vertical line separating the game area and the scoreboard
        pg.draw.line(self.main_surface, (0, 0, 0), 
                    (s.SCREEN_WIDTH, 0), 
                    (s.SCREEN_WIDTH, s.SCREEN_HEIGHT), 
                    width=2)
        
        # Draw generation text at the top of the screen
        gen_text = self.title_font.render(f"Generation: {self.current_generation}", True, (0, 0, 0))
        gen_text_rect = gen_text.get_rect()
        gen_text_rect.centerx = s.SCREEN_WIDTH // 2
        gen_text_rect.top = 10
        self.main_surface.blit(gen_text, gen_text_rect)
        
        # Update the display with the rendered elements
        pg.display.update()   
              
    def add_to_top_5(self, fitness_score):
        """Adds a new fitness score to the list of top 5 scores, maintaining only the top 5 highest scores."""
        # Add the new score to the list
        self.top_5_scores.append(fitness_score)
        
        # Sort the list in descending order (highest fitness first)
        self.top_5_scores.sort(reverse=True)
        
        # Keep only the top 5 highest scores
        if len(self.top_5_scores) > 5:
            self.top_5_scores = self.top_5_scores[:5]
 
    def render_scoreboard(self):
        """Renders the top 5 generation scores to the scoreboard area."""
        # Title for the scoreboard section
        title = self.title_font.render("Top 5 Generation Scores", True, (0, 0, 0))  # Black text for contrast
        title_rect = title.get_rect(centerx=s.SCOREBOARD_WIDTH // 2, top=20)
        self.scoreboard_surface.blit(title, title_rect)
        
        # Sort generation scores by best fitness, in descending order, and limit to top 5
        sorted_scores = sorted(self.generation_scores, key=lambda x: x[1], reverse=True)[:5]
        
        # Render each score as a row in the scoreboard
        for i, (gen_num, score) in enumerate(sorted_scores, 1):
            # Alternate row colors (light gray and white)
            row_color = (255, 255, 255) if i % 2 == 0 else (230, 230, 230)
            
            # Create the row rectangle with a smooth border radius
            row_rect = pg.Rect(20, 80 + i * 50, s.SCOREBOARD_WIDTH - 40, 40)
            pg.draw.rect(self.scoreboard_surface, row_color, row_rect, border_radius=8)
            
            # Render generation and score text inside each row
            gen_text = self.score_font.render(f"Gen {gen_num}", True, (0, 0, 0))  # Black text
            score_text = self.score_font.render(f"Best Fitness: {score:.2f}", True, (50, 50, 50))  # Dark gray text
            
            # Position the text within the row (left-aligned for generation, right-aligned for score)
            gen_text_rect = gen_text.get_rect(left=row_rect.left + 20, centery=row_rect.centery)
            score_text_rect = score_text.get_rect(right=row_rect.right - 20, centery=row_rect.centery)
            
            # Blit the text onto the row
            self.scoreboard_surface.blit(gen_text, gen_text_rect)
            self.scoreboard_surface.blit(score_text, score_text_rect)
    
    def check_collision(self, bird, obstacle):
        """Checks for collisions between a bird and an obstacle using rectangle collision detection."""
        bird_rect = pg.Rect(bird.x, bird.y, bird.width, bird.height)
        top_obstacle_rect = pg.Rect(obstacle.x, 0, obstacle.width, obstacle.y_top)
        bottom_obstacle_rect = pg.Rect(obstacle.x, obstacle.y_bottom, obstacle.width, s.SCREEN_HEIGHT - obstacle.y_bottom)
        
        return (bird_rect.colliderect(top_obstacle_rect) or 
                bird_rect.colliderect(bottom_obstacle_rect))
    
    def run(self):
        """Main game loop that continuously handles events, updates the game state, and renders everything."""
        while self.running:
            self.handle_events()  # Handle events (such as quitting)
            self.update()  # Update game state (move birds, check collisions)
            self.render()  # Render the game state to the screen
            self.clock.tick(60)  # Limit the frame rate to 60 FPS
        
        pg.quit()  # Quit Pygame when the game loop ends
