import pygame
import math
import time

pygame.init()

# Game variables 
score = 0 
strikes = 0
level = 1
fruits = []
bombs = []
ice_cubes = []
frozen = False
frozen_timer = 0 
input_type = None

input_type = select_input_type()

# 

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

  