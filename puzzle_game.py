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
        self.background_color = self.config.get("background_color", (0, 0, 0))
        self.tile_color = self.config.get("tile_color", (255, 255, 255))
        self.text_color = self.config.get("text_color", (0, 0, 0))

        self.player_name = player_name

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Colorful Puzzle Game")

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.stats = Statistics()

        # Load tile textures or images (example textures)
        self.tile_images = []
        for i in range(1, self.rows * self.cols):
            image = pygame.Surface((self.tile_size, self.tile_size))
            image.fill((random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))  # Random color
            pygame.draw.rect(image, (0, 0, 0), (0, 0, self.tile_size, self.tile_size), 5)  # Border
            self.tile_images.append(image)

        self.tiles = list(range(1, self.rows * self.cols)) + [0]  # Last tile is the empty space
        random.shuffle(self.tiles)
        self.empty_tile = self.tiles.index(0)

        self.font = pygame.font.Font("assets/fonts/Ubuntu-Regular.ttf", self.font_size)
        self.running = True

        pygame.mixer.init()
        self.tile_move_sound = pygame.mixer.Sound('assets/music/Carton_move_2.wav')

        pygame.mixer.music.load('assets/music/Pixel Dreams.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Background effects: falling stars
        self.stars = [{'x': random.randint(0, self.width), 'y': random.randint(0, self.height), 'speed': random.uniform(0.5, 2.5)} for _ in range(100)]

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
        total_width = self.cols * (self.tile_size + self.grid_margin) - self.grid_margin
        total_height = self.rows * (self.tile_size + self.grid_margin) - self.grid_margin
        start_x = (self.width - total_width) // 2
        start_y = (self.height - total_height) // 2

        for i in range(self.rows):
            for j in range(self.cols):
                tile = self.tiles[i * self.cols + j]
                if tile != 0:
                    x = start_x + j * (self.tile_size + self.grid_margin)
                    y = start_y + i * (self.tile_size + self.grid_margin)
                    # Example: Draw textured tiles
                    self.screen.blit(self.tile_images[tile - 1], (x, y))
                    text = self.font.render(str(tile), True, self.text_color)
                    text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                    self.screen.blit(text, text_rect)

    def move_tile(self, direction):
        row, col = divmod(self.empty_tile, self.cols)
        if direction == "down" and row > 0:
            swap_index = self.empty_tile - self.cols
            self.tile_move_sound.play()
        elif direction == "up" and row < self.rows - 1:
            swap_index = self.empty_tile + self.cols
            self.tile_move_sound.play()
        elif direction == "right" and col > 0:
            swap_index = self.empty_tile - 1
            self.tile_move_sound.play()
        elif direction == "left" and col < self.cols - 1:
            swap_index = self.empty_tile + 1
            self.tile_move_sound.play()
        else:
            return
        self.tiles[self.empty_tile], self.tiles[swap_index] = self.tiles[swap_index], self.tiles[self.empty_tile]
        self.empty_tile = swap_index

    def update_stars(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > self.height:
                star['x'] = random.randint(0, self.width)
                star['y'] = 0

    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(star['x']), int(star['y'])), 2)

    def draw_gradient_background(self):
        color_top = (0, 0, 0)
        color_bottom = (25, 25, 112)
        for y in range(self.height):
            color = (
                int(color_top[0] + (color_bottom[0] - color_top[0]) * y / self.height),
                int(color_top[1] + (color_bottom[1] - color_top[1]) * y / self.height),
                int(color_top[2] + (color_bottom[2] - color_top[2]) * y / self.height),
            )
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

    def run(self):
        frame_idx = 0
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

            self.update_stars()
            self.draw_gradient_background()
            self.draw_stars()
            self.draw_tiles()
            pygame.display.update()

        pygame.mixer.music.stop()
        self.stats.update_player_stats(self.player_name, moves=100, time=60.5)

if __name__ == "__main__":
    game = PuzzleGame("config.xml", "Player1")
    game.run()
