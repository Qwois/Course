import pygame
import pygame_gui
import xml.etree.ElementTree as ET
from puzzle_game import PuzzleGame
from settings import SettingsMenu, Settings
from stats import Statistics
from pygame_gui.elements import UITextEntryLine, UIButton

class MainMenu:
    def __init__(self, config_filename):
        self.config = self.load_xml_config(config_filename)

        self.width, self.height = self.config.get("window_width", 800), self.config.get("window_height", 600)

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Colorful Puzzle Game")

        self.settings = Settings()  # Создаем экземпляр настроек
        self.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')
        self.stats = Statistics()
        self.background_image = pygame.image.load("assets/background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.setup_ui()

        self.running = True
        self.player_name = None

    def load_xml_config(self, filename):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            config = {}
            for child in root:
                if child.tag in ["window_width", "window_height", "rows", "cols", "tile_size", "grid_margin", "grid_thickness", "font_size"]:
                    config[child.tag] = int(child.text)
                elif child.tag in ["background_color", "tile_color", "text_color"]:
                    config[child.tag] = tuple(map(int, child.text.split(",")))
            return config
        except Exception as e:
            print(f"Error loading XML configuration from {filename}: {e}")
            raise

    def setup_ui(self):
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 - 75), (200, 50)),
            text='Play',
            manager=self.manager,
            object_id='#main_menu_button'
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2), (200, 50)),
            text='Settings',
            manager=self.manager,
            object_id='#main_menu_button'
        )
        self.stats_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 + 75), (200, 50)),
            text='Statistics',
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
                        if event.ui_element == self.play_button:
                            self.show_name_input()
                        elif event.ui_element == self.settings_button:
                            self.show_settings()
                        elif event.ui_element == self.stats_button:
                            self.show_stats()
                                
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.blit(self.background_image, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

    def show_name_input(self):
        self.running = False
        name_input = NameInputMenu(self)
        name_input.run()

    def start_game(self, player_name):
        game = PuzzleGame("config.xml", player_name)
        game.run()

    def show_settings(self):
        self.running = False
        settings_menu = SettingsMenu(self.width, self.height, self.settings)
        settings_menu.run()

    def show_stats(self):
        self.stats.load_stats()
        stats_window = StatsWindow(self)
        stats_window.run()

class NameInputMenu:
    def __init__(self, main_menu):
        pygame.init()
        self.width, self.height = main_menu.width, main_menu.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Enter Your Name")

        self.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')
        self.main_menu = main_menu
        self.setup_ui()

        self.running = True

    def setup_ui(self):
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 - 50), (200, 50)),
            manager=self.manager,
            object_id='#main_menu_button'    
        )
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2), (200, 50)),
            text='Start Game',
            manager=self.manager,
            object_id='#main_menu_button'           
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 + 50), (200, 50)),
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
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.start_button:
                            self.main_menu.start_game(self.name_input.get_text())
                        elif event.ui_element == self.back_button:
                            self.running = False
                            self.main_menu.running = True
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.fill((255, 1, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

class StatsWindow:
    def __init__(self, main_menu):
        pygame.init()
        self.width, self.height = main_menu.width, main_menu.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Statistics")

        self.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')
        self.main_menu = main_menu
        self.setup_ui()

        self.running = True

    def setup_ui(self):
        self.stats_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 - 50), (200, 50)),
            text="Statistics Placeholder",
            manager=self.manager
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2), (200, 50)),
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
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.back_button:
                            self.running = False
                            self.main_menu.running = True
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.fill((255, 1, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    menu = MainMenu("config.xml")
    menu.run()
