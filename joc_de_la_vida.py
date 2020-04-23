# -*- coding: utf-8 -*-

import pygame
import time, os
import numpy as np

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# TÍTOL DE LA FINESTRA:
pygame.display.set_caption("El joc de la vida - @pribaqnet")

# CARREGUEM ICONA SI EXISTEIX
iconPath = "./icono.ico"

if os.path.exists(iconPath):

    icono = pygame.image.load(iconPath)
    pygame.display.set_icon(icono)

# CREACIÓ DE LA FINESTRA
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

# COLOR DE FONS
bg = 25, 25, 25
screen.fill(bg)

# QUANTITAT DE CEL·LES
nxC, nyC = 60, 60

# MIDA DE LES CEL·LES
dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# CONTROL DE L'EXECUCIÓ: (El joc comença pausat per a poder estructurar les cel·lules)
pauseExec = False
endGame = False

# ACUMULADOR D'INTERACCIONS:
iteration = 0

# LOOP PRINCIPAL:
while not endGame:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # CONTADOR DE POBLACIÓ
    population = 0

    # EVENTS TECLAT I RATOLÍ
    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.QUIT:
            endGame = True
            break

        if event.type == pygame.KEYDOWN:

            # AMB LA TECLA [ESC] ES TANCA EL JOC
            if event.key == pygame.K_ESCAPE:
                endGame = True
                break

            # AMB LA TECLA [R] ES NETEJA LA MATRIU
            if event.key == pygame.K_r:
                iteration = 0
                gameState = np.zeros((nxC, nyC))
                newGameState = np.zeros((nxC, nyC))
                pauseExec = True
            else:
                # AMB QUALSEVOL ALTRE TECLA ES PAUSA/REPREN EL JOC
                pauseExec = not pauseExec

        # DETECCIÓ CLICK RATOLÍ
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:

            # EL CLICK DE LA RODETA PAUSA EL JOC
            if mouseClick[1]:
                pauseExec = not pauseExec
            else:

                # OBTENIM LES CORDENADES DEL RATOLÍ
                posX, posY, = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

                # EL CLICK DRET I ESQUERRA PERMUTEN ENTRE VIDA O MORT
                newGameState[celX, celY] = not gameState[celX, celY]

    if not pauseExec:
        iteration += 1

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                # CÀLCUL DE CEL·LULES VEÏNES PROPERES
                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # NORMA 1 -> Una cel·lula morta amb 3 cel·lules veïnes vives, reviu
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # NORMA 2 -> Una cel·lula viva amb menys de 2 o més de 3 cel·lules veïnes, mor
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # INCREMENTEM LA POBLACIÓ
            if gameState[x, y] == 1:
                population += 1

            # CREEM ELS POLIGONS DE LES CEL·LULES
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pauseExec:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # ACTUALITZEM EL TÍTOL DE LA FINESTRA
    title = f"El joc de la vida - @pribaqnet - Població: {population} - Interaccions: {iteration}"
    if pauseExec:
        title += " - [PAUSAT]"
    pygame.display.set_caption(title)

    # Actualizo gameState
    gameState = np.copy(newGameState)

    # Muestro y actualizo los fotogramas en cada iteración del bucle principal
    pygame.display.flip()

print("Joc finalitzat - @pribaqnet")
