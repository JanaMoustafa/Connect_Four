import numpy as np
import pygame
import sys
import math
from threading import Timer
import random

EASY = 0
MEDIUM = 1
HARD = 2
VERY_HARD = 3

ROWS = 6
COLUMNS = 7

PLAYER_TURN = 0
AI_TURN = 1

PLAYER_PIECE = 1
AI_PIECE = 2
SQUARESIZE = 120
width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE / 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
Maroon = (102, 0, 0)



def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board



def drop_piece(board, row, col, piece):
    board[row][col] = piece



def is_valid_location(board, col):
    return board[0][col] == 0



def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None


def winning_move(board, piece):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

    for c in range(3, COLUMNS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][
                c - 3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, (255, 192, 203), (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   circle_radius)
            else:
                pygame.draw.circle(screen, (137, 207, 240), (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   circle_radius)
                pygame.display.update()

    pygame.display.update()



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def show_difficulty_menu(screen, clock):
    # Fill background with beige color
    screen.fill((245, 245, 220))

    top_font = pygame.font.SysFont("comicsansms", 52, bold=True)
    title_font = pygame.font.SysFont("comicsansms", 40, italic=True)
    menu_font = pygame.font.SysFont("comicsansms", 28)

    offset_x = 100  # Shift everything 100 pixels to the right

    # Draw rectangles behind level texts for better visibility
    very_hard_text = "Very Hard"
    very_hard_width, _ = menu_font.size(very_hard_text)

    level_rects = [
        pygame.Rect(45 + offset_x, 180, 110, 40),
        pygame.Rect(45 + offset_x, 240, 130, 40),
        pygame.Rect(45 + offset_x, 300, 110, 40),
        pygame.Rect(width // 2 - very_hard_width // 2 - 10, height // 2 - 15, very_hard_width + 20, 40),
        pygame.Rect(445 + offset_x, 180, 110, 40),
        pygame.Rect(445 + offset_x, 240, 130, 40),
        pygame.Rect(445 + offset_x, 300, 110, 40),
    ]
    rect_colors = [
        (0, 100, 100),
        (100, 100, 0),
        (100, 50, 50),
        (100, 0, 100),
        (0, 100, 100),
        (100, 100, 0),
        (100, 50, 50),
    ]
    for rect, color in zip(level_rects, rect_colors):
        pygame.draw.rect(screen, color, rect, border_radius=8)

    draw_text("Connect Four", top_font, BLACK, screen, width // 2 - 250 + offset_x, 50)
    # Center "Minimax Algorithm" and levels
    minimax_text = "Minimax Algorithm"
    minimax_text_width, _ = title_font.size(minimax_text)
    minimax_x = 50 + offset_x + (110 - minimax_text_width) // 2
    draw_text(minimax_text, title_font, BLACK, screen, minimax_x, 130)

    easy_text = "Easy"
    easy_width, _ = menu_font.size(easy_text)
    draw_text(easy_text, menu_font, (0, 255, 255), screen, 50 + offset_x + (110 - easy_width) // 2, 180)

    medium_text = "Medium"
    medium_width, _ = menu_font.size(medium_text)
    draw_text(medium_text, menu_font, (255, 255, 0), screen, 50 + offset_x + (130 - medium_width) // 2, 240)

    hard_text = "Hard"
    hard_width, _ = menu_font.size(hard_text)
    draw_text(hard_text, menu_font, (255, 100, 100), screen, 50 + offset_x + (110 - hard_width) // 2, 300)

    # Center "Alpha Beta Purning" and levels
    alpha_beta_text = "Alpha Beta Purning"
    alpha_beta_text_width, _ = title_font.size(alpha_beta_text)
    alpha_beta_x = 445 + offset_x + (110 - alpha_beta_text_width) // 2
    draw_text(alpha_beta_text, title_font, BLACK, screen, alpha_beta_x, 130)

    easy_text_right = "Easy"
    easy_width_right, _ = menu_font.size(easy_text_right)
    draw_text(easy_text_right, menu_font, (0, 255, 255), screen, 445 + offset_x + (110 - easy_width_right) // 2, 180)

    medium_text_right = "Medium"
    medium_width_right, _ = menu_font.size(medium_text_right)
    draw_text(medium_text_right, menu_font, (255, 255, 0), screen, 445 + offset_x + (130 - medium_width_right) // 2, 240)

    hard_text_right = "Hard"
    hard_width_right, _ = menu_font.size(hard_text_right)
    draw_text(hard_text_right, menu_font, (255, 100, 100), screen, 445 + offset_x + (110 - hard_width_right) // 2, 300)

    very_hard_text = "Very Hard"
    very_hard_width, _ = menu_font.size(very_hard_text)

    # Draw algorithm name above "Very Hard" level
    algorithm_name = "Minimax Alpha Beta"
    algorithm_width, _ = menu_font.size(algorithm_name)
    draw_text(algorithm_name, menu_font, BLACK, screen, width // 2 - algorithm_width // 2, height // 2 - 50)

    draw_text(very_hard_text, menu_font, (255, 0, 255), screen, width // 2 - very_hard_width // 2, height // 2 - 10)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                offset_x = 100
                if 45 + offset_x <= x <= 155 + offset_x and 180 <= y <= 220:
                    return EASY, EASY
                elif 45 + offset_x <= x <= 175 + offset_x and 240 <= y <= 280:
                    return MEDIUM, MEDIUM
                elif 45 + offset_x <= x <= 155 + offset_x and 300 <= y <= 340:
                    return HARD, HARD
                elif 445 + offset_x <= x <= 555 + offset_x and 180 <= y <= 220:
                    return EASY, EASY
                elif 445 + offset_x <= x <= 575 + offset_x and 240 <= y <= 280:
                    return MEDIUM, MEDIUM
                elif 445 + offset_x <= x <= 555 + offset_x and 300 <= y <= 340:
                    return HARD, HARD
                elif width // 2 - 60 <= x <= width // 2 + 60 and height // 2 - 15 <= y <= height // 2 + 25:
                    return VERY_HARD, VERY_HARD



def end_game():
    global game_over
    game_over = True
    print(game_over)


def draw_play_again_button():
    button_width = 200
    button_height = 100
    button_x = width // 2 - button_width // 2
    button_y = 100


    pygame.draw.rect(screen, (137, 207, 240), (button_x, button_y, button_width, button_height))


    play_again_font = pygame.font.Font(None, 48)
    draw_text("Play Again", play_again_font, WHITE, screen, button_x + 20, button_y + 20)

    pygame.display.update()


def draw_ai_thoughts(col, score, my_font):
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
    text = f"AI chooses column {col} with score {score}"
    label = my_font.render(text, 1, WHITE)
    screen.blit(label, (40, 10))
    pygame.display.update()

def main():
    pygame.init()

    my_font = pygame.font.SysFont("monospace", 30)


    left_difficulty, right_difficulty = show_difficulty_menu(screen, pygame.time.Clock())

    board = create_board()
    game_over = False
    not_over = True
    # Ensure only one player starts with AI_TURN to avoid AI playing twice consecutively
    if random.random() < 0.5:
        left_turn = PLAYER_TURN
        right_turn = AI_TURN
    else:
        left_turn = AI_TURN
        right_turn = PLAYER_TURN

    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION and not_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                xpos = pygame.mouse.get_pos()[0]
                if left_turn == PLAYER_TURN:
                    pygame.draw.circle(screen, (255, 192, 203), (xpos, int(SQUARESIZE / 2)), circle_radius)
                elif right_turn == PLAYER_TURN:
                    pygame.draw.circle(screen, GREEN, (xpos, int(SQUARESIZE / 2)), circle_radius)

            if event.type == pygame.MOUSEBUTTONDOWN and not_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if left_turn == PLAYER_TURN:
                    xpos = event.pos[0]
                    col = int(math.floor(xpos / SQUARESIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        if row is None:
                            continue
                        drop_piece(board, row, col, PLAYER_PIECE)
                        if winning_move(board, PLAYER_PIECE):
                            print("YOU WON!")
                            label = my_font.render("YOU WON!", 1, GREEN)
                            screen.blit(label, (40, 50))

                            not_over = False
                            game_over = True
                        left_turn = AI_TURN
                        t = Timer(3.0, end_game)
                        t.start()
                        draw_board(board)

                elif right_turn == PLAYER_TURN:
                    xpos = event.pos[0]
                    col = int(math.floor(xpos / SQUARESIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        if row is None:
                            continue
                        drop_piece(board, row, col, PLAYER_PIECE)
                        if winning_move(board, PLAYER_PIECE):
                            print("YOU WON!")
                            label = my_font.render("YOU WON!", 1, GREEN)
                            screen.blit(label, (40, 50))

                            not_over = False
                            game_over = True
                        right_turn = AI_TURN
                        t = Timer(3.0, end_game)
                        t.start()
                        draw_board(board)

            pygame.display.update()

        if left_turn == AI_TURN and not game_over and not_over:

            pygame.time.wait(500)

            if left_difficulty == EASY:
                depth = 1
                col, score = alpha_beta_pruning(board, depth, -math.inf, math.inf, True)
            elif left_difficulty == MEDIUM:
                depth = 2
                col, score = alpha_beta_pruning(board, depth, -math.inf, math.inf, True)
            elif left_difficulty == HARD:
                depth = 4
                col, score = alpha_beta_pruning(board, depth, -math.inf, math.inf, True)
            elif left_difficulty == VERY_HARD:
             depth = 6
            col, score = minimaxalpha(board, depth, -math.inf, math.inf, True)

            draw_ai_thoughts(col, score, my_font)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                if row is None:
                    continue
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    print("AI WON")
                    label = my_font.render("AI WON!", 1, GREEN)

                    screen.blit(label, (40, 50))
                    not_over = False
                    game_over = True
                left_turn = PLAYER_TURN
                t = Timer(3.0, end_game)
                t.start()

                draw_board(board)

        elif right_turn == AI_TURN and not game_over and not_over:

            pygame.time.wait(500)

            if right_difficulty == EASY:
                depth = 1
                col, _ = alpha_beta_pruning(board, depth, -math.inf, math.inf, True)
            elif right_difficulty == MEDIUM:
                depth = 2
                col, _ = alpha_beta_pruning(board, depth, -math.inf, math.inf, True)
            else:
                depth = 4
                col, _ = alpha_beta_pruning(board, depth, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                if row is None:
                    continue
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    print("AI WON")
                    label = my_font.render("AI WON!", 1, GREEN)

                    screen.blit(label, (40, 50))
                    not_over = False
                    game_over = True
                right_turn = PLAYER_TURN
                t = Timer(3.0, end_game)
                t.start()

                draw_board(board)


    draw_play_again_button()
    pygame.display.update()


    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if width // 2 - 70 <= x <= width // 2 + 70 and 80 <= y <= 200:

                    game_over = False
                    main()



def score_position(board, piece):
    score = 0


    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6


    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)


    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)


    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)


    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score



def minimax(board, depth, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value



def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0



def get_valid_locations(board):
    valid_locations = []
    for column in range(COLUMNS):
        if is_valid_location(board, column):
            valid_locations.append(column)
    return valid_locations



def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = alpha_beta_pruning(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = alpha_beta_pruning(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value


def minimaxalpha(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimaxalpha(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimaxalpha(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value


if __name__ == '__main__':
    main()