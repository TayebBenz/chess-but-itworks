import chess
import chess.svg
import sys, pygame
from pygame.locals import *
import random
import datetime
from numba import jit


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


def advance_tree(move):
    global tree
    for son in tree.sons:
        if son.move == move:
            tree = son
            return
    print("error couldnt advance the tree")
    print(move)
    print(board)
    sys.exit()

def random_move(move):
    if len(move) == 0:
        print("Error passed empty list")
    rand = random.randrange(0,len(move))
    return move[rand]



def generate_move(board,depth):

    global total_moves
    total_moves = 0
    best_move = first_move(board,depth)

    print("total moves :", total_moves)

    if not best_move:
        print("Error moves empty")
        sys.exit()

    chosen_one = random_move(best_move)
    board.push(chosen_one)



def Tree_cont_Ai(root,board):
    value = None
    for son in root.sons:
        board.push(son.move)
        if not root.sons:
            print("error expected sons to be populated")
            print(board)
            sys.exit()
        else:
            if board.is_checkmate():
                son.value = 900
                board.pop()
                return
            Tree_cont_player(son,board)
            for grandson in son.sons:
                if value == None:
                    value = grandson.value
                elif value > grandson.value:
                    value = grandson.value
            son.value = value
        board.pop()

def Tree_cont_player(root,board):
    value = None
    for son in root.sons:
        board.push(son.move)
        if not son.sons:
            son.sons = possible_moves(board,2)
        else:
            if board.is_checkmate():
                son.value = -900
                board.pop()
                return
            Tree_cont_Ai(son,board)

        for grandson in son.sons:
            if value == None:
                value = grandson.value
            elif value < grandson.value:
                value = grandson.value
        son.value = value
        board.pop()


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


def possible_moves(board,depth,alpha,beta):
    value = None
    tmp_value = None
    for move in board.legal_moves:
        board.push(move)

        if board.is_checkmate() or board.is_stalemate():
            tmp_value = evaluate_position(board)
        else:
            tmp_value = counter_moves(board,depth-1,alpha,beta)


        if value == None:
            value = tmp_value
        elif tmp_value > value:
            value = tmp_value

        if value == None:
            print("Error inside possible_moves",depth)
            print(board)
            sys.exit()
        board.pop()

        alpha = max(alpha,tmp_value)
        if beta <= alpha:
            break

    if value == None:
        print("Error inside possible_moves returning None value",depth)
        print(board)
        sys.exit()

    return value

def counter_moves(board,depth,alpha,beta):
    value = None
    tmp_value = None
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate() or board.is_stalemate() or depth == 1:
            tmp_value = evaluate_position(board)
        else:
            tmp_value = possible_moves(board,depth-1,alpha,beta)

        if value == None:
            value = tmp_value
        elif tmp_value < value:
            value = tmp_value

        if value == None:
            print("Error inside counter_moves",depth)
            print(moves)
            sys.exit()
        board.pop()

        beta = min(beta,tmp_value)
        if beta <= alpha:
            break

    if value == None:
        print("Error inside counter_moves returning None value",depth)
        print(moves)
        sys.exit()

    return value

@jit(nopython=True)
def New_Eval(pieces):
    Eval = 0
    for piece_symbol in pieces:
        if piece_symbol == 'r':
            Eval += -5
        elif  piece_symbol == 'n':
            Eval += -3
        elif  piece_symbol == 'b':
            Eval += -3
        elif  piece_symbol == 'q':
            Eval += -9
        elif  piece_symbol == 'p':
            Eval += -1
        elif  piece_symbol == 'P':
            Eval += 1
        elif  piece_symbol == 'R':
            Eval += 5
        elif  piece_symbol == 'N':
            Eval += 3
        elif  piece_symbol == 'B':
            Eval += 3
        elif  piece_symbol == 'Q':
            Eval += 9

    return Eval

def evaluate_position(board):
    global total_moves
    total_moves += 1
    Eval = 0
    for piece in board.piece_map().values():
        Eval += pieceValue_disc[piece.symbol()]
    return Eval

def test_Eval(board):
    for piece in board.piece_map().values():
        piece.symbol()


# def evaluate_position(board):
#     global total_moves
#     total_moves+=1
#     count = 0
#     piece_map =  board.piece_map()
#
#     if board.turn:
#         for square in piece_map:
#             count += pieceValue_disc[board.piece_at(square).symbol()]
#
#     else:
#         for square in piece_map:
#             count += mirror_pieceValue_disc[board.piece_at(square).symbol()]
#
#     return count
