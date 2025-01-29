import pygame

class MenuItem:
    def __init__(self, text, action=None, submenu=None):
        self.text = text
        self.action = action
        self.submenu = submenu
        self.rect = None

class DropdownMenu:
    def __init__(self, translations):
        self.translations = translations
        self.current_language = 'English'
        
        # Colors
        self.color_normal = pygame.Color('lightskyblue3')
        self.color_hover = pygame.Color('dodgerblue2')
        self.color_text = pygame.Color('white')
        self.font = pygame.font.Font(None, 36)
        
        # Menu dimensions
        self.width = 200
        self.item_height = 40
        
        # Menu structure
        self.main_menu = [
            MenuItem('New game'),
            MenuItem('Options'),
            MenuItem('Exit')
        ]
        
        self.options_menu = [
            MenuItem('Select language'),
            MenuItem('Set mode'),
            MenuItem('Show leaderboard')
        ]
        
        self.language_menu = [
            MenuItem('English'),
            MenuItem('French'),
            MenuItem('Russian'),
            MenuItem('Chinese')
        ]
        
        self.mode_menu = [
            MenuItem('Classic game'),
            MenuItem('Zen mode'),
            MenuItem('Fruit Attack')
        ]
        
        self.current_menu = self.main_menu
        self.is_open = True  
        self.screen_width = 800  
        self.screen_height = 600  

    def translate_text(self, text):
        if text in self.translations.get(self.current_language, {}):
            return self.translations[self.current_language][text]
        return text

    def draw(self, screen):
        if not self.is_open:
            text = self.font.render("Press Enter to get to menu", True, self.color_text)
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
            screen.blit(text, text_rect)
            return

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
    
        menu_height = len(self.current_menu) * self.item_height
        start_x = (self.screen_width - self.width) // 2
        start_y = (self.screen_height - menu_height) // 2

        mouse_pos = pygame.mouse.get_pos()

        for i, item in enumerate(self.current_menu):
            item_rect = pygame.Rect(start_x, start_y + i * self.item_height,
                                  self.width, self.item_height)
            item.rect = item_rect
            
            color = self.color_hover if item_rect.collidepoint(mouse_pos) else self.color_normal
            pygame.draw.rect(screen, color, item_rect)
            
            text = self.font.render(self.translate_text(item.text), True, self.color_text)
            text_rect = text.get_rect(center=item_rect.center)
            screen.blit(text, text_rect)

        
        if self.current_menu != self.main_menu:
            text = self.font.render("Press backspace to return", True, self.color_text)
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
            screen.blit(text, text_rect)

    def handle_event(self, event):
        if not self.is_open:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.is_open = True
                self.current_menu = self.main_menu
                return None, None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_open = False
                return None, None
            
            if event.key == pygame.K_BACKSPACE and self.current_menu != self.main_menu:
                if self.current_menu in [self.language_menu, self.mode_menu]:
                    self.current_menu = self.options_menu
                elif self.current_menu == self.options_menu:
                    self.current_menu = self.main_menu
                return None, None

        if event.type == pygame.MOUSEBUTTONDOWN and self.is_open:
            print("Mouse click detected")
            for item in self.current_menu:
                print(f"Checking item: {item.text}")
                if item.rect and item.rect.collidepoint(event.pos):
                    print(f"Clicked on: {item.text}")
                    if item.text == 'Options':
                        self.current_menu = self.options_menu
                        return None, None
                    elif item.text == 'Select language':
                        self.current_menu = self.language_menu
                        return None, None
                    elif item.text == 'Set mode':
                        self.current_menu = self.mode_menu
                        return None, None
                    elif item.text == 'New game':
                        self.is_open = False
                        self.current_menu = self.main_menu
                        return item.text, 'new_game'
                    elif item.text in ['English', 'French', 'Russian', 'Chinese']:
                        self.current_menu = self.options_menu
                        return item.text, 'language'
                    elif item.text in ['Classic game', 'Zen mode', 'Fruit Attack']:
                        self.current_menu = self.options_menu
                        return item.text, 'action'
                    elif item.text == 'Show leaderboard':
                        return item.text, 'action'
                    elif item.text == 'Exit':
                        return item.text, 'action'

        return None, None