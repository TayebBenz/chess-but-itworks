import chess
import sys, pygame
from pygame.locals import *
import random
from datetime import datetime
import chessrender as render
import AIkekW as Ai
import datetime
from timeit import timeit
from numba.typed import List


class Mouse:
    pos = None
    square = []



pygame.init()

board = chess.Board()
mouse = Mouse()

# colors
black = 0,0,0
white = 255,255,255



render.init()

while 1:
    render.screen.fill(black)
    if board.turn:
        tmp_date = datetime.datetime.now()
        Ai.generate_move(board,4)
        print("It took around :",datetime.datetime.now()-tmp_date)
    else:
        mouse.pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for button in pygame.mouse.get_pressed(num_buttons=3):
                    if button == True:
                        collision = render.collided(mouse.pos)
                        if collision != None:
                            mouse.square.append(collision)
            if event.type == MOUSEBUTTONUP:
                for square in mouse.square:
                    collision = render.collided(mouse.pos)
                    if collision != None:
                        move = chess.Move(square,collision)
                        if move in board.legal_moves:
                            board.push(move)
                mouse.square = []

    render.board()
    render.pieces(board,mouse)

    pygame.display.flip()
