import chess
import chess.svg
import sys, pygame
from pygame.locals import *
import random
from datetime import datetime



random.seed(datetime.now())

class Tree:
    move = None
    value = None
    sons = []


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



def random_move(move):
    if len(move) == 0:
        print("Error passed empty list")
    rand = random.randrange(0,len(move))
    return move[rand]



def generate_move(board,depth):
    calculated_moves = possible_moves(board,depth)
    value = None
    best_move =[]

    for node in calculated_moves:
        if not best_move:
            best_move = [node]
            value = node.value
        else:
            if node.value > value:
                best_move = [node]
                value = node.value
            elif node.value == value:
                best_move.append(node)

    if not best_move:
        print("Error moves empty")
        sys.exit()

    chosen_one = random_move(best_move)
    board.push(chosen_one.move)
    print(chosen_one.value)



def possible_moves(board,depth):
    calcu_moves = []

    for move in board.legal_moves:
        board.push(move)
        value = None
        worst_value = None
        if board.is_checkmate():
            value = 900
            move =[]
        else:

            moves = counter_moves(board,depth-1)
            for counter in moves:
                if value == None:
                    value = counter.value
                elif counter.value < value:
                    value = counter.value


            if value == None:
                print("Error inside possible_moves",depth)
                print(board)
                sys.exit()

        node = Tree()
        node.move = move
        node.value = value
        node.sons = moves
        calcu_moves.append(node)

        if not calcu_moves:
            print("list is empty",depth)
            print(node)
        board.pop()

    if not calcu_moves:
        print("Error returning empty list",depth)
        print(board)
    return calcu_moves

def counter_moves(board,depth):
    calcu_moves = []
    for move in board.legal_moves:
        board.push(move)
        value = None

        if board.is_checkmate():
            value = -900
            move =[]
        else:
            if depth == 1:
                value = evaluate_position(board)
                moves = []
            else:
                moves = possible_moves(board,depth-1)
                for counter in moves:
                    if value == None:
                        value = counter.value
                    elif counter.value > value:
                        value = counter.value

        if value == None:
            print("Error inside counter_moves",depth)
            print(moves)
            sys.exit()

        node = Tree()
        node.move = move
        node.value = value
        node.sons = moves
        calcu_moves.append(node)
        board.pop()

    if not calcu_moves:
        print("Error returning empty list",depth)
    return calcu_moves

def evaluate_position(board):
    count = 0
    piece_map =  board.piece_map()
    if board.turn:
        for square in piece_map:
                count += pieceValue_disc[board.piece_at(square).symbol()]
    else:
        for square in piece_map:
                count += mirror_pieceValue_disc[board.piece_at(square).symbol()]
    return count
