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
from math import *
from variables import *
from affichage import *

def main():
	'''Fonction principale du jeu
	'''
	global IMAGES_DICT, FPSCLOCK, gameDisplay
	# Pygame initialization and basic set up of the global variables.
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	
	#création de la fenêtre
#	gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
	gameDisplay = pygame.display.set_mode((WINWIDTH, WINHEIGHT),pygame.RESIZABLE) 
	#titre de la fenetre
	pygame.display.set_caption('La Mine Hantée')
	
	#appel de la fonction affichant l'écran d'accueil
	choix_accueil = affiche_accueil() #choix_accueil prend la valeur retournée par affiche_accueil(), soit 'nouveau_jeu', soit 'reprendre_jeu'
	
	#gestion du choix fait par l'utilisateur sur l'écran d'accueil ('nouveau_jeu','reprendre_jeu' ou 'quitter')
	if choix_accueil == 'nouveau_jeu':
		parametres_jeu = init_jeu() #parametres_jeu prend la valeur retournée par init_jeu, un dictionnaire contenant (dimension, joueur1,joueur2,joueur3,joueur4,go)
		plateau = cl.Plateau(parametres_jeu['dimension'],parametres_jeu['nb_joueurs'])
		init_affichage_plateau(plateau)
	elif choix_accueil == 'reprendre_jeu':
		#/!\ à ajouter : doit mettre la fonction appelant l'écran du choix des parties sauvegardées
		terminate()
	elif choix_accueil == 'quitter':
		terminate()		  
	
	while True:
		
		actualisation_affichage_plateau(plateau)
	
	
	"""À ce stade on a créé le plateau et les joueurs, contenus dans la variable plateau et dico_joueur
	plateau : contient les cartes"""
	# while True:
	# 	print("joueur{} est le joueur actif".format())
	# 	print("J{} est le joueur actif")
	# 	plateau.joueur_actif = 1

	return terminate()
	


def boucle_deplacement(plateau):
	'''
	Fonction permettant d'enregistrer le déplacement potentiel du joueur actif pendant son tour, en retournant une liste de directions.
	Si le déplacement est validé, retourne deux listes qui seront utilisées pour faire bouger le joueur.
	Récupère les évenements boutons flèches, escape et enter. Création au fur et à mesure :
		1. liste_cartes : listes des objets Cartes du déplacement
		2. liste_mouvements : liste des mouvements du déplacement ('gauche','haut',...)
	Parametres : plateau : Plateau
	-->: liste_cartes, liste_mouvements
	'''
	liste_cartes = [] #futur liste des cartes par lesquelles passe ce déplacement
	liste_mouvements = [] #listes des directions du déplacements
	deplacement_valide = True #le deplacement est autorisée par les régles
	x_init, y_init = plateau.joueur_actif.position #position initiale du joueur actif
	x, y = x_init, y_init #position du joueur au fur et à mesure du déplacement
	carte_depart = plateau.matrice[x_init, y_init] #carte de départ sur laquelle le joueur actif se situe
	carte_actuelle = carte_depart #dernière carte choisie pendant le déplacement
	direction_opposee = {'haut':'bas','bas':'haut','gauche':'droite','droite':'gauche'}

	while True:
		#gestion des évenements joueurs lors du déplacement
		for event in pygame.event.get():
			#evenements de type touche pressée
			if event.type == pygame.KEYDOWN:
				
				#le joueur appuie sur la flèche haut
				if event.key == pygame.K_UP:
					#vérification que le déplacement est possible (absence de mur sur les deux cartes concernéees)
					if plateau.deplacement_possible(x, y,'haut')==True:
						if liste_mouvements[-1]!='bas': 
							#la carte en haut de la carte actuelle est ajoutée liste des cartes successives du déplacement
							liste_mouvements += ['haut']
							liste_cartes += [plateau.carte_a_cote('haut',x,y)]
							carte_actuelle = liste_cartes[-1]
						else: #si le mouvement consiste à revenir en arrière
							#on enlève le dernier mouvement de la liste des mouvements
							liste_mouvements.remove(liste_mouvements[-1])
							#on enlève la dernière carte de la liste des cartes
							liste_cartes.remove(liste_cartes[-1])
							#la carte actuelle devient la dernière carte 
							carte_actuelle = liste_cartes[-1]
					print("Player pressed up!")
					
				#le joueur appuie sur la flèche gauche				  
				elif event.key == pygame.K_LEFT:
					if plateau.deplacement_possible(x, y,'gauche'):
						if liste_mouvements[-1]!='droite':
							liste_mouvements += ['gauche']
							#la carte à gauche de la carte actuelle est ajoutée liste des cartes successives du déplacement
							liste_cartes += [plateau.carte_a_cote[carte_actuelle]]
							plateau.carte_a_cote[carte_actuelle]
						else:
							#on enlève le dernier mouvement de la liste des mouvements
							liste_mouvements.remove(liste_mouvements[-1])
							#on enlève la dernière carte de la liste des cartes
							liste_cartes.remove(liste_cartes[-1])
							#la carte actuelle devient la dernière carte 
							carte_actuelle = liste_cartes[-1]							
					print("Player pressed left!")
					
				#le joueur appuie sur la flèche bas					   
				elif event.key == pygame.K_DOWN:
					if plateau.deplacement_possible(x, y,'bas'):
						if liste_mouvements[-1] != 'haut':
							liste_mouvements += ['bas']
							#la carte en bas de la carte actuelle est ajoutée liste des cartes successives du déplacement
							liste_cartes += [plateau.carte_a_cote[carte_actuelle]]
							plateau.carte_a_cote[carte_actuelle]
						else:
							#on enlève le dernier mouvement de la liste des mouvements
							liste_mouvements.remove(liste_mouvements[-1])
							#on enlève la dernière carte de la liste des cartes
							liste_cartes.remove(liste_cartes[-1])
							#la carte actuelle devient la dernière carte 
							carte_actuelle = liste_cartes[-1]							
					print("Player pressed down!")
					
				#le joueur appuie sur la flèche droite
				elif event.key == pygame.K_RIGHT:
					if plateau.deplacement_possible(x, y,'droite'):
						if liste_mouvements[-1] != 'gauche':
							#la carte à droite de la carte actuelle est ajoutée liste des cartes successives du déplacement
							liste_cartes += [plateau.carte_a_cote[carte_actuelle]]
							plateau.carte_a_cote[carte_actuelle]
						else:
							#on enlève le dernier mouvement de la liste des mouvements
							liste_mouvements.remove(liste_mouvements[-1])
							#on enlève la dernière carte de la liste des cartes
							liste_cartes.remove(liste_cartes[-1])
							#la carte actuelle devient la dernière carte 
							carte_actuelle = liste_cartes[-1]														
					print("Player pressed right!")
					
				#confirmer le déplacement si celui ci est possible en appuayant sur entrée
				elif event.key == pygame.K_RETURN:
					if deplacement_valide:
						print('Deplacement validé !')
						
						return liste_cartes

				#avorte la tentative de déplacement si on appuie sur échap
				elif event.key == pygame.K_ESCAPE:
					return
		#màj de l'écran
		pygame.display.update()
		FPSCLOCK.tick()


def rotation_carte_jouable(Plateau,Carte):
	mouse = pygame.mouse.get_pos()
	clic = pygame.mouse.get_pressed()
	fleche1= IMAGES_DICT['fleche1'].get_rect()
	fleche2= IMAGES_DICT['fleche1'].get_rect()
	while True:
		for event in pygame.event.get():	
			if event.type == QUIT:
				terminate()		
			elif event.type == pygame.MOUSEMOTION:
				if clic[0] == 1 and fleche1[0]+fleche1[2] > mouse[0] > fleche1[0] and fleche1[1]+fleche1[3]> mouse[1] >fleche1[1]:
					Plateau.carte_jouable.tourner('gauche')
					Plateau.carte_jouable.update_murs()
					print('tourner gauche')
				elif clic[0] == 1 and fleche2[0]+fleche2[2] > mouse[0] > fleche2[0] and fleche2[1]+fleche2[3]> mouse[1] >fleche2[1]:
					Plateau.carte_jouable.tourner('droite')
					Plateau.carte_jouable.update_murs()
					print('droite')
		actualisation_affichage_plateau()
		pygame.display.update()
		FPSCLOCK.tick()

def insertion_carte_jouable(Plateau, Carte):
	global espace, pixel_case, gameDisplay, WINWIDTH, WINHEIGHT, dimension
	mouse = pygame.mouse.get_pos()
	clic = pygame.mouse.get_pressed()
	while True:
		for event in pygame.event.get():	
			if event.type == QUIT:
				terminate()
			elif event.type == pygame.MOUSEBUTTONUP:
				if clic[0] == 1 and espace > mouse[1] > espace+(dimension*pixel_case) and 0> mouse[0] >dimension*pixel_case:
					arrondiInf_x = floor(mouse[0]/100)*100
					x_carte=int(arrondiInf_x-espace)/pixel_case
					arrondiInf_y = floor(mouse[1]/100)*100
					y_carte=int(arrondiInf_y/pixel_case)
					Plateau.inserer_carte(Plateau.carte_jouable,[x_carte,y_carte])

def terminate():
	'''
	Fonction qui ferme la fenetre
	'''
	pygame.quit()
#	 sys.exit()
	
if __name__ == '__main__':
	main()
	

#test
# plateau = cl.Plateau(11,3)
# init_affichage_plateau()
# actualisation_affichage_plateau()
