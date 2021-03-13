import sys, pygame
import chess
from pygame.locals import *

disc = {}
focus = None
# colors
black = 0,0,0
white = 255,255,255


darkSquare = pygame.image.load("Assets/dark.png")
whiteSquare = pygame.image.load("Assets/white.png")

whitepawn = pygame.image.load("Assets/whitepawn.png")
whitebishop = pygame.image.load("Assets/whitebishop.png")
whiterook = pygame.image.load("Assets/whiterook.png")
whiteknight = pygame.image.load("Assets/whiteknight.png")
whitequeen = pygame.image.load("Assets/whitequeen.png")
whiteking = pygame.image.load("Assets/whiteking.png")

darkpawn = pygame.image.load("Assets/darkpawn.png")
darkbishop = pygame.image.load("Assets/darkbishop.png")
darkrook = pygame.image.load("Assets/darkrook.png")
darkknight = pygame.image.load("Assets/darkknight.png")
darkqueen = pygame.image.load("Assets/darkqueen.png")
darkking = pygame.image.load("Assets/darkking.png")


attack = pygame.image.load("Assets/attacks.png")
lastMove = pygame.image.load("Assets/lastMove.png")

endArrow = pygame.image.load("Assets/EndArrow.png")
nextArrow = pygame.image.load("Assets/nextArrow.png")
beginArrow = pygame.image.load("Assets/beginArrow.png")
previousArrow = pygame.image.load("Assets/previousArrow.png")




size = width, height = 1000,600

screen = pygame.display.set_mode(size)


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



def init_test():
    x= 400
    y= 100
    bollen = True
    for int in range(1,65):
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
        x-=50
        if int % 8 == 0:
            x = 400
            y+= 50
            bollen = not bollen
def init():
    x = 50
    y = 100
    bollen = True
    for int in range(1,65):
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
        x+=50
        if (int+1) % 8 == 0 and int != 0:
            y+=50
            x = 50
            bollen = not bollen

def board(b):
    for key in disc.keys():
        if disc[key][1] == "white":
            whiteS_rect = whiteSquare.get_rect(center=disc[key][0])
            screen.blit(whiteSquare, whiteS_rect)
        else:
            darkS_rect = darkSquare.get_rect(center=disc[key][0])
            screen.blit(darkSquare, darkS_rect)

    nextArrow_rect = nextArrow.get_rect(center=(715,425))
    screen.blit( nextArrow,  nextArrow_rect)
    endArrow_rect = endArrow.get_rect(center=(780,425))
    screen.blit( endArrow,  endArrow_rect)

    previousArrow_rect = previousArrow.get_rect(center=(595,425))
    screen.blit( previousArrow,  previousArrow_rect)
    beginArrow_rect = beginArrow.get_rect(center=(530,425))
    screen.blit( beginArrow,  beginArrow_rect)

    if not(not b.move_stack):
        last_move = b.peek().uci()
        lastMove_rect =lastMove.get_rect(center=disc[(int(last_move[1])-1)*8+(ord(last_move[0])-ord('a')+1)][0])
        screen.blit(lastMove, lastMove_rect)
        lastMove_rect =lastMove.get_rect(center=disc[(int(last_move[3])-1)*8+(ord(last_move[2])-ord('a')+1)][0])
        screen.blit(lastMove, lastMove_rect)



def collided(position):
    global focus
    for int in range(1,65):
        if whiteSquare.get_rect(center=disc[int][0]).collidepoint(position):
            focus = int-1
            return int-1
    focus = None
    return None

def Arrows_collision(position):
    if nextArrow.get_rect(center=(715,425)).collidepoint(position):
        return "next"
    elif endArrow.get_rect(center=(780,425)).collidepoint(position):
        return "end"
    elif previousArrow.get_rect(center=(595,425)).collidepoint(position):
        return "previous"
    elif beginArrow.get_rect(center=(530,425)).collidepoint(position):
        return "begin"
    return None


def pieces(board,mouse):
    global focus
    piece_map =  board.piece_map()

    for square in piece_map:
        piece = board.piece_at(square)
        if square in mouse.square:
            screen.blit(piece_disc[piece.symbol()],piece_disc[piece.symbol()].get_rect(center=mouse.pos))
        else:
            screen.blit(piece_disc[piece.symbol()],piece_disc[piece.symbol()].get_rect(center=disc[square+1][0]))
    if not(not focus):
        for square in range(0,64):
            if chess.Move(focus,square) in board.legal_moves:
                attack_rect = attack.get_rect(center=disc[square+1][0])
                screen.blit(attack, attack_rect)
