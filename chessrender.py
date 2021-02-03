import sys, pygame
from pygame.locals import *

disc = {}

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



def init():
    x = 50
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
        x+=50
        if (int+1) % 8 == 0 and int != 0:
            y+=50
            x = 50
            bollen = not bollen

def board():
    for key in disc.keys():
        if disc[key][1] == "white":
            whiteS_rect = whiteSquare.get_rect(center=disc[key][0])
            screen.blit(whiteSquare, whiteS_rect)
        else:
            darkS_rect = darkSquare.get_rect(center=disc[key][0])
            screen.blit(darkSquare, darkS_rect)

def collided(position):
    for int in range(0,64):
        if whiteSquare.get_rect(center=disc[int][0]).collidepoint(position):
            return int
    return None

def pieces(board,mouse):
    piece_map =  board.piece_map()

    for square in piece_map:
        piece = board.piece_at(square)
        if square in mouse.square:
            screen.blit(piece_disc[piece.symbol()],piece_disc[piece.symbol()].get_rect(center=mouse.pos))
        else:
            screen.blit(piece_disc[piece.symbol()],piece_disc[piece.symbol()].get_rect(center=disc[square][0]))
