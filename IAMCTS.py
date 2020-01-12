# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:26:18 2020

@author: kevin
"""

from classes import *
import random as rd
import copy 

def chemins_possibles(plateau):
	"""Fonction qui renvoie la liste des déplacements possibles à partir de la case de départ du joueur actif
	"""
	id_joueur_actif = plateau.joueur_actif
	joueur_actif = plateau.liste_joueurs[id_joueur_actif - 1]
	liste_directions = ['haut','bas','gauche','droite']
	#permet de stocker les déplacements -- les branches que l'on a déjà explorées sont incluses
	stockage_deplacements=[[joueur_actif.position]]
	#stocke les déplacements du tour précédent celui que l'on étudie -- permet de n'explorer que les dernières branches développées
	liste_derniers_deplacements = [[joueur_actif.position]]
	#booléen servant à arrêter la boucle
	continuer = True
	
	while continuer:
		liste_deplacements_possibles = []
		#on parcourt la liste des déplacements effectués précédemments
		#i.e. on explore les branches développées au tour d'avant
		for dernier_deplacement in liste_derniers_deplacements:
			for direction in liste_directions:
				if deplacement_licite_IA(plateau,dernier_deplacement,direction):
					x_position, y_position = dernier_deplacement[-1]
					liste_deplacements_possibles+=[dernier_deplacement+[plateau.carte_a_cote(x_position,y_position,direction).position]]
		#on actualise les derniers déplacements avec ceux enregistrés au dernier tour, afin de n'explorer que les dernieres branches
		liste_derniers_deplacements=liste_deplacements_possibles.copy()
		#on stocke les déplacements possibles enregistrés pendant le tour
		stockage_deplacements+=liste_derniers_deplacements.copy()
		#si les branches ne sont plus explorables, on arrête la boucle
		if len(liste_deplacements_possibles)==0:
			continuer = False
	return stockage_deplacements

def deplacement_aleatoire(plateau):
	"""Fonction effectuant un deplacement aleatoire du joueur actif
	Le joueur peut aller sur toutes les cases qui lui sont accessibles de manière équiprobable
	"""
	liste_chemins = chemins_possibles(plateau)
	nb_chemins = len(liste_chemins)
	#tirage au sort du chemin
	index_aleatoire = rd.randint(0,nb_chemins-1)
	return liste_chemins[index_aleatoire]

def validation_deplacement(plateau, deplacement):
	"""Fonction qui prend en entrée un plateau et un déplacement (i.e. une liste de positions), et réalise le déplacement du joueur actif
	"""
	id_joueur_actif = plateau.joueur_actif
	joueur_actif = plateau.liste_joueurs[id_joueur_actif-1]
	fantome_attrape = 0
	if len(deplacement)>1:
		for index in range(len(deplacement)-1):
			carte_depart = plateau.matrice[deplacement[index][0],deplacement[index][1]]
			carte_visee = plateau.matrice[deplacement[index+1][0],deplacement[index+1][1]]
			#actualisation de la position
			carte_depart.chasseur.remove(id_joueur_actif)
			carte_visee.chasseur += [id_joueur_actif]
			joueur_actif.position = carte_visee.position
			joueur_actif.attraper_pepite(carte_visee)
			if fantome_attrape == 0:
				joueur_actif.attraper_fantome(plateau)
				fantome_attrape+=1
				
			
			

def deplacement_licite_IA(plateau, suivi_deplacement,direction):
	"""Fonction adaptée de deplacement_licite (dans main) et deplacement_possible dans classes (methode de plateau)
	Arguments:
		plateau: objet de type plateau
		suivi_deplacement: déplacement du joueur en cours
		direction: direction vers laquelle veut se déplacer le joueur
	---
	return Booléen
	"""
	direction_opposee = {'haut':'bas','bas':'haut','gauche':'droite','droite':'gauche'}
	position = suivi_deplacement[-1]
	x_position = position[0]
	y_position = position [1]

	#récupération des cartes correspondants aux coordonnées
	carte_actuelle = plateau.matrice[x_position, y_position]
	carte_visee = plateau.carte_a_cote(x_position, y_position,direction)
	#s'il n(y a pas de murs sur les deux cartes)
	if carte_actuelle.murs[direction] == False and carte_visee.murs[direction_opposee[direction]] == False:
		#si l'utilisateur ne fait pas marche arrière, on vérifie qu'il ne va pas sur une case où il est déjà passé précédemment
		if carte_visee.position in suivi_deplacement:
			licite = False
		else:
			licite = True
	else:
		licite = False
	return licite

def insertion_carte_aleatoire(plateau):
	"""Réalise une insertion aleatoire d'une carte sur le plateau
	"""
	dimension = plateau.dimension
	carte_a_inserer = plateau.carte_jouable
	positions_possibles_insertion= [[x_pos,y_pos] for x_pos in range(1,dimension-1,2) for y_pos in [0,dimension-1]]+[[x_pos,y_pos] for y_pos in range(1,dimension-1,2) for x_pos in [0,dimension-1]]
	#choix de la position aléatoire
	alea_position= rd.randint(0,(len(positions_possibles_insertion)-1))
	position_aleatoire = positions_possibles_insertion[alea_position]
	
	#choix de l'orientation aléatoire
	alea_orientation = rd.randint(0,3)
	carte_a_inserer.orientation = alea_orientation
	
	#insertion sur une position aléatoire
	plateau.inserer_carte(carte_a_inserer,position_aleatoire)
	

def evaluation_plateau(plateau):
	"""Fonction qui renvoie une évaluation de la situation du joueur actif
	---
	return evaluation - int - minimum de la différence entre le score du joueur actif et celui des autres joueurs	
	"""
	liste_joueurs = plateau.liste_joueurs
	id_joueur_actif = plateau.joueur_actif
	joueur_actif = liste_joueurs[id_joueur_actif - 1]
	score_joueur_actif = joueur_actif.score
	evaluation = 5000 #valeur élevée pour trouver un minimum à coup sûr
	
	#calcul de l'évaluation
	for joueur in liste_joueurs:
		if joueur.id != id_joueur_actif:
			diff_score = score_joueur_actif - joueur.score
			if evaluation > diff_score:
				evaluation = diff_score
	return evaluation

def IA_MCTS(plateau, profondeur_insertion = 2, nb_simulations_insertion = 50, profondeur_chemin = 5, nb_simulations_chemins = 50):
	"""Fonction qui réalise une exploration du jeu pour le joueur actif
	---
	profondeur: int -- nombre de tours de jeu explorés (i.e pour lequel chaque joueur du plateau joue)
	nb_simultations: int -- nombre d'explorations réalisées
	=> L'exploration pour trouver l'insertion optimale et le chemin optimal (à partir de l'insertion optimale) se fait en 2 temps, d'où la multiplicité 
	des paramètres
	---
	renvoie
	---
	Cette fonction s'articule en 2 parties
	1. une première partie qui parcourt toutes les positions possibles pour l'insertion de carte
	et renvoie une insertion optimale
	2. une seconde partie qui réexplore les différents chemins possibles à partir de cette insertion optimale
	"""
	### PARTIE 1: RECHERCHE DE L'INSERTION OPTIMALE
	
	dimension = plateau.dimension
	#liste de toutes les positions où l'on peut effectuer une insertion
	positions_possibles_insertion= [[x_pos,y_pos] for x_pos in range(1,dimension-1,2) for y_pos in [0,dimension-1]]+[[x_pos,y_pos] for y_pos in range(1,dimension-1,2) for x_pos in [0,dimension-1]]
	#liste de toutes les orientations possibles
	liste_orientations = [i for i in range(4)]
	nb_tours_joueur = plateau.nb_joueurs*profondeur_insertion
	
	#dico stockant les évaluations pour chaque couple (x_insertion,y_insertion, orientation) où x et y sont les coordonnées où la carte a été insérée
	dico_insertions ={}
	
	#parcours de toutes les positions possibles
	for position in positions_possibles_insertion:
		#pour chacune des positions, on parcourt toutes les orientations
		for orientation in liste_orientations:
			x_position, y_position = position
			dico_insertions[(x_position,y_position,orientation)] = 0
			for iteration in range(nb_simulations_insertion):
				#copie du plateau sur lequel on va effectuer des modifs
				plateau_recherche = copy.deepcopy(plateau)
				#1er tour de jeu, l'insertion est déjà déterminée
				carte_jouable = plateau_recherche.carte_jouable
				carte_jouable.orientation = orientation
				plateau_recherche.inserer_carte(carte_jouable,position)
				#on réalise ensuite un tour de jeu aléatoire
				chemin_aleatoire = deplacement_aleatoire(plateau_recherche)
				validation_deplacement(plateau_recherche, chemin_aleatoire)
				plateau_recherche.changer_joueur()
				#on réalise ensuite les tours de jeu des joueurs successivement, de manière aléatoire
				for tour in range(1,nb_tours_joueur):
					insertion_carte_aleatoire(plateau_recherche)
					chemin_aleatoire = deplacement_aleatoire(plateau_recherche)
					validation_deplacement(plateau_recherche, chemin_aleatoire)
					plateau_recherche.changer_joueur()
				#mise à jour du score de cette insertion
				evaluation = evaluation_plateau(plateau_recherche)
				dico_insertions[(x_position,y_position, orientation)]+= evaluation/nb_simulations_insertion

	#recuperation de la suggestion d'insertion
	clef_dico_suggeree = max(dico_insertions, key = dico_insertions.get)
	position_insertion_optimale = [clef_dico_suggeree[0],clef_dico_suggeree[1]]
	orientation_optimale = clef_dico_suggeree[2]
	evaluation_insertion =  dico_insertions[clef_dico_suggeree]
	
	### PARTIE 2: RECHERCHE DU CHEMIN OPTIMAL A PARTIR DU POINT D'INSERTION OPTIMAL
	nb_tours_joueur = plateau.nb_joueurs*profondeur_chemin
	plateau_rch_chemin = copy.deepcopy(plateau)
	#insertion optimale de la carte selon le MCTS
	carte_jouable = plateau_rch_chemin.carte_jouable
	carte_jouable.orientation = orientation_optimale
	plateau_rch_chemin.inserer_carte(carte_jouable,position_insertion_optimale)
	
	liste_chemins = chemins_possibles(plateau_rch_chemin)
	
	#création d'un dico où sont stockés les scores des chemins dont la descendance va être explorée
	dico_score_chemin = {}
	
	#parcours de tous les chemins possibles
	for index_chemin in range(len(liste_chemins)):
		#initialisation du score des chemins à 0
		dico_score_chemin[index_chemin] = 0
		chemin_explore = liste_chemins[index_chemin]
		for iteration in range(nb_simulations_chemins):
			plateau_recherche = copy.deepcopy(plateau_rch_chemin)
			#1er étape: on valide le chemin pré-défini dont on va évaluer la descendance
			validation_deplacement(plateau_recherche, chemin_explore)
			plateau_recherche.changer_joueur()
			#on réalise ensuite les tours de jeu des joueurs successivement, de manière aléatoire
			for tour in range(1,nb_tours_joueur):
				insertion_carte_aleatoire(plateau_recherche)
				chemin_aleatoire = deplacement_aleatoire(plateau_recherche)
				validation_deplacement(plateau_recherche, chemin_aleatoire)
				plateau_recherche.changer_joueur()
			#mise à jour du score de cette insertion
			evaluation = evaluation_plateau(plateau_recherche)
			dico_score_chemin[index_chemin]+= evaluation/nb_simulations_chemins
				
	#recuperation de la suggestion d'insertion
	clef_dico_chemin_suggere = max(dico_score_chemin, key = dico_score_chemin.get)
	deplacement_optimal = liste_chemins[clef_dico_chemin_suggere]
	evaluation_chemin =  dico_score_chemin[clef_dico_chemin_suggere]
	return position_insertion_optimale, orientation_optimale, deplacement_optimal
