import pygame
import random
import os

pygame.init()

# Constants 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.Font(None, 36)

GRAVITY = 0.5  
INITIAL_SPEED = 8
LEVEL_SPEED_INCREASE = 1.3
FRUIT_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Game assets to be replaced by real assets in the final version

FRUIT_IMAGE = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(FRUIT_IMAGE, RED, (25, 25), 25)
BOMB_IMAGE = pygame.Surface((60, 60), pygame.SRCALPHA)
pygame.draw.circle(BOMB_IMAGE, WHITE, (30, 30), 30)
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

    def update_position(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += GRAVITY  

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = FONT.render(self.letter, True, WHITE)
        screen.blit(text, self.rect.center)

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
        screen.blit(text, self.rect.center)

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
        screen.blit(text, self.rect.center)

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
        self.mode = None 
        self.speed = INITIAL_SPEED









# Game loop
while True: 
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:
      quit_game()
    
    if input_type == 'mouse': 
      if event.type == pygame.MOUSEBUTTONDOWN:
        handle_swipe(event.position)
    
    if input_type == 'keyboard':
      if event.type == pygame.KEYDOWN:
        handle_key_press(event.key)

    if input_type == 'hand gesture':
      pass
  
  # update game
  if not frozen: 
    move_objects()
    if input_type == 'mouse':
      check_collision_mouse()
    elif input_type == 'keyboard':
      check_collision_keyboard()
    else:
      pass
    update_score_and_strikes()
    check_level_progression()

  # render game
  draw_background()
  draw_objects()
  if input_type == 'keyboard':
    draw_letters()
  draw_score_and_strikes()
  draw_level()

  # end game condition
  if strikes => 3 ou bomb_sliced: 
    quit_game()
  
  # update game
  pygame.display.flip()

  