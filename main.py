# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:14:18 2019

@author: SARREGUEMINES
"""

import random, sys, copy, os, pygame
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 900 # width of the program's window, in pixels
WINHEIGHT = 800 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

BLUE = (0,80,255)
WHITE  = (255, 255, 255)
BLACK = (0,0,0)


def main():
    global IMAGES_DICT, FPSCLOCK, gameDisplay
    
    # Pygame initialization and basic set up of the global variables.
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    
    #création de la fenêtre
#    gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
    gameDisplay = pygame.display.set_mode((WINWIDTH, WINHEIGHT),pygame.RESIZABLE)
    
    #titre de la fenetre
    pygame.display.set_caption('La Mine Hantée')
    
    #dictionnaire contenant l'ensemble des images du jeu
    IMAGES_DICT = {'titre': pygame.image.load('images/ecran_titre/titre.png'),
                   'bouton_nouv_jeu':pygame.image.load('images/ecran_titre/bouton_nouv_jeu.png'),
                   'bouton_nouv_jeu_hover':pygame.image.load('images/ecran_titre/bouton_nouv_jeu_bright.png'),
                   'bouton_reprendre':pygame.image.load('images/ecran_titre/bouton_reprendre.png'),
                   'bouton_reprendre_hover':pygame.image.load('images/ecran_titre/bouton_reprendre_bright.png'),
                   'bouton_quitter':pygame.image.load('images/ecran_titre/bouton_quitter.png'),
                   'bouton_quitter_hover':pygame.image.load('images/ecran_titre/bouton_quitter_bright.png'),
                   }
    
    affiche_accueil()
    
def affiche_accueil():
    
    gameDisplay.fill(BLACK)
    
    #affichage du titre
    titreRect = IMAGES_DICT['titre'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4))
    gameDisplay.blit(IMAGES_DICT['titre'], titreRect)
    
    #initilisation des variables pour les boutons
    bouton_nouveau_jeuRect = IMAGES_DICT['bouton_nouv_jeu'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4+150))
    bouton_nouveau_jeu_hoverRect = IMAGES_DICT['bouton_nouv_jeu_hover'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4+150))
    bouton_reprendreRect = IMAGES_DICT['bouton_reprendre'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4+250))
    bouton_reprendre_hoverRect = IMAGES_DICT['bouton_reprendre_hover'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4+250))
    bouton_quitterRect = IMAGES_DICT['bouton_quitter'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4+350))
    bouton_quitter_hoverRect = IMAGES_DICT['bouton_quitter_hover'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4+350))

    
    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.
        
        mouse = pygame.mouse.get_pos()

        #mise en place de l'affichage et de la surbrillance des boutons
        if bouton_nouveau_jeuRect.x+bouton_nouveau_jeuRect.width > mouse[0] > bouton_nouveau_jeuRect.x and bouton_nouveau_jeuRect.y+bouton_nouveau_jeuRect.height > mouse[1] > bouton_nouveau_jeuRect.y:
            gameDisplay.blit(IMAGES_DICT['bouton_nouv_jeu_hover'],bouton_nouveau_jeu_hoverRect)
        else:
            gameDisplay.blit(IMAGES_DICT['bouton_nouv_jeu'],bouton_nouveau_jeuRect)
        
        if bouton_reprendreRect.x+bouton_reprendreRect.width > mouse[0] > bouton_reprendreRect.x and bouton_reprendreRect.y+bouton_reprendreRect.height > mouse[1] > bouton_reprendreRect.y:
            gameDisplay.blit(IMAGES_DICT['bouton_reprendre_hover'],bouton_reprendre_hoverRect)
        else:
            gameDisplay.blit(IMAGES_DICT['bouton_reprendre'],bouton_reprendreRect)
            
        if bouton_quitterRect.x+bouton_quitterRect.width > mouse[0] > bouton_quitterRect.x and bouton_quitterRect.y+bouton_quitterRect.height > mouse[1] > bouton_quitterRect.y:
            gameDisplay.blit(IMAGES_DICT['bouton_quitter_hover'],bouton_quitter_hoverRect)
        else:
            gameDisplay.blit(IMAGES_DICT['bouton_quitter'],bouton_quitterRect)

        # Display the gameDisplay contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()

def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()