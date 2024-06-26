import pygame
import pygame_gui
import os
import pickle
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
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button:
                            self.start_game()
                        elif event.ui_element == self.settings_button:
                            self.show_settings()
                        elif event.ui_element == self.stats_button:
                            self.show_stats()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

    def start_game(self):
        game = PuzzleGame("config.xml")
        game.run()

    def show_settings(self):
        self.running = False
        settings_menu = SettingsMenu(self)
        settings_menu.run()

    def show_stats(self):
        self.stats.load_stats()
        print(f"Games Played: {self.stats.games_played}")
        print(f"Total Moves: {self.stats.total_moves}")
        print(f"Best Time: {self.stats.best_time}")

if __name__ == "__main__":
    menu = MainMenu("config.xml")
    menu.run()
