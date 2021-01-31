import chess
import chess.svg
import sys, pygame
from pygame.locals import *
import random
from datetime import datetime



random.seed(datetime.now())
pygame.init()

#structures
class Tree:
    move = None
    value = None
    children = []


# varible init
disc = {}
mouse_piece = []
board = chess.Board()
size = width, height = 1500, 1000
min_value = 10000
white_tree = None
dark_tree = None

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

def white_max(depth):
    children = []
    moves = board.legal_moves
    value = None
    for move in moves:
        board.push(move)

        tupl = dark_min(depth-1)
        if value == None:
            value = tupl[1]
        else:
            if tupl[1] > value:
                value = tupl[1]

        node = Tree()
        node.move = move
        node.children = tupl[0]
        node.value = tupl[1]
        children.append(node)
        board.pop()
    return children,value

def dark_min(depth):
    children = []
    moves = board.legal_moves
    value = None
    for move in moves:
        board.push(move)

        if(depth > 0):
            tupl = white_max(depth-1)
        else:
            tupl = ([],evaluate_position())
        if value == None:
            value = tupl[1]
        else:
            if tupl[1] < value:
                value = tupl[1]
        node = Tree()
        node.move = move
        node.children = tupl[0]
        node.value = tupl[1]

        children.append(node)
        board.pop()
    return children,value

def generate_move(depth):
    global white_tree
    global dark_tree
    best_move = []
    value = None
    moves = board.legal_moves
    for move in moves:
        board.push(move)
        node = Tree()
        tupl = dark_min(depth-1)
        node.move = move
        node.value = tupl[1]
        node.children = tupl[0]
        if value == None:
            value = tupl[1]
            best_move.append(node)
        elif value < tupl[1]:
            value = tupl[1]
            best_move = [node]
        elif value == tupl[1]:
            best_move.append(node)
        board.pop()

    if white:
        white_tree = random_move(best_move)
        board.push(white_tree.move)
        if dark_tree != None:
            dark_tree = matching_son(dark_tree.children,white_tree.move)
    else:
        dark_tree = random_move(best_move)
        board.push(dark_tree.move)
        if white_tree != None:
            white_tree = matching_son(white_tree.children,dark_tree.move)
            for son in white_tree.children:
                print(son.move)

def continue_tree(tree):
    global white_tree
    global dark_tree
    best_move = []
    value = None
    for son in tree.children:
        board.push(son.move)
        tupl = con_white_max(son.children)
        node = Tree()
        node.move = son.move
        node.value = tupl[1]
        node.children = tupl[0]
        if value == None:
            value = tupl[1]
            best_move.append(node)
        elif value < tupl[1]:
            value = tupl[1]
            best_move = [node]
        elif value == tupl[1]:
            best_move.append(node)
        board.pop()
        if white:
            white_tree = random_move(best_move)
            board.push(white_tree.move)
            if dark_tree != None:
                matching_son(white_tree.children,white_tree.move)
        else:
            dark_tree = random_move(best_move)
            board.push(dark_tree.move)
            if white_tree != None:
                matching_son(dark_tree.children,dark_tree.move)

def con_white_max(tree):
    children = []
    # moves = board.legal_moves
    value = None
    if not tree:
        tupl = white_max(1)
        return tupl

    for son in tree:
        board.push(son.move)
        tupl = con_dark_min(son.children)
        son.value = tupl[1]
        if value == None:
            value = tupl[1]
        elif value < tupl[1]:
            value = tupl[1]
        board.pop()

    return tree,value

def con_dark_min(tree):
    children = []
    # moves = board.legal_moves
    value = None
    if not tree:
        tupl = white_max(1)
        return tupl
    for son in tree:
        board.push(son.move)
        tupl = con_white_max(son.children)
        son.value = tupl[1]
        if value == None:
            value = tupl[1]
        elif value > tupl[1]:
            value = tupl[1]
        board.pop()

    return tree,value

def matching_son(sons,move):
    for son in sons:
        if son.move == move:
            return son
    print("error",move)
    pygame.QUIT

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
    else:
        for square in piece_map:
                count += mirror_pieceValue_disc[board.piece_at(square).symbol()]
    return count

init()
# white = board.turn
# generate_move(1)
# white = board.turn
# generate_move(1)
#
# print(white_tree)
# print(dark_tree)
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
    if not board.is_checkmate() and not board.is_stalemate():
        if not white:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            if dark_tree == None:
                generate_move(3)
            else:
                continue_tree(dark_tree)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            if white_tree == None:
                generate_move(3)
            else:
                continue_tree(white_tree)


        min_value = 10000

    render_board()
    render_piece()
    pygame.display.flip()
