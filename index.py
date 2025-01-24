import pygame as pg

# Initialize Pygame
pg.init()

# Load and scale the bird image
try:
    bird = pg.image.load("images/bird.png")
    scaled_bird = pg.transform.scale(bird, (75, 75))
except Exception as e:
    print(f"Error loading or scaling bird image: {e}")
    pg.quit()
    exit()

# Screen setup
screen = pg.display.set_mode((600, 700))
pg.display.set_caption("Flappy Bird AI")

# Font for Game Over text
font = pg.font.Font(None, 74)
game_over_text = font.render("Game Over!", True, (255, 0, 0))

# Bird's initial position and gravity
bird_x, bird_y = 100, 300
gravity = 0.2

# Game state
running = True
game_over = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
        # Allow key press only if the game is not over
        if not game_over and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            bird_y -= 100

    # Check if the bird hits the edges
    if not game_over and (bird_y < 0 or bird_y > 700 - 75):  # Top and bottom bounds
        game_over = True  # Set game state to "over"
        print("Game Over! The bird hit the edge.")

    # Fill the screen with a background color
    screen.fill((135, 206, 235))

    if game_over:
        # Display the "Game Over" message
        screen.blit(game_over_text, (150, 300))
    else:
        # Draw the bird
        screen.blit(scaled_bird, (bird_x, bird_y))
        bird_y += gravity  # Apply gravity only if the game is not over

    # Update the display
    pg.display.update()

# Quit Pygame
pg.quit()
