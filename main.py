# -*- coding: utf-8 -*-
"""
Fichier principal du jeu. Contenu :
    
main : fonction principale du jeu
affiche_accueil : appelée au début de main, affiche l'écran d'accueil du jeu
init_jeu : appelée dans main SI l'utilisateur clique sur nouveau jeu dans la fonction affiche_accueil. Affiche l'écran d'initilisation d'un nouveau jeu
initialisation_partie: en fonction des paramètres choisie par les joueurs, crée le plateau, initialisa les joueurs et leur mission
boucle_deplacement : appelée dans main pendant le jeu, pour gérer le déplacement du joueur_actif. 
terminate : appelée lorque le joueur appuie sur échap. Ferme la fenetre de jeu.
"""


import random, sys, copy, os, pygame
from random import shuffle
from pygame.locals import *
import classes as cl

FPS = 30 # frames per second to update the screen
WINWIDTH = 1100 # width of the program's window, in pixels
WINHEIGHT = 800 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

BLUE = (0,80,255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

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

def main():
    '''Fonction principale du jeu
    '''
    global IMAGES_DICT, FPSCLOCK, gameDisplay
    
    # Pygame initialization and basic set up of the global variables.
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    
    #création de la fenêtre
#   gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
    gameDisplay = pygame.display.set_mode((WINWIDTH, WINHEIGHT),pygame.RESIZABLE) 
    #titre de la fenetre
    pygame.display.set_caption('La Mine Hantée')
    

    #appel de la fonction affichant l'écran d'accueil
    choix_accueil = affiche_accueil() #choix_accueil prend la valeur retournée par affiche_accueil(), soit 'nouveau_jeu', soit 'reprendre_jeu'
    
    #gestion du choix fait par l'utilisateur sur l'écran d'accueil ('nouveau_jeu','reprendre_jeu' ou 'quitter')
    if choix_accueil == 'nouveau_jeu':
        parametres_jeu = init_jeu() #parametres_jeu prend la valeur retournée par init_jeu, un tuple d'int contenant (dimension, joueur1,joueur2,joueur3,joueur4)
        print(parametres_jeu)
        #Création du plateau sur lequel on va jouer
        plateau, dico_joueurs = initialisation_partie(parametres_jeu)
    elif choix_accueil == 'reprendre_jeu':
        #/!\ à ajouter : doit mettre la fonction appelant l'écran du choix des parties sauvegardées
        pass
    elif choix_accueil == 'quitter':
        terminate()       
    
    print(plateau, dico_joueurs)
    """
    À ce stade on a créé le plateau et les joueurs, contenus dans la variable plateau et dico_joueur
    plateau : contient les cartes
    dico_joueurs : contient les objets Chasseurs
    """
#
#    while True:
#        print("joueur{} est le joueur actif".format())
#        print("J{} est le joueur actif")

    return terminate()
    
def affiche_accueil():
    '''Fonction permettant l'affichage de l'écran d'accueil du jeu, ou on peut faire les choix suivants : nouveau jeu, reprendre, quitter
    -->: 'nouveau_jeu', 'reprendre_jeu' : c'est 2 valeurs sont utilisées dans main() pour appeler les fonctions adéquates
    '''
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
        
        mouse = pygame.mouse.get_pos() #recupere la position de la souris
        clic = pygame.mouse.get_pressed() #recupere l'évenement clic de la souris (clic[0] = clic gauche, clic[1] = clic droit)

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
                return 'nouveau_jeu'
            if event.type == pygame.QUIT:
                return 'quitter'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif clic[0] == 1 and bouton_quitterRect.x+bouton_quitterRect.width > mouse[0] > bouton_quitterRect.x and bouton_quitterRect.y+bouton_quitterRect.height > mouse[1] > bouton_quitterRect.y:
                terminate()
                return # user has pressed a key, so return.
        

        # Display the gameDisplay contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()

def init_jeu():
    '''Fonction gérant l'écran permettant d'initialiser les pramètres du nouveau jeu : dimension, nb de joueurs, humain ou ordi
    -->: dictionnaire contenant : dimension(int), nb_joueurs (in), joueur 1(int), joueur 2(int), joueur 3(int), joueur4(int)
    dimension : dimension du plateau
    joueur x(int) : 0 si ce joueur n'existe pas (2 ou 3 joueurs), 1 si c'est un humain, 2 si c'est une IA
    '''
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
            if dim9Rect.x+dim9Rect.width > mouse[0] > dim9Rect.x and dim9Rect.y+dim9Rect.height> mouse[1] >dim9Rect.y and event.type == pygame.MOUSEBUTTONUP:
                if bouton_dim9 ==  IMAGES_DICT['choix_dim9_grey']:
                    bouton_dim9 = IMAGES_DICT['choix_dim9']
                    bouton_dim7 = IMAGES_DICT['choix_dim7_grey']
                    dimension = 9
            if dim7Rect.x+dim9Rect.width > mouse[0] > dim7Rect.x and dim9Rect.y+dim7Rect.height> mouse[1] >dim7Rect.y and event.type == pygame.MOUSEBUTTONUP:
                if bouton_dim7 ==  IMAGES_DICT['choix_dim7_grey']:
                    bouton_dim7 = IMAGES_DICT['choix_dim7']
                    bouton_dim9 = IMAGES_DICT['choix_dim9_grey']
                    dimension = 7
                    
            #Events choix humain/ordi joueur 1
            if boutonj1humRect.width+boutonj1humRect.x > mouse[0] > boutonj1humRect.x and boutonj1humRect.y+ boutonj1humRect.height> mouse[1] > boutonj1humRect.y and event.type == pygame.MOUSEBUTTONUP:
                if bouton_j1_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j1_hum = IMAGES_DICT['choix_hum']
                    bouton_j1_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur1 = 1
            if boutonj1ordiRect.width+boutonj1ordiRect.x > mouse[0] > boutonj1ordiRect.x and boutonj1ordiRect.y+ boutonj1ordiRect.height> mouse[1] > boutonj1ordiRect.y and event.type == pygame.MOUSEBUTTONUP:
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
            if boutonj3humRect.width+boutonj3humRect.x > mouse[0] > boutonj3humRect.x and boutonj3humRect.y+ boutonj3humRect.height> mouse[1] > boutonj3humRect.y and event.type == pygame.MOUSEBUTTONUP and nb_joueurs >= 3:
                if bouton_j3_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j3_hum = IMAGES_DICT['choix_hum']
                    bouton_j3_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur3 = 1
            if boutonj3ordiRect.width+boutonj3ordiRect.x > mouse[0] > boutonj3ordiRect.x and boutonj3ordiRect.y+ boutonj3ordiRect.height> mouse[1] > boutonj3ordiRect.y and event.type == pygame.MOUSEBUTTONUP and nb_joueurs >= 3:
                if bouton_j3_ordi ==  IMAGES_DICT['choix_ordi_grey']:
                    bouton_j3_ordi = IMAGES_DICT['choix_ordi']
                    bouton_j3_hum =  IMAGES_DICT['choix_hum_grey']
                    joueur3 = 2
            
            #Events joueur 4
            if boutonj4humRect.width+boutonj4humRect.x > mouse[0] > boutonj4humRect.x and boutonj4humRect.y+ boutonj4humRect.height> mouse[1] > boutonj4humRect.y and event.type == pygame.MOUSEBUTTONUP and nb_joueurs == 4:
                if bouton_j4_hum ==  IMAGES_DICT['choix_hum_grey']:
                    bouton_j4_hum = IMAGES_DICT['choix_hum']
                    bouton_j4_ordi = IMAGES_DICT['choix_ordi_grey']
                    joueur4 = 'humain'
            if boutonj4ordiRect.width+boutonj4ordiRect.x > mouse[0] > boutonj4ordiRect.x and boutonj4ordiRect.y+ boutonj4ordiRect.height> mouse[1] > boutonj4ordiRect.y and event.type == pygame.MOUSEBUTTONUP and nb_joueurs == 4:
                if bouton_j4_ordi ==  IMAGES_DICT['choix_ordi_grey']:
                    bouton_j4_ordi = IMAGES_DICT['choix_ordi']
                    bouton_j4_hum =  IMAGES_DICT['choix_hum_grey']
                    joueur4 = 'humain'
            
            #Gestion du nombre de joueurs
            if ajoutJoueurRect.width + ajoutJoueurRect.x > mouse[0] > ajoutJoueurRect.x and ajoutJoueurRect.y+ ajoutJoueurRect.height> mouse[1] > ajoutJoueurRect.y and event.type == pygame.MOUSEBUTTONUP and nb_joueurs != 4:
                nb_joueurs += 1
                print('nb',nb_joueurs)
            if retireJoueurRect.width+retireJoueurRect.x > mouse[0] > retireJoueurRect.x and retireJoueurRect.y+ retireJoueurRect.height> mouse[1] > retireJoueurRect.y and event.type == pygame.MOUSEBUTTONUP and nb_joueurs != 2:
                nb_joueurs -= 1
                print('nbm',nb_joueurs)
            
            #Gestion du bouton valider
            if validerRect.width+validerRect.x > mouse[0] > validerRect.x and validerRect.y+ validerRect.height> mouse[1] > validerRect.y and event.type == pygame.MOUSEBUTTONUP:
                print('dim,j1,j2,j3,j4:',dimension, joueur1, joueur2, joueur3, joueur4)
                return {'dimension':dimension, 'nb_joueurs':nb_joueurs,'joueur1': joueur1, 'joueur2':joueur2, 'joueur3':joueur3, 'joueur4':joueur4}
                
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                    return # user has pressed a key, so return.
    
        
        pygame.display.update()
        FPSCLOCK.tick()
 
def boucle_deplacement(plateau):
    '''
    Fonction permettant le déplacement du joueur actif pendant son tour
    Parametres : plateau : Plateau
    -->: None
    '''
    liste_deplacement = [] #futur liste des cartes par lesquelles passe ce déplacement
    deplacement_valide = True #le deplacement est autorisée par les régles
    x_init, y_init = plateau.joueur_actif.position #position initiale du joueur actif
    x, y = x_init, y_init #position du joueur au fur et à mesure du déplacement
    carte_depart = plateau.matrice[x_init, y_init] #carte de départ sur laquelle le joueur actif se situe
    carte_actuelle = carte_depart #dernière carte choisie pendant le déplacement

    while True:
        #gestion des évenements joueurs lors du déplacement
        for event in pygame.event.get():
            #evenements de type touche pressée
            if event.type == pygame.KEYDOWN:
                #le joueur appuie sur la flèche haut
                if event.key == pygame.K_UP:
                    if plateau.deplacement_possible(plateau.joueur_actif,'haut'):
                        #la carte en haut de la carte actuelle est ajoutée liste des cartes successives du déplacement
                        liste_deplacement += [carte_a_cote[carte_actuelle]]
                        print(liste_deplacement)
                        print("Player pressed up!")
                #le joueur appuie sur la flèche gauche                
                elif event.key == pygame.K_LEFT:
                    if plateau.deplacement_possible(plateau.joueur_actif,'gauche'):
                        #la carte à gauche de la carte actuelle est ajoutée liste des cartes successives du déplacement
                        liste_deplacement += [carte_a_cote[carte_actuelle]]
                        print(liste_deplacement)
                    print("Player pressed left!")
                #le joueur appuie sur la flèche bas                    
                elif event.key == pygame.K_DOWN:
                    if plateau.deplacement_possible(plateau.joueur_actif,'bas'):
                        #la carte en bas de la carte actuelle est ajoutée liste des cartes successives du déplacement
                        liste_deplacement += [carte_a_cote[carte_actuelle]]
                        print(liste_deplacement)
                    print("Player pressed down!")
                #le joueur appuie sur la flèche droite
                elif event.key == pygame.K_RIGHT:
                    if plateau.deplacement_possible(plateau.joueur_actif,'droite'):
                        #la carte à droite de la carte actuelle est ajoutée liste des cartes successives du déplacement
                        liste_deplacement += [carte_a_cote[carte_actuelle]]
                        print(liste_deplacement)
                    print("Player pressed right!")
                #avorte la tentative de déplacement si on appuie sur échap
                elif event.key == pygame.K_ESCAPE:
                    return
        #màj de l'écran
        pygame.display.update()
        FPSCLOCK.tick()

def initialisation_partie(parametres_jeu):
    """Fonction initialisant les objets d'un jeu.
    Arguments:
        dico_parametres {dict} -- Contient les valeurs de dimension, nb_joueur, et type de joueur
    
    Returns:
        Plateau, dict -- plateau de jeu, dictionnaire contenant les objets type Chasseur
    """

    ###Initialisation du plateau
    plateau = cl.Plateau(parametres_jeu['dimension'],parametres_jeu['nb_joueurs'])
    dico_joueurs = {}

    ###Initialisation des chasseurs et de leurs missions
    for i in range(1,parametres_jeu['nb_joueurs']+1):
        if parametres_jeu['joueur'+str(i)] == 1: #le ieme joueurs est humain
            dico_joueurs[i] = cl.Chasseur(i) #on crée un objet Chasseur ajouté au dictionnaire des joueurs
        elif parametres_jeu['joueur'+str(i)] == 2: #le ieme joueurs est une IA
            pass
    
    ###Initialisation des missions des joueurs
    fantomes = [x for x in range(1,22)] #cette liste contient les fantomes disponibles
    shuffle(fantomes) #on la mélange
    for j in dico_joueurs.values(): #parcourt les objets Chasseur contenus dans le dictionnaire
        for x in range(3):
            j.mission.append(fantomes[0]) #on ajoute à la liste mission du joueur le premier objet de la liste mélangée
            fantomes.remove(fantomes[0]) #on retire ensuite le premier objet de la liste

    ###Placement des joueurs sur le plateau si dim = 7
    if parametres_jeu['dimension'] == 7:
        dico_joueurs[1].position, dico_joueurs[2].position = [2,2], [4,4]
        if  parametres_jeu['nb_joueurs'] == 3:
            dico_joueurs[3].position = [2,4]
        if  parametres_jeu['nb_joueurs'] == 4:
            dico_joueurs[4].position = [4,2]

    return plateau, dico_joueurs

def terminate():
    '''
    Fonction qui ferme la fenetre
    '''
    pygame.quit()
#    sys.exit()
    
if __name__ == '__main__':
    main()
