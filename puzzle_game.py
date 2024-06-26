import pygame
import random
import xml.etree.ElementTree as ET
from settings import Settings

class PuzzleGame:
    def __init__(self, config_filename):
        self.config = self.load_xml_config(config_filename)
        self.settings = Settings()

        self.width, self.height = self.config.get("window_width", 800), self.config.get("window_height", 600)
        self.rows, self.cols = self.config.get("rows", 3), self.config.get("cols", 3)
        self.tile_size = self.config.get("tile_size", 100)
        self.grid_width = self.cols * self.tile_size
        self.grid_height = self.rows * self.tile_size
        self.grid_x = (self.width - self.grid_width) // 2
        self.grid_y = (self.height - self.grid_height) // 2

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Colorful Puzzle Game")

        self.background_color = self.config.get("background_color", (0, 0, 0))
        self.tile_color = self.config.get("tile_color", (50, 50, 50))
        self.text_color = self.config.get("text_color", (255, 255, 255))
        self.font_size = self.config.get("font_size", 36)

        self.running = True
        self.moves = 0

        self.new_puzzle()

        self.animating = False
        self.animation_speed = 8
        self.target_row = 0
        self.target_col = 0

        self.won = False

        if self.settings.get_music_enabled():
            pygame.mixer.music.load('assets/music/Pixel Dreams.mp3')
            pygame.mixer.music.play(-1)

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

    def new_puzzle(self):
        self.grid = [[(i * self.cols + j) % (self.rows * self.cols) for j in range(self.cols)] for i in range(self.rows)]
        random.shuffle(sum(self.grid, []))
        self.empty_tile = self.rows * self.cols - 1

    def draw(self):
        self.screen.fill(self.background_color)
        font = pygame.font.Font(None, self.font_size)
        for row in range(self.rows):
            for col in range(self.cols):
                tile_value = self.grid[row][col]
                if tile_value != self.empty_tile:
                    tile_x = self.grid_x + col * self.tile_size
                    tile_y = self.grid_y + row * self.tile_size
                    pygame.draw.rect(self.screen, self.tile_color, (tile_x, tile_y, self.tile_size, self.tile_size))
                    text = font.render(str(tile_value + 1), True, self.text_color)
                    text_rect = text.get_rect(center=(tile_x + self.tile_size // 2, tile_y + self.tile_size // 2))
                    self.screen.blit(text, text_rect)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and not self.animating:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.moves += 1
                    self.handle_move(event.key)

    def handle_move(self, key):
        row, col = divmod(self.empty_tile, self.cols)
        if key == pygame.K_UP and row < self.rows - 1:
            self.target_row, self.target_col = row + 1, col
        elif key == pygame.K_DOWN and row > 0:
            self.target_row, self.target_col = row - 1, col
        elif key == pygame.K_LEFT and col < self.cols - 1:
            self.target_row, self.target_col = row, col + 1
        elif key == pygame.K_RIGHT and col > 0:
            self.target_row, self.target_col = row, col - 1
        else:
            return
        self.start_animation()

    def start_animation(self):
        self.animating = True
        self.animation_progress = 0

    def update_animation(self):
        if self.animating:
            self.animation_progress += self.animation_speed
            if self.animation_progress >= self.tile_size:
                self.animating = False
                self.swap_tiles()
                self.check_win()

    def swap_tiles(self):
        row, col = divmod(self.empty_tile, self.cols)
        self.grid[row][col], self.grid[self.target_row][self.target_col] = self.grid[self.target_row][self.target_col], self.grid[row][col]
        self.empty_tile = self.target_row * self.cols + self.target_col

    def check_win(self):
        if all(self.grid[row][col] == row * self.cols + col for row in range(self.rows) for col in range(self.cols)):
            self.won = True
            print("You win!")
            self.update_stats()

    def update_stats(self):
        from stats import Statistics
        stats = Statistics()
        stats.update(self.moves)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update_animation()
            self.draw()
            clock.tick(60)
