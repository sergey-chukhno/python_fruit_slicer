import pygame
import random
import sys
import json
from translations import TRANSLATIONS
from menu_system import DropdownMenu
import subprocess # to launch leaderboard from menu


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Constants 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.Font(None, 36)

# Game settings
GRAVITY = 0.5  
BASE_SPEED = 0.005  # Base speed for level 2 and above
INITIAL_SPEED = BASE_SPEED / 2  # Initial speed for level 1 (half of base speed)
LEVEL_SPEED_INCREASE = 1.3
FRUIT_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Load assets
FRUIT_IMAGE = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(FRUIT_IMAGE, RED, (25, 25), 25)
BOMB_IMAGE = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(BOMB_IMAGE, WHITE, (25, 25), 25)
ICE_CUBE_IMAGE = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(ICE_CUBE_IMAGE, BLUE, (25, 25), 25)

# Game classes
class Fruit:
    def __init__(self, letter, image, x, y, vx, vy):
        self.letter = letter
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = vx
        self.vy = vy
        self.has_peaked = False
        

    def update_position(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += GRAVITY 

        if self.vy >= 0:
            self.has_peaked = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = FONT.render(self.letter, True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

class Bomb:
    def __init__(self, letter, image, x, y, vx, vy):
        self.letter = letter
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = vx
        self.vy = vy

    def update_position(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += GRAVITY

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = FONT.render(self.letter, True, RED)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

class IceCube:
    def __init__(self, letter, image, x, y, vx, vy):
        self.letter = letter
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = vx
        self.vy = vy

    def update_position(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += GRAVITY

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = FONT.render(self.letter, True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)
        
class Game:
    def __init__(self):
        self.score = 0
        self.strikes = 0
        self.level = 1
        self.fruits = []
        self.bombs = []
        self.ice_cubes = []
        self.frozen = False
        self.frozen_timer = 0
        self.mode = None  # 'mouse' or 'keyboard'
        self.speed = INITIAL_SPEED
        self.menu = DropdownMenu(TRANSLATIONS)
        self.current_language = 'English'
        self.game_started = False

    def get_max_objects(self):
        return 1 + self.level   

    def get_total_objects(self):
        return len(self.fruits) + len(self.bombs) + len(self.ice_cubes)

    def handle_key_press(self, key):
        try:
            key_char = chr(key).upper()
        except ValueError:
            return
        self.slice_objects(key_char=key_char)

    def handle_swipe(self, position):
        self.slice_objects(position=position)

    def slice_objects(self, key_char=None, position=None):
        if key_char:
            sliced_fruits = [fruit for fruit in self.fruits if fruit.letter == key_char]
            sliced_bombs = [bomb for bomb in self.bombs if bomb.letter == key_char]
            sliced_ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube.letter == key_char]
        else:
            sliced_fruits = [fruit for fruit in self.fruits if fruit.rect.collidepoint(position)]
            sliced_bombs = [bomb for bomb in self.bombs if bomb.rect.collidepoint(position)]
            sliced_ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube.rect.collidepoint(position)]

        if sliced_fruits:
            self.score += len(sliced_fruits)
            self.fruits = [fruit for fruit in self.fruits if fruit not in sliced_fruits]
            print(f"Combo! Sliced {len(sliced_fruits)} fruits!")
            
            # Level up every 10 points
            if self.score > 0 and self.score % 10 == 0:
                self.level += 1
                if self.level == 2:
                    self.speed = BASE_SPEED
                else:
                    self.speed *= LEVEL_SPEED_INCREASE
                print(f"Level up! Now at level {self.level}")

        if sliced_bombs:
            print("You sliced a bomb! Game over!")
            self.end_game()

        if sliced_ice_cubes:
            self.frozen = True
            self.frozen_timer = pygame.time.get_ticks()
            print("Game frozen for 15 seconds!")
            self.ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube not in sliced_ice_cubes]

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.frozen and current_time - self.frozen_timer >= 3000:  # 15 seconds
            self.frozen = False

        if not self.frozen:
            for fruit in self.fruits:
                fruit.update_position()
            for bomb in self.bombs:
                bomb.update_position()
            for ice_cube in self.ice_cubes:
                ice_cube.update_position()

            # Remove objects that are no longer on the screen

            # For fruits, we check if they have peaked and fallen below the screen to get a strike
            fruits_to_remove = []
            for fruit in self.fruits[:]:
                if fruit.has_peaked and fruit.rect.y >= SCREEN_HEIGHT: 
                    self.strikes += 1
                    fruits_to_remove.append(fruit)
                    print(f'Strike! Missed a fruit. Strikes: {self.strikes}')

            for fruit in fruits_to_remove:
                self.fruits.remove(fruit)

            self.bombs = [bomb for bomb in self.bombs if bomb.rect.y < SCREEN_HEIGHT]
            self.ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube.rect.y < SCREEN_HEIGHT]

            if self.strikes >= 3:
                print("Game over! You missed too many fruits.")
                self.end_game()

            if self.get_total_objects() < self.get_max_objects():
                self.spawn_objects()

    def spawn_objects(self):
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = SCREEN_HEIGHT 
        vx = random.uniform(-self.speed, self.speed)
        
        base_upward_velocity = 21 
        vy = random.uniform(-base_upward_velocity * 1.2, -base_upward_velocity)

        # Only spawn if we haven't reached the maximum objects for this level
        if self.get_total_objects() < self.get_max_objects():
            if random.random() < 0.7:  # 70% chance to spawn a fruit
                letter = random.choice(FRUIT_LETTERS)
                self.fruits.append(Fruit(letter, FRUIT_IMAGE, x, y, vx, vy))
            elif random.random() < 0.9:  # 20% chance to spawn a bomb
                letter = random.choice(FRUIT_LETTERS)
                self.bombs.append(Bomb(letter, BOMB_IMAGE, x, y, vx, vy))
            else:  # 10% chance to spawn an ice cube
                letter = random.choice(FRUIT_LETTERS)
                self.ice_cubes.append(IceCube(letter, ICE_CUBE_IMAGE, x, y, vx, vy))

    def draw(self, screen):
        screen.fill(BLACK)
        # Draw game objects
        for fruit in self.fruits:
            fruit.draw(screen)
        for bomb in self.bombs:
            bomb.draw(screen)
        for ice_cube in self.ice_cubes:
            ice_cube.draw(screen)

        # Draw score and strikes
        score_text = FONT.render(f"{TRANSLATIONS[self.current_language]['Score']}: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        strikes_text = FONT.render(f"{TRANSLATIONS[self.current_language]['Strikes']}: {self.strikes}", True, WHITE)
        screen.blit(strikes_text, (10, 50))
        level_text = FONT.render(f"{TRANSLATIONS[self.current_language]['Level']}: {self.level}", True, WHITE)
        screen.blit(level_text, (10, 90))

        # Draw frozen status
        if self.frozen:
            frozen_text = FONT.render("FROZEN!", True, BLUE)
            screen.blit(frozen_text, (SCREEN_WIDTH - 150, 10))

        self.menu.draw(screen)

    def end_game(self):
      print(f"Your final score: {self.score}")
    
      # Create Pygame input box for name
      input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 30, SCREEN_WIDTH // 2, 60)
      color_inactive = pygame.Color('lightskyblue3')
      color_active = pygame.Color('dodgerblue2')
      color = color_inactive
      active = False
      text = ''
      done = False
      
      # Load existing scores or create new file
      try:
          with open('score.json', 'r') as f:
              scores = json.load(f)
      except (FileNotFoundError, json.JSONDecodeError):
          scores = []
      
      while not done:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
              if event.type == pygame.MOUSEBUTTONDOWN:
                  active = input_box.collidepoint(event.pos)
                  color = color_active if active else color_inactive
              if event.type == pygame.KEYDOWN:
                  if active:
                      if event.key == pygame.K_RETURN:
                          # Save score and exit
                          scores.append({"name": text, "score": self.score})
                          with open('score.json', 'w') as f:
                              json.dump(scores, f)
                          done = True
                      elif event.key == pygame.K_BACKSPACE:
                          text = text[:-1]
                      else:
                          if len(text) < 20:  # Limit name length
                              text += event.unicode
          
          # Draw input box
          screen = pygame.display.get_surface()
          screen.fill(BLACK)
          txt_surface = FONT.render(text, True, color)
          width = max(SCREEN_WIDTH // 2, txt_surface.get_width() + 10)
          input_box.w = width
          screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
          pygame.draw.rect(screen, color, input_box, 2)
          
          # Draw prompt text
          prompt_text = FONT.render("Enter your name:", True, WHITE)
          screen.blit(prompt_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 80))
          
          pygame.display.flip()
      
      pygame.quit()
      sys.exit()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()

    game = Game()
    game.mode = 'keyboard'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.end_game()

            menu_selection, action_type = game.menu.handle_event(event)
            if menu_selection:
                if menu_selection == 'Exit':
                    game.end_game()
                elif menu_selection == 'New game':
                    game = Game()  
                    game.mode = 'keyboard'
                    game.game_started = True
                elif menu_selection in ['English', 'French', 'Russian', 'Chinese']:
                    game.current_language = menu_selection
                    game.menu.current_language = menu_selection
                elif menu_selection == 'Show leaderboard':
                    subprocess.Popen([sys.executable, 'leaderboard.py'])
                elif menu_selection in ['Classic game', 'Zen mode', 'Fruit Attack']:
                    game = Game()
                    game.mode = 'keyboard'
                    game.game_started = True
                  
                    if menu_selection == 'Zen mode':
                        game.strikes = float('inf')  # No game over from strikes in Zen mode
                    elif menu_selection == 'Fruit Attack':
                        game.speed *= 2  # Double the speed for Fruit Attack mode
            
            if not game.menu.is_open and game.game_started:  # Add both conditions
                if game.mode == 'mouse':
                    if event.type == pygame.MOUSEBUTTONDOWN:  # Removed menu.is_open check
                        game.handle_swipe(event.pos)
                elif game.mode == 'keyboard':
                    if event.type == pygame.KEYDOWN:  # Removed menu.is_open check
                        game.handle_key_press(event.key)

        if not game.menu.is_open and game.game_started: 
            game.update()
          
        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()