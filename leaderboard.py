import json
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
FONT = pygame.font.Font(None, 36)

def load_scores():
    try:
        with open('score.json', 'r') as f:
            scores = json.load(f)
        return sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def draw_table(screen, scores):
    header_name = FONT.render("Name", True, WHITE)
    header_score = FONT.render("Score", True, WHITE)
    screen.blit(header_name, (SCREEN_WIDTH // 4, 100))
    screen.blit(header_score, (SCREEN_WIDTH * 3 // 4 - 50, 100))
    
    pygame.draw.line(screen, WHITE, 
                    (SCREEN_WIDTH // 4 - 20, 140),
                    (SCREEN_WIDTH * 3 // 4 + 50, 140), 2)
    
    # Draw scores
    for i, score in enumerate(scores):
        if i == 0:
            color = GOLD
        elif i == 1:
            color = SILVER
        elif i == 2:
            color = BRONZE
        else:
            color = WHITE
            
        name = FONT.render(score['name'], True, color)
        score_text = FONT.render(str(score['score']), True, color)
        
        y_position = 160 + i * 60
        screen.blit(name, (SCREEN_WIDTH // 4, y_position))
        screen.blit(score_text, (SCREEN_WIDTH * 3 // 4 - 50, y_position))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fruit Slicer Leaderboard")
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        screen.fill(BLACK)
        
        # Draw title
        title = FONT.render("TOP 5 PLAYERS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Draw scores table
        scores = load_scores()
        draw_table(screen, scores)
        
        # Draw exit instruction
        exit_text = FONT.render("Press ESC to exit", True, WHITE)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()