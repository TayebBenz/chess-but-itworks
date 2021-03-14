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
import threading


class Mouse:
    pos = None
    square = []



pygame.init()

board = chess.Board()
render_board = board.copy()
mouse = Mouse()
tmp_stack = []
generating_move = False

# colors
black = 0,0,0
white = 255,255,255



render.init_test()
while 1:
    render.screen.fill(black)
    if board.turn and not generating_move and not board.is_game_over():
        tmp_date = datetime.datetime.now()
        x = threading.Thread(target=Ai.generate_move, args=(board,2), daemon=True)
        generating_move = True
        x.start()
        # Ai.generate_move(board,2)
        # print("It took around :",datetime.datetime.now()-tmp_date)
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
                                while not(not tmp_stack):
                                    render_board.push(tmp_stack.pop())
                            elif collision == "previous":
                                if not not(render_board.move_stack):
                                    tmp_stack.append(render_board.pop())
                            elif collision == "begin":
                                while len(render_board.move_stack) >= 1:
                                    tmp_stack.append(render_board.pop())


            if event.type == MOUSEBUTTONUP:
                for square in mouse.square:
                    collision = render.collided(mouse.pos)
                    if collision != None:
                        move = chess.Move(square,collision)
                        if move in board.legal_moves:
                            board.push(move)
                mouse.square = []

    if generating_move and threading.active_count() == 1:
        print("It took around :",datetime.datetime.now()-tmp_date)
        generating_move = False
    if not tmp_stack and not generating_move:
        render_board = board.copy()

    if  board.is_game_over():
        mouse.square = []
        while 1:
            render.screen.fill(black)
            for event in pygame.event.get():
                mouse.pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT: sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    for button in pygame.mouse.get_pressed(num_buttons=3):
                        if button == True:
                            collision = render.Arrows_collision(mouse.pos)
                            if collision != None:
                                if collision == "next":
                                    if not(not tmp_stack):
                                        render_board.push(tmp_stack.pop())
                                elif collision == "end":
                                    while not(not tmp_stack):
                                        render_board.push(tmp_stack.pop())
                                elif collision == "previous":
                                    if not not(render_board.move_stack):
                                        tmp_stack.append(render_board.pop())
                                elif collision == "begin":
                                    while len(render_board.move_stack) >= 1:
                                        tmp_stack.append(render_board.pop())
            render.game_over(board)
            render.board(render_board)
            render.pieces(render_board,mouse)
            pygame.display.flip()

    render.board(render_board)
    render.pieces(render_board,mouse)

    pygame.display.flip()
