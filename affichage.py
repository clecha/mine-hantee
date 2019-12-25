# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 00:20:01 2019

@author: SARREGUEMINES
"""
import pygame
from variables import *
from main import terminate



def affiche_accueil():
	global gameDisplay
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
			if event.type == pygame.QUIT:
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
				
				#Gestion du bouton valider
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
		
def position_pixel(Carte, position=None):
	global espace
	marge = 5
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
		bouge = '_dark'
	elif Carte.position[0] in [0,Plateau.dimension-1] or Carte.position[1] in [0,Plateau.dimension-1] :
		bouge = '_hover'
		if hover:
			bouge = '_bright'
	else:
		bouge = ''

	# Affichage de la carte de type labyrinthe
	#Carte type 1
	if Carte.type_carte==1:
		if Carte.orientation==1 or Carte.orientation==3:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],90)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		else:
			gameDisplay.blit(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],(x_pixel,y_pixel))
	#Carte type 2
	if Carte.type_carte==2:
		if Carte.orientation==0:
			gameDisplay.blit(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],(x_pixel,y_pixel))
		elif Carte.orientation==3:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],90)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		elif Carte.orientation==2:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],180)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		else:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],270)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
	#Carte type 3
	if Carte.type_carte==3:
		if Carte.orientation==0:
			gameDisplay.blit(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],(x_pixel,y_pixel))
		elif Carte.orientation==3:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],90)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		elif Carte.orientation==2:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],180)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		else:
			carte_rotate=pygame.transform.rotate(IMAGES_DICT['carte'+str(Carte.type_carte)+bouge],270)
			gameDisplay.blit(carte_rotate,(x_pixel,y_pixel))
		

	#Affichage de la pépite
	if Carte.pepite == True:
		gameDisplay.blit(IMAGES_DICT['pepite'],(x_pixel+40,y_pixel+40))	

	#Affichage du chasseur
	chasseur = Carte.chasseur
	if chasseur != 0:
		id_chasseur = chasseur.id
		#print(id_chasseur)
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
	print("init plateau")
	pixel_case=int(WINHEIGHT/plateau.dimension)
	
	#change l'échelle des images
	IMAGES_DICT={'pepite': pygame.transform.scale(pygame.image.load('images/persos/pepite.png'),(int(pixel_case/6),int(pixel_case/6))),
		'chasseur1': pygame.transform.scale(pygame.image.load('images/persos/chasseur1.png').convert_alpha(),(int(pixel_case*2/3),int(pixel_case*2/3))),
		'chasseur2': pygame.transform.scale(pygame.image.load('images/persos/chasseur2.png'),(int(pixel_case*2/3),int(pixel_case*2/3))),
		'chasseur3': pygame.transform.scale(pygame.image.load('images/persos/chasseur3.png'),(int(pixel_case*2/3),int(pixel_case*2/3))),
		'chasseur4': pygame.transform.scale(pygame.image.load('images/persos/chasseur4.png'),(int(pixel_case*2/3),int(pixel_case*2/3))),
		'fantome': pygame.transform.scale(pygame.image.load('images/persos/fantome.png'),(int(pixel_case*3/5),int(pixel_case*3/5))),	
		'carte1' : pygame.transform.scale(pygame.image.load('images/cartes/type1.png').convert_alpha(),(pixel_case,pixel_case)),
		'carte2' : pygame.transform.scale(pygame.image.load('images/cartes/type2.png').convert_alpha(),(pixel_case,pixel_case)),
		'carte3' : pygame.transform.scale(pygame.image.load('images/cartes/type3.png').convert_alpha(),(pixel_case,pixel_case)),
		'carte1_dark': pygame.transform.scale(IMAGES_DICT['carte1_dark'],(pixel_case,pixel_case)),
		'carte2_dark': pygame.transform.scale(IMAGES_DICT['carte2_dark'],(pixel_case,pixel_case)),
		'carte3_dark': pygame.transform.scale(IMAGES_DICT['carte3_dark'],(pixel_case,pixel_case)),
        'carte1_bright' : pygame.transform.scale(IMAGES_DICT['carte1_bright'],(pixel_case,pixel_case)),
        'carte2_bright' : pygame.transform.scale(IMAGES_DICT['carte2_bright'],(pixel_case,pixel_case)),
        'carte3_bright' : pygame.transform.scale(IMAGES_DICT['carte3_bright'],(pixel_case,pixel_case)),
        'carte1_hover' : pygame.transform.scale(IMAGES_DICT['carte1_hover'],(pixel_case,pixel_case)),
        'carte2_hover' : pygame.transform.scale(IMAGES_DICT['carte2_hover'],(pixel_case,pixel_case)),
        'carte3_hover' : pygame.transform.scale(IMAGES_DICT['carte3_hover'],(pixel_case,pixel_case)),
		'fleche1': pygame.image.load('images/fleche1.png'),
		'fleche2': pygame.image.load('images/fleche2.png')
			 }
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
	'''l=[(10,20),(255,20),(10,265),(255,265)] #liste des positions du texte
	m=[(170,0),(425,0),(170,245),(425,245)]	
	i=0
	for j in dico_joueurs.values():
		
		gameDisplay.blit(IMAGES_dict['chasseur'+str(j.id)],(m[i][0],m[i][1]))
		
		fontObj = pygame.font.SysFont('arial',25)
		
		gameDisplayDeTexte = fontObj.render('Mission: '+(', '.join(str(elem) for elem in j.mission),True,WHITE)
		monRectangleDeTexte	 = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte .topleft = (l[i][0],l[i][1])
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
		
	
		gameDisplayDeTexte = fontObj.render('Nombre de pépites: '+str(j.pepite),True,WHITE)
		monRectangleDeTexte	 = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte .topleft = (l[i][0],l[i][1]+55)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
	
		gameDisplayDeTexte = fontObj.render('Fantômes attrapés: '+(', '.join(str(elem) for elem in j.fantome),True,WHITE)
		monRectangleDeTexte	 = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte .topleft = (l[i][0],l[i][1]+110)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
	
		gameDisplayDeTexte = fontObj.render('Joker: ' + j.joker,True,WHITE)
		monRectangleDeTexte	 = gameDisplayDeTexte.get_rect()
		monRectangleDeTexte .topleft = (l[i][0],l[i][1]+185)
		gameDisplay.blit(gameDisplayDeTexte,monRectangleDeTexte)
		
		i+=1'''