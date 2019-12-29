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
import numpy as np
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
		redimension_images(parametres_jeu['dimension'])
		init_affichage_plateau(plateau)
		plateau.actualisation_matrice_surfaces()
		gagne = False
	elif choix_accueil == 'reprendre_jeu':
		#/!\ à ajouter : doit mettre la fonction appelant l'écran du choix des parties sauvegardées
		terminate()
	elif choix_accueil == 'quitter':
		terminate()		  
	
	while not gagne:
		actualisation_affichage_plateau(plateau)
		plateau, gagne = tour_de_jeu(plateau)
		plateau.changer_joueur()

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_ESCAPE:
					terminate()

		pygame.display.update()
		FPSCLOCK.tick()
	#JEU TERMINE
	podium = qui_a_gagne(plateau)
	print('CLASSEMENT')
	for rang in range(1,plateau.nb_joueurs+1):
		print(str(rang)+'. ', podium[rang-1])
	# afficher_fin_jeu()
	
def tour_de_jeu(plateau):
	print('===========================================')
	print('Au tour du joueur'+str(plateau.joueur_actif))
	print('Mission: ', plateau.liste_joueurs[plateau.joueur_actif-1].mission)
	print('Fantomes attrapés:', plateau.liste_joueurs[plateau.joueur_actif-1].fantomes)
	print('Score actuel: ',plateau.liste_joueurs[plateau.joueur_actif-1].score)
	deplacement_fait = False
	insertion_carte_faite = False
	termine = deplacement_fait*insertion_carte_faite
	#PREMIERE PARTIE DU TOUR : INSERTION DE LA CARTE (OBLIGATOIRE)
	while not insertion_carte_faite:
		# print('Il faut placer la carte')
		actualisation_affichage_plateau(plateau)
		#gestion du highlight des cartes cliquables sur le plateau
		#coordonnées de la souris
		x_souris, y_souris = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
		#HIGHLIGHT SUR LES CARTES EN HOVER SI 
		if not insertion_carte_faite:
			for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
				carte = plateau.matrice[index[0],index[1]]
				if surface_carte.collidepoint(x_souris, y_souris) and carte.bougeable:
					if (carte.position[0] in [0,plateau.dimension-1] or carte.position[1] in [0,plateau.dimension-1]):
						dessine_carte(plateau,carte,carte.position,True) #True est le parametre qui permet le highlight
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 3:
					#TEST
					for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
						carte = plateau.matrice[index[0],index[1]]
						if surface_carte.collidepoint(x_souris, y_souris):
							print('test4',carte.__dict__)
				#INSERTION
				#recupération des coordonnées de la souris
				x_souris,y_souris = event.pos
				#itération sur la matrice des surfaces ou index = (ligne,colonne), surface_carte = objet Surface
				if event.button ==1:
					for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
						carte = plateau.matrice[index[0],index[1]]
						if surface_carte.collidepoint(x_souris, y_souris):
							if (carte.position[0] in [0,plateau.dimension-1] or carte.position[1] in [0,plateau.dimension-1]) and carte.bougeable:
								plateau.inserer_carte(plateau.carte_jouable,carte.position)
								insertion_carte_faite = True
				#TOURNER CARTE JOUABLE
				#création des Rect associées associées avec get_rect()
				position_fleche1, position_fleche2 = IMAGES_DICT['fleche1'].get_rect().move((150,530)),IMAGES_DICT['fleche2'].get_rect().move((275,530))
				if position_fleche1.collidepoint(x_souris, y_souris):
					plateau.carte_jouable.tourner('gauche')
					plateau.carte_jouable.update_murs()
				elif position_fleche2.collidepoint(x_souris, y_souris):
					plateau.carte_jouable.tourner('droite')
					plateau.carte_jouable.update_murs()
		pygame.display.update()
		FPSCLOCK.tick()
	#=======================================	
	#DEUXIEME PARTIE DU TOUR : DEPLACEMENT (FACULTATIF)
	gagne = False
	chasseur = plateau.liste_joueurs[plateau.joueur_actif-1]
	position_initiale = chasseur.position
	carte_initiale = plateau.matrice[position_initiale[0],position_initiale[1]]
	suivi_deplacement = [carte_initiale]
	cartes_fantomes_pris = []
	carte_pepite_prises = []
	derniere_direction = None
	while not deplacement_fait:
		actualisation_affichage_plateau(plateau)
		carte_jouable_jouee(plateau)
		if len(suivi_deplacement) != 1:
			affichage_deplacement(suivi_deplacement[:-1],plateau)
		#gestion des évenements
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 3:
					#TEST
					for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
						carte1 = plateau.matrice[index[0],index[1]]
						# print('cartes', carte1.position)
						if surface_carte.collidepoint(x_souris, y_souris):
							print('test4',carte1.__dict__)
			if event.type == pygame.KEYDOWN:
				#gestion du changement de perso (provisoire):
				#JOUEUR ACTIF
				# if event.key == pygame.K_p:
				# 	plateau.changer_joueur()
				# 	print('Le joueur actif est le',plateau.joueur_actif)

				#Deplacement
				#BAS
				if event.key == pygame.K_UP and derniere_direction != 'bas':
					carte_arrivee, pepite_attrapee = plateau.deplacer_joueur(plateau.joueur_actif,'haut')
					suivi_deplacement += [carte_arrivee]
					if pepite_attrapee:
						carte_pepite_prises += [carte_arrivee]
					if suivi_deplacement[-1] == None:
						del suivi_deplacement[-1]
					else:
						derniere_direction = 'haut'
				#HAUT
				elif event.key == pygame.K_DOWN and derniere_direction != 'haut':
					carte_arrivee, pepite_attrapee = plateau.deplacer_joueur(plateau.joueur_actif,'bas')
					suivi_deplacement += [carte_arrivee]
					if pepite_attrapee:
						carte_pepite_prises += [carte_arrivee]
					if suivi_deplacement[-1] == None:
						del suivi_deplacement[-1]
					else:
						derniere_direction = 'bas'
				#GAUCHE
				elif event.key == pygame.K_LEFT and derniere_direction != 'droite':
					carte_arrivee, pepite_attrapee = plateau.deplacer_joueur(plateau.joueur_actif,'gauche')
					suivi_deplacement += [carte_arrivee]
					if pepite_attrapee:
						carte_pepite_prises += [carte_arrivee]
					if suivi_deplacement[-1] == None:
						del suivi_deplacement[-1]
					else:
						derniere_direction = 'gauche'
				#DROITE
				elif event.key == pygame.K_RIGHT and derniere_direction != 'gauche':
					carte_arrivee, pepite_attrapee = plateau.deplacer_joueur(plateau.joueur_actif,'droite')
					suivi_deplacement += [carte_arrivee]
					if pepite_attrapee:
						carte_pepite_prises += [carte_arrivee]
					if suivi_deplacement[-1] == None:
						del suivi_deplacement[-1]
					else:
						derniere_direction = 'droite'
				#PRISE FANTOME
				elif event.key == pygame.K_f and plateau.matrice[chasseur.position[0],chasseur.position[1]].fantome != 0:
					chasseur = plateau.liste_joueurs[plateau.joueur_actif-1]
					cartes_fantomes_pris += [chasseur.attraper_fantome(plateau)]
					print('fantome attrapés du j'+str(plateau.joueur_actif),chasseur.fantomes)
				#VALIDATION
				elif event.key == pygame.K_RETURN:
					print('Deplacement terminé')
					print('Score final du tour: ',plateau.liste_joueurs[plateau.joueur_actif-1].score)
					deplacement_fait = True
				#ANNULATION
				elif event.key == pygame.K_ESCAPE: #annulation du déplacement
					#remise des fantomes sur les cartes
					while cartes_fantomes_pris != []:
						# print(cartes_fantomes_pris)
						num_fantome = chasseur.fantomes[-1]
						cartes_fantomes_pris[-1].fantome = cl.Fantome(num_fantome) #recréarion des fantomes
						plateau.fantomes_restants +=1
						if num_fantome in chasseur.mission:
							chasseur.score-= 20
						# 	self.mission.remove(num_fantome)
						# 	if self.mission == []:
						# 		self.score+=40
							if chasseur.mission_complete():
								chasseur.score -= 40
						else:
							chasseur.score-=5
						del cartes_fantomes_pris[-1]
						del chasseur.fantomes[-1]
					# print('apres1',cartes_fantomes_pris)
					#remise des pepites sur les cartes
					for carte in carte_pepite_prises:
						carte.pepite = True
						chasseur.score -= -1
					carte_pepite_prises = []
					#reposition du chasseur
					chasseur.position = position_initiale
					carte_initiale.chasseur += [chasseur.id]
					suivi_deplacement[-1].chasseur.remove(plateau.joueur_actif)
					#vidange des listes de suivi
					suivi_deplacement = [carte_initiale]
					derniere_direction = None
		pygame.display.update()
		FPSCLOCK.tick()
	#TEST PARTIE GAGNE
	if plateau.fantomes_restants == 0:
		gagne = True
	else:
		gagne = False
	return plateau, gagne

def qui_a_gagne(plateau):
	"""Definit qui a gagne.
	Arguments:
		plateau {Plateau()} -- plateau du jeu
	"""
	# scores_joueurs = []
	# for joueur in plateau.liste_joueurs:
	# 	scores_joueurs += [(joueur, joueur.score)]
	# sorted(scores_joueurs, key=lambda scores_joueurs: scores_joueurs[1])
	# print(scores_joueurs)
	# dico = {}
	# for rang in range(1,plateau.nb_joueurs+1):
	# 	dico[rang] = scores_joueurs[rang-1][0]
	joueurs = plateau.liste_joueurs
	sorted(joueurs, key=lambda joueurs:joueurs.score)
	# print([joueur.id for joueur in joueurs])
	return [joueur.id for joueur in joueurs]

# def boucle_deplacement(plateau):
# 	'''
# 	Fonction permettant d'enregistrer le déplacement potentiel du joueur actif pendant son tour, en retournant une liste de directions.
# 	Si le déplacement est validé, retourne deux listes qui seront utilisées pour faire bouger le joueur.
# 	Récupère les évenements boutons flèches, escape et enter. Création au fur et à mesure :
# 		1. liste_cartes : listes des objets Cartes du déplacement
# 		2. liste_mouvements : liste des mouvements du déplacement ('gauche','haut',...)
# 	Parametres : plateau : Plateau
# 	-->: liste_cartes, liste_mouvements
# 	'''
# 	liste_cartes = [] #futur liste des cartes par lesquelles passe ce déplacement
# 	liste_mouvements = [] #listes des directions du déplacements
# 	deplacement_valide = True #le deplacement est autorisée par les régles
# 	x_init, y_init = plateau.joueur_actif.position #position initiale du joueur actif
# 	x, y = x_init, y_init #position du joueur au fur et à mesure du déplacement
# 	carte_depart = plateau.matrice[x_init, y_init] #carte de départ sur laquelle le joueur actif se situe
# 	carte_actuelle = carte_depart #dernière carte choisie pendant le déplacement
# 	direction_opposee = {'haut':'bas','bas':'haut','gauche':'droite','droite':'gauche'}

# 	while True:
# 		#gestion des évenements joueurs lors du déplacement
# 		for event in pygame.event.get():
# 			#evenements de type touche pressée
# 			if event.type == pygame.KEYDOWN:
				
# 				#le joueur appuie sur la flèche haut
# 				if event.key == pygame.K_UP:
# 					#vérification que le déplacement est possible (absence de mur sur les deux cartes concernéees)
# 					if plateau.deplacement_possible(x, y,'haut')==True:
# 						if liste_mouvements[-1]!='bas': 
# 							#la carte en haut de la carte actuelle est ajoutée liste des cartes successives du déplacement
# 							liste_mouvements += ['haut']
# 							liste_cartes += [plateau.carte_a_cote('haut',x,y)]
# 							carte_actuelle = liste_cartes[-1]
# 						else: #si le mouvement consiste à revenir en arrière
# 							#on enlève le dernier mouvement de la liste des mouvements
# 							liste_mouvements.remove(liste_mouvements[-1])
# 							#on enlève la dernière carte de la liste des cartes
# 							liste_cartes.remove(liste_cartes[-1])
# 							#la carte actuelle devient la dernière carte 
# 							carte_actuelle = liste_cartes[-1]
# 					print("Player pressed up!")
					
# 				#le joueur appuie sur la flèche gauche				  
# 				elif event.key == pygame.K_LEFT:
# 					if plateau.deplacement_possible(x, y,'gauche'):
# 						if liste_mouvements[-1]!='droite':
# 							liste_mouvements += ['gauche']
# 							#la carte à gauche de la carte actuelle est ajoutée liste des cartes successives du déplacement
# 							liste_cartes += [plateau.carte_a_cote[carte_actuelle]]
# 							plateau.carte_a_cote[carte_actuelle]
# 						else:
# 							#on enlève le dernier mouvement de la liste des mouvements
# 							liste_mouvements.remove(liste_mouvements[-1])
# 							#on enlève la dernière carte de la liste des cartes
# 							liste_cartes.remove(liste_cartes[-1])
# 							#la carte actuelle devient la dernière carte 
# 							carte_actuelle = liste_cartes[-1]							
# 					print("Player pressed left!")
					
# 				#le joueur appuie sur la flèche bas					   
# 				elif event.key == pygame.K_DOWN:
# 					if plateau.deplacement_possible(x, y,'bas'):
# 						if liste_mouvements[-1] != 'haut':
# 							liste_mouvements += ['bas']
# 							#la carte en bas de la carte actuelle est ajoutée liste des cartes successives du déplacement
# 							liste_cartes += [plateau.carte_a_cote[carte_actuelle]]
# 							plateau.carte_a_cote[carte_actuelle]
# 						else:
# 							#on enlève le dernier mouvement de la liste des mouvements
# 							liste_mouvements.remove(liste_mouvements[-1])
# 							#on enlève la dernière carte de la liste des cartes
# 							liste_cartes.remove(liste_cartes[-1])
# 							#la carte actuelle devient la dernière carte 
# 							carte_actuelle = liste_cartes[-1]							
# 					print("Player pressed down!")
					
# 				#le joueur appuie sur la flèche droite
# 				elif event.key == pygame.K_RIGHT:
# 					if plateau.deplacement_possible(x, y,'droite'):
# 						if liste_mouvements[-1] != 'gauche':
# 							#la carte à droite de la carte actuelle est ajoutée liste des cartes successives du déplacement
# 							liste_cartes += [plateau.carte_a_cote[carte_actuelle]]
# 							plateau.carte_a_cote[carte_actuelle]
# 						else:
# 							#on enlève le dernier mouvement de la liste des mouvements
# 							liste_mouvements.remove(liste_mouvements[-1])
# 							#on enlève la dernière carte de la liste des cartes
# 							liste_cartes.remove(liste_cartes[-1])
# 							#la carte actuelle devient la dernière carte 
# 							carte_actuelle = liste_cartes[-1]														
# 					print("Player pressed right!")
					
# 				#confirmer le déplacement si celui ci est possible en appuayant sur entrée
# 				elif event.key == pygame.K_RETURN:
# 					if deplacement_valide:
# 						print('Deplacement validé !')
						
# 						return liste_cartes

# 				#avorte la tentative de déplacement si on appuie sur échap
# 				elif event.key == pygame.K_ESCAPE:
# 					return
# 		#màj de l'écran
# 		pygame.display.update()
# 		FPSCLOCK.tick()

#FONCTION INUTILE ?
# def rotation_carte_jouable(Plateau,Carte):
# 	mouse = pygame.mouse.get_pos()
# 	clic = pygame.mouse.get_pressed()
# 	fleche1= IMAGES_DICT['fleche1'].get_rect()
# 	fleche2= IMAGES_DICT['fleche1'].get_rect()
# 	while True:
# 		for event in pygame.event.get():	
# 			if event.type == QUIT:
# 				terminate()		
# 			elif event.type == pygame.MOUSEMOTION:
# 				if clic[0] == 1 and fleche1[0]+fleche1[2] > mouse[0] > fleche1[0] and fleche1[1]+fleche1[3]> mouse[1] >fleche1[1]:
# 					Plateau.carte_jouable.tourner('gauche')
# 					Plateau.carte_jouable.update_murs()
# 					print('tourner gauche')
# 				elif clic[0] == 1 and fleche2[0]+fleche2[2] > mouse[0] > fleche2[0] and fleche2[1]+fleche2[3]> mouse[1] >fleche2[1]:
# 					Plateau.carte_jouable.tourner('droite')
# 					Plateau.carte_jouable.update_murs()
# 					print('droite')
# 		actualisation_affichage_plateau()
# 		pygame.display.update()
# 		FPSCLOCK.tick()

#def insertion_carte_jouable(Plateau, Carte):
#	global espace, pixel_case, gameDisplay, WINWIDTH, WINHEIGHT, dimension
#	mouse = pygame.mouse.get_pos()
#	clic = pygame.mouse.get_pressed()
#
#	for event in pygame.event.get():	
#		if event.type == QUIT:
#			terminate()
#		elif event.type == pygame.MOUSEBUTTONUP:
#			if clic[0] == 1 and espace > mouse[1] > espace+(dimension*pixel_case) and 0> mouse[0] >dimension*pixel_case:
#				arrondiInf_x = floor(mouse[0]/100)*100
#				x_carte=int(arrondiInf_x-espace)/pixel_case
#				arrondiInf_y = floor(mouse[1]/100)*100
#				y_carte=int(arrondiInf_y/pixel_case)
#				Plateau.inserer_carte(Plateau.carte_jouable,[x_carte,y_carte])

# def insertion_carte_jouable(Plateau, Carte):
# 	global espace, pixel_case, gameDisplay, WINWIDTH, WINHEIGHT, dimension

# 	for event in pygame.event.get():	
# 		if event.type == QUIT:
# 			terminate()
# 		elif event.type == pygame.MOUSEBUTTONUP:
# 			if clic[0] == 1 and espace > mouse[1] > espace+(dimension*pixel_case) and 0> mouse[0] >dimension*pixel_case:
# 				arrondiInf_x = floor(mouse[0]/100)*100
# 				x_carte=int(arrondiInf_x-espace)/pixel_case
# 				arrondiInf_y = floor(mouse[1]/100)*100
# 				y_carte=int(arrondiInf_y/pixel_case)
# 				Plateau.inserer_carte(Plateau.carte_jouable,[x_carte,y_carte])

def redimension_images(dimension):
	'''Redimension des images selon la dimension du plateau
	
	Transforme certaines images de IMAGES_DICT
	
	Arguments:
		dimension {int} -- dimension du plateau de jeu
	'''
	global IMAGES_DICT, pixel_case
	IMAGES_DICT['pepite']= pygame.transform.scale(IMAGES_DICT['pepite'],(int(pixel_case/6),int(pixel_case/6)))
	IMAGES_DICT['chasseur1']= pygame.transform.scale(IMAGES_DICT['chasseur1'],(pixel_case,pixel_case))
	IMAGES_DICT['chasseur2']= pygame.transform.scale(IMAGES_DICT['chasseur2'],(pixel_case,pixel_case))
	IMAGES_DICT['chasseur3']= pygame.transform.scale(IMAGES_DICT['chasseur3'],(pixel_case,pixel_case))
	IMAGES_DICT['chasseur4']= pygame.transform.scale(IMAGES_DICT['chasseur4'],(pixel_case,pixel_case))
	IMAGES_DICT['fantome']= pygame.transform.scale(IMAGES_DICT['fantome'],(pixel_case,pixel_case))
	IMAGES_DICT['carte1' ]= pygame.transform.scale(IMAGES_DICT['carte1'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2' ]= pygame.transform.scale(IMAGES_DICT['carte2'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3' ]= pygame.transform.scale(IMAGES_DICT['carte3'],(pixel_case,pixel_case))
	IMAGES_DICT['carte1_dark' ]= pygame.transform.scale(IMAGES_DICT['carte1_dark'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2_dark' ]= pygame.transform.scale(IMAGES_DICT['carte2_dark'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3_dark' ]= pygame.transform.scale(IMAGES_DICT['carte3_dark'],(pixel_case,pixel_case))
	IMAGES_DICT['carte1_bright' ]= pygame.transform.scale(IMAGES_DICT['carte1_bright'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2_bright' ]= pygame.transform.scale(IMAGES_DICT['carte2_bright'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3_bright' ]= pygame.transform.scale(IMAGES_DICT['carte3_bright'],(pixel_case,pixel_case))
	IMAGES_DICT['carte1_hover' ]= pygame.transform.scale(IMAGES_DICT['carte1_hover'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2_hover' ]= pygame.transform.scale(IMAGES_DICT['carte2_hover'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3_hover' ]= pygame.transform.scale(IMAGES_DICT['carte3_hover'],(pixel_case,pixel_case))
	IMAGES_DICT['fleche1']= pygame.transform.scale(IMAGES_DICT['fleche1'],(pixel_case,pixel_case))
	IMAGES_DICT['fleche2']= pygame.transform.scale(IMAGES_DICT['fleche2'],(pixel_case,pixel_case))

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
