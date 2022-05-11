import random
import arcade

# CONSTANTS
SCREEN_WIDTH = 430
SCREEN_HEIGHT = 430
SCREEN_TITLE = '2048'
ROW_COUNT = 4
COLUMN_COUNT = 4
BORDER_COLOR = (187, 173, 160)
CELL_BACKGROUND = (205, 193, 180)

TILE_WIDTH = SCREEN_WIDTH // COLUMN_COUNT
TILE_HEIGHT = SCREEN_HEIGHT // ROW_COUNT


class Tile(arcade.Sprite):
    def __init__(self, image, number):
        super().__init__(image, scale=1)
        self.number = number
        self.direction = None
        # self.physics_engine = arcade.PhysicsEngineSimple(self, window.tiles)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left <= 0:
            self.left = 0
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.top >= SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom <= 0:
            self.bottom = 0


class Game(arcade.Window):

    def __init__(self) -> None:

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.tiles = arcade.SpriteList(spatial_hash_cell_size=100, use_spatial_hash=True)
        self.tile_positions = [["*" for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
        self.score = 0
        self.game_state = True
        self.final_text = ''

    def setup(self):
        # creating initial tiles
        self.generate_random_tile(2)

    def on_draw(self):
        self.clear(CELL_BACKGROUND)
        self.tiles.draw()
        self.draw_grid()
        arcade.draw_text(f'SCORE {self.score}', 20, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16)
        if self.game_state == False:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                         (237, 194, 46, 170))
            arcade.draw_text(self.final_text, 90, SCREEN_HEIGHT // 2, arcade.color.WHITE, 40)
            if self.final_text == 'YOU WIN!':
                arcade.draw_text('PRESS ENTER TO PLAY MORE', 20, SCREEN_HEIGHT // 2 - 60, arcade.color.WHITE, 19)
                arcade.draw_text('PRESS N TO START A NEW GAME', 5, SCREEN_HEIGHT // 2 - 110, arcade.color.WHITE, 19)

    def draw_grid(self):
        for x in range(1, ROW_COUNT):
            # Horizontal lines
            st_x = 0
            st_y = x * 108
            end_x = SCREEN_WIDTH
            end_y = x * 108
            arcade.draw_line(start_x=st_x, start_y=st_y, end_x=end_x, end_y=end_y, color=BORDER_COLOR, line_width=11)
        for y in range(1, COLUMN_COUNT):
            # VERTICAL LINES
            st_x = y * 108
            st_y = 0
            end_x = y * 108
            end_y = SCREEN_HEIGHT
            arcade.draw_line(start_x=st_x, start_y=st_y, end_x=end_x, end_y=end_y, color=BORDER_COLOR, line_width=10)

    def generate_random_tile(self, cell_n):
        cells = cell_n
        while cells > 0:

            # CHECK IF THERE ARE ANY EMPTY SLOTS FIRST!!!
            empty_slots = False
            for row in self.tile_positions:
                if "*" in row:
                    empty_slots = True
            if empty_slots:
                tile = Tile(f'tiles/2tile.png', number=2)
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                if self.tile_positions[3 - y][x] == '*':
                    tile.center_x = (10 + 100) * x + 50
                    tile.center_y = (10 + 100) * y + 50
                    cells -= 1
                    self.tiles.append(tile)
                    self.tile_positions[3 - y][x] = [2, tile]
            else:

                break

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game_state:
            if symbol == arcade.key.LEFT:
                for tile in self.tiles:
                    tile.direction = 'LEFT'
                    self.check_cell_collision('LEFT')
            if symbol == arcade.key.RIGHT:
                for tile in self.tiles:
                    tile.direction = 'RIGHT'
                    self.check_cell_collision('RIGHT')
            if symbol == arcade.key.UP:
                for tile in self.tiles:
                    tile.direction = 'UP'
                    self.check_cell_collision('UP')
            if symbol == arcade.key.DOWN:
                for tile in self.tiles:
                    tile.direction = 'DOWN'
                    self.check_cell_collision('DOWN')
            self.generate_random_tile(1)
            victory, defeat = self.check_victories()
            if victory:
                self.game_state = False
                self.final_text = 'YOU WIN!'
            if defeat:
                self.game_state = False
                self.final_text = 'YOU LOSE!'
        else:
            if symbol == arcade.key.ENTER:
                self.game_state = True
            if symbol == arcade.key.N:
                self.reset_game()

    def reset_game(self):
        self.tiles.clear()
        self.tile_positions = [["*" for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
        self.score = 0
        self.game_state = True
        self.final_text = ''
        self.generate_random_tile(2)

    def update(self, delta_time: float):
        if self.game_state:
            self.tiles.update()

    def check_cell_collision(self, direction):

        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT - 1):
                # LEFT
                if direction == 'RIGHT':
                    try:
                        # check for collsiion with a cell with an identical number
                        if self.tile_positions[i][j][0] == self.tile_positions[i][j + 1][0]:
                            self.tiles.remove(self.tile_positions[i][j][1])
                            self.tile_positions[i][j] = '*'
                            number = self.tile_positions[i][j + 1][1].number * 2
                            self.tile_positions[i][j + 1][1].number = number
                            self.tile_positions[i][j + 1][0] = number
                            self.score += number
                            self.tile_positions[i][j + 1][1].texture = arcade.load_texture(
                                f'tiles/{number}tile.png')
                    except Exception:
                        pass
                    # collapsing the cells
                    if self.tile_positions[i][j] != "*" and self.tile_positions[i][j + 1] == '*':
                        self.tile_positions[i][j][1].center_x += 110
                        self.tile_positions[i][j + 1] = self.tile_positions[i][j]
                        self.tile_positions[i][j] = '*'
        for i in range(1, ROW_COUNT + 1):
            for j in range(1, COLUMN_COUNT):
                if direction == 'LEFT':
                    try:
                        if self.tile_positions[-i][-j][0] == self.tile_positions[-i][-j - 1][0]:
                            self.tiles.remove(self.tile_positions[-i][-j][1])
                            self.tile_positions[-i][-j] = '*'
                            number = self.tile_positions[-i][-j - 1][1].number * 2
                            self.tile_positions[-i][-j - 1][1].number = number
                            self.tile_positions[-i][-j - 1][0] = number
                            self.score += number
                            self.tile_positions[-i][-j - 1][1].texture = arcade.load_texture(f'tiles/{number}tile.png')
                    except Exception:
                        pass
                    # collapsing the cells
                    if self.tile_positions[-i][-j] != "*" and self.tile_positions[-i][-j - 1] == '*':
                        self.tile_positions[-i][-j][1].center_x -= 110
                        self.tile_positions[-i][-j - 1] = self.tile_positions[-i][-j]
                        self.tile_positions[-i][-j] = '*'

        for i in range(1, ROW_COUNT):
            for j in range(1, COLUMN_COUNT + 1):

                if direction == 'UP':
                    # try:
                    if self.tile_positions[-i][-j] != '*' and self.tile_positions[-i][-j][0] == \
                            self.tile_positions[-i - 1][-j][0]:
                        self.tiles.remove(self.tile_positions[-i][-j][1])
                        self.tile_positions[-i][-j] = '*'
                        number = self.tile_positions[-i - 1][-j][1].number * 2
                        self.tile_positions[-i - 1][-j][1].number = number
                        self.tile_positions[-i - 1][-j][0] = number
                        self.score += number
                        self.tile_positions[-i - 1][-j][1].texture = arcade.load_texture(f'tiles/{number}tile.png')
                    if self.tile_positions[-i][-j][0] != "*" and self.tile_positions[-i - 1][-j] == '*':
                        self.tile_positions[-i][-j][1].center_y += 110
                        self.tile_positions[-i - 1][-j] = self.tile_positions[-i][-j]
                        self.tile_positions[-i][-j] = '*'

        for i in range(ROW_COUNT - 1):
            for j in range(COLUMN_COUNT):
                if direction == 'DOWN':
                    for row in self.tile_positions:
                        if self.tile_positions[i][j] != "*" and self.tile_positions[i][j][0] == \
                                self.tile_positions[i + 1][j][0]:
                            self.tiles.remove(self.tile_positions[i][j][1])
                            self.tile_positions[i][j] = '*'
                            number = self.tile_positions[i + 1][j][1].number * 2
                            self.tile_positions[i + 1][j][1].number = number
                            self.tile_positions[i + 1][j][0] = number
                            self.score += number
                            self.tile_positions[i + 1][j][
                                1].texture = arcade.load_texture(
                                f'tiles/{number}tile.png')
                    # collapsing the cells
                    if self.tile_positions[i][j][0] != "*" and self.tile_positions[i + 1][j] == '*':
                        self.tile_positions[i][j][1].center_y -= 110
                        self.tile_positions[i + 1][j] = self.tile_positions[i][j]
                        self.tile_positions[i][j] = '*'

    def check_victories(self):
        victory = False
        for row in self.tile_positions:
            for cell in row:
                if cell != '*' and 2048 in cell:
                    victory = True
                    break

        # check defeat: if any mergeable cells left, the game isn't over yet
        defeat = True

        for row in self.tile_positions:
            for cell in row:
                if cell == '*':
                    defeat = False
                    break
        # horizontal check
        for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT - 1):
                if self.tile_positions[x][y][0] == self.tile_positions[x][y + 1][0]:
                    defeat = False
                    break
        # vertical check
        for x in range(ROW_COUNT - 1):
            for y in range(COLUMN_COUNT):
                if self.tile_positions[x][y][0] == self.tile_positions[x + 1][y][0]:
                    defeat = False
                    break

        return victory, defeat


window = Game()
window.setup()

arcade.run()
