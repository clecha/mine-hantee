# -*- coding: utf-8 -*-
"""
CONTENU
affiche_accueil() - Affichage de la page d'accueil
init_jeu() - Affichage de la page d'initialisation des paramètres du jeu
interface_choix_sauvegarde() - affiche la page de reprise des sauvegardes
position_pixel() - Permet d'obtenir la position x,y en pixel d'une carte du plateau 
dessine_carte() - Permet de dessiner une carte
init_affichage_plateau() - Init du plateau (juste le fond, sans les cartes)
actualisation_affichage_plateau() - Actualisation du pateau (cartes seulement)
affichage_deplacement() - Affichage la trace du déplacement d'un joueur pdt son tour de jeu
carte_jouable_jouee() - Affiche une croix sur la carte jouable si elle a déjà été jouée (ie insérée) pdt le tour
affichage_fin_jeu() - Affiche la fin de jeu (scores et classement)
"""
import pygame
import os, sys, glob
from variables import *
from main import *
import classes as cl


def affiche_accueil():
	# global gameDisplay
	'''Fonction permettant l'affichage de l'écran d'accueil du jeu, ou on peut faire les choix suivants : nouveau jeu, reprendre, quitter
	-->: 'nouveau_jeu', 'reprendre_jeu' : c'est 2 valeurs sont utilisées dans main() pour appeler les fonctions adéquates
	/!\ il faut encore écrire l'éveneement cliquer sur reprendre le jeu 
	'''
#	gameDisplay = pygame.display.set_mode((WINWIDTH, WINHEIGHT),pygame.RESIZABLE)
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
		if bouton_nouveau_jeuRect.collidepoint(mouse):
			gameDisplay.blit(IMAGES_DICT['bouton_nouv_jeu_hover'],bouton_nouveau_jeu_hoverRect)
		else:
			gameDisplay.blit(IMAGES_DICT['bouton_nouv_jeu'],bouton_nouveau_jeuRect)		
		if bouton_reprendreRect.collidepoint(mouse):
			gameDisplay.blit(IMAGES_DICT['bouton_reprendre_hover'],bouton_reprendre_hoverRect)
		else:
			gameDisplay.blit(IMAGES_DICT['bouton_reprendre'],bouton_reprendreRect)			
		if bouton_quitterRect.collidepoint(mouse):
			gameDisplay.blit(IMAGES_DICT['bouton_quitter_hover'],bouton_quitter_hoverRect)
		else:
			gameDisplay.blit(IMAGES_DICT['bouton_quitter'],bouton_quitterRect)
		
		for event in pygame.event.get():
			if clic[0] and bouton_nouveau_jeuRect.collidepoint(mouse):
				return 'nouveau_jeu'
			elif clic[0] and bouton_reprendreRect.collidepoint(mouse):
				return 'reprendre_jeu'
			elif event.type == pygame.QUIT:
				return 'quitter'
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					terminate()
			elif clic[0] and bouton_quitterRect.collidepoint(mouse):
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
			if event.type == MOUSEBUTTONUP:
				if dim9Rect.collidepoint(mouse):
					if bouton_dim9 ==  IMAGES_DICT['choix_dim9_grey']:
						bouton_dim9 = IMAGES_DICT['choix_dim9']
						bouton_dim7 = IMAGES_DICT['choix_dim7_grey']
						dimension = 9
				if dim7Rect.collidepoint(mouse):
					if bouton_dim7 ==  IMAGES_DICT['choix_dim7_grey']:
						bouton_dim7 = IMAGES_DICT['choix_dim7']
						bouton_dim9 = IMAGES_DICT['choix_dim9_grey']
						dimension = 7					
				#Events choix humain/ordi joueur 1
				if boutonj1humRect.collidepoint(mouse):
					if bouton_j1_hum ==	 IMAGES_DICT['choix_hum_grey']:
						bouton_j1_hum = IMAGES_DICT['choix_hum']
						bouton_j1_ordi = IMAGES_DICT['choix_ordi_grey']
						joueur1 = 1
				if boutonj1ordiRect.collidepoint(mouse):
					if bouton_j1_ordi ==  IMAGES_DICT['choix_ordi_grey']:
						bouton_j1_ordi = IMAGES_DICT['choix_ordi']
						bouton_j1_hum =	 IMAGES_DICT['choix_hum_grey']
						joueur1 = 2
			   
				#clicabilité joueur 2
				if boutonj2humRect.collidepoint(mouse):
					if bouton_j2_hum ==	 IMAGES_DICT['choix_hum_grey']:
						bouton_j2_hum = IMAGES_DICT['choix_hum']
						bouton_j2_ordi = IMAGES_DICT['choix_ordi_grey']
						joueur2 = 1
				if boutonj2ordiRect.collidepoint(mouse):
					if bouton_j2_ordi ==  IMAGES_DICT['choix_ordi_grey']:
						bouton_j2_ordi = IMAGES_DICT['choix_ordi']
						bouton_j2_hum =	 IMAGES_DICT['choix_hum_grey']
						joueur2 = 2

				#Event joueur 3
				if boutonj3humRect.collidepoint(mouse):
					if bouton_j3_hum ==	 IMAGES_DICT['choix_hum_grey']:
						bouton_j3_hum = IMAGES_DICT['choix_hum']
						bouton_j3_ordi = IMAGES_DICT['choix_ordi_grey']
						joueur3 = 1
				if boutonj3ordiRect.collidepoint(mouse):
					if bouton_j3_ordi ==  IMAGES_DICT['choix_ordi_grey']:
						bouton_j3_ordi = IMAGES_DICT['choix_ordi']
						bouton_j3_hum =	 IMAGES_DICT['choix_hum_grey']
						joueur3 = 2
				
				#Events joueur 4
				if boutonj4humRect.collidepoint(mouse):
					if bouton_j4_hum ==	 IMAGES_DICT['choix_hum_grey']:
						bouton_j4_hum = IMAGES_DICT['choix_hum']
						bouton_j4_ordi = IMAGES_DICT['choix_ordi_grey']
						joueur4 = 1
				if boutonj4ordiRect.collidepoint(mouse):
					if bouton_j4_ordi ==  IMAGES_DICT['choix_ordi_grey']:
						bouton_j4_ordi = IMAGES_DICT['choix_ordi']
						bouton_j4_hum =	 IMAGES_DICT['choix_hum_grey']
						joueur4 = 2
				
				#Gestion du nombre de joueurs
				if ajoutJoueurRect.collidepoint(mouse) and nb_joueurs != 4:
					nb_joueurs += 1
					print('nb',nb_joueurs)
				if retireJoueurRect.collidepoint(mouse) and nb_joueurs != 2:
					nb_joueurs -= 1
					print('nbm',nb_joueurs)
				
				#Gestion du bouton valider // Renvoie True si le joueur accepte un nouveau jeu
				if validerRect.collidepoint(mouse):
					print('dim,j1,j2,j3,j4:',dimension, joueur1, joueur2, joueur3, joueur4)
					return {'dimension':dimension, 'nb_joueurs':nb_joueurs,'joueur1': joueur1, 'joueur2':joueur2, 'joueur3':joueur3, 'joueur4':joueur4}
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					terminate()
		
		pygame.display.update()
		FPSCLOCK.tick()
		
def interface_choix_sauvegarde():
	"""Fonction permettant d'afficher l'interface où la sauvegarde à partir de laquelle on veut jouer sera sélectionnée
	""" 
	#Sauvegarde sélectionnée par l'utilisateur
	sauvegarde_selectionnee = None
	envie_de_jouer = True
	
	#Initialisation des variables images
	titre_reprendre_jeu = IMAGES_DICT['titre_sauvegardes']
	text_save1 = IMAGES_DICT['save1']
	text_save2 = IMAGES_DICT['save2']
	text_save3 = IMAGES_DICT['save3']
	text_save4 = IMAGES_DICT['save4']
	button_save_vide = IMAGES_DICT['save_vide']
	bouton_reprendre = IMAGES_DICT['reprendre']
	bouton_reprendre_bright = IMAGES_DICT['reprendre_bright']
	
	#Initialisation des surfaces liées aux images
	titreRect = IMAGES_DICT['titre_sauvegardes'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4))
	save1Rect = text_save1.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20))
	save2Rect = text_save2.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20+75))
	save3Rect = text_save3.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20+2*75))
	save4Rect = text_save4.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20+3*75))
	bouton_reprendreRect = bouton_reprendre.get_rect(topright=(HALF_WINWIDTH+2*(save1Rect.width+10),WINHEIGHT-150))
	
	#Recuperation du chemin du fichier
	dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
	os.chdir(dirname)
	
	#Recuperation des noms de fichiers pour l'affichage et création des boutons + rectangles associés + les boutons pour les hovers // pour les sauvegardes existantes
	font = pygame.font.SysFont("comicsansms", 24)
	liste_bouton = []
	liste_bouton_hover = []
	liste_rect=[]
	liste_sauvegarde=[]
	#créations des boutons contenant des sauvegardes pleines
	for file in glob.glob("*.dat"):
		nom_sauvegarde = file[0:-4]
		button = font.render(nom_sauvegarde, True, (255, 255, 255),(80,80,80))
		buttonHover = font.render(nom_sauvegarde, True, (255, 255, 255),(51,255,102))
		rect = button.get_rect(center=(HALF_WINWIDTH*1.15+save1Rect.width, HALF_WINHEIGHT*11/20+75*len(liste_bouton)))
		liste_bouton+=[button]
		liste_bouton_hover+=[buttonHover]
		liste_rect+=[rect]
		liste_sauvegarde+=[nom_sauvegarde]
	
	#Création des boutons (non-cliquables) des sauvegardes vides
	nb_save_pleines = len(liste_bouton)
	liste_save_vides = []
	for num_save_vide in range(nb_save_pleines,4):
		save_videRect = button_save_vide.get_rect(center=(HALF_WINWIDTH*1.15+save1Rect.width, HALF_WINHEIGHT*11/20+75*num_save_vide))
		liste_save_vides+=[(button_save_vide,save_videRect)]
	
	#Initialisation de la condition d'affichage
	afficher = True
	#les deux booléens qui suivent permettent de gérer la sélection des sauvegardes
	selection_en_cours = False
	index_precedent = None
	
	while afficher:
		gameDisplay.fill(BLACK)
		
		#Affichage des surfaces fixes
		gameDisplay.blit(titre_reprendre_jeu,titreRect)
		gameDisplay.blit(text_save1,save1Rect)
		gameDisplay.blit(text_save2,save2Rect)
		gameDisplay.blit(text_save3,save3Rect)
		gameDisplay.blit(text_save4,save4Rect)
		
		#Affichage des boutons
		for index in range(len(liste_bouton)):
			gameDisplay.blit(liste_bouton[index],liste_rect[index])
			
		for button,rect in liste_save_vides:
			gameDisplay.blit(button,rect)
		gameDisplay.blit(bouton_reprendre,bouton_reprendreRect)

		#Récupération des events position de la souris et clic de la souris
		mouse = pygame.mouse.get_pos()
		clic = pygame.mouse.get_pressed()
				
		#Gestion des évènements
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				afficher = False
				envie_de_jouer = False
				plateau = None
			if event.type == MOUSEBUTTONUP:
				for index in range(len(liste_bouton)):
					#gestion de la collision des boutons (sauvegardes pleines) et de la souris
					if liste_rect[index].collidepoint(mouse):
						#lorsque l'on sélectionne un bouton, celui-ci devient vert ou inversement
						liste_bouton[index],liste_bouton_hover[index] = liste_bouton_hover[index], liste_bouton[index]
						
						#1er cas: pas de sélection en cours
						if not selection_en_cours:
							sauvegarde_selectionnee = liste_sauvegarde[index]
							selection_en_cours = True
						#2e cas: lorsque l'on clique sur un bouton différent du précédent, le bouton précédent reprend sa couleur originelle
						elif selection_en_cours and index != index_precedent:
							liste_bouton[index_precedent],liste_bouton_hover[index_precedent] = liste_bouton_hover[index_precedent], liste_bouton[index_precedent]
							selection_en_cours = True
							sauvegarde_selectionnee = liste_sauvegarde[index]
						#3e cas: on clique sur un bouton déjà sélectionnée -- cad qu'on déselectionne	
						elif selection_en_cours and index == index_precedent:
							sauvegarde_selectionnee = None
							selection_en_cours = False
							
						index_precedent = index
				
				#gestion du bouton "reprendre"
				if bouton_reprendreRect.collidepoint(mouse):
					#interaction possible que si une sélection est réalisée
					if selection_en_cours:
						plateau = charger_sauvegarde(sauvegarde_selectionnee)
						afficher = False
		
		#gestion du bouton reprendre // affichage en vert foncé lorsqu'une sauvegarde est selectionnée
		if selection_en_cours:
			bouton_reprendre = IMAGES_DICT['reprendre']
		else:
			bouton_reprendre = IMAGES_DICT['reprendre_bright']
		
		pygame.display.update()
		FPSCLOCK.tick()
	return envie_de_jouer, plateau

def sauvegarde_pdt_partie(plateau):
	"""Fonction permettant d'afficher l'interface où l'on pourra faire une sauvegarde pendant la partie
		---
		plateau: prend en entrée le plateau à sauvegarder
		--- 
		retourne:
		retour_au_jeu: variable retournée à la fin de la fonction, permet de relancer tour_de_jeu si l'utilisateur sort de l'interface
	""" 
	#Sauvegarde sélectionnée par l'utilisateur
	sauvegarde_selectionnee = None
	#variable retournée à la fin de la fonction, permet de relancer tour_de_jeu si l'utilisateur sort de l'interface
	retour_au_jeu = False
	#Initialisation des variables images
	titre_sauvegarde_jeu = IMAGES_DICT['titre_sauvegardes']
	text_save1 = IMAGES_DICT['save1']
	text_save2 = IMAGES_DICT['save2']
	text_save3 = IMAGES_DICT['save3']
	text_save4 = IMAGES_DICT['save4']
	button_save_vide = IMAGES_DICT['save_vide']
	bouton_sauvegarde = IMAGES_DICT['sauvegarder']
	bouton_sauvegarde_bright = IMAGES_DICT['sauvegarder_bright']
	save_vide_hover = IMAGES_DICT['save_vide_hover']
	bouton_retour = IMAGES_DICT['bouton_retour']
	
	#Initialisation des surfaces liées aux images
	titreRect = IMAGES_DICT['titre_sauvegardes'].get_rect(center=(HALF_WINWIDTH, HALF_WINHEIGHT/4))
	save1Rect = text_save1.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20))
	save2Rect = text_save2.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20+75))
	save3Rect = text_save3.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20+2*75))
	save4Rect = text_save4.get_rect(center=(HALF_WINWIDTH*0.9, HALF_WINHEIGHT*11/20+3*75))
	bouton_sauvegardeRect = bouton_sauvegarde.get_rect(topright=(HALF_WINWIDTH+2*(save1Rect.width+10),WINHEIGHT-150))
	bouton_retourRect = bouton_retour.get_rect(topright=(HALF_WINWIDTH+10,WINHEIGHT-150))
	
	#Recuperation du chemin du fichier
	dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
	os.chdir(dirname)
	
	#Recuperation des noms de fichiers pour l'affichage et création des boutons + rectangles associés + les boutons pour les hovers // pour les sauvegardes existantes
	font = pygame.font.SysFont("comicsansms", 24)
	liste_bouton = []
	liste_bouton_hover = []
	liste_rect=[]
	liste_sauvegarde=[]
	#créations des boutons contenant des sauvegardes pleines
	for file in glob.glob("*.dat"):
		nom_sauvegarde = file[0:-4]
		button = font.render(nom_sauvegarde, True, (255, 255, 255),(80,80,80))
		buttonHover = font.render(nom_sauvegarde, True, (255, 255, 255),(51,255,102))
		rect = button.get_rect(center=(HALF_WINWIDTH*1.15+save1Rect.width, HALF_WINHEIGHT*11/20+75*len(liste_bouton)))
		liste_bouton+=[button]
		liste_bouton_hover+=[buttonHover]
		liste_sauvegarde+=[nom_sauvegarde]
		liste_rect+=[rect]
	
	#Création des boutons (cliquables) des sauvegardes vides
	nb_save_pleines = len(liste_bouton)
	liste_save_vides = []
	for num_save_vide in range(nb_save_pleines,4):
		save_videRect = button_save_vide.get_rect(center=(HALF_WINWIDTH*1.15+save1Rect.width, HALF_WINHEIGHT*11/20+75*num_save_vide))
		liste_bouton+=[button_save_vide]
		liste_rect+=[save_videRect]
		liste_bouton_hover+=[save_vide_hover]
		liste_sauvegarde+=[None]
	
	#Initialisation de la condition d'affichage
	afficher = True
	#les deux booléens qui suivent permettent de gérer la sélection des sauvegardes
	selection_en_cours = False
	index_precedent = None
	
	while afficher:
		gameDisplay.fill(BLACK)
		
		#Affichage des surfaces fixes
		gameDisplay.blit(titre_sauvegarde_jeu,titreRect)
		gameDisplay.blit(text_save1,save1Rect)
		gameDisplay.blit(text_save2,save2Rect)
		gameDisplay.blit(text_save3,save3Rect)
		gameDisplay.blit(text_save4,save4Rect)
		
		#Affichage des boutons 
		for index in range(len(liste_bouton)):
			gameDisplay.blit(liste_bouton[index],liste_rect[index])
		gameDisplay.blit(bouton_sauvegarde,bouton_sauvegardeRect)
		gameDisplay.blit(bouton_retour,bouton_retourRect)

		#Récupération des events position de la souris et clic de la souris
		mouse = pygame.mouse.get_pos()
		clic = pygame.mouse.get_pressed()
				
		#Gestion des évènements
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				afficher = False
				sauvegarde_selectionnee = None
			if event.type == MOUSEBUTTONUP:
				for index in range(len(liste_bouton)):
					#gestion de la collision des boutons (sauvegardes pleines) et de la souris
					if liste_rect[index].collidepoint(mouse):
						#lorsque l'on sélectionne un bouton, celui-ci devient vert ou inversement
						liste_bouton[index],liste_bouton_hover[index] = liste_bouton_hover[index], liste_bouton[index]
						
						#1er cas: pas de sélection en cours
						if not selection_en_cours:
							sauvegarde_selectionnee = liste_sauvegarde[index]
							selection_en_cours = True
						#2e cas: lorsque l'on clique sur un bouton différent du précédent, le bouton précédent reprend sa couleur originelle
						elif selection_en_cours and index != index_precedent:
							liste_bouton[index_precedent],liste_bouton_hover[index_precedent] = liste_bouton_hover[index_precedent], liste_bouton[index_precedent]
							selection_en_cours = True
							sauvegarde_selectionnee = liste_sauvegarde[index]
						#3e cas: on clique sur un bouton déjà sélectionnée -- cad qu'on déselectionne	
						elif selection_en_cours and index == index_precedent:
							sauvegarde_selectionnee = None
							selection_en_cours = False
							
						index_precedent = index
				
				#gestion du bouton "sauvegarde"
				if bouton_sauvegardeRect.collidepoint(mouse):
					#interaction possible que si une sélection est réalisée
					if selection_en_cours:
						afficher = False
						#sauvegarde du plateau et délétion éventuelle si une sauvegarde non vide est sélectionnée
						sauvegarde(plateau)
						delete_sauvegarde(sauvegarde_selectionnee)
						retour_au_jeu = True
				if bouton_retourRect.collidepoint(mouse):
					afficher = False
					sauvegarde_selectionnee = None
					retour_au_jeu = True
		
		#gestion du bouton sauvegarde // affichage en vert foncé lorsqu'une sauvegarde est selectionnée
		if selection_en_cours:
			bouton_sauvegarde = IMAGES_DICT['sauvegarder']
		else:
			bouton_reprendre = IMAGES_DICT['sauvegarder_bright']
			

		pygame.display.update()
		FPSCLOCK.tick()
	return retour_au_jeu
		


def position_pixel(Carte, position=None):
	global espace, marge
	
	# On vérifie que la carte est bien présente sur le plateau, i.e. que ce n'est pas la carte jouable
	if Carte.jouable == False and position != None:
		x_carte = position[0]
		y_carte = position[1]
		
		#Conversion de la position matricielle en position en pixel
		x_pixel = espace + x_carte * pixel_case + x_carte*marge/2
		y_pixel = y_carte * pixel_case + y_carte*marge/2
	
	# Carte hors plateau 
	else:
		x_pixel = 190
		y_pixel = 560
		
	return x_pixel, y_pixel
	
def dessine_carte(Plateau, Carte, position = None,hover=False):
	global gameDisplay, BLACK, espace, WINWIDTH, WINHEIGHT

	#obtention des coordonnées en pixels de la carte
	x_pixel, y_pixel = position_pixel(Carte, position)
#	print(x_pixel, y_pixel)
	if Carte.bougeable == False:
		couleur = '_dark'
	elif Carte.position[0] in [0,Plateau.dimension-1] or Carte.position[1] in [0,Plateau.dimension-1] :
		couleur = '_hover'
		if hover:
			couleur = '_bright'
	else:
		couleur = ''

	# Affichage de la carte de type labyrinthe
	#Carte type 1
	if Carte.type_carte==1:
		if Carte.orientation==1 or Carte.orientation==3:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],90)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		else:
			gameDisplay.blit(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],(x_pixel,y_pixel))
	#Carte type 2
	if Carte.type_carte==2:
		if Carte.orientation==0:
			gameDisplay.blit(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],(x_pixel,y_pixel))
		elif Carte.orientation==3:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],90)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		elif Carte.orientation==2:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],180)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		else:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],270)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
	#Carte type 3
	if Carte.type_carte==3:
		if Carte.orientation==0:
			gameDisplay.blit(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],(x_pixel,y_pixel))
		elif Carte.orientation==3:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],90)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		elif Carte.orientation==2:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],180)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		else:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+couleur],270)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		

	#Affichage de la pépite
	if Carte.pepite == True:
		gameDisplay.blit(IMAGES_DICT['pepite'],(x_pixel+40,y_pixel+40))	

	#Affichage du chasseur
	if Carte.chasseur != []:
		for id_chasseur in Carte.chasseur:
			gameDisplay.blit(IMAGES_DICT['chasseur'+str(id_chasseur)],(x_pixel+2*pixel_case/10,y_pixel+pixel_case/10))
		
	#Affichage du fantôme
	fantome = Carte.fantome
	if fantome != 0 :
		id_fantome = fantome.numero
		gameDisplay.blit(IMAGES_DICT['fantome'],(x_pixel+2,y_pixel+2))
		fontObj = pygame.font.SysFont('arial',20,bold=True)
		gameDisplayDeTexte=fontObj.render(str(id_fantome),True,BLACK)
		monRectangleDeTexte=gameDisplayDeTexte.get_rect()
		monRectangleDeTexte.topleft = (x_pixel+3*pixel_case/10,y_pixel+5)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
		
		

def init_affichage_plateau(plateau):
	global espace, pixel_case, gameDisplay, WINWIDTH, WINHEIGHT, IMAGES_DICT
	pixel_case=int(WINHEIGHT/plateau.dimension)
	
	#change l'échelle des images
	IMAGES_DICT['pepite'] = pygame.transform.scale(pygame.image.load('images/persos/pepite.png'),(int(pixel_case/6),int(pixel_case/6)))
	IMAGES_DICT['chasseur1']= pygame.transform.scale(pygame.image.load('images/persos/chasseur1.png').convert_alpha(),(int(pixel_case*2/3),int(pixel_case*2/3)))
	IMAGES_DICT['chasseur2'] = pygame.transform.scale(pygame.image.load('images/persos/chasseur2.png'),(int(pixel_case*2/3),int(pixel_case*2/3)))
	IMAGES_DICT['chasseur3'] = pygame.transform.scale(pygame.image.load('images/persos/chasseur3.png'),(int(pixel_case*2/3),int(pixel_case*2/3)))
	IMAGES_DICT['chasseur4'] = pygame.transform.scale(pygame.image.load('images/persos/chasseur4.png'),(int(pixel_case*2/3),int(pixel_case*2/3)))
	IMAGES_DICT['fantome'] = pygame.transform.scale(pygame.image.load('images/persos/fantome.png'),(int(pixel_case*3/5),int(pixel_case*3/5)))
	IMAGES_DICT['carte1'] = pygame.transform.scale(pygame.image.load('images/cartes/type1.png').convert_alpha(),(pixel_case,pixel_case))
	IMAGES_DICT['carte2'] = pygame.transform.scale(pygame.image.load('images/cartes/type2.png').convert_alpha(),(pixel_case,pixel_case))
	IMAGES_DICT['carte3'] = pygame.transform.scale(pygame.image.load('images/cartes/type3.png').convert_alpha(),(pixel_case,pixel_case))
	IMAGES_DICT['carte1_dark'] = pygame.transform.scale(IMAGES_DICT['carte1_dark'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2_dark'] = pygame.transform.scale(IMAGES_DICT['carte2_dark'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3_dark'] = pygame.transform.scale(IMAGES_DICT['carte3_dark'],(pixel_case,pixel_case))
	IMAGES_DICT['carte1_bright'] = pygame.transform.scale(IMAGES_DICT['carte1_bright'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2_bright'] = pygame.transform.scale(IMAGES_DICT['carte2_bright'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3_bright'] = pygame.transform.scale(IMAGES_DICT['carte3_bright'],(pixel_case,pixel_case))
	IMAGES_DICT['carte1_hover'] = pygame.transform.scale(IMAGES_DICT['carte1_hover'],(pixel_case,pixel_case))
	IMAGES_DICT['carte2_hover'] = pygame.transform.scale(IMAGES_DICT['carte2_hover'],(pixel_case,pixel_case))
	IMAGES_DICT['carte3_hover'] = pygame.transform.scale(IMAGES_DICT['carte3_hover'],(pixel_case,pixel_case))
	IMAGES_DICT['fleche1'] = pygame.image.load('images/plateau/fleche1.png')
	IMAGES_DICT['fleche2'] = pygame.image.load('images/plateau/fleche2.png')
	IMAGES_DICT['sauvegarder_plateau'] = pygame.image.load('images/plateau/sauvegarder_plateau.png')
	
	#Affichage du plateau et de tous les éléments qui ne changent pas au cours de la partie
	# 
	# gameDisplay = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
	# pygame.display.set_caption('La mine hantée')
	#remplissage du fond en gris
	gameDisplay.fill(GREY)
	#dessin du quadrillage en haut à gauche
	pygame.draw.line(gameDisplay,WHITE,(10,240),(490,240),5)
	pygame.draw.line(gameDisplay,WHITE,(240,10),(240,485),5)
	#écriture du titre au dessus de la carte jouable
	fontObj = pygame.font.SysFont('arial',40)
	gameDisplayDeTexte = fontObj.render('Carte: ',True,WHITE)
	monRectangleDeTexte	 = gameDisplayDeTexte.get_rect()
	monRectangleDeTexte .topleft = (10,550)
	gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
	#affichage des flèches
	gameDisplay.blit(IMAGES_DICT['fleche1'],(150,530))
	gameDisplay.blit(IMAGES_DICT['fleche2'],(275,530))
	#affichage du bouton sauvegarder // creation du rectangle
	sauvegarder_plateau = IMAGES_DICT['sauvegarder_plateau']
	rect_sauvegarder = sauvegarder_plateau.get_rect(topleft=(0,0))
	gameDisplay.blit(sauvegarder_plateau, rect_sauvegarder)	


	
def actualisation_affichage_plateau(plateau):
	global espace, pixel_case, gameDisplay, WINWIDTH, WINHEIGHT, dico_joueurs
	dimension = plateau.dimension
	matrice = plateau.matrice

	#Parcours du plateau pour afficher toutes les cases
	for ligne in range(dimension):
		for col in range(dimension):
			position = [ligne,col]
			carte = matrice[ligne][col]
			dessine_carte(plateau,carte, position)
				
	#affichage de la carte jouable
	carte_jouable = plateau.carte_jouable
	dessine_carte(plateau,carte_jouable)

	#affichage des données spécifiques à chaque joueur
	l=[(10,20),(255,20),(10,265),(255,265)] #liste des positions du texte
	m=[(170,0),(425,0),(170,245),(425,245)]	
	
	nb_joueurs=plateau.nb_joueurs
	for i in range (nb_joueurs):
		gameDisplay.blit(IMAGES_DICT['chasseur'+str(plateau.liste_joueurs[i].id)],(m[i][0],m[i][1]))
		fontObj = pygame.font.SysFont('arial',20)
		
		list=plateau.liste_joueurs[i].mission
		mission = ', '.join(str(elem) for elem in list)
		gameDisplayDeTexte = fontObj.render('Mission: '+str(mission),True,WHITE)
		monRectangleDeTexte = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte.topleft = (l[i][0],l[i][1]+10)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
		
		
		gameDisplayDeTexte = fontObj.render('Nombre de pépites: '+str(plateau.liste_joueurs[i].pepite),True,WHITE)
		monRectangleDeTexte = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte.topleft = (l[i][0],l[i][1]+55)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
		
		list=plateau.liste_joueurs[i].fantomes
		fantomes = ', '.join(str(elem) for elem in list)
		gameDisplayDeTexte = fontObj.render('Fantômes attrapés: '+str(fantomes),True,WHITE)
		monRectangleDeTexte = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte.topleft = (l[i][0],l[i][1]+110)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
			
		if plateau.liste_joueurs[i].joker: 
			joker=str('Disponible')
		else :
			joker=str('Indisponible')
		gameDisplayDeTexte = fontObj.render('Joker: '+str(joker),True,WHITE)
		monRectangleDeTexte = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte.topleft = (l[i][0],l[i][1]+155)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
		
		gameDisplayDeTexte = fontObj.render('Score: ' +str(plateau.liste_joueurs[i].score),True,WHITE)
		monRectangleDeTexte = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte.topleft = (l[i][0],l[i][1]+195)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
			
		
def affichage_deplacement(liste_cartes, plateau):
	global gameDisplay, pixel_case
	#VERIFICATION DE LA VALIDITE DU DEPLACEMENT
	size = 20
	for carte in liste_cartes:
		# position_carte = carte.position
		x_position, y_position = position_pixel(carte,carte.position)
		# print('aa',x_position, y_position)
		position_cercle = (int(x_position+pixel_case/2),int(y_position+pixel_case/2))
		# print('bb',int(x_position-pixel_case/2),int(y_position-pixel_case/2))
		# surface = plateau.matrice_surfaces[carte.position[0],carte.position[1]]
		# print('s',surface.top, surface.left)
		pygame.draw.circle(gameDisplay, (50,205,50, 100), position_cercle,int(size), 8)
	return plateau

def carte_jouable_jouee(plateau):
	global gameDisplay, pixel_case
	carte = plateau.carte_jouable
	marge = 5
	# x_topleft, y_topleft = position_pixel(carte)
	# x_topright, y_topright = x_topleft+pixel_case, y_topleft
	# x_bottomleft, y_bottomleft = x_topleft, y_topleft+pixel_case
	# x-bottomright, y_bottomright = x_topleft+pixel_case, y_topleft+pixel_case
	topleft = position_pixel(carte)
	topright = (topleft[0]+pixel_case-marge, topleft[1]+marge)
	bottomright = (topright[0]-marge,topright[1]+pixel_case-marge)
	bottomleft = (topleft[0]+marge,topleft[1]+pixel_case-marge)
	pygame.draw.line(gameDisplay,RED,topleft,bottomright,10)
	pygame.draw.line(gameDisplay,RED,topright,bottomleft,10)
	return plateau

def affichage_fin_jeu():
	#écriture du titre au dessus de la carte jouable
	fontObj = pygame.font.SysFont('arial',40)
	gameDisplayDeTexte = fontObj.render("C'est gagné ! ",True,WHITE)
	monRectangleDeTexte	 = gameDisplayDeTexte.get_rect()
	monRectangleDeTexte .topleft = (WINWIDTH/2,WINHEIGHT/2)
	gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			terminate()
		
## JOKER 
def i_a(noeudDepart, noeudFinal,plateau):
	"""Boucle while principale :
		- on met le meilleur noeud de la liste ouverte dans la liste fermée
		et on appelle la fonction qui va chercher ses voisins
		- lorsque le meilleur noeud correspond au noeud final on sort de la
		boucle pour afficher le chemin
		- si le noeud final n'est pas atteint et si la liste des noeud à
		explorer est vide : il n'y a pas de solution"""
	global listeOuverte,listeFermee,noeudCourant
	
	listeOuverte = []
	listeFermee = []
	
	#Initialistion du noeudCourant avec le noeud de départ
	noeudCourant = noeudDepart
	noeudCourant.coutH = Distance(noeudCourant,noeudFinal,plateau)
	noeudCourant.coutF = noeudCourant.coutH
	#On le met dans la liste ouverte
	listeOuverte.append(noeudCourant)
	
	while (not(noeudCourant.x_position == noeudFinal.x_position and noeudCourant.y_position == noeudFinal.y_position)
		and listeOuverte != []):
		# On choisi le meilleur noeud ce sera le noeud courant
		noeudCourant = MeilleurNoeud()
		listeFermee.append(noeudCourant)
		listeOuverte.remove(noeudCourant)
		
		# On va chercher les voisins du noeud courant
		AjouterCasesAdjacentes(noeudCourant,noeudFinal,plateau)
	RemonterListe()
	noeudArrivee=listeFermee[-1]
	print(noeudArrivee.x_position,noeudArrivee.y_position)
	return(noeudArrivee.x_position,noeudArrivee.y_position)
	
		
	# # on a atteint le noeud final
	# if noeudCourant.x_position == noeudFinal.x_position and noeudCourant.y_position == noeudFinal.y_position :
	# 	RemonterListe()
	# # On a pas atteint le noeud final et il n'y a plus de noeud à explorer
	# elif listeOuverte == []:
	# 	print('===========================================')
	# 	print('PAS DE SOLUTION')

def MeilleurNoeud():
	"""Fonction qui renvoie le meilleur noeud de la liste ouverte en fonction
	de son cout en F (plus long chemin)"""
	cout = 5000000
	noeud = None
	for n in listeOuverte:
		if n.coutF < cout:
			cout = n.coutF
			noeud = n
	#print(noeud.x_position)
	return noeud
	
def AjouterCasesAdjacentes(noeudCourant,noeudFinal,plateau):
	"""Fonction qui cherche tous les voisins possibles au noeud courant passé
	en parametre."""
	global listeOuverte,listeFermee
	dimension = plateau.dimension
	deplacements=['haut','bas','gauche','droite']
	#L=[]
	for direction in deplacements:
		if direction=='haut':
			dir=(0,-1)
		elif direction=='bas':
			dir=(0,1)
		elif direction=='gauche':
			dir=(-1,0)
		else: 
			dir=(1,0)
		coordSuivante=(noeudCourant.x_position+dir[0],noeudCourant.y_position+dir[1])
		#On vérifie qu'on sort pas de la matrice
		if coordSuivante[0] >= 0 and coordSuivante[0] <= dimension-1 and coordSuivante[1] >= 0 and coordSuivante[1] <= dimension-1:
			#On vérifie que le voisin n'est pas un obstacle
			if plateau.deplacement_possible(noeudCourant.x_position,noeudCourant.y_position, direction):
				#On crée un objet noeud au coordonnée du voisin
				noeudTemp = cl.Noeud(coordSuivante)
				#print('noeudTemppos')
				#print(noeudTemp.x_position)
				#Le noeud courant sera son parent
				noeudTemp.parent = noeudCourant
				#L.append(noeudTemp)
				#print('L')
				#print(L)
				#On s'assure que ce voisin ne fait pas deja parti de la liste fermée
				if noeudTemp.DejaPresentDansListe(listeFermee)==False:
					#On calcule ses couts
					noeudTemp.coutG = noeudTemp.parent.coutG + Distance(noeudTemp,noeudTemp.parent,plateau)
					# print('coutG')
					# print(noeudTemp.coutG)
					noeudTemp.coutH = Distance(noeudTemp,noeudFinal,plateau)
					# print('coutH')
					# print(noeudTemp.coutH)
					noeudTemp.coutF = noeudTemp.coutG + noeudTemp.coutH
					# print('coutF')
					# print(noeudTemp.coutF)
					#On regarde si ce voisin est déjà présent dans la liste ouverte
					n = noeudTemp.DejaPresentDansListe(listeOuverte)
					if n != False:
						#On compare son cout G avec celui de la liste ouverte(n)
						if noeudTemp.coutG < n.coutG:
							#Si il est inférieur on remplace les couts et le parent de n par ceux du voisin récemment trouvé
							n.parent = noeudCourant
							n.coutG = noeudTemp.coutG
							n.coutH = noeudTemp.coutH
							n.coutF = noeudTemp.coutF
							#Dans le cas contraire on ne change rien...
	
					#Ce voisin n'est pas déja présent dans le liste ouverte et donc on l'y ajoute
					else:
						listeOuverte.append(noeudTemp)
						# print('listeouverte')
						# print(listeOuverte[0].x_position)
						# print(listeOuverte[-1].x_position)
						# print('fin')


def Distance(noeud1,noeud2,plateau):
	"""Calcule des distances entre 2 noeuds suivant l'heuristique choisie"""
	a =  noeud2.x_position - noeud1.x_position
	b =  noeud2.y_position - noeud1.y_position
	#print('Distance')
	#print((a*a) + (b*b))
	#return ((a*a) + (b*b))
	carte = plateau.matrice[noeud2.x_position,noeud2.y_position]
	pepite= carte.pepite
	if pepite: 
		return ((a*a) + (b*b))
	else: 
		return ((a*a) + (b*b)+2)


def RemonterListe():
	"""Le but est atteint, cette fonction remonte le chemin d'ascendant en
	ascendant en partant du dernier noeud courant choisi"""
	size = 20
	chemin = []
	n = listeFermee[-1]
	chemin.append(n)
	n = n.parent
		### on crée des ronds pour chaque noeud appartenant au chemin gagnant
	while n.parent != n:
		chemin.append(n)
		x_pixel = espace + n.x_position * pixel_case + n.x_position*marge/2
		x=int(x_pixel+pixel_case/2)
		y_pixel = n.y_position * pixel_case + n.y_position*marge/2
		y=int(y_pixel+pixel_case/2)
		pygame.draw.circle(gameDisplay, (70,225,70,100), (x,y),int(size), 8)
		n = n.parent
	chemin.append(n)
	x_pixel = espace + n.x_position * pixel_case + n.x_position*marge/2
	x=int(x_pixel+pixel_case/2)
	y_pixel = n.y_position * pixel_case + n.y_position*marge/2
	y=int(y_pixel+pixel_case/2)
	pygame.draw.circle(gameDisplay, (70,225,70, 100), (x,y),int(size), 8)
	
def position_fantome(plateau, id_fantome):
	dimension=plateau .dimension 
	for x in range (dimension):
		for y in range (dimension):
			carte = plateau.matrice[x,y]
			fantome = carte.fantome
			if carte.fantome != 0:
				num_fantome = fantome.numero
				if num_fantome == id_fantome:
					return carte.position
					
