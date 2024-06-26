import os
import pickle
import pygame
import pygame_gui

class Settings:
    def __init__(self):
        self.settings_file = "settings.dat"
        self.music_enabled = True
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "rb") as f:
                    settings = pickle.load(f)
                    self.music_enabled = settings.get("music_enabled", True)
            except (EOFError, pickle.UnpicklingError):
                self.save_settings()
        else:
            self.save_settings()

    def save_settings(self):
        with open(self.settings_file, "wb") as f:
            settings = {
                "music_enabled": self.music_enabled,
            }
            pickle.dump(settings, f)

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        self.save_settings()

    def get_music_enabled(self):
        return self.music_enabled

class SettingsMenu:
    def __init__(self, width, height, settings, main_menu):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Settings")

        self.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')
        self.settings = settings
        self.main_menu = main_menu

        self.setup_ui()
        self.running = True

    def setup_ui(self):
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2), (200, 50)),
            text='Back',
            manager=self.manager,
            object_id='#main_menu_button'  
        )

        self.music_toggle_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 - 100), (200, 50)),
            text='Toggle Music: On' if self.settings.get_music_enabled() else 'Toggle Music: Off',
            manager=self.manager
        )

        self.background_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 + 100), (200, 50)),
            text='Change Background',
            manager=self.manager
        )

    def show_main_menu(self):
        self.running = False
        self.main_menu.run()

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.show_main_menu()
                elif event.ui_element == self.music_toggle_button:
                    self.settings.toggle_music()
                    self.music_toggle_button.set_text('Toggle Music: On' if self.settings.get_music_enabled() else 'Toggle Music: Off')
                elif event.ui_element == self.background_button:
                    # Implement logic to change background
                    pass
        self.manager.process_events(event)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_events(event)
            self.manager.update(time_delta)
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()
