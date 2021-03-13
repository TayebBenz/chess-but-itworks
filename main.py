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
render_board = board.copy()
mouse = Mouse()
tmp_stack = []

# colors
black = 0,0,0
white = 255,255,255



render.init_test()

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
                        if collision != None and not tmp_stack:
                            mouse.square.append(collision)
                        collision = render.Arrows_collision(mouse.pos)
                        if collision != None:
                            if collision == "next":
                                if not(not tmp_stack):
                                    render_board.push(tmp_stack.pop())
                            elif collision == "end":
                                render_board = board.copy()
                                tmp_stack = []
                            elif collision == "previous":
                                if not not(render_board.move_stack):
                                    tmp_stack.append(render_board.pop())
                            elif collision == "begin":
                                while len(render_board.move_stack) > 1:
                                    tmp_stack.append(render_board.pop())


            if event.type == MOUSEBUTTONUP:
                for square in mouse.square:
                    collision = render.collided(mouse.pos)
                    if collision != None:
                        move = chess.Move(square,collision)
                        if move in board.legal_moves:
                            board.push(move)
                mouse.square = []

    if not tmp_stack:
        render_board = board.copy()
    render.board(render_board)
    render.pieces(render_board,mouse)

    pygame.display.flip()
