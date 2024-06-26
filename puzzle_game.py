import pygame
import pygame_gui
import random
import xml.etree.ElementTree as ET
from stats import Statistics

class PuzzleGame:
    def __init__(self, config_filename, player_name):
        self.config = self.load_xml_config(config_filename)
        self.width, self.height = self.config.get("window_width", 800), self.config.get("window_height", 600)
        self.rows, self.cols = self.config.get("rows", 4), self.config.get("cols", 4)
        self.tile_size = self.config.get("tile_size", 100)
        self.grid_margin = self.config.get("grid_margin", 5)
        self.grid_thickness = self.config.get("grid_thickness", 5)
        self.font_size = self.config.get("font_size", 48)

        self.player_name = player_name

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Colorful Puzzle Game")

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.stats = Statistics()

        self.tiles = list(range(1, self.rows * self.cols)) + [0]  # Last tile is the empty space
        random.shuffle(self.tiles)
        self.empty_tile = self.tiles.index(0)

        self.font = pygame.font.Font(None, self.font_size)
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

    def draw_tiles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                tile = self.tiles[i * self.cols + j]
                if tile != 0:
                    x = j * (self.tile_size + self.grid_margin) + self.grid_margin
                    y = i * (self.tile_size + self.grid_margin) + self.grid_margin
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.tile_size, self.tile_size))
                    text = self.font.render(str(tile), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                    self.screen.blit(text, text_rect)

    def move_tile(self, direction):
        row, col = divmod(self.empty_tile, self.cols)
        if direction == "down" and row > 0:
            swap_index = self.empty_tile - self.cols
        elif direction == "up" and row < self.rows - 1:
            swap_index = self.empty_tile + self.cols
        elif direction == "right" and col > 0:
            swap_index = self.empty_tile - 1
        elif direction == "left" and col < self.cols - 1:
            swap_index = self.empty_tile + 1
        else:
            return
        self.tiles[self.empty_tile], self.tiles[swap_index] = self.tiles[swap_index], self.tiles[self.empty_tile]
        self.empty_tile = swap_index

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_tile("up")
                    elif event.key == pygame.K_DOWN:
                        self.move_tile("down")
                    elif event.key == pygame.K_LEFT:
                        self.move_tile("left")
                    elif event.key == pygame.K_RIGHT:
                        self.move_tile("right")
            self.screen.fill((0, 0, 0))
            self.draw_tiles()
            pygame.display.update()
        self.stats.update_player_stats(self.player_name, moves=100, time=60.5)  # Обновите с реальными значениями


if __name__ == "__main__":
    game = PuzzleGame("config.xml", "Player1")
    game.run()
