import pygame
from pygame.locals import *
import numpy as np
import random as rd

BRIQUE = (132,46,27)
BLACK = (0,0,0)
GREY=(50,50,50)
WHITE=(255,255,255)
ORANGE=(190,46, 20)
pygame.init()

class Carte(object):
	"""Classe des cartes constituant le plateau"""
	def __init__(self,position,type_carte,orientation = 0,fixe=False):
		self.position = position #liste de la position sur la matrice du aplteau [x,y]
		self.type_carte = int(type_carte) #type de carte (1,2,3)
		self.orientation = int(orientation) #entre 0,1,2,3
		self.fantome = 0 #numero du fantome présent sur la carte, vaut 0 si pas de fantome
		self.pepite = True #toutes les cartes possèdent une pépite en debut de jeu
		self.chasseur = 0 #id du chasseur présent sur la carte, 0 par défaut
		self.fixe=fixe

class Fantome(object):
	"""Fantomes"""
	def __init__(self, numero,position):
		self.numero = numero #numero du fantome
		self.position = position #liste [x,y] de sa position sur la matrice du plateau
		self.attrape = False #attrapé ou non

class Chasseur(object):
	"""Joueurs"""
	def __init__(self,id,position):
		self.id = id
		self.position=position
		'''if self.id==1:
			self.position=[740,240]
		elif self.id==2:
			self.position=[940,240]
		elif self.id==3:
			self.position=[740,440]
		elif self.id==4:
			self.position=[940,440]'''
		self.mission = []
		self.pepite = 0
		self.score = 0
		self.joker = True
		self.fantome = []
		self.mouv_possibles = [] #à deduire du type et de l'orientation de la carte


class Plateau(object):
	""" Plateau de jeu """
	def __init__(self, dimension=7):
		self.dimension = dimension #dimension du plateau

	def dessine_pepite (self, Carte):
		if Carte.pepite==True:
			pepite = pygame.image.load('images/persos/pepite.png').convert_alpha()
			self.maSurface.blit(pepite,(Carte.position[0]+40,Carte.position[1]+40))

	'''def dessine_fantome (self, Carte, Fantome):
		if Carte.fantome==True:
			fantome = pygame.image.load('fantome.png').convert_alpha()
			self.maSurface.blit((Carte.position[0]+70,Carte.position[1]+10))'''

	'''def dessine_chasseur (self, Carte, Chasseur):
		if Carte.chasseur==1:
			chasseur = pygame.image.load('Chasseur1.png').convert_alpha()
			self.maSurface.blit(chasseur,(Chasseur.position[0],Chasseur.position[1]))
		elif Carte.fantome==2:
			chasseur = pygame.image.load('Chasseur2.png').convert_alpha()
			self.maSurface.blit(chasseur,(Chasseur.position[0],Chasseur.position[1]))
		elif Carte.fantome==3:
			chasseur = pygame.image.load('Chasseur3.png').convert_alpha()
			self.maSurface.blit(chasseur,(Chasseur.position[0],Chasseur.position[1]))
		elif Carte.fantome==4:
			chasseur = pygame.image.load('Chasseur4.png').convert_alpha()
			self.maSurface.blit(chasseur,(Chasseur.position[0],Chasseur.position[1]))'''

	"Créer les cartes et leurs murs"
	def dessine_carte(self,Carte):
		#Carte type 1
		if Carte.type_carte==1:
			if Carte.orientation==0 or Carte.orientation==2:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+4),(Carte.position[0]+100,Carte.position[1]+4),10)
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+95),(Carte.position[0]+100,Carte.position[1]+95),10)
			else:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+4,Carte.position[1]),(Carte.position[0]+4,Carte.position[1]+100),10)
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+95,Carte.position[1]),(Carte.position[0]+95,Carte.position[1]+100),10)
		#Carte type 2
		if Carte.type_carte==2:
			if Carte.orientation==0:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+4),(Carte.position[0]+100,Carte.position[1]+4),10)
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+4,Carte.position[1]),(Carte.position[0]+4,Carte.position[1]+100),10)
			elif Carte.orientation==1:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+4),(Carte.position[0]+100,Carte.position[1]+4),10)
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+95,Carte.position[1]),(Carte.position[0]+95,Carte.position[1]+100),10)
			elif Carte.orientation==2:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+95),(Carte.position[0]+100,Carte.position[1]+95),10)
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+95,Carte.position[1]),(Carte.position[0]+95,Carte.position[1]+100),10)
			else:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+95),(Carte.position[0]+100,Carte.position[1]+95),10)
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+4,Carte.position[1]),(Carte.position[0]+4,Carte.position[1]+100),10)
		#Carte type 3
		if Carte.type_carte==3:
			if Carte.orientation==0:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+4),(Carte.position[0]+100,Carte.position[1]+4),10)
			elif Carte.orientation==1:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+95,Carte.position[1]),(Carte.position[0]+95,Carte.position[1]+100),10)
			elif Carte.orientation==2:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0],Carte.position[1]+95),(Carte.position[0]+100,Carte.position[1]+95),10)
			else:
				pygame.draw.line(self.maSurface,BLACK,(Carte.position[0]+4,Carte.position[1]),(Carte.position[0]+4,Carte.position[1]+100),10)
		self.dessine_pepite(Carte)
		#self.dessine_fantome(Carte, Fantome)
		#self.dessine_chasseur(Carte,Chasseur)

	"Céer le plateau de jeu et positionne les différentes cartes (fixes et mobiles)"
	def dessine_plateau(self,Carte):
		espace=int(500)
		pixel_case=int(100)
		largeur=int((self.dimension*pixel_case)+espace)
		hauteur=int((self.dimension*pixel_case))
		self.maSurface = pygame.display.set_mode((largeur,hauteur))
		pygame.display.set_caption('La mine hantée')
		self.maSurface.fill(GREY)
		pygame.draw.rect(self.maSurface,ORANGE,(500,0,hauteur,hauteur))
		pygame.draw.rect(self.maSurface,ORANGE,(175,520,pixel_case,pixel_case))
		pygame.draw.rect(self.maSurface,WHITE,(169,514,pixel_case+12,pixel_case+12),10)
		#identification des cases fixes
		for i in range (espace, largeur,2*pixel_case):
			for j in range(0, hauteur, 2*pixel_case):
				pygame.draw.rect(self.maSurface,BRIQUE,(i,j,pixel_case,pixel_case))

		#placement des cartes fixes
			#1. placement des bords - sur les lignes
		orientation=0
		for ligne in range(0, hauteur,(self.dimension-1)*pixel_case):
			for col in range(espace+(2*pixel_case),largeur-pixel_case,2*pixel_case):
				carte=Carte([col,ligne], 3, orientation,True)
				plateau.dessine_carte(carte)
			orientation+=2

			#2. placement des bords - sur les colonnes
		orientation=3
		for col in range(espace,largeur,(self.dimension-1)*pixel_case):
			for ligne in range(2*pixel_case,hauteur-pixel_case,2*pixel_case):
				carte=Carte([col,ligne], 3, orientation,True)
				plateau.dessine_carte(carte)
			orientation-=2

			#3. placement des coins
		carte = Carte((espace,0), 2, 0,True)
		plateau.dessine_carte(carte)
		carte = Carte((largeur-pixel_case,0), 2, 1,True)
		plateau.dessine_carte(carte)
		carte = Carte((largeur-pixel_case,hauteur-pixel_case), 2, 2,True)
		plateau.dessine_carte(carte)
		carte = Carte((espace,hauteur-pixel_case), 2, 3,True)
		plateau.dessine_carte(carte)

			#4. placement du centre
		for col in range(espace+2*pixel_case,largeur-pixel_case, 2*pixel_case):
			for ligne in range(2*pixel_case, hauteur-pixel_case, 2*pixel_case):
				orientation = rd.randint(0,3)
				carte= Carte([col,ligne], 3, orientation,True)
				plateau.dessine_carte(carte)

		#placement des cartes aléatoires
		nb_cartes_fixes = ((self.dimension +  1)/2)**2
		#print(nb_cartes_fixes)
		nb_cartes_alea = self.dimension**2 - nb_cartes_fixes + 1
		#print(nb_cartes_alea)

		nb_type_1= round(nb_cartes_alea*0.38)
		nb_type_2= round(nb_cartes_alea*0.44)
		nb_type_3= int(nb_cartes_alea - nb_type_1 - nb_type_2)

			#on initialise une liste contenant les types de cartes, pour simuler le tirage aléatoire
		liste_types = [1 for k in range(nb_type_1)] + [2 for k in range(nb_type_2)] + [3 for k in range(nb_type_3)]

			#On parcourt les cases pour leur assigner aléatoirement un type de carte
			#1. parcours des lignes à rang pair (0,2,4 ..)
		for col in range(espace+pixel_case,largeur,2*pixel_case):
			for ligne in range(0,hauteur, 2*pixel_case):
					#on choisit un élément aléatoire de la liste
				alea=rd.randint(0,(len(liste_types)-1))
				type_carte = liste_types.pop(alea)
				orientation = rd.randint(0,3)
				carte = Carte([col,ligne], type_carte, orientation,False)
				plateau.dessine_carte(carte)


			#2. parcours des lignes à rang impair (1,3,5 ..)
		for col in range(espace,largeur, pixel_case):
			for ligne in range(pixel_case,hauteur, 2*pixel_case):
					#on choisit un élément aléatoire de la liste
				while len(liste_types)-1 >1:
					alea=rd.randint(0,(len(liste_types)-1))
					type_carte = liste_types.pop(alea)
					orientation = rd.randint(0,3)
					carte = Carte([col,ligne], type_carte, orientation,False)
					plateau.dessine_carte(carte)
				orientation = rd.randint(0,3)
				carte = Carte([col,ligne], liste_types[1], orientation,False)
				plateau.dessine_carte(carte)


		#carte restante
		carte_jouable =Carte([175,520], liste_types[0], 0,False)
		plateau.dessine_carte(carte_jouable)

		#Quadrillage
		for i in range (espace,largeur,pixel_case):
			pygame.draw.line(self.maSurface,GREY,(i,0),(i,hauteur))
		for j in range (0,hauteur,pixel_case):
			pygame.draw.line(self.maSurface,GREY,(espace,j),(largeur,j),2)

		fontObj = pygame.font.SysFont('arial',40)
		maSurfaceDeTexte = fontObj.render('Mission: ',True,WHITE)
		monRectangleDeTexte	 = maSurfaceDeTexte.get_rect()
		monRectangleDeTexte .topleft = (30,20)
		self.maSurface.blit(maSurfaceDeTexte,monRectangleDeTexte)

		maSurfaceDeTexte = fontObj.render('Nombre de pépites: ',True,WHITE)
		monRectangleDeTexte	 = maSurfaceDeTexte.get_rect()
		monRectangleDeTexte .topleft = (30,120)
		self.maSurface.blit(maSurfaceDeTexte,monRectangleDeTexte)

		maSurfaceDeTexte = fontObj.render('Fantômes attrapés: ',True,WHITE)
		monRectangleDeTexte	 = maSurfaceDeTexte.get_rect()
		monRectangleDeTexte .topleft = (30,200)
		self.maSurface.blit(maSurfaceDeTexte,monRectangleDeTexte)

		maSurfaceDeTexte = fontObj.render('Joker: ',True,WHITE)
		monRectangleDeTexte	 = maSurfaceDeTexte.get_rect()
		monRectangleDeTexte .topleft = (30,330)
		self.maSurface.blit(maSurfaceDeTexte,monRectangleDeTexte)

		maSurfaceDeTexte = fontObj.render('Carte: ',True,WHITE)
		monRectangleDeTexte	 = maSurfaceDeTexte.get_rect()
		monRectangleDeTexte .topleft = (30,510)
		self.maSurface.blit(maSurfaceDeTexte,monRectangleDeTexte)

		pygame.draw.rect(self.maSurface,WHITE,(60,400,370,70), 4)
		fontObj = pygame.font.SysFont('arial',60)
		maSurfaceDeTexte = fontObj.render('Score: ',True,WHITE)
		monRectangleDeTexte	 = maSurfaceDeTexte.get_rect()
		monRectangleDeTexte .topleft = (70,400)
		self.maSurface.blit(maSurfaceDeTexte,monRectangleDeTexte)



plateau=Plateau()
plateau.dessine_plateau(Carte)


inProgress = True

while inProgress:
	#plateau=Plateau()
	#if plateau.dimension % 2 == 1 and plateau.dimension >= 7:
	#plateau.dessine_plateau(Carte)
	#plateau.dessine_pepite()
	#else:
	#print("Veuillez rentrer un nombre de cartes impair et supérieur à 7.")
	for event in pygame.event.get():
		if event.type == QUIT:
			inProgress = False
	pygame.display.update()
pygame.quit()


