import chess
import sys, pygame
from pygame.locals import *
import random
import datetime


total_moves = 0


random.seed(datetime.datetime.now())

tree = None

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

    global total_moves
    total_moves = 0
    best_move = first_move(board.copy(),depth)

    print("total moves :", total_moves)

    if not best_move:
        print("Error moves empty")
        sys.exit()

    chosen_one = random_move(best_move)
    board.push(chosen_one)


def minmaxing(board,alpha,beta,depth,maximixingPlayer):

    if depth == 0:
        return evaluate_position(board)

    if board.is_checkmate():
        if maximixingPlayer:
            return -990
        else:
            return 990
    elif board.is_stalemate():
        return 0

    if maximixingPlayer:
        maxEval = -999
        for move in board.legal_moves:
            board.push(move)
            Eval = minmaxing(board,alpha,beta,depth-1,False)
            maxEval = max(maxEval,Eval)
            board.pop()

            alpha = max(alpha,Eval)
            if beta < alpha:
                break

        return maxEval

    else:
        minEval = 999
        for move in board.legal_moves:
            board.push(move)
            Eval = minmaxing(board,alpha,beta,depth-1,True)
            minEval = min(minEval,Eval)
            board.pop()

            beta = min(beta,Eval)
            if beta < alpha:
                break
        return minEval


def first_move(board,depth):
    bestMoves = []
    Evalmax = -999
    alpha = -990
    beta = 990

    for move in board.legal_moves:
        board.push(move)

        if board.is_checkmate() or board.is_stalemate():
            Eval = evaluate_position(board)
        else:
            Eval = minmaxing(board,alpha,beta,depth-1,False)

        if Eval > Evalmax:
            bestMoves = [move]
            Evalmax = Eval
        elif Eval == Evalmax:
            bestMoves.append(move)

        alpha = max(alpha,Eval)
        board.pop()


    if not bestMoves:
        print("Error returning empty list",depth)
        print(board)

    print("Best Eval :",Evalmax)
    return bestMoves


def evaluate_position(board):
    global total_moves
    total_moves += 1
    Eval = 0
    for piece in board.piece_map().values():
        Eval += pieceValue_disc[piece.symbol()]
    return Eval
