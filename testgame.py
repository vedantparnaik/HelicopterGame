import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Helicopter Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Helicopter settings
heli_width, heli_height = 50, 30
heli_x, heli_y = 100, HEIGHT // 2
heli_speed = 0

# Obstacle settings
obstacle_width = 50
obstacle_gap = 200
obstacle_speed = 5

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False
paused = False
collision_sound_played = False  # Flag to track collision sound state

# Function to get the correct path for bundled files
def resource_path(relative_path):
    # Check if the script is bundled as an executable
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Function to draw the helicopter
def draw_helicopter(x, y):
    pygame.draw.rect(screen, CYAN, (x, y, heli_width, heli_height))
    pygame.draw.rect(screen, BLACK, (x + 10, y - 10, 30, 10))  # Top fan

# Function to draw obstacles
def draw_obstacle(x, gap_y):
    pygame.draw.rect(screen, RED, (x, 0, obstacle_width, gap_y))  # Top part
    pygame.draw.rect(screen, RED, (x, gap_y + obstacle_gap, obstacle_width, HEIGHT - gap_y - obstacle_gap))  # Bottom part

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to draw the corner menu
def draw_corner_menu():
    font_small = pygame.font.Font(None, 24)
    resume_text = font_small.render("Resume", True, WHITE)
    exit_text = font_small.render("Exit", True, WHITE)
    
    screen.blit(resume_text, (WIDTH - 90, 10))
    screen.blit(exit_text, (WIDTH - 90, 40))

# # Load the collision sound and background music
# collision_sound = pygame.mixer.Sound("collision_sound.wav")  # Replace with your sound file
# pygame.mixer.music.load("background_music_.mp3")  # Replace with your background music file
# pygame.mixer.music.play(-1, 0.0)  # Play background music in a loop

# Load the collision sound and background music
collision_sound = pygame.mixer.Sound(resource_path("collision_sound.wav"))  # Use resource_path for correct file path
pygame.mixer.music.load(resource_path("background_music_.mp3"))  # Use resource_path for correct file path
pygame.mixer.music.play(-1, 0.0)  # Play background music in a loop


# Function to draw the game-over menu
def draw_game_over_menu():
    font_large = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

    # Game Over text
    game_over_text = font_large.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    # Restart option
    restart_text = font_small.render("Press R to Restart", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))

    # Exit option
    exit_text = font_small.render("Press Q to Exit", True, WHITE)
    screen.blit(exit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

# Main game loop (updated section for game-over handling)
def main():
    global heli_y, heli_speed, game_over, score, paused, collision_sound_played

    obstacle_x = WIDTH
    obstacle_gap_y = random.randint(100, HEIGHT - 100 - obstacle_gap)

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    heli_speed = -5
                elif event.key == pygame.K_p and not game_over:  # Pause the game
                    paused = True
                elif event.key == pygame.K_r:  # Restart the game after game over
                    if game_over:
                        game_over = False
                        heli_y = HEIGHT // 2
                        obstacle_x = WIDTH
                        score = 0
                        collision_sound_played = False  # Reset collision sound flag
                        pygame.mixer.music.play(-1, 0.0)  # Restart background music
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and not game_over:
                    heli_speed = 5

            if paused or game_over:
                if game_over:
                    draw_game_over_menu()
                else:
                    draw_corner_menu()

                pygame.display.flip()
                continue


        if not game_over:
            heli_y += heli_speed
            obstacle_x -= obstacle_speed

            # Check for collision
            if (
                heli_y < 0 or
                heli_y + heli_height > HEIGHT or
                (obstacle_x < heli_x + heli_width and obstacle_x + obstacle_width > heli_x and
                 (heli_y < obstacle_gap_y or heli_y + heli_height > obstacle_gap_y + obstacle_gap))
            ):
                if not collision_sound_played:
                    collision_sound.play()  # Play collision sound once
                    collision_sound_played = True
                game_over = True
                pygame.mixer.music.stop()  # Stop the background music when game over

            # Reset obstacle and increase score
            if obstacle_x + obstacle_width < 0:
                obstacle_x = WIDTH
                obstacle_gap_y = random.randint(100, HEIGHT - 100 - obstacle_gap)
                score += 1

        # Draw everything
        draw_helicopter(heli_x, heli_y)
        draw_obstacle(obstacle_x, obstacle_gap_y)
        display_score(score)

        pygame.display.flip()
        clock.tick(30)


# Run the game
main()
