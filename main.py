# -*- coding: utf-8 -*-
"""
Fichier principal du jeu. Contenu :
	
main : fonction principale du jeu
affiche_accueil : appelée au début de main, affiche l'écran d'accueil du jeu
init_jeu : appelée dans main SI l'utilisateur clique sur nouveau jeu dans la fonction affiche_accueil. Affiche l'écran d'initilisation d'un nouveau jeu
initialisation_partie: en fonction des paramètres choisie par les joueurs, crée le plateau, initialisa les joueurs et leur mission
boucle_deplacement : appelée dans main pendant le jeu, pour gérer le déplacement du joueur_actif. 
terminate : appelée lorque le joueur appuie sur échap. Ferme la fenetre de jeu.
sauvegarde: fonction permettant de sauvegarder le plateau dans un fichier .db
charger_sauvegarde: renvoie un plateau de jeu sauvegardé précédemment
"""

import random, sys, copy, os, pygame
from random import shuffle
import numpy as np
from pygame.locals import *
import classes as cl
from math import *
from variables import *
from affichage import *
import shelve as sh
from datetime import datetime
from IAMCTS import *

def main():
	'''Fonction principale du jeu
	'''
	global IMAGES_DICT, FPSCLOCK, gameDisplay
	#INITIALISATION DE PYGAME
	pygame.init()
	
	#FENETRE
	#titre de la fenetre
	pygame.display.set_caption('La Mine Hantée')
	
	#AFFICHAGE DE L'ACCUEIL
	choix_accueil = affiche_accueil() #choix_accueil prend la valeur retournée par affiche_accueil(), soit 'nouveau_jeu', soit 'reprendre_jeu'
	#initialisation du choix utilisateur, permet de quitter le menu sans message d'erreur
	envie_de_jouer = False
	#gestion du choix fait par l'utilisateur sur l'écran d'accueil ('nouveau_jeu','reprendre_jeu' ou 'quitter')
	if choix_accueil == 'nouveau_jeu':
		parametres_jeu= init_jeu() #parametres_jeu prend la valeur retournée par init_jeu, un dictionnaire contenant (dimension, joueur1,joueur2,joueur3,joueur4,go)
		envie_de_jouer = True
		#liste indiquant si les joueurs sont un ordinateur ou non
		liste_joueur_IA = [parametres_jeu['joueur1'],parametres_jeu['joueur2'],parametres_jeu['joueur3'],parametres_jeu['joueur4']]
		niveauIA = parametres_jeu['niveauIA']
		#création du plateau
		plateau = cl.Plateau(parametres_jeu['dimension'],parametres_jeu['nb_joueurs'],liste_joueur_IA,niveauIA)
	elif choix_accueil == 'reprendre_jeu':
		envie_de_jouer, plateau = interface_choix_sauvegarde()
	elif choix_accueil == 'quitter':
		envie_de_jouer = False		  
	#BOUCLE PRINCIPALE
	if envie_de_jouer:
		#redimension des surfaces des images des cartes
		redimension_images(plateau.dimension)
		#actualisation de la matrice des surfaces
		plateau.actualisation_matrice_surfaces()
		#la partie continue de jouer tant que l'utilisateur n'a pas choisi d'arrêter de jouer ou que la partie n'est pas finie
		#la valeur d'envie_de_jouer est actualisée lors du tour de jeu:
		#si l'utilisateur décide de fermer la fenetre, cette valeur devient False
			#actualisation_affichage_plateau(plateau)
		tour_de_jeu(plateau)

		#JEU TERMINE
		if plateau.gagne:
			podium = qui_a_gagne(plateau)
			affichage_fin_jeu(plateau)
	pygame.quit()
	sys.exit(0)
	
	
def tour_de_jeu(plateau):
	#AFFICHAGE DES INFORMATIONS DU JOUEUR
	print('===========================================')
	print('Au tour du joueur'+str(plateau.joueur_actif))
	print('Mission: ', plateau.liste_joueurs[plateau.joueur_actif-1].mission)
	print('Fantomes attrapés:', plateau.liste_joueurs[plateau.joueur_actif-1].fantomes)
	print('Score actuel: ',plateau.liste_joueurs[plateau.joueur_actif-1].score)

	#on initialise une variable indiquant que le joueur souhaite jouer -- cela permet d'arrêter les boucles proprement lorsque le joueur quitte le jeu
	envie_de_jouer = True
	#Variables servant à arrêter l'affichage des cartes lors de l'ouverture de l'interface de sauvegarde
	affichage_sauvegarde = False
	retour_au_jeu = False
	#rectangle associé au bouton de sauvegarde:
	bouton_sauvegarde = IMAGES_DICT['sauvegarder_plateau'].get_rect(topleft=(0,0))
	
	#reconnaissance du type de joueur:
	id_joueur_actif = plateau.joueur_actif
	joueur_actif = plateau.liste_joueurs[id_joueur_actif-1]
	
	afficher_joker = False
	
	# si le joueur est une IA
	if joueur_actif.IA:
		if plateau.niveauIA == 1:
			profondeur_insertion = 1
			nb_simulations_insertion = 30
			profondeur_chemin = 2
			nb_simulations_chemins = 30
		elif plateau.niveauIA == 2:
			profondeur_insertion = 2
			nb_simulations_insertion = 40
			profondeur_chemin = 3
			nb_simulations_chemins = 40
		elif plateau.niveauIA == 3:
			profondeur_insertion = 3
			nb_simulations_insertion = 50
			profondeur_chemin = 5
			nb_simulations_chemins = 50
		
		print('CPU playing')
		position_insertion_optimale, orientation_optimale, deplacement_optimal = IA_MCTS(plateau, profondeur_insertion, nb_simulations_insertion, profondeur_chemin, nb_simulations_chemins)
		
		### GESTION DE L'INSERTION DE LA CARTE
		#modification de l'orientation de la carte
		carte_jouable = plateau.carte_jouable
		carte_jouable.orientation = orientation_optimale
		#insertion de la carte
		plateau.inserer_carte(carte_jouable, position_insertion_optimale)
		
		#GESTION DU DEPLACEMENT
		if len(deplacement_optimal)>0:
			validation_deplacement(plateau,deplacement_optimal)
			
		plateau.insertion_carte_faite = True
		plateau.deplacement_fait = True
		plateau.changer_joueur()
		tour_de_jeu(plateau)
		
		#si le joueur n'est pas une IA:
	else:

		#PREMIERE PARTIE DU TOUR : INSERTION DE LA CARTE (OBLIGATOIRE)
		while not plateau.insertion_carte_faite and envie_de_jouer and not affichage_sauvegarde:
			#initialisation du plateau (fond sans les cartes)
			init_affichage_plateau(plateau)
			actualisation_affichage_plateau(plateau)
			#affichage du joker si utilisé:
			if afficher_joker:
				affichage_deplacement([position_insertion_optimale], plateau, (200,50,50, 100), afficher_joker)
			#Gestion du highlight des cartes cliquables sur le plateau
			#Coordonnées de la souris
			x_souris, y_souris = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
			#Highlight sur les cartes en hover 
			if not plateau.insertion_carte_faite:
				for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
					carte = plateau.matrice[index[0],index[1]]
					if surface_carte.collidepoint(x_souris, y_souris) and carte.bougeable:
						if (carte.position[0] in [0,plateau.dimension-1] or carte.position[1] in [0,plateau.dimension-1]):
							dessine_carte(plateau,carte,carte.position,True) #True est le parametre qui permet le highlight
			#Gestion des events
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN: #JOKER
					if event.key == pygame.K_j and joueur_actif.joker:
						#déploiement du joker
						position_insertion_optimale, orientation_optimale, deplacement_optimal = IA_MCTS(plateau)
		
						### GESTION DE L'INSERTION DE LA CARTE
						#modification de l'orientation de la carte
						carte_jouable = plateau.carte_jouable
						carte_jouable.orientation = orientation_optimale
						afficher_joker = True
						joueur_actif.joker=False
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 3: #si clic droit
						#Test (provisoire)
						for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
							carte = plateau.matrice[index[0],index[1]]
							if surface_carte.collidepoint(x_souris, y_souris):
								print('test4',carte.__dict__)
					#INSERTION
					#Recupération des coordonnées de la souris
					x_souris,y_souris = event.pos
					#Itération sur la matrice des surfaces ou index = (ligne,colonne), surface_carte = objet Surface
					if event.button ==1:
						for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
							carte = plateau.matrice[index[0],index[1]]
							if surface_carte.collidepoint(x_souris, y_souris):					
								if (carte.position[0] in [0,plateau.dimension-1] or carte.position[1] in [0,plateau.dimension-1]) and carte.bougeable:
									plateau.inserer_carte(plateau.carte_jouable,carte.position)
									plateau.insertion_carte_faite = True
									#dans le cas où le joker a été activé
									if afficher_joker:
										#si l'insertion n'est pas faite dans l'endroit optimal, on n'affiche pas le déplacement optimal
										if [index[0],index[1]] != [position_insertion_optimale[0],position_insertion_optimale[1]]:
											afficher_joker = False

					#TOURNER CARTE JOUABLE
					#création des Rect associées associées avec get_rect()
					position_fleche1, position_fleche2 = IMAGES_DICT['fleche1'].get_rect().move((150,530)),IMAGES_DICT['fleche2'].get_rect().move((275,530))
					if position_fleche1.collidepoint(x_souris, y_souris):
						plateau.carte_jouable.tourner('gauche')
						plateau.carte_jouable.update_murs()
					elif position_fleche2.collidepoint(x_souris, y_souris):
						plateau.carte_jouable.tourner('droite')
						plateau.carte_jouable.update_murs()
					#SAUVEGARDE
					if bouton_sauvegarde.collidepoint(x_souris,y_souris):
						#la variable affichage sauvegarde permet d'arrêter l'affichage des cartes
						affichage_sauvegarde = True
				if event.type == pygame.QUIT:
					envie_de_jouer = False	
			#affichage de l'interface de sauvegarde si l'utilisateur en fait le choix
			if affichage_sauvegarde:
				retour_au_jeu = sauvegarde_pdt_partie(plateau)
				affichage_sauvegarde = False
			if retour_au_jeu:
				init_affichage_plateau(plateau)
				tour_de_jeu(plateau)
				retour_au_jeu = False
					
			pygame.display.update()
			FPSCLOCK.tick()
		#=======================================	
		#DEUXIEME PARTIE DU TOUR : DEPLACEMENT (FACULTATIF)
		#Initialisation des variables utiles
		chasseur = plateau.liste_joueurs[plateau.joueur_actif-1] #chasseur actif
		position_initiale = chasseur.position #position de départ
		carte_initiale = plateau.matrice[position_initiale[0],position_initiale[1]]  #carte de départ
		suivi_deplacement = [carte_initiale] #liste contenant les cartes traversées lors du déplacement
		cartes_fantomes_pris = [] #liste contenant les cartes ou un fantome est capturé
		carte_pepite_prises = [] #liste contenant les cartes ou une pépite est ramassée
		derniere_direction = None #dernière direction (utile pour éviter les retours en arrière)
		
		while not plateau.deplacement_fait and envie_de_jouer and not affichage_sauvegarde:
			#initialisation du plateau (fond sans les cartes)
			init_affichage_plateau(plateau)
			actualisation_affichage_plateau(plateau)
			carte_jouable_jouee(plateau) #affiche une croix sur la carte jouable pour montrer qu'elle a déjà été insérée
			#affichage du joker si utilisé:
			if afficher_joker:
				affichage_deplacement(deplacement_optimal, plateau, (50,50,50, 100), afficher_joker)
			#Coordonnées de la souris
			x_souris, y_souris = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
			#affichage de la trace du déplacement du joueur 
			if len(suivi_deplacement) != 1:
				affichage_deplacement(suivi_deplacement[:-1],plateau)
			#gestion des évenements
			for event in pygame.event.get():
				#gestion des clics
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 3:
						#TEST
						for index, surface_carte in np.ndenumerate(plateau.matrice_surfaces):
							carte1 = plateau.matrice[index[0],index[1]]
							if surface_carte.collidepoint(x_souris, y_souris):
								print('test4',carte1.__dict__)
					#SAUVEGARDE
					elif bouton_sauvegarde.collidepoint(x_souris,y_souris):
						#la variable affichage sauvegarde permet d'arrêter l'affichage des cartes
						affichage_sauvegarde = True
				if event.type == pygame.KEYDOWN:
					#gestion du changement de pers:
					#JOUEUR ACTIF
	
					#Traduction de l'event (déplacement) en chaine de caractère
					if event.key in [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]:
						if event.key == pygame.K_UP:
							direction = 'haut'
						elif event.key == pygame.K_DOWN:
							direction = 'bas'
						elif event.key == pygame.K_LEFT:
							direction = 'gauche'
						elif event.key == pygame.K_RIGHT:
							direction = 'droite'
					
						#DEPLACEMENT
						if deplacement_licite(plateau,plateau.joueur_actif,suivi_deplacement,direction,derniere_direction):
							carte_arrivee, pepite_attrapee = plateau.deplacer_joueur(plateau.joueur_actif,direction)
							suivi_deplacement += [carte_arrivee]
							if pepite_attrapee:
								carte_pepite_prises += [carte_arrivee]
							#si le déplacement n'a pas été possible (mur) (la fonction déplacer_joueur renvoie alors None, qu'il faut supprimer de la liste suivi_deplacements)
							if suivi_deplacement[-1] == None:
								del suivi_deplacement[-1]
							else:
								derniere_direction = direction #mise à jour de la dernière direction si le déplacement a eu lieu
					#PRISE FANTOME
					elif event.key == pygame.K_f and plateau.matrice[chasseur.position[0],chasseur.position[1]].fantome != 0  and len(cartes_fantomes_pris)==0:
						chasseur = plateau.liste_joueurs[plateau.joueur_actif-1]
						fantome_pris = chasseur.attraper_fantome(plateau)
						#Verification que le fantome soit effectivement attrapable
						if fantome_pris != False:
							cartes_fantomes_pris += [fantome_pris]
						print('fantome attrapés du j'+str(plateau.joueur_actif),chasseur.fantomes)
						print('cartes_fantomes_pris'+str(plateau.joueur_actif),cartes_fantomes_pris)
					#VALIDATION
					elif event.key == pygame.K_RETURN:
						print('Deplacement terminé')
						print('Score final du tour: ',plateau.liste_joueurs[plateau.joueur_actif-1].score)
						plateau.deplacement_fait = True
					#ANNULATION
					elif event.key == pygame.K_ESCAPE: #annulation du déplacement
						#remise des fantomes sur les cartes
						while cartes_fantomes_pris != []:
							num_fantome = chasseur.fantomes[-1]
							cartes_fantomes_pris[-1].fantome = cl.Fantome(num_fantome) #recréation des fantomes
							#remise à jour des fantomes restants
							plateau.fantomes_restants +=1
							#Remise à jour du score du joueur
							if num_fantome in chasseur.mission:
								chasseur.score-= 20
								chasseur.mission.remove(num_fantome)
								if chasseur.mission_complete():
									chasseur.score -= 40
							else:
								chasseur.score-=5
							#Suppression des cartes
							del cartes_fantomes_pris[-1]
							del chasseur.fantomes[-1]
						#Remise des pepites sur les cartes et màj du score
						for carte in carte_pepite_prises:
							carte.pepite = True
							chasseur.score -= -1
						#Réinit de la liste des pepites
						carte_pepite_prises = []
						#Reposition du chasseur
						chasseur.position = position_initiale
						carte_initiale.chasseur += [chasseur.id]
						suivi_deplacement[-1].chasseur.remove(plateau.joueur_actif)
						#Vidange des listes de suivi et de la derniere direction
						suivi_deplacement = [carte_initiale]
						derniere_direction = None
				if event.type == pygame.QUIT:
					envie_de_jouer = False
			#affichage de l'interface de sauvegarde si l'utilisateur en fait le choix
			if affichage_sauvegarde:
				retour_au_jeu = sauvegarde_pdt_partie(plateau)
				affichage_sauvegarde = False
			if retour_au_jeu:
				init_affichage_plateau(plateau)
				tour_de_jeu(plateau)
				retour_au_jeu = False
			pygame.display.update()
			FPSCLOCK.tick()
		#TEST PARTIE GAGNE)
		if plateau.fantomes_restants == 0:
			plateau.gagne = True
		else:
			plateau.gagne = False
		if not plateau.gagne and envie_de_jouer and plateau.insertion_carte_faite and plateau.deplacement_fait:
			plateau.changer_joueur()
			tour_de_jeu(plateau)
		else:# a completer avec l'ecran de fin de jeu
			affichage_fin_jeu(plateau)
			pygame.quit()
			sys.exit(0)

def qui_a_gagne(plateau):
	"""Definit qui a gagne.
	Arguments:
		plateau {Plateau()} -- plateau du jeu
	"""
	joueurs = plateau.liste_joueurs
	sorted(joueurs, key=lambda joueurs:joueurs.score)
	return [joueur.id for joueur in joueurs]

def deplacement_licite(plateau,id_joueur,suivi_deplacement,direction,derniere_direction):
	"""Fonction permettant de savoir si un déplacement est licite ou non (déplacement sur plusieurs cases ou non)
	Arguments:
		plateau: objet de type plateau
		id_joueur: id du joueur
		suivi_deplacement: déplacement du joueur en cours
		direction: direction vers laquelle veut se déplacer le joueur
		derniere_direction: derniere direction opérée par le joueur (= None ou une des 4 directions de l'espace plan)
	---
	return Booléen
	"""
	#Recuperation des évenements et traduction en chaine de caractère
	direction_opposee = {'haut':'bas','bas':'haut','gauche':'droite','droite':'gauche'}
	joueur = plateau.liste_joueurs[id_joueur-1]
	#on verifie que l'utilisateur ne fait pas marche arrière
	if derniere_direction != direction_opposee[direction]:
		x_joueur, y_joueur = joueur.position
		carte_visee = plateau.carte_a_cote(x_joueur,y_joueur,direction)
		#si l'utilisateur ne fait pas marche arrière, on vérifie qu'il ne va pas sur une case où il est déjà passé dans le même tour
		if carte_visee in suivi_deplacement:
			licite = False
		else:
			licite = True
	else:
		licite = False
	return licite

def sauvegarde(plateau):
	""" Fonction qui permet de sauvegarder un plateau dans un fichier à un instant t
	Utilise le module shelf qui store des fichiers pythons dans une sorte de dictionnaire
	---
	plateau: objet de type plateau
	sauvegarder: booléen indiquant si l'utilisateur veut sauvegarder ou non
	"""
	#recuperation de la date et de l'heure pour nommer le fichier
	now = datetime.now()
	nom_sauvegarde = now.strftime("%d-%m-%Y %Hh%Mm%Ss")
	
	#Ouverture du fichier de sauvegarde
	save = sh.open(nom_sauvegarde)
	
	#On stocke les fichiers dans le "dictionnaire" qui sert de sauvegarde
	save['plateau'] = plateau
	save.close()
	
def charger_sauvegarde(nom_sauvegarde):
	save = sh.open(nom_sauvegarde)
	plateau=save['plateau']
	save.close()
	return plateau

def delete_sauvegarde(nom_sauvegarde):
	if nom_sauvegarde != None:
		#Recuperation du chemin du fichier
		dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
		os.chdir(dirname)
		
		#delétion des fichiers avec le nom de sauvegarde
		for file in glob.glob(nom_sauvegarde+'.*'):
			os.remove(file)

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