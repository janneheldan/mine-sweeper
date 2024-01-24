import pygame as pg
import random
import time
import csv

# Constants for game difficulty and board size
GAME_DIFFICULTY = {
    0: (9, 9, 10),
    1: (16, 16, 40),
    2: (30, 16, 99),
}

# Constants for colors
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
}

# Constants for sprites
DUCK = pg.image.load("./sprites/duck.png")
SLING = pg.image.load("./sprites/sling.png")
TILE_1 = pg.image.load("./sprites/tile_1.png")
TILE_2 = pg.image.load("./sprites/tile_2.png")
TILE_3 = pg.image.load("./sprites/tile_3.png")
TILE_4 = pg.image.load("./sprites/tile_4.png")
TILE_5 = pg.image.load("./sprites/tile_5.png")
TILE_6 = pg.image.load("./sprites/tile_6.png")
TILE_7 = pg.image.load("./sprites/tile_7.png")
TILE_8 = pg.image.load("./sprites/tile_8.png")
TILE_BACK = pg.image.load("./sprites/tile_back.png")
TILE_EMPTY = pg.image.load("./sprites/tile_empty.png")
TILE_FLAG = pg.image.load("./sprites/tile_flag.png")
TILE_MINE = pg.image.load("./sprites/tile_mine.png")

# Dictionary for tiles
TILES_DICT = {
    1: TILE_1,
    2: TILE_2,
    3: TILE_3,
    4: TILE_4,
    5: TILE_5,
    6: TILE_6,
    7: TILE_7,
    8: TILE_8,
    9: TILE_EMPTY,
    10: TILE_FLAG,
    11: TILE_BACK,
    0: TILE_MINE,
}

def setup():
    """
    Set ups pygame and return screen and clock
    """
    pg.init()
    screen = pg.display.set_mode((640, 640))
    pg.display.set_caption("Minesweeper")
    clock = pg.time.Clock()
    return screen, clock 


def load_highscores():
    """
    Loads highscores from score.csv 
    If file does not exist, creates it
    """
    highscores = []
    try:
        with open("score.csv", "r") as file:
            reader = csv.reader(file)
            highscores = list(reader)
        return highscores[-9:]
    except FileNotFoundError:
        with open("score.csv", "w") as file:
            pass
        return highscores
def save_highscores(win_or_loss, difficulty, score):
    """
    Saves highscores to score.csv 
    """
    current_time = time.strftime("%d/%m/%Y")
    diff = ["easy", "medium", "hard"]
    with open("score.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if win_or_loss:
            win_or_loss = "win"
        else:
            win_or_loss = "loss"
        writer.writerow([current_time, win_or_loss, diff[difficulty], score])

def start_screen(screen):
    """
    Start screen for the game
    """
    score = load_highscores()
    font = pg.font.Font("freesansbold.ttf", 22)
    padding = 10
    text = font.render("MINESWEEPER PERSONAL HIGHSCORES:", True, COLORS["BLACK"])
    screen.fill(COLORS["WHITE"])
    screen.blit(text, (padding, 15))
    text = font.render(f"Date, W/L, Difficulty, Score", True, COLORS["BLACK"])
    screen.blit(text, (padding, 50))
    pg.draw.line(screen, COLORS["BLACK"], (0, 90), (640, 90), 5)
    # line above the press 1, 2, 3 text
    pg.draw.line(screen, COLORS["BLACK"], (0, 550), (640, 550), 5)
    text = font.render("Choose difficulty:", True, COLORS["BLACK"])
    screen.blit(text, (padding, 560))
    text = font.render("Press 1 for easy, 2 for medium, 3 for hard", True, COLORS["BLACK"])
    screen.blit(text, (padding, 600))

    for i in range(len(score)):
        text = font.render(f"{score[i][0]}, {score[i][1]}, {score[i][2]}, {score[i][3]}", True, COLORS["BLACK"])
        screen.blit(text, (padding, 0 + i * 50 + 100))
        pass
    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None, None, False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    return 1, 0, True
                elif event.key == pg.K_2:
                    return 1, 1, True
                elif event.key == pg.K_3:
                    return 1, 2, True

def game_screen(screen, board, visited_tiles, difficulty):
    """
    Game screen for the game
    """
    number_of_clicks = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0, 0, False, number_of_clicks, False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if check_title(event.pos[0], event.pos[1], board) == 0:
                        number_of_clicks += 1
                        show_tile(event.pos[0], event.pos[1], board, screen, visited_tiles)
                        if check_win(visited_tiles, difficulty):
                            return 2, True, number_of_clicks, True
                    elif check_title(event.pos[0], event.pos[1], board) == 1:
                        number_of_clicks += 1
                        show_tile(event.pos[0], event.pos[1], board, screen, visited_tiles)
                        return 2, True, number_of_clicks, False
                elif event.button == 3:
                    flag_tile(event.pos[0], event.pos[1], screen)

def create_board(difficulty):
    """
    Creates board for the game
    """
    board = [[-1 for _ in range(GAME_DIFFICULTY[difficulty][0])] for _ in range(GAME_DIFFICULTY[difficulty][1])]
    for _ in range(GAME_DIFFICULTY[difficulty][2]):
        y = random.randint(0, GAME_DIFFICULTY[difficulty][1] - 1)
        x = random.randint(0, GAME_DIFFICULTY[difficulty][0] - 1)
        while board[y][x] == 0:
            y = random.randint(0, GAME_DIFFICULTY[difficulty][1] - 1)
            x = random.randint(0, GAME_DIFFICULTY[difficulty][0] - 1)
        board[y][x] = 0 

    for y in range(GAME_DIFFICULTY[difficulty][1]):
        for x in range(GAME_DIFFICULTY[difficulty][0]):
            if board[y][x] != 0:
                ans = count_mines(x, y, board)
                if ans == 0:
                    board[y][x] = 9
                else: 
                    board[y][x] = count_mines(x, y, board)
    return board


def count_mines(x, y, data):
    """
    Counts mines around a tile 
    """
    ans = 0
    count = -1

    for i in [-1, 0, 1]:
        while count < 2:
            try:
                if y - i >= 0 and x + count >= 0:
                    if data[y-i][x+count] == 0:
                        ans += 1
            except IndexError:
                pass
            count += 1
        count = -1
    return ans 

def draw_board(difficulty, screen):
    """
    Draws board for the game
    """
    pg.display.set_mode((GAME_DIFFICULTY[difficulty][0] * 40, GAME_DIFFICULTY[difficulty][1] * 40))
    for y in range(GAME_DIFFICULTY[difficulty][1]):
        for x in range(GAME_DIFFICULTY[difficulty][0]):
            screen.blit(TILES_DICT[11], (x * 40, y * 40))
    pg.display.update()

def game_end(difficulty, screen, board, win_or_loss, score):
    """
    Game end screen for the game
    """
    for y in range(GAME_DIFFICULTY[difficulty][1]):
        for x in range(GAME_DIFFICULTY[difficulty][0]):
            screen.blit(TILES_DICT[board[y][x]], (x * 40, y * 40))

    if win_or_loss:
        pg.display.set_caption("Press space to play again")
        text = pg.font.Font("freesansbold.ttf", 28).render(f"You won! - Your score: {score}", True, COLORS["BLACK"])
        r = text.get_rect()
        r.center = screen.get_rect().center
        pg.draw.rect(screen, COLORS["BLACK"], r)
        screen.blit(text, r)
    else:
        pg.display.set_caption("Press space to play again")
        text = pg.font.Font("freesansbold.ttf", 28).render(f"You lost! - Score: {score}", True, COLORS["WHITE"])
        r = text.get_rect()
        r.center = screen.get_rect().center
        pg.draw.rect(screen, COLORS["BLACK"], r)
        screen.blit(text, r)
    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0, False 
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return 0, True

def show_surr_tiles(x_pos, y_pos, board, screen, visited, visited_tiles):
    """
    Shows surrounding tiles of a tile 
    """
    x = x_pos // 40
    y = y_pos // 40

    if visited[y][x]:
        return

    visited_tiles[y][x] = True
    visited[y][x] = True
    screen.blit(TILES_DICT[board[y][x]], (x * 40, y * 40))

    if board[y][x] == 9:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= y - i < len(board) and 0 <= x + j < len(board[0]):
                    show_surr_tiles((x + j) * 40, (y - i) * 40, board, screen, visited, visited_tiles)
    pg.display.update()

def show_tile(x, y, board, screen, visited_tiles):
    """
    Shows a tile
    """
    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    show_surr_tiles(x, y, board, screen, visited, visited_tiles)


def flag_tile(x_pos, y_pos, screen):
    """
    Flags a tile
    """
    x = x_pos // 40
    y = y_pos // 40
    screen.blit(TILES_DICT[10], (x * 40, y * 40))
    pg.display.update()

def check_title(x_pos, y_pos, board):
    """
    Checks if a tile is a mine or not
    """
    x = x_pos // 40
    y = y_pos // 40

    if board[y][x] == 0:
        return 1 
    else:
        return 0 
    
def check_win(visited_tiles, difficulty):
    """
    Checks if the player has won or not
    """
    number_of_tiles = len(visited_tiles) * len(visited_tiles[0]) 
    for i in range(len(visited_tiles)):
        for j in range(len(visited_tiles[0])):
            if visited_tiles[i][j]:
                number_of_tiles -= 1
    if number_of_tiles == GAME_DIFFICULTY[difficulty][2]:
        return True
    else:
        return False

def main():
    screen, clock = setup()
    board = [] 
    visited_tiles = []
    score, state, difficulty = 0, 0, 0
    running = True
    win_or_loss = False

    while running:
        clock.tick(30)
        if state == 0:
            state, difficulty, running = start_screen(screen)
            if not running:
                break
            board = create_board(difficulty)
            draw_board(difficulty, screen)
            visited_tiles = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
        elif state == 1:
            state, running, score, win_or_loss = game_screen(screen, board, visited_tiles, difficulty)
        elif state == 2:
            save_highscores(win_or_loss, difficulty, score)
            state, running = game_end(difficulty, screen, board, win_or_loss, score)
            pg.display.set_mode((640, 640))
            pg.display.set_caption("Minesweeper")
    pg.quit()

if __name__ == "__main__":
    main()
