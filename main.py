import pygame
import random
import sys
import json
import os

pygame.init()
pygame.mixer.init()

# Game settings

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Ninja")

LANGUAGE = "en"
sound_effect = True

cursor_img = pygame.image.load("Image/shuriken_cursor.png")
cursor_img = pygame.transform.scale(cursor_img, (50, 50))
pygame.mouse.set_visible(False)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (79, 79, 79)

# Game constants
GRAVITY = 0.3
BASE_SPEED = 0.001
INITIAL_SPEED = BASE_SPEED / 2
LEVEL_SPEED_INCREASE = 1.3
FRUIT_LETTERS = "ABCDE"
FONT = pygame.font.Font("Image/CFCrayons-Regular.ttf", 50)
font_s = pygame.font.Font("Image/CFCrayons-Regular.ttf", 25)
font_xs = pygame.font.Font("Image/CFCrayons-Regular.ttf", 15)

# Game assets 

#  Audio files

menu_music =  pygame.mixer_music.load("Audio/Menu_Music.mp3")
next_sound = pygame.mixer.Sound("Audio/sound-effects/Next_button.wav")
selected_sound = pygame.mixer.Sound("Audio/sound-effects/Pause.wav")
apple_sound = pygame.mixer.Sound("Audio/sound-effects/Impact-Apple.wav")
banana_sound = pygame.mixer.Sound("Audio/sound-effects/Impact-Banana.wav")
coco_sound = pygame.mixer.Sound("Audio/sound-effects/Impact-Coconut.wav")
orange_sound = pygame.mixer.Sound("Audio/sound-effects/Impact-Orange.wav")
pineapple_sound = pygame.mixer.Sound("Audio/sound-effects/Impact-Pineapple.wav")
watermelon_sound = pygame.mixer.Sound("Audio/sound-effects/Impact-Watermelon.wav")
bomb_fuse = pygame.mixer.Sound("Audio/sound-effects/Bomb-Fuse.wav")
start_sound = pygame.mixer.Sound("Audio/sound-effects/Game-start.wav")
over_sound = pygame.mixer.Sound("Audio/sound-effects/Game-Over.wav")
life_sound = pygame.mixer.Sound("Audio/sound-effects/penalty.wav")
best_sound =  pygame.mixer.Sound("Audio/sound-effects/New-best-score.wav")
throw_sound = pygame.mixer.Sound("Audio/sound-effects/Throw-fruit.wav")
explosion_sound = pygame.mixer.Sound("Audio/sound-effects/Bomb-explode.wav")

# Game images
background_image = pygame.transform.scale(pygame.image.load("Image/background.png"), (800, 600))
play_button = pygame.transform.scale(pygame.image.load("Image/play.png"), (250, 250))
play_select = pygame.transform.scale(pygame.image.load("Image/play2.png"), (250, 250))
play_button_fr = pygame.transform.scale(pygame.image.load("Image/play_fr.png"), (250, 250))
settings_button = pygame.transform.scale(pygame.image.load("Image/sett.png"), (250, 250))
settings_select = pygame.transform.scale(pygame.image.load("Image/sett2.png"), (250, 250))
settings_button_fr = pygame.transform.scale(pygame.image.load("Image/setting_fr.png"), (250, 250))
score_button = pygame.transform.scale(pygame.image.load("Image/scores.png"), (250,250))
score_select = pygame.transform.scale(pygame.image.load("Image/score_sel.png"), (250,250))
sun_image = pygame.transform.scale(pygame.image.load("Image/sun.png"), (400, 400))
kunai_image = pygame.transform.scale(pygame.image.load("Image/Kunai.png"), (150, 150))
kunai_two = pygame.transform.scale(pygame.image.load("Image/Kunai_two.png"), (150, 150))
kunai_three =  pygame.transform.scale(pygame.image.load("Image/Kunai_three.png"), (150, 150))
kunai_four =  pygame.transform.scale(pygame.image.load("Image/Kunai_four.png"), (150, 150))
draw_menu = pygame.transform.scale(pygame.image.load("Image/DrawMenu.png"), (800, 500))
logo = pygame.transform.scale(pygame.image.load("Image/logo.png"), (300, 300))
tree = pygame.transform.scale(pygame.image.load("Image/Tree.png"), (400, 300))
red_sp = pygame.transform.scale(pygame.image.load("Image/splash_red.png"), (80, 80))
yellow_sp = pygame.transform.scale(pygame.image.load("Image/splash_yellow.png"), (80, 80))
orange_sp = pygame.transform.scale(pygame.image.load("Image/splash_orange.png"), (80, 80))
apple_cut = pygame.transform.scale(pygame.image.load("Image/apple_slash.png"), (100, 100))
heart = pygame.transform.scale(pygame.image.load("Image/heart.png"), (50, 50))
heart_loss = pygame.transform.scale(pygame.image.load("Image/heart_loss.png"), (50, 50))
back_arrow = pygame.transform.scale(pygame.image.load("Image/Back_Arrow.png"), (150, 150))
france_flag = pygame.transform.scale(pygame.image.load("Image/France_Draw.png"), (150, 150))
england_flag = pygame.transform.scale(pygame.image.load("Image/England_Draw.png"), (150, 150))
music_image = pygame.transform.scale(pygame.image.load("Image/music_logo.png"), (150, 150))
music_two = pygame.transform.scale(pygame.image.load("Image/music_second.png"), (150, 150))
no_music = pygame.transform.scale(pygame.image.load("Image/no_music.png"), (150, 150))
no_sound_img = pygame.transform.scale(pygame.image.load("Image/sound_off.png"), (150, 150))
on_sound_img = pygame.transform.scale(pygame.image.load("Image/sound_on.png"), (150, 150))
achivement_icon = pygame.transform.scale(pygame.image.load("Image/Achivement.png"), (80, 80))
achivement_case = pygame.transform.scale(pygame.image.load("Image/achiv_case.png"), (50, 50))
achivement_box = pygame.transform.scale(pygame.image.load("Image/achiv_contener.png"), (550, 200))
achivement_win = pygame.transform.scale(pygame.image.load("Image/Achivement.png"), (50, 50))
pause_img = pygame.transform.scale(pygame.image.load("Image/pause.png"), (80, 80))
resume_img = pygame.transform.scale(pygame.image.load("Image/resume.png"), (150, 150))
quit_img = pygame.transform.scale(pygame.image.load("Image/quit_img.png"), (150, 150))
replay_img = pygame.transform.scale(pygame.image.load("Image/replay.png"), (150, 150))


FRUIT_IMAGE = [
    pygame.transform.scale(pygame.image.load("Image/apple.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/banana.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/coconut.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/orange.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/pineapple.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/watermelon.png"), (80, 80))
]
BOMB_IMAGE = pygame.transform.scale(pygame.image.load("Image/Bomb.png"), (80, 80))
BOMB_EXP = pygame.transform.scale(pygame.image.load("Image/explosion.png"), (80, 80))
ICE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load("Image/freeze_fruit.png"), (100, 100))
FRUIT_SPLASH = [
    pygame.transform.scale(pygame.image.load("Image/splash_red.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/splash_orange.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Image/splash_yellow.png"), (80, 80)),
]

play_click = pygame.Rect(300, 200, 200, 80)
settings_click = pygame.Rect(300, 300, 200, 80)
score_click = pygame.Rect(300,400, 200, 80)
achivement_click = pygame.Rect(680,0,80,80)

# Game Classes
class Fruit:
    def __init__(self, letter, image, x, y, vx, vy):
        self.letter = letter
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = vx
        self.vy = vy
        self.has_peaked = False
        self.sound = self.get_fruit_sound(image)
    
    def get_fruit_sound(self, image):
        if image == FRUIT_IMAGE[0]: 
            return apple_sound
        elif image == FRUIT_IMAGE[1]:  
            return banana_sound
        elif image == FRUIT_IMAGE[2]:  
            return coco_sound
        elif image == FRUIT_IMAGE[3]:
            return orange_sound
        elif image == FRUIT_IMAGE[4]: 
            return pineapple_sound
        elif image == FRUIT_IMAGE[5]:
            return watermelon_sound
        return orange_sound

    def update_position(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += GRAVITY
        if self.vy >= 0:
            self.has_peaked = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = FONT.render(self.letter, True, GREEN)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Bomb:
    def __init__(self, letter, image, x, y, vx, vy):
        self.letter = letter
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = vx
        self.vy = vy
        pygame.mixer.Sound.play(bomb_fuse)

    def update_position(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += GRAVITY

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = FONT.render(self.letter, True, RED)
        text_rect = text.get_rect(center=self.rect.center)
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
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.achievements = {
            "fruit_master": False,
            "bomb_dodger": False, 
            "ice_breaker": False
        }
        self.fruits_cut = 0
        self.bombs_dodged = 0
        self.ice_cubes_cut = 0  

        self.score = 0
        self.strikes = 0
        self.level = 1
        self.fruits = []
        self.bombs = []
        self.explosion = None
        self.explosion_timer = None 
        self.ice_cubes = []
        self.splashes = []
        self.frozen = False
        self.frozen_timer = 0
        self.mode = 'keyboard'
        self.speed = INITIAL_SPEED
        self.running = True
        self.best = False
        self.best_timer = 0 
        self.paused = False
        self.combo_message = None 
        self.combo_timer = 0
        self.load_achievements()

    # Define max num of objects on the screen
    def get_max_objects(self):
        return 1 + self.level

    def get_total_objects(self):
        return len(self.fruits) + len(self.bombs) + len(self.ice_cubes)

    # Game input: keyboard
    def handle_key_press(self, key):
        try:
            key_char = chr(key).upper()
        except ValueError:
            return
        self.slice_objects(key_char=key_char)

    # Function for fruit slicing
    def slice_objects(self, key_char=None, position=None):
        if key_char:
            sliced_fruits = [fruit for fruit in self.fruits if fruit.letter == key_char]
            sliced_bombs = [bomb for bomb in self.bombs if bomb.letter == key_char]
            sliced_ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube.letter == key_char]

        combo_count = len(sliced_fruits)

        if combo_count > 0:
            self.fruits_cut += combo_count 
            self.score += combo_count * combo_count 

        for fruit in sliced_fruits:
            pygame.mixer.Sound.play(fruit.sound)

        self.fruits = [fruit for fruit in self.fruits if fruit not in sliced_fruits]

        if combo_count > 1:
            self.combo_message = f"Combo x{combo_count}!"
            self.combo_timer = pygame.time.get_ticks()

        if sliced_bombs:
            sliced_bomb = sliced_bombs[0]
            self.explosion = {
                "image": BOMB_EXP,
                "position": sliced_bomb.rect.topleft,
                "timer": 1000
            }
            self.explosion_timer = pygame.time.get_ticks()
            pygame.mixer.stop()
            pygame.mixer.Sound.play(explosion_sound)
            self.bombs = [bomb for bomb in self.bombs if bomb not in sliced_bombs]

        if sliced_ice_cubes:
            self.ice_cubes_cut += len(sliced_ice_cubes)
            self.frozen = True
            self.frozen_timer = pygame.time.get_ticks()
            self.ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube not in sliced_ice_cubes]

    def check_achievements(self):
        if self.fruits_cut >= 100 and not self.achievements["fruit_master"]:
            self.achievements["fruit_master"] = True
            self.save_achievements()
            print("Fruit Master débloqué !")

        if self.bombs_dodged >= 10 and not self.achievements["bomb_dodger"]:
            self.achievements["bomb_dodger"] = True
            self.save_achievements()
            print("Bomb Dodger débloqué !")

        if self.ice_cubes_cut >= 5 and not self.achievements["ice_breaker"]:
            self.achievements["ice_breaker"] = True
            self.save_achievements() 
            print("Ice Breaker débloqué !")


    def save_achievements(self):
        with open("achievements.json", "w") as f:
            json.dump(self.achievements, f, indent=4)
        
    def load_achievements(self):
        if os.path.exists("achievements.json"): 
            with open("achievements.json", "r") as f:
                try:
                    self.achievements = json.load(f) 
                except json.JSONDecodeError:
                    print("Erreur .json")
                
    def count_unlocked_achievements(self):
        return sum(1 for achievement in self.achievements.values() if achievement)

    # Game update method
    def update(self):
        current_time = pygame.time.get_ticks()

        self.check_achievements()

        if self.explosion:
            if current_time - self.explosion_timer >= self.explosion["timer"]:
                self.end_game() 
                return
            
        if self.frozen and current_time - self.frozen_timer >= 5000:
            self.frozen = False

        if not self.frozen:
            for fruit in self.fruits:
                fruit.update_position()
            for bomb in self.bombs:
                bomb.update_position()
            for ice_cube in self.ice_cubes:
                ice_cube.update_position()

            self.splashes = [splash for splash in self.splashes if splash["timer"] > 0]
            for splash in self.splashes:
                splash["timer"] -= 16

            # Remove objects from screen
            fruits_to_remove = []
            for fruit in self.fruits[:]:
                if fruit.has_peaked and fruit.rect.y >= SCREEN_HEIGHT:
                    self.strikes += 1
                    fruits_to_remove.append(fruit)
                    pygame.mixer.Sound.play(life_sound)

            for fruit in fruits_to_remove:
                self.fruits.remove(fruit)

            for bomb in self.bombs:
                if bomb.rect.y >= SCREEN_HEIGHT:
                    self.bombs_dodged += 1
                    bomb_fuse.stop() 

            self.bombs = [bomb for bomb in self.bombs if bomb.rect.y < SCREEN_HEIGHT]
            self.ice_cubes = [ice_cube for ice_cube in self.ice_cubes if ice_cube.rect.y < SCREEN_HEIGHT]

            if self.strikes >= 3:
                bomb_fuse.stop()
                self.end_game()

            if self.get_total_objects() < self.get_max_objects():
                self.spawn_objects()

    def show_combo(self, combo_count):
        text = FONT.render(f"Combo x{combo_count}!", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))  
        pygame.display.flip()
        pygame.time.delay(5000) 

    # Function to spawn fruits on the screen
    def spawn_objects(self):
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = SCREEN_HEIGHT
        vx = random.uniform(-self.speed, self.speed)
        base_upward_velocity = 15
        vy = random.uniform(-base_upward_velocity * 1.2, -base_upward_velocity)

        if self.get_total_objects() < self.get_max_objects():
            if random.random() < 0.7:
                letter = random.choice(FRUIT_LETTERS)
                image = random.choice(FRUIT_IMAGE)
                self.fruits.append(Fruit(letter, image, x, y, vx, vy))
                pygame.mixer.Sound.play(throw_sound)
            elif random.random() < 0.9:
                letter = random.choice(FRUIT_LETTERS)
                self.bombs.append(Bomb(letter, BOMB_IMAGE, x, y, vx, vy))
                pygame.mixer.Sound.play(throw_sound)
            else:
                letter = random.choice(FRUIT_LETTERS)
                self.ice_cubes.append(IceCube(letter, ICE_CUBE_IMAGE, x, y, vx, vy))
                pygame.mixer.Sound.play(throw_sound)

    # Drawing elements on the screen 
    def draw(self, screen):
        screen.blit(background_image, (0, 0))
        
        for splash in self.splashes:
            screen.blit(splash["image"], splash["position"])   
        for fruit in self.fruits:
            fruit.draw(screen)
        for bomb in self.bombs:
            bomb.draw(screen)
        for ice_cube in self.ice_cubes:
            ice_cube.draw(screen)


        if self.combo_message and pygame.time.get_ticks() - self.combo_timer < 1000:
            combo_text = FONT.render(self.combo_message, True, RED)
            screen.blit(combo_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
        else:
            self.combo_message = None

        if self.explosion:
            screen.blit(self.explosion["image"], self.explosion["position"])
        
        try:
            with open('score.json', 'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
    
        best_score = 0
        if scores:
            best_score = max(score['score'] for score in scores)


        if self.score > best_score and self.best == False:
            pygame.mixer.Sound.play(best_sound)
            best_text = FONT.render("BEST SCORE", True, BLACK)
            screen.blit(best_text,(350,350))
            self.best = True
            self.best_score_timer = pygame.time.get_ticks() 
        
        if self.best and pygame.time.get_ticks() - self.best_score_timer < 3000:
            if LANGUAGE == "en":
                best_text = FONT.render("BEST SCORE", True, BLACK)
                screen.blit(best_text, (275, 100))
            elif LANGUAGE =="fr":
                best_text = FONT.render("MEILLEUR SCORE", True, BLACK)
                screen.blit(best_text, (250, 100))
    

        score_text = FONT.render(f" : {self.score}", True, BLACK)
        screen.blit(score_text, (50, 15))
        screen.blit(pygame.transform.scale(FRUIT_IMAGE[0], (50, 50)), (0, 10))
        if LANGUAGE == "en":
            best_text = font_s.render(f"BEST : {best_score} ", True,BLACK)
        elif LANGUAGE == "fr":
            best_text = font_s.render(f"MEILLEUR : {best_score} ", True,BLACK)
        screen.blit(best_text, (10, 60))
        
        for i in range(3):
            if i < (3 - self.strikes):
                screen.blit(heart, (625 + i * 60, 10))
            else:
                screen.blit(heart_loss, (625 + i * 60, 10))

        if self.frozen:
            frozen_text = FONT.render("FROZEN!", True, BLUE)
            screen.blit(frozen_text, (SCREEN_WIDTH - 475, 150))

        screen.blit(pause_img, (10, SCREEN_HEIGHT - 80))
        self.pause_rect = pygame.Rect(10, SCREEN_HEIGHT - 80, 80, 80)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x, mouse_y))

    def draw_pause_menu(self, screen):
        pause_menu_rect = pygame.Rect(250, 200, 300, 200)
        screen.blit(draw_menu,(0,50))  

        pause_text = FONT.render("Pause", True, (0, 0, 0))
        screen.blit(pause_text, (350,150))

        self.resume_rect = pygame.Rect(225, 250, 100, 100)
        pygame.draw.rect(screen,GREEN, self.resume_rect,3)
        screen.blit(resume_img,(200,225))

        self.quit_rect = pygame.Rect(350, 250, 100, 100)
        pygame.draw.rect(screen,GREEN, self.quit_rect,3)
        screen.blit(quit_img,(325,225))

        self.replay_rect = pygame.Rect(475, 250, 100, 100)
        pygame.draw.rect(screen,GREEN, self.replay_rect,3)
        screen.blit(replay_img,(450,225))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x, mouse_y))
        pygame.display.flip() 

    # Game over function
    def end_game(self):
        self.running = False
        pygame.mixer.stop()
        pygame.mixer.Sound.play(over_sound)

        input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 30, SCREEN_WIDTH // 2, 60)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False
        
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
                            if text.strip():
                                scores.append({"name": text, "score": self.score})
                                scores.sort(key=lambda x: x["score"], reverse=True)
                                scores = scores[:10]
                                with open('score.json', 'w') as f:
                                    json.dump(scores, f)
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if len(text) < 20:
                                text += event.unicode
            
            screen = pygame.display.get_surface()
            screen.blit(background_image, (0, 0))
            
            
            for i, score_entry in enumerate(scores[:4]):
                score_text = FONT.render(
                    f"{score_entry['name']}: {score_entry['score']}", 
                    True, 
                    BLACK
                )
                screen.blit(score_text, (325,350+i*50))
            
            if LANGUAGE == "en":
                game_over_text = FONT.render("Game Over!", True, BLACK)
                final_score_text = FONT.render(f"Your Score: {self.score}", True, BLACK)
                screen.blit(game_over_text, (300,100))
                screen.blit(final_score_text, (280,150))
                prompt_text = FONT.render("Enter your name:", True, BLACK)
                screen.blit(prompt_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 80))
            elif LANGUAGE == "fr":
                game_over_text = FONT.render("Partie Terminer!", True, BLACK)
                final_score_text = FONT.render(f"Ton Score: {self.score}", True, BLACK)
                screen.blit(game_over_text, (250,100))
                screen.blit(final_score_text, (280,150))
                prompt_text = FONT.render("Entre ton nom:", True, BLACK)
                screen.blit(prompt_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 80))
            
            
            txt_surface = FONT.render(text, True, color)
            width = max(SCREEN_WIDTH // 2, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(cursor_img, (mouse_x, mouse_y))
            
            pygame.display.flip()

def settings_menu():
    global LANGUAGE
    global cursor_img
    global sound_effect
    running = True
    title_font = pygame.font.Font("Image/CFCrayons-Regular.ttf", 35)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pygame.mixer.Sound.play(selected_sound)
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if france_rect.collidepoint(mouse_pos):
                        LANGUAGE = "fr"
                        cursor_img = pygame.transform.scale(pygame.image.load("Image/bread_cursor.png"),(50,50))
                        pygame.mixer.Sound.play(selected_sound)
                    elif england_rect.collidepoint(mouse_pos):
                        LANGUAGE = "en"
                        cursor_img = pygame.transform.scale(pygame.image.load("Image/shuriken_cursor.png"),(50,50))
                        pygame.mixer.Sound.play(selected_sound)
                    elif back_rect.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(selected_sound)
                        running = False
                    elif music_one_rect.collidepoint(mouse_pos):
                        pygame.mixer_music.load("Audio/Menu_Music.mp3")
                        pygame.mixer_music.play()
                    elif music_two_rect.collidepoint(mouse_pos):
                        pygame.mixer_music.load("Audio/music_second.mp3")
                        pygame.mixer_music.play()
                    elif no_music_rect.collidepoint(mouse_pos):
                        pygame.mixer_music.stop()
                    elif no_sound_rect.collidepoint(mouse_pos):
                        sound_effect = not sound_effect

                        selected_sound.set_volume(1.0 if sound_effect else 0.0)
                        next_sound.set_volume(1.0 if sound_effect else 0.0)
                        apple_sound.set_volume(1.0 if sound_effect else 0.0)
                        banana_sound.set_volume(1.0 if sound_effect else 0.0)
                        coco_sound.set_volume(1.0 if sound_effect else 0.0)
                        orange_sound.set_volume(1.0 if sound_effect else 0.0)
                        pineapple_sound.set_volume(1.0 if sound_effect else 0.0)
                        watermelon_sound.set_volume(1.0 if sound_effect else 0.0)
                        bomb_fuse.set_volume(1.0 if sound_effect else 0.0)
                        start_sound.set_volume(1.0 if sound_effect else 0.0)
                        over_sound.set_volume(1.0 if sound_effect else 0.0)


        if LANGUAGE == "en":
            language_text = title_font.render("Language : ", True, BLACK)
            music_text= title_font.render("Musics : ", True, BLACK)
        elif LANGUAGE == "fr":
            language_text = title_font.render("Langues : ", True, BLACK)
            music_text= title_font.render("Musiques : ", True, BLACK)

        screen.blit(background_image, (0, 0))
        screen.blit(draw_menu, (0, 50))
        screen.blit(language_text, (200,150))
        screen.blit(france_flag,(225,200))
        screen.blit(england_flag,(450,200))
        screen.blit(music_text,(200,350))
        screen.blit(music_image,(150,350))
        screen.blit(music_two, (275,350))
        screen.blit(no_music, (400, 350))
        screen.blit(on_sound_img if sound_effect else no_sound_img,(525,350))

        france_rect = pygame.Rect(240,240,120,80)
        england_rect = pygame.Rect(465,240,120,80)
        music_one_rect = pygame.Rect(180,380,80,80)
        music_two_rect = pygame.Rect(310,380,80,80)
        no_music_rect = pygame.Rect(430,380,80,80)
        no_sound_rect = pygame.Rect(560,380,80,80)
        screen.blit(back_arrow, (25,-10))
        back_rect = pygame.Rect(70,40, 120, 50)


        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x, mouse_y))

        pygame.display.update()

def leaderboard():
    running = True
    title_font = pygame.font.Font("Image/CFCrayons-Regular.ttf", 70)
    score_font = pygame.font.Font("Image/CFCrayons-Regular.ttf", 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pygame.mixer.Sound.play(selected_sound)
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(selected_sound)
                        running = False
                    
        try:
            with open('score.json', 'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
            
        screen.blit(background_image, (0, 0))
        
        if LANGUAGE == "en":
            title = title_font.render("Leaderboard", True, BLACK)
            screen.blit(title, (235,25))
        elif LANGUAGE == "fr":
            title = title_font.render("Tableau des Scores", True, BLACK)
            screen.blit(title, (225,25))
        
        for i, score in enumerate(scores[:10]):
            y_pos = 150 + i * 45
            
            rank = score_font.render(f"-{i+1}", True, BLACK)
            screen.blit(rank, (50, y_pos))
            
            name = score_font.render(score['name'], True, BLACK)
            screen.blit(name, (150, y_pos))
            
            score_text = score_font.render(str(score['score']), True, BLACK)
            screen.blit(score_text, (700, y_pos))
            screen.blit(back_arrow, (50,0))
            back_rect = pygame.Rect(70,40, 120, 50)
            pygame.draw.rect(screen,GREEN, back_rect,3)
                  
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x, mouse_y))

        pygame.display.update()

def achivement(game):
    running = True
    title_font = pygame.font.Font("Image/CFCrayons-Regular.ttf", 70)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False
        
        screen.blit(background_image, (0, 0))
        screen.blit(back_arrow, (20, -10))
        screen.blit(achivement_case, (220,200))
        screen.blit(achivement_case, (220,325))
        screen.blit(achivement_case, (220,450))
        screen.blit(achivement_box, (150,125))
        screen.blit(achivement_box, (150,250))
        screen.blit(achivement_box, (150,375))
        back_rect = pygame.Rect(40,30, 120, 50)
            
        if game.achievements["fruit_master"]:
            screen.blit(achivement_win, (220,200))
        if game.achievements["bomb_dodger"]:
            screen.blit(achivement_win, (220,325))
        if game.achievements["ice_breaker"]:
            screen.blit(achivement_win, (220,450))

        if LANGUAGE == "en":
            title_text = title_font.render("Achievements", True , BLACK)
            screen.blit(title_text,(225,25))
            first_title_text = font_s.render("Fruit Master", True , BLACK)
            first_text = font_xs.render("Cut 100 fruits without missing a single one",True, BLACK)
            screen.blit(first_title_text,(350,180))
            screen.blit(first_text,(300,220))
            second_title_text = font_s.render("Bomb Dodger", True, BLACK)
            second_text = font_xs.render("Survive 10 bombs without detonating a single one",True, BLACK)
            screen.blit(second_title_text,(350,305))
            screen.blit(second_text,(300,345))
            three_title_text = font_s.render("Ice Breaker", True, BLACK)
            three_text = font_xs.render("Cut 5 ice cubes in a single game.",True, BLACK)
            screen.blit(three_title_text,(355,430))
            screen.blit(three_text,(300,470))

        elif LANGUAGE == "fr":
            title_text = title_font.render("Exploits",True,BLACK) 
            screen.blit(title_text,(300,25))
            first_title_text = font_s.render("Maitre des Fruits", True , BLACK)
            first_text = font_xs.render("Coupez 100 fruits sans manquer un seul fruit",True, BLACK)
            screen.blit(first_title_text,(350,180))
            screen.blit(first_text,(300,220))
            second_title_text = font_s.render("Esquiveur de Bombes", True, BLACK)
            second_text = font_xs.render("Survivez a 10 bombes sans en faire exploser une seule",True, BLACK)
            screen.blit(second_title_text,(325,305))
            screen.blit(second_text,(300,345))
            three_title_text = font_s.render("Brise-glace", True, BLACK)
            three_text = font_xs.render("Coupez 5 glacons en une seule partie",True, BLACK)
            screen.blit(three_title_text,(355,430))
            screen.blit(three_text,(300,470))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x, mouse_y))
        


        pygame.display.update()

def main_menu(game):
    selected = 0
    running = True
    apple_y = 193
    apple_direction = 1
    banana_y = 313
    banana_direction = 1
    orange_y = 400
    orange_direction = 1

    pygame.mixer.music.play()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_click.collidepoint(mouse_pos):
                        pygame.mixer_music.stop()
                        pygame.mixer.Sound.play(selected_sound)
                        pygame.mixer.Sound.play(start_sound)
                        return "play"
                    elif settings_click.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(selected_sound)
                        settings_menu()
                    elif score_click.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(selected_sound)
                        leaderboard()
                    elif achivement_click.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(selected_sound)
                        return "achivement"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 4
                    pygame.mixer.Sound.play(next_sound)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % 4
                    pygame.mixer.Sound.play(next_sound)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        pygame.mixer_music.stop()
                        pygame.mixer.Sound.play(selected_sound)
                        pygame.mixer.Sound.play(start_sound)
                        return "play"
                    elif selected == 1:
                        pygame.mixer.Sound.play(selected_sound)
                        settings_menu()
                    elif selected == 2:
                        pygame.mixer.Sound.play(selected_sound)
                        leaderboard()
                    elif selected == 3:
                        pygame.mixer.Sound.play(selected_sound)
                        achivement(game)

            mouse_pos = pygame.mouse.get_pos()
            if play_click.collidepoint(mouse_pos):
                if selected != 0:
                    pygame.mixer.Sound.play(next_sound)
                selected = 0
            elif settings_click.collidepoint(mouse_pos):
                if selected != 1:
                    pygame.mixer.Sound.play(next_sound)
                selected = 1
            elif score_click.collidepoint(mouse_pos):
                if selected != 2:
                    pygame.mixer.Sound.play(next_sound)
                selected = 2
            elif achivement_click.collidepoint(mouse_pos):
                if selected != 3:
                    pygame.mixer.Sound.play(next_sound)
                selected = 3

        mouse_x, mouse_y = pygame.mouse.get_pos()

        apple_y += apple_direction
        if apple_y > 200 or apple_y < 180:
            apple_direction *= -1

        banana_y += banana_direction
        if banana_y > 320 or banana_y < 290:
            banana_direction *= -1

        orange_y += orange_direction
        if orange_y > 420 or orange_y < 390:
            orange_direction *= -1

        screen.blit(background_image, (0, 0))
        screen.blit(score_button, (275,330))
        screen.blit(achivement_icon, (680,0))
        screen.blit(sun_image, (-150, -150))
        screen.blit(logo, (250, -50))
        screen.blit(tree, (-80, 300))
        screen.blit(red_sp, (600, 300))
        screen.blit(apple_cut, (600, 525))
        screen.blit(yellow_sp, (400, 500))

        achievements_unlocks = game.count_unlocked_achievements()

        if achievements_unlocks == 1:
            kunai_display = kunai_two
        elif achievements_unlocks == 2:
            kunai_display = kunai_three
        elif achievements_unlocks >= 3:
            kunai_display = kunai_four
        else:
            kunai_display = kunai_image


        if LANGUAGE == "fr":
            if selected == 0:
                screen.blit(kunai_display, (180, 170))
                screen.blit(FRUIT_IMAGE[0], (525, apple_y))
                screen.blit(play_button_fr, (275, 130))
                screen.blit(settings_button_fr, (275, 230))
                screen.blit(score_button, (275, 330))
            elif selected == 1:
                screen.blit(kunai_display, (180, 260))
                screen.blit(FRUIT_IMAGE[1], (525, banana_y))
                screen.blit(play_button_fr, (275, 130))
                screen.blit(settings_button_fr, (275, 230))
                screen.blit(score_button, (275, 330))
            elif selected == 2:
                screen.blit(kunai_display, (180, 360))
                screen.blit(FRUIT_IMAGE[3], (525, orange_y))
                screen.blit(play_button_fr, (275, 130))
                screen.blit(settings_button_fr, (275, 230))
                screen.blit(score_button, (275, 330))
            elif selected == 3:
                screen.blit(kunai_display,(560, -35))
                screen.blit(play_button_fr, (275, 130))
                screen.blit(settings_button_fr, (275, 230))
                screen.blit(score_button, (275, 330))

        else:  
            if selected == 0:
                screen.blit(kunai_display, (180, 170))
                screen.blit(FRUIT_IMAGE[0], (525, apple_y))
                screen.blit(play_select, (275, 130))
                screen.blit(settings_button, (275, 230))
                screen.blit(score_button, (275, 330))
            elif selected == 1:
                screen.blit(kunai_display, (180, 260))
                screen.blit(FRUIT_IMAGE[1], (525, banana_y))
                screen.blit(play_button, (275, 130))
                screen.blit(settings_select, (275, 230))
                screen.blit(score_button, (275, 330))
            elif selected == 2:
                screen.blit(kunai_display, (180, 360))
                screen.blit(FRUIT_IMAGE[3], (525, orange_y))
                screen.blit(play_button, (275, 130))
                screen.blit(settings_button, (275, 230))
                screen.blit(score_select, (275, 330))
            elif selected == 3:
                screen.blit(kunai_display,(560, -35))
                screen.blit(play_button, (275, 130))
                screen.blit(settings_button, (275, 230))
                screen.blit(score_button, (275, 330))

            
        screen.blit(cursor_img, (mouse_x, mouse_y))

        pygame.display.update()
        pygame.time.delay(15)

    return None

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        menu_result = main_menu(game)
        
        if menu_result == "play":
            game = Game()
            return_to_menu = False
            
            while game.running and not return_to_menu: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game.running = False
                        elif event.key == pygame.K_SPACE:
                            game.paused = not game.paused 
                            print("Jeu en pause" if game.paused else "Reprise du jeu")
                        else:
                            game.handle_key_press(event.key)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: 
                            mouse_pos = pygame.mouse.get_pos()
                            if game.pause_rect.collidepoint(mouse_pos):
                                game.paused = not game.paused
                                print("Jeu en pause" if game.paused else "Reprise du jeu")

                if game.paused:
                    while game.paused:
                        screen.blit(background_image, (0, 0))
                        game.draw_pause_menu(screen)
                        pygame.display.flip()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    mouse_pos = pygame.mouse.get_pos()
                                    if game.resume_rect.collidepoint(mouse_pos):
                                        game.paused = False
                                        print("Reprise du jeu")
                                    elif game.quit_rect.collidepoint(mouse_pos):
                                        return_to_menu = True 
                                        game.paused = False
                                    elif game.replay_rect.collidepoint(mouse_pos):
                                        game = Game() 
                                        game.paused = False
                else:
                    game.update()

                game.draw(screen)
                pygame.display.flip()
                clock.tick(60)
        elif menu_result == "achivement":
            achivement(game)
        elif menu_result is None:
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()