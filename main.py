# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:14:18 2019

@author: SARREGUEMINES
"""

import random, sys, copy, os, pygame
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 1100 # width of the program's window, in pixels
WINHEIGHT = 800 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

BLUE = (0,80,255)
WHITE = (255, 255, 255)
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
                   #########images de l'écran du choix des paramètres du nouveau jeu#############
                   'choix_nouv_jeu':pygame.image.load('images/init_jeu/Nouveau jeu.png'),
                   'choix_dimensions':pygame.image.load('images/init_jeu/Dimensions du plateau.png'),
                   'choix_dim7':pygame.image.load('images/init_jeu/bouton_7.png'),
                   'choix_dim7_grey':pygame.image.load('images/init_jeu/bouton_7_grey.png'),
                   'choix_dim9':pygame.image.load('images/init_jeu/bouton_9.png'),
                   'choix_dim9_grey':pygame.image.load('images/init_jeu/bouton_9_grey.png'),
                   'choix_j1':pygame.image.load('images/init_jeu/Joueur 1.png'),
                   'choix_j2':pygame.image.load('images/init_jeu/Joueur 2.png'),
                   'choix_j3':pygame.image.load('images/init_jeu/Joueur 3.png'),
                   'choix_j4':pygame.image.load('images/init_jeu/Joueur 4.png'),
                   'choix_hum':pygame.image.load('images/init_jeu/bouton_hum.png'),
                   'choix_hum_grey':pygame.image.load('images/init_jeu/bouton_hum_grey.png'),
                   'choix_ordi':pygame.image.load('images/init_jeu/bouton_ordi.png'),
                   'choix_ordi_grey':pygame.image.load('images/init_jeu/bouton_ordi_grey.png'),
                   'choix_ajouter_joueur':pygame.image.load('images/init_jeu/bouton_ajoute.png'),
                   'choix_ajouter_joueur_dis':pygame.image.load('images/init_jeu/bouton_ajoute_disabled.png'),
                   'choix_retirer_joueur':pygame.image.load('images/init_jeu/bouton_retire.png'),
                   'choix_retirer_joueur_dis':pygame.image.load('images/init_jeu/bouton_retire_disabled.png'),
                   'choix_valider':pygame.image.load('images/init_jeu/bouton_valider.png'),
                   }
    
    a = affiche_accueil()
    print(a)
    return terminate()
    
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

    mouse = pygame.mouse.get_pos()
    
    while True: # Main loop for the start screen.
        
        mouse = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()

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
        
        for event in pygame.event.get():
            if clic[0] == 1 and bouton_nouveau_jeuRect.x+bouton_nouveau_jeuRect.width > mouse[0] > bouton_nouveau_jeuRect.x and bouton_nouveau_jeuRect.y+bouton_nouveau_jeuRect.height > mouse[1] > bouton_nouveau_jeuRect.y:
                return init_jeu()
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            elif clic[0] == 1 and bouton_quitterRect.x+bouton_quitterRect.width > mouse[0] > bouton_quitterRect.x and bouton_quitterRect.y+bouton_quitterRect.height > mouse[1] > bouton_quitterRect.y:
                terminate()
                return # user has pressed a key, so return.
        

        # Display the gameDisplay contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()

def init_jeu():
    dimension = 7
    nb_joueurs = 2
    joueur1 = 1
    joueur2 = 1
    joueur3 = 0
    joueur4 = 0
    
    #Initalisation des variables images pour les boutons
    bouton_dim7 = IMAGES_DICT['choix_dim7']
    bouton_dim9 = IMAGES_DICT['choix_dim9_grey']
    bouton_j1_hum = IMAGES_DICT['choix_hum']
    bouton_j1_ordi = IMAGES_DICT['choix_ordi_grey']
    bouton_j2_hum = IMAGES_DICT['choix_hum'] 
    bouton_j2_ordi = IMAGES_DICT['choix_ordi_grey'] 
    bouton_j3_hum = IMAGES_DICT['choix_hum'] 
    bouton_j3_ordi = IMAGES_DICT['choix_ordi_grey']
    bouton_j4_hum = IMAGES_DICT['choix_hum'] 
    bouton_j4_ordi = IMAGES_DICT['choix_ordi_grey']
    
    bouton_ajoute_joueur = IMAGES_DICT['choix_ajouter_joueur']
    bouton_retire_joueur = IMAGES_DICT['choix_retirer_joueur_dis'] 
    
    bouton_valider = IMAGES_DICT['choix_valider'] 

    while True:
        gameDisplay.fill(BLACK)
        
        #Récupération des events position de la souris et clic de la souris
        mouse = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()
        
        #Initialisation des surfaces liées aux titres des boutons
        titreRect = IMAGES_DICT['choix_nouv_jeu'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4))
        dimRect = IMAGES_DICT['choix_dimensions'].get_rect(topright=(HALF_WINWIDTH, HALF_WINHEIGHT/2))
        j1Rect = IMAGES_DICT['choix_j1'].get_rect(topright=(HALF_WINWIDTH, HALF_WINHEIGHT/2+75))
        j2Rect = IMAGES_DICT['choix_j2'].get_rect(topright=(HALF_WINWIDTH, HALF_WINHEIGHT/2+75*2))
        j3Rect = IMAGES_DICT['choix_j3'].get_rect(topright=(HALF_WINWIDTH, HALF_WINHEIGHT/2+75*3))
        j4Rect = IMAGES_DICT['choix_j4'].get_rect(topright=(HALF_WINWIDTH, HALF_WINHEIGHT/2+75*4))
        
        #Changement des images des boutons ajouter/retirer des joueurs       
        if nb_joueurs == 2: 
            bouton_retire_joueur = IMAGES_DICT['choix_retirer_joueur_dis']
        else:
            bouton_retire_joueur = IMAGES_DICT['choix_retirer_joueur']
            
        if nb_joueurs == 4:
            bouton_ajoute_joueur = IMAGES_DICT['choix_ajouter_joueur_dis']
        else:
             bouton_ajoute_joueur = IMAGES_DICT['choix_ajouter_joueur']
        

        #Initilisation des surfaces boutons humain/ordi
        boutonj1humRect = bouton_j1_hum.get_rect(topright=(HALF_WINWIDTH+dimRect.width, HALF_WINHEIGHT/2+75))
        boutonj1ordiRect = bouton_j1_ordi.get_rect(topright=(HALF_WINWIDTH+dimRect.width+boutonj1humRect.width+10, HALF_WINHEIGHT/2+75))
        boutonj2humRect = bouton_j2_hum.get_rect(topright=(HALF_WINWIDTH+dimRect.width, HALF_WINHEIGHT/2+75*2))
        boutonj2ordiRect = bouton_j2_ordi.get_rect(topright=(HALF_WINWIDTH+dimRect.width+boutonj2humRect.width+10, HALF_WINHEIGHT/2+75*2))
        boutonj3humRect = bouton_j3_hum.get_rect(topright=(HALF_WINWIDTH+dimRect.width, HALF_WINHEIGHT/2+75*3))
        boutonj3ordiRect = bouton_j3_ordi.get_rect(topright=(HALF_WINWIDTH+dimRect.width+boutonj3humRect.width+10, HALF_WINHEIGHT/2+75*3))  
        boutonj4humRect = bouton_j4_hum.get_rect(topright=(HALF_WINWIDTH+dimRect.width, HALF_WINHEIGHT/2+75*4))
        boutonj4ordiRect = bouton_j4_ordi.get_rect(topright=(HALF_WINWIDTH+dimRect.width+boutonj4humRect.width+10, HALF_WINHEIGHT/2+75*4))
        #Initialisatioon de la surface boutons dimension
        dim7Rect = bouton_dim7.get_rect(topright=(HALF_WINWIDTH+dimRect.width, HALF_WINHEIGHT/2))
        dim9Rect = bouton_dim9.get_rect(topright=(HALF_WINWIDTH+dim7Rect.width+dimRect.width+10, HALF_WINHEIGHT/2))                        
        #Initialisation des surfaces boutons de gestion du nombre de joueurss
        ajoutJoueurRect =  bouton_ajoute_joueur.get_rect(topright=(HALF_WINWIDTH,WINHEIGHT-150))
        retireJoueurRect = bouton_retire_joueur.get_rect(topright=(HALF_WINWIDTH+ajoutJoueurRect.width+10,WINHEIGHT-150))
        #Initialisation de la surface valider
        validerRect = bouton_valider.get_rect(topright=(HALF_WINWIDTH+2*(ajoutJoueurRect.width+10),WINHEIGHT-150))
        
        #Affichage des titres
        gameDisplay.blit(IMAGES_DICT['choix_nouv_jeu'], titreRect)
        gameDisplay.blit(IMAGES_DICT['choix_dimensions'], dimRect)
        gameDisplay.blit(IMAGES_DICT['choix_j1'], j1Rect)
        gameDisplay.blit(IMAGES_DICT['choix_j2'], j2Rect)
        #Affichage des boutons pour le choix de la dimension
        gameDisplay.blit(bouton_dim7,dim7Rect)
        gameDisplay.blit(bouton_dim9,dim9Rect)                   
        #Affichage des choix humain ou ordi pour le joueur 1
        gameDisplay.blit(bouton_j1_hum,boutonj1humRect)
        gameDisplay.blit(bouton_j1_ordi,boutonj1ordiRect)
        #Affichage des choix humain ou ordi pour le joueur 2
        gameDisplay.blit(bouton_j2_hum,boutonj2humRect)
        gameDisplay.blit(bouton_j2_ordi,boutonj2ordiRect)
        #Affichage des boutons ajouter/retirer des joueurs
        gameDisplay.blit(bouton_ajoute_joueur,ajoutJoueurRect)
        gameDisplay.blit(bouton_retire_joueur,retireJoueurRect)
        #Affichage du bouton valider
        gameDisplay.blit(bouton_valider,validerRect)


        #Affichage conditionnel des joueurs 3 et4 
        if nb_joueurs >= 3:
            #Affichage du titre j3
            gameDisplay.blit(IMAGES_DICT['choix_j3'], j3Rect)
            #Affichage des choix humain ou ordi pour le joueur 3
            gameDisplay.blit(bouton_j3_hum,boutonj3humRect)
            gameDisplay.blit(bouton_j3_ordi,boutonj3ordiRect)  
            
        if nb_joueurs == 4:
            #affichage du titre j4
            gameDisplay.blit(IMAGES_DICT['choix_j4'], j4Rect)
            #affichage des choix humain ou ordi pour le joueur 4
            gameDisplay.blit(bouton_j4_hum,boutonj4humRect)
            gameDisplay.blit(bouton_j4_ordi,boutonj4ordiRect)
        
        for event in pygame.event.get():
            #Events boutons du choix de dimensions
            if dim9Rect.x+dim9Rect.width > mouse[0] > dim9Rect.x and dim9Rect.y+dim9Rect.height> mouse[1] >dim9Rect.y and event.type == MOUSEBUTTONUP:
                if bouton_dim9 ==  IMAGES_DICT['choix_dim9_grey']:
                    bouton_dim9 = IMAGES_DICT['choix_dim9']
                    bouton_dim7 = IMAGES_DICT['choix_dim7_grey']
                    dimension = 9
            if dim7Rect.x+dim9Rect.width > mouse[0] > dim7Rect.x and dim9Rect.y+dim7Rect.height> mouse[1] >dim7Rect.y and event.type == MOUSEBUTTONUP:
                if bouton_dim7 ==  IMAGES_DICT['choix_dim7_grey']:
                    bouton_dim7 = IMAGES_DICT['choix_dim7']
                    bouton_dim9 = IMAGES_DICT['choix_dim9_grey']
                    dimension = 7
                    
            #Events choix humain/ordi joueur 1
            if boutonj1humRect.width+boutonj1humRect.x > mouse[0] > boutonj1humRect.x and boutonj1humRect.y+ boutonj1humRect.height> mouse[1] > boutonj1humRect.y and event.type == MOUSEBUTTONUP:
                if bouton_j1_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j1_hum = IMAGES_DICT['choix_hum']
                    bouton_j1_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur1 = 1
            if boutonj1ordiRect.width+boutonj1ordiRect.x > mouse[0] > boutonj1ordiRect.x and boutonj1ordiRect.y+ boutonj1ordiRect.height> mouse[1] > boutonj1ordiRect.y and event.type == MOUSEBUTTONUP:
                if bouton_j1_ordi ==  IMAGES_DICT['choix_ordi_grey']:
                    bouton_j1_ordi = IMAGES_DICT['choix_ordi']
                    bouton_j1_hum =  IMAGES_DICT['choix_hum_grey']
                    joueur1 = 2
           
            #clicabilité joueur 2
            if boutonj2humRect.width+boutonj2humRect.x > mouse[0] > boutonj2humRect.x and boutonj2humRect.y+ boutonj2humRect.height> mouse[1] > boutonj2humRect.y and clic[0] == 1:
                if bouton_j2_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j2_hum = IMAGES_DICT['choix_hum']
                    bouton_j2_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur2 = 1
            if boutonj2ordiRect.width+boutonj2ordiRect.x > mouse[0] > boutonj2ordiRect.x and boutonj2ordiRect.y+ boutonj2ordiRect.height> mouse[1] > boutonj2ordiRect.y and clic[0] == 1:
                if bouton_j2_ordi ==  IMAGES_DICT['choix_ordi_grey']:
                    bouton_j2_ordi = IMAGES_DICT['choix_ordi']
                    bouton_j2_hum =  IMAGES_DICT['choix_hum_grey']
                    joueur2 = 2

            #Event joueur 3
            if boutonj3humRect.width+boutonj3humRect.x > mouse[0] > boutonj3humRect.x and boutonj3humRect.y+ boutonj3humRect.height> mouse[1] > boutonj3humRect.y and event.type == MOUSEBUTTONUP and nb_joueurs >= 3:
                if bouton_j3_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j3_hum = IMAGES_DICT['choix_hum']
                    bouton_j3_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur3 = 1
            if boutonj3ordiRect.width+boutonj3ordiRect.x > mouse[0] > boutonj3ordiRect.x and boutonj3ordiRect.y+ boutonj3ordiRect.height> mouse[1] > boutonj3ordiRect.y and event.type == MOUSEBUTTONUP and nb_joueurs >= 3:
                if bouton_j3_ordi ==  IMAGES_DICT['choix_ordi_grey']:
                    bouton_j3_ordi = IMAGES_DICT['choix_ordi']
                    bouton_j3_hum =  IMAGES_DICT['choix_hum_grey']
                    joueur2 = 2
            
            #Events joueur 4
            if boutonj4humRect.width+boutonj4humRect.x > mouse[0] > boutonj4humRect.x and boutonj4humRect.y+ boutonj4humRect.height> mouse[1] > boutonj4humRect.y and event.type == MOUSEBUTTONUP and nb_joueurs == 4:
                if bouton_j4_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j4_hum = IMAGES_DICT['choix_hum']
                    bouton_j4_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur4 = 'humain'
            if boutonj4ordiRect.width+boutonj4ordiRect.x > mouse[0] > boutonj4ordiRect.x and boutonj4ordiRect.y+ boutonj4ordiRect.height> mouse[1] > boutonj4ordiRect.y and event.type == MOUSEBUTTONUP and nb_joueurs == 4:
                if bouton_j4_ordi ==  IMAGES_DICT['choix_ordi_grey']:
                    bouton_j4_ordi = IMAGES_DICT['choix_ordi']
                    bouton_j4_hum =  IMAGES_DICT['choix_hum_grey']
                    joueur4 = 'humain'
            
            #Gestion du nombre de joueurs
            if ajoutJoueurRect.width + ajoutJoueurRect.x > mouse[0] > ajoutJoueurRect.x and ajoutJoueurRect.y+ ajoutJoueurRect.height> mouse[1] > ajoutJoueurRect.y and event.type == MOUSEBUTTONUP and nb_joueurs != 4:
                nb_joueurs += 1
                print('nb',nb_joueurs)
            if retireJoueurRect.width+retireJoueurRect.x > mouse[0] > retireJoueurRect.x and retireJoueurRect.y+ retireJoueurRect.height> mouse[1] > retireJoueurRect.y and event.type == MOUSEBUTTONUP and nb_joueurs != 2:
                nb_joueurs -= 1
                print('nbm',nb_joueurs)
            
            #Gestion du bouton valider
            if validerRect.width+validerRect.x > mouse[0] > validerRect.x and validerRect.y+ validerRect.height> mouse[1] > validerRect.y and event.type == MOUSEBUTTONUP:
                print('cest ok')
                return dimension, joueur1, joueur2, joueur3, joueur4
                
                
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                    return # user has pressed a key, so return.
    
        
        pygame.display.update()
        FPSCLOCK.tick()
    

def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()