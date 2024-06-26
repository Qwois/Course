import pygame
import pygame_gui
import xml.etree.ElementTree as ET
from puzzle_game import PuzzleGame
from settings import SettingsMenu
from stats import Statistics

class MainMenu:
    def __init__(self, config_filename):
        self.config = self.load_xml_config(config_filename)

        self.width, self.height = self.config.get("window_width", 800), self.config.get("window_height", 600)

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Colorful Puzzle Game")

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.stats = Statistics()
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
            manager=self.manager
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2), (200, 50)),
            text='Settings',
            manager=self.manager
        )
        self.stats_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 + 75), (200, 50)),
            text='Statistics',
            manager=self.manager
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
            self.screen.fill((0, 0, 0))
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
        settings_menu = SettingsMenu(self)
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

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.main_menu = main_menu
        self.setup_ui()

        self.running = True

    def setup_ui(self):
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 - 50), (200, 50)),
            manager=self.manager
        )
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2), (200, 50)),
            text='Start Game',
            manager=self.manager
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height // 2 + 50), (200, 50)),
            text='Back',
            manager=self.manager
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
                        if event.ui_element == self.start_button:
                            player_name = self.name_input.get_text()
                            self.running = False
                            self.main_menu.start_game(player_name)
                        elif event.ui_element == self.back_button:
                            self.running = False
                            self.main_menu.run()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

class StatsWindow:
    def __init__(self, main_menu):
        pygame.init()
        self.width, self.height = main_menu.width, main_menu.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Statistics")

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.main_menu = main_menu
        self.setup_ui()

        self.running = True

    def setup_ui(self):
        stats_text = self.get_stats_text()
        self.stats_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((50, 50), (self.width - 100, self.height - 150)),
            html_text=stats_text,
            manager=self.manager
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 100, self.height - 70), (200, 50)),
            text='Back',
            manager=self.manager
        )

    def get_stats_text(self):
        stats = self.main_menu.stats
        stats.load_stats()
        text = "<b>Statistics</b><br>"
        for player, player_stats in stats.player_stats.items():
            text += f"<b>{player}</b><br>"
            text += f"Games Played: {player_stats['games_played']}<br>"
            text += f"Total Moves: {player_stats['total_moves']}<br>"
            text += f"Best Time: {player_stats['best_time']}<br><br>"
        return text

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
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    menu = MainMenu("config.xml")
    menu.run()
