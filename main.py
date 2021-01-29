import chess
import chess.svg
import sys, pygame
from pygame.locals import *
import random
from datetime import datetime



random.seed(datetime.now())
pygame.init()


# varible init
disc = {}
mouse_piece = []
board = chess.Board()
size = width, height = 1500, 1000
min_value = 10000

# colors
black = 0,0,0
white = 255,255,255

# images
darkSquare = pygame.image.load("dark.png")
whiteSquare = pygame.image.load("white.png")

whitepawn = pygame.image.load("whitepawn.png")
whitebishop = pygame.image.load("whitebishop.png")
whiterook = pygame.image.load("whiterook.png")
whiteknight = pygame.image.load("whiteknight.png")
whitequeen = pygame.image.load("whitequeen.png")
whiteking = pygame.image.load("whiteking.png")

darkpawn = pygame.image.load("darkpawn.png")
darkbishop = pygame.image.load("darkbishop.png")
darkrook = pygame.image.load("darkrook.png")
darkknight = pygame.image.load("darkknight.png")
darkqueen = pygame.image.load("darkqueen.png")
darkking = pygame.image.load("darkking.png")

# fonts
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont(None, 100)
reply_font = pygame.font.SysFont(None, 60)
stalemate_font =  pygame.font.SysFont(None, 80)

# messages
white_won = font.render('White won!',True,white)
black_won = font.render('Black won!',True,(130,130,130))
white_turn = font.render('White turn',True,white)
black_turn = font.render('Black turn',True,(130,130,130))
stalemate_message = stalemate_font.render('Draw by stalemate',True,white)
replay_message = reply_font.render('Press Enter to replay!',True,white)


# dictionary for rendering
piece_disc = {'P':whitepawn,
            'N':whiteknight,
            'B':whitebishop,
            'R':whiterook,
            'Q':whitequeen,
            'K':whiteking,

            'p':darkpawn,
            'n':darkknight,
            'b':darkbishop,
            'r':darkrook,
            'q':darkqueen,
            'k':darkking}

pieceValue_disc = {'P': 1,
            'N':3,
            'B':3,
            'R':5,
            'Q':9,
            'K':900,

            'p':-1,
            'n':-3,
            'b':-3,
            'r':-5,
            'q':-9,
            'k':-900}

mirror_pieceValue_disc = {'P': -1,
            'N':-3,
            'B':-3,
            'R':-5,
            'Q':-9,
            'K':-900,

            'p':1,
            'n':3,
            'b':3,
            'r':5,
            'q':9,
            'k':900}





def init():
    x = 100
    y = 100
    bollen = True
    for int in range(0,64):
        if bollen == True:
            if int % 2:
                disc[int] = [(x,y),"dark"]
            else:
                disc[int] = [(x,y),"white"]
        else:
            if int % 2:
                disc[int] = [(x,y),"white"]
            else:
                disc[int] = [(x,y),"dark"]
        x+=100
        if (int+1) % 8 == 0 and int != 0:
            y+=100
            x = 100
            bollen = not bollen

def render_board():
    global disc

    for key in disc.keys():
        if disc[key][1] == "white":
            whiteS_rect = whiteSquare.get_rect(center=disc[key][0])
            screen.blit(whiteSquare, whiteS_rect)
        else:
            darkS_rect = darkSquare.get_rect(center=disc[key][0])
            screen.blit(darkSquare, darkS_rect)

def render_piece():
    piece_map =  board.piece_map()

    for square in piece_map:
        piece = board.piece_at(square)
        if square in mouse_piece:
                screen.blit(piece_disc[piece.symbol()],piece_disc[piece.symbol()].get_rect(center=pygame.mouse.get_pos()))
        else:
            screen.blit(piece_disc[piece.symbol()],piece_disc[piece.symbol()].get_rect(center=disc[square][0]))

def generate_move():
    total_moves = board.legal_moves.count()
    moves = board.legal_moves
    rand = random.randrange(0,total_moves)
    for move,int in zip(moves,range(0,total_moves)):
        if rand == int:
            board.push(move)
            break

def init_gene(depth):
    best_move = []
    moves = board.legal_moves
    value = 0
    for move in moves:
        board.push(move)
        tmp_value = dark_min(depth-1,False)
        if not best_move:
            value = tmp_value
            best_move = [move]
        else:
            if tmp_value > value:
                best_move = [move]
                value = tmp_value
            elif tmp_value == value:
                best_move.append(move)
        board.pop()
    board.push(random_move(best_move))

def white_max(depth,fault):
    moves = board.legal_moves
    value = 10000
    for move in moves:
        board.push(move)

        tmp_value = dark_min(depth-1,fault)
        if value == 10000:
            value = tmp_value
        else:
            if tmp_value > value:
                value = tmp_value
        board.pop()
    return value

def dark_min(depth,fault):
    global min_value
    passing_fault = fault
    moves = board.legal_moves
    value = 10000
    for move in moves:
        board.push(move)
        current_valuation = evaluate_position()
        if min_value == 10000:
            min_value =  current_valuation
        elif min_value > current_valuation:
            if(fault == True):
                board.pop()
                return value
            passing_fault = True

        if(depth > 0):
            tmp_value = white_max(depth-1,passing_fault)
        else:
            tmp_value = current_valuation
        if value == 10000:
            value = tmp_value
        else:
            if tmp_value < value:
                value = tmp_value
        board.pop()
    return value

def generate_1depth_move():
    best_move = []
    total_moves = board.legal_moves.count()
    moves = board.legal_moves
    for move in moves:
        board.push(move)
        tmp_value = generate_2depth_move()
        if not best_move:
            value = tmp_value
            best_move = [move]
        else:
            if tmp_value > value:
                best_move = [move]
                value = tmp_value
            elif tmp_value == value:
                best_move.append(move)
        board.pop()
    board.push(random_move(best_move))

def generate_2depth_move():
    best_move = []
    total_moves = board.legal_moves.count()
    moves = board.legal_moves
    value = 0
    for move in moves:
        board.push(move)
        tmp_value = evaluate_position()
        if not best_move:
            value = tmp_value
            best_move = [move]
        else:
            if tmp_value < value:
                best_move = [move]
                value = tmp_value
            elif tmp_value == value:
                best_move.append(move)
        board.pop()
    return value

def random_move(move):
    if len(move) == 0:
        return move[0]
    rand = random.randrange(0,len(move))
    return move[rand]


def evaluate_position():
    count = 0
    piece_map =  board.piece_map()
    if white:
        for square in piece_map:
                count += pieceValue_disc[board.piece_at(square).symbol()]
        if count == None:
            print(board)
    else:
        for square in piece_map:
                count += mirror_pieceValue_disc[board.piece_at(square).symbol()]
        if count == None:
            print(board)
    return count

init()
while 1:
    screen.fill(black)

    # if not board.turn:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT: sys.exit()
    #         if event.type == MOUSEBUTTONDOWN:
    #             for button in pygame.mouse.get_pressed(num_buttons=3):
    #                 if button == True:
    #                     for int in range(0,64):
    #                         if whiteSquare.get_rect(center=disc[int][0]).collidepoint(pygame.mouse.get_pos()):
    #                             mouse_piece.append(int)
    #         if event.type == MOUSEBUTTONUP:
    #             for square in mouse_piece:
    #                 for int in range(0,64):
    #                     if whiteSquare.get_rect(center=disc[int][0]).collidepoint(pygame.mouse.get_pos()):
    #                         move = chess.Move(square,int)
    #                         if move in board.legal_moves:
    #                             board.push(move)
    #                             evaluate_position()
    #             mouse_piece = []
    # else:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT: sys.exit()
    #     init_gene(3)
    #     min_value = 10000
    white = board.turn
    if not white:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        init_gene(3)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        init_gene(3)

    min_value = 10000

    render_board()
    render_piece()
    pygame.display.flip()
