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
    pg.init()
    screen = pg.display.set_mode((640, 640))
    pg.display.set_caption("Minesweeper")
    clock = pg.time.Clock()
    return screen, clock 


def load_highscores():
    with open("score.csv", "r") as file:
        reader = csv.reader(file)
        highscores = list(reader)
    return highscores

def start_screen(screen):
    score = load_highscores()
    font = pg.font.Font("freesansbold.ttf", 28)
    text = font.render("Minesweeper personal highscore:", True, COLORS["BLACK"])
    screen.fill(COLORS["WHITE"])
    pg.draw.line(screen, COLORS["BLACK"], (0, 40), (640, 40), 2)
    screen.blit(text, (0, 15))

    for i in range(len(score)):
        text = font.render(f"{score[i][0]}: {score[i][1]}", True, COLORS["BLACK"])
        screen.blit(text, (0, 0 + i * 50 + 50))
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

def game_screen(screen, board):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0, 0, False, 0 
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if check_title(event.pos[0], event.pos[1], board) == 0:
                        show_tile(event.pos[0], event.pos[1], board, screen)
                    elif check_title(event.pos[0], event.pos[1], board) == 1:
                        return 2, True
                    elif check_title(event.pos[0], event.pos[1], board) == 2:
                        pass
                elif event.button == 3:
                    flag_tile(event.pos[0], event.pos[1], board, screen)

def create_board(difficulty):
    board = [[-1 for _ in range(GAME_DIFFICULTY[difficulty][0])] for _ in range(GAME_DIFFICULTY[difficulty][1])]
    for i in range(GAME_DIFFICULTY[difficulty][2]):
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
    pg.display.set_mode((GAME_DIFFICULTY[difficulty][0] * 40, GAME_DIFFICULTY[difficulty][1] * 40))
    for y in range(GAME_DIFFICULTY[difficulty][1]):
        for x in range(GAME_DIFFICULTY[difficulty][0]):
            screen.blit(TILES_DICT[11], (x * 40, y * 40))
    pg.display.update()

def game_end(difficulty, screen, board):
    for y in range(GAME_DIFFICULTY[difficulty][1]):
        for x in range(GAME_DIFFICULTY[difficulty][0]):
            screen.blit(TILES_DICT[board[y][x]], (x * 40, y * 40))
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0, False 
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return 0, True

def show_surr_tiles(x_pos, y_pos, board, screen, visited):
    x = x_pos // 40
    y = y_pos // 40

    if visited[y][x]:
        return

    visited[y][x] = True
    screen.blit(TILES_DICT[board[y][x]], (x * 40, y * 40))

    if board[y][x] == 9:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= y - i < len(board) and 0 <= x + j < len(board[0]):
                    show_surr_tiles((x + j) * 40, (y - i) * 40, board, screen, visited)
    pg.display.update()

def show_tile(x, y, board, screen):
    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    show_surr_tiles(x, y, board, screen, visited)


def flag_tile(x_pos, y_pos, board, screen):
    x = x_pos // 40
    y = y_pos // 40
    screen.blit(TILES_DICT[10], (x * 40, y * 40))
    pg.display.update()

def check_title(x_pos, y_pos, board):
    x = x_pos // 40
    y = y_pos // 40

    if board[y][x] == 0:
        return 1 
    else:
        return 0 

def check_win():
    pass


def main():
    screen, clock = setup()
    board = [] 
    score, state, difficulty = 0, 0, 0
    running = True

    while running:
        clock.tick(30)
        if state == 0:
            state, difficulty, running = start_screen(screen)
            board = create_board(difficulty)
            draw_board(difficulty, screen)
        elif state == 1:
            state, running = game_screen(screen, board)
        elif state == 2:
            state, running = game_end(difficulty, screen, board)
            pg.display.set_mode((640, 640))
    pg.quit()

if __name__ == "__main__":
    main()