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
    def __init__(self, main_menu):
        pygame.init()
        self.width, self.height = main_menu.width, main_menu.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Settings")

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.background_image = pygame.image.load("assets/background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.main_menu = main_menu
        self.setup_ui()

        self.running = True

    def setup_ui(self):
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height - 70), (200, 50)),
            text='Back',
            manager=self.manager,
            object_id='#main_menu_button'
        )

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.back_button:
                            self.running = False
                            self.main_menu.run()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.blit(self.background_image, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    settings_menu = SettingsMenu(None)
    settings_menu.run()
