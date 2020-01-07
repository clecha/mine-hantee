# -*- coding: utf-8 -*-
"""
CONTENU
variables globales du jeu
dictionnaire des images du jeu
"""
from pygame.locals import *
import pygame

FPS = 30 # frames per second to update the screen
WINWIDTH = 1200 # width of the program's window, in pixels
WINHEIGHT = 700 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)


BLUE = (0,80,255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREY=(50,50,50)
RED = (139,0,0)

espace = 500
pixel_case=int(WINHEIGHT/7)

FPSCLOCK = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((WINWIDTH+15, WINHEIGHT+15),pygame.RESIZABLE)

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
			   #########images plateau de jeu##########
			 'pepite': pygame.image.load('images/persos/pepite.png'),
			 'chasseur1': pygame.image.load('images/persos/chasseur1.png'),
			 'chasseur2': pygame.image.load('images/persos/chasseur2.png'),
			 'chasseur3': pygame.image.load('images/persos/chasseur3.png'),
			 'chasseur4': pygame.image.load('images/persos/chasseur4.png'),
			 'fantome': pygame.image.load('images/persos/fantome.png'),	
             'carte1' : pygame.image.load('images/cartes/type1.png').convert_alpha(),
             'carte2' : pygame.image.load('images/cartes/type2.png').convert_alpha(),
             'carte3' : pygame.image.load('images/cartes/type3.png').convert_alpha(),	
             'carte1_dark' : pygame.image.load('images/cartes/type1_dark.png').convert_alpha(),
             'carte2_dark' : pygame.image.load('images/cartes/type2_dark.png').convert_alpha(),
             'carte3_dark' : pygame.image.load('images/cartes/type3_dark.png').convert_alpha(),
             'carte1_bright' : pygame.image.load('images/cartes/type1_bright.png').convert_alpha(),
             'carte2_bright' : pygame.image.load('images/cartes/type2_bright.png').convert_alpha(),
             'carte3_bright' : pygame.image.load('images/cartes/type3_bright.png').convert_alpha(),
             'carte1_hover' : pygame.image.load('images/cartes/type1_hover.png').convert_alpha(),
             'carte2_hover' : pygame.image.load('images/cartes/type2_hover.png').convert_alpha(),
             'carte3_hover' : pygame.image.load('images/cartes/type3_hover.png').convert_alpha(),	
             'fleche1': pygame.image.load('images/plateau/fleche1.png'),
             'fleche2': pygame.image.load('images/plateau/fleche2.png'),
			 'sauvegarder_plateau':pygame.image.load('images/plateau/sauvegarder_plateau.png'),
			 #########images interface reprendre jeu##########
			 'titre_sauvegardes':pygame.image.load('images/choix_sauvegarde/titre_sauvegardes.png'),
			 'save1':pygame.image.load('images/choix_sauvegarde/save1.png'),
			 'save2':pygame.image.load('images/choix_sauvegarde/save2.png'),
			 'save3':pygame.image.load('images/choix_sauvegarde/save3.png'),
			 'save4':pygame.image.load('images/choix_sauvegarde/save4.png'),
			 'save_vide':pygame.image.load('images/choix_sauvegarde/save_vide.png'),
			 'reprendre':pygame.image.load('images/choix_sauvegarde/reprendre.png'),
			 'reprendre_bright':pygame.image.load('images/choix_sauvegarde/reprendre_bright.png'),
			 'save_vide_hover':pygame.image.load('images/choix_sauvegarde/save_vide_hover.png'),
			 'sauvegarder':pygame.image.load('images/choix_sauvegarde/sauvegarder.png'),
			 'sauvegarder_bright':pygame.image.load('images/choix_sauvegarde/sauvegarder_bright.png'),
			 'bouton_retour':pygame.image.load('images/choix_sauvegarde/retour.png'),
			 #########images interface classement##########
			 'titre_classement':pygame.image.load('images/classement/titre_classement.png'),
			 'big_chasseur1': pygame.image.load('images/classement/chasseur1.png'),
			 'big_chasseur2': pygame.image.load('images/classement/chasseur2.png'),
			 'big_chasseur3': pygame.image.load('images/classement/chasseur3.png'),
			 'big_chasseur4': pygame.image.load('images/classement/chasseur4.png'),
			 'titre_score': pygame.image.load('images/classement/titre_score.png'),
			 'couronne': pygame.image.load('images/classement/couronne.png'),
			 'bouton_retour_menu': pygame.image.load('images/classement/bouton_retour.png'),
			 'bouton_retour_menu_hover': pygame.image.load('images/classement/bouton_retour_hover.png'),
			   }

