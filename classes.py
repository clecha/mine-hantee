"""
CONTENU
Classes du jeu:
-----------------
Plateau()
Carte()
Fantome()
Chasseur()
-----------------
"""

import numpy as np
import random as rd
import shelve as sh
import affichage as af
from variables import IMAGES_DICT

class Plateau(object):
	"""
	Plateau de jeu
	--------------
	Attributs:
	--------------
	fantomes_restants [int] - nombre de fantome non capturés
	dimension [int] - dimension du plateau, >= 7
	matrice [array] -  taille dimension * dimension, contient les objets Cartes du plateau
	matrice_surfaces [array] :  array de taille dimension * dimension, contenant les Rect associés aux Cartes
	carte_jouable [Carte] - la carte inserable qui est hors plateau
	joueur_actif [int] -- id du joueur actif
	liste_joueurs [list] - liste des objets Chasseur du plateau
	nb_joueurs [int] - entre 1 et 4 -- indique le nb de joueurs	
	deplacement_fait [booléen] -- indique si le déplacement du joueur actif a été réalisé ou non
	insertion_carte_faite [booléen] -- indique si le joueur actif a déjà inséré sa carte ou non
	gagne [booléen] -- indique si le jeu est encore en cours ou non
	--------------
	Fonctions:	
	--------------
	__init__
	actualisation_matrice_surfaces
	affichage_console
	inserer_carte
	sauvegarde
	charger_sauvegarde
	carte_a_cote
	deplacement_possible
	changer_joueur
	deplacer_joueur

	"""
	def __init__(self, dimension = 7, nb_joueurs = 4, liste_joueur_IA=[1,1,0,0],niveauIA=3):
		#liste joueur IA = 0 si le joueur n'existe pas, 1 si c'est un joueur, 2 si c'est un ordi
		self.fantomes_restants = 21
		self.dimension = dimension #dimension du plateau
		self.joueur_actif = 1
		self.liste_joueurs = []
		self.nb_joueurs = nb_joueurs
		self.deplacement_fait = False
		self.insertion_carte_faite = False
		self.gagne = False
		self.niveauIA = niveauIA
		if dimension % 2 == 1 and dimension >= 7:
		#création de la matrice contenant les objets cartes
			self.matrice = np.zeros((dimension,dimension), dtype= object)
			# PLACEMENT DES CARTES FIXES
			#rappel: init de carte = Carte(type_carte,jouable = False, orientation = 0, presence_pepite = True, bougeable = False, position = [0,0])
			#1. placement des bords - sur les lignes
			orientation=3
			for ligne in range(0,dimension, dimension-1):
				for col in range(2, dimension-1, 2):
					self.matrice[ligne][col] = Carte(3, False, orientation, True, False, [ligne,col])
					# print('attributs de la carte 1b '+str(ligne)+str(col)+' ', self.matrice[ligne][col].__dict__)
				orientation=1
									
			#2. placement des bords - sur les colonnes
			orientation=0
			for col in range(0,dimension, dimension-1):
				for ligne in range(2, dimension-1, 2):
					# print('#2:', ligne, col)
					self.matrice[ligne][col] = Carte(3, False, orientation, True, False,[ligne,col])
					# print('t2',self.matrice[ligne][col].murs)
				orientation+=2
	
			#3. placement des coins
			self.matrice[0][0] = Carte(2, False, 0, True, False,[0,0])
			self.matrice[0][dimension-1] = Carte(2, False, 3, True, False,[0,dimension-1])
			self.matrice[dimension-1][0] = Carte(2, False, 1, True, False,[dimension-1,0])
			self.matrice[dimension-1][dimension-1] = Carte(2, False, 2, True, False,[dimension-1,dimension-1])
			
			#4. placement du centre
			for ligne in range(2, dimension-2, 2):
				for col in range(2, dimension-2, 2):
					orientation = rd.randint(0,3)
					self.matrice[ligne][col] = Carte(3, False, orientation, True, False,[ligne,col])

			# PLACEMENT DES CARTES MOBILES
			nb_cartes_fixes = ((dimension +	 1)/2)**2
			nb_cartes_alea = dimension**2 - nb_cartes_fixes + 1
		
			nb_type_1= round(nb_cartes_alea*0.38)
			nb_type_2= round(nb_cartes_alea*0.44)
			nb_type_3= int(nb_cartes_alea - nb_type_1 - nb_type_2)
		
			#on initialise une liste contenant les types de cartes, pour simuler le tirage aléatoire
			liste_types = [1 for k in range(nb_type_1)] + [2 for k in range(nb_type_2)] + [3 for k in range(nb_type_3)]
			cpt_cartes_alea = nb_cartes_alea - 1
			
			#Liste des positions des cartes aléatoires, qui sera utilisé pour le placement des fantomes
			liste_pos_carte_alea = []
			
			#On parcourt les cases pour leur assigner aléatoirement un type de carte
			#1. parcours des lignes à rang pair (0,2,4 ..)
			for ligne in range(0, dimension, 2):
				for col in range(1, dimension, 2):
					#on choisit un élément aléatoire de la liste
					alea = rd.randint(0,cpt_cartes_alea)
					type_carte = liste_types.pop(alea)
					orientation = rd.randint(0,3)
					# print('#3:', ligne, col)
					self.matrice[ligne][col] = Carte(type_carte, False, orientation, True, True, [ligne,col])
					cpt_cartes_alea-=1
					liste_pos_carte_alea+=[[ligne,col]]
		
			#2. parcours des lignes à rang impair (1,3,5 ..)
			for ligne in range(1, dimension, 2):
				for col in range(0, dimension, 1):
					#on choisit un élément aléatoire de la liste
					alea = rd.randint(0,cpt_cartes_alea)
					type_carte = liste_types.pop(alea)
					orientation = rd.randint(0,3)
					# print('#4:', ligne, col)
					self.matrice[ligne][col] = Carte(type_carte, False, orientation, True, True, [ligne,col])
					cpt_cartes_alea-=1
					liste_pos_carte_alea+= [[ligne,col]]
		
		# CARTE JOUABLE
				self.carte_jouable = Carte(liste_types[0], True, 0, False, True, [None,None])
				
				
			# PLACEMENT DES JOUEURS
			# cree la liste des joueurs
			liste_id_joueurs = [k for k in range(1,self.nb_joueurs + 1)]
			
			# on crée une liste des fantomes qui servira pour l'attribut des missions
			liste_fantomes = [k for k in range(1,22)]
			rd.shuffle(liste_fantomes)
			
			#liste des positions possibles, que l'on va randomiser pour attribuer aléatoirement aux joueurs
			init = dimension // 2 - 1
			liste_pos_joueurs = [[init,init],[init,init+2],[init+2,init],[init+2,init+2]]
			rd.shuffle(liste_pos_joueurs)
			
			#on parcourt la liste des joueurs pour leur attribuer une position et une mission
			for id_joueur in liste_id_joueurs:
				ligne, col = liste_pos_joueurs[id_joueur-1]
				IA = liste_joueur_IA[id_joueur-1]
				#création du Chasseur() et ajout à la liste des joueurs
				mission=liste_fantomes[0:3]
				mission.sort()
				if IA == 1:
					self.liste_joueurs.append(Chasseur(id_joueur,[ligne,col],mission,False))
				else:
					self.liste_joueurs.append(Chasseur(id_joueur,[ligne,col],mission,True))
				#ajout de l'id du joueur à sa carte de départ
				self.matrice[ligne][col].chasseur += [id_joueur] #id du chasseur (type int)
				self.matrice[ligne][col].pepite = False #on enlève la pépite de ces cartes
				###alternative
				# self.matrice[ligne][col].chasseur = Chasseur(id_joueur,[ligne,col], liste_fantomes[0:3])
				# self.liste_joueurs.append(self.matrice[ligne][col].chasseur)
				
				#On retire les fantomes déjà attribués
				liste_fantomes.pop(0),liste_fantomes.pop(1),liste_fantomes.pop(2)
				
			
			#On place les fantomes aléatoirement avec la liste des positions liste_pos_carte_alea construite précédemment
			#On randomise la liste et on ne garde que les 21 premiers elements (positions) qui vont servir positionner les fantomes
			rd.shuffle(liste_pos_carte_alea)
			liste_pos_carte_alea=liste_pos_carte_alea[0:21]
			
			#On parcourt ensuite cette liste de position pour y placer les fantomes
			for k in range(1,22):
				ligne, col = liste_pos_carte_alea[k-1]
				self.matrice[ligne][col].fantome = Fantome(int(k))
			
		else:
			print("Veuillez rentrer un nombre de cartes impair et supérieur à 7.")

		#initialisation de la matrice des surfaces
		self.matrice_surfaces = np.zeros((dimension,dimension), dtype= object)
		self.actualisation_matrice_surfaces()

	def actualisation_matrice_surfaces(self):
		"""Actualisation de la matrice des surfaces get_rect associées aux cartes
		-->: /
		"""
		#parcourt de la matrice
		for i in range(self.dimension):
			for j in range(self.dimension):
				carte = self.matrice[i,j] #on recupere l'objet carte
				x,y = af.position_pixel(carte, (i,j)) #et ses coordonnées
				# print('#5:', i, j)
				self.matrice_surfaces[i,j] = IMAGES_DICT['carte'+str(carte.type_carte)].get_rect().move((x,y)) #création de l'objet Surface, placement dans la matrice 

	#affichage console
	def affichage_console(self):
		"""Fonction qui créée un affichage console du plateau en cours
		--> Utilisée pour faire des verifications lors du code surtout // pas utile à proprement parlé
		"""
#		try:
		dimension = self.dimension
		matrice_affichage_jouabilite = np.zeros((dimension,dimension), dtype=object)
		matrice_affichage_type_carte = np.zeros((dimension,dimension))
		matrice_affichage_orientation = np.zeros((dimension,dimension))
		matrice_affichage_chasseurs = np.zeros((dimension,dimension))
		matrice_affichage_fantomes = np.zeros((dimension,dimension))
		for col in range(dimension):
			for ligne in range(dimension):
				carte = self.matrice[ligne][col]
				id_joueur = carte.chasseur
				matrice_affichage_jouabilite[ligne][col] = carte.jouable
				matrice_affichage_type_carte[ligne][col] = carte.type_carte
				matrice_affichage_orientation[ligne][col] = carte.orientation
				if len(id_joueur)==0:
					matrice_affichage_chasseurs[ligne][col] = 0
				else:
					matrice_affichage_chasseurs[ligne][col] = carte.chasseur[0]
				fantome = carte.fantome
				if type(fantome) != int:
					matrice_affichage_fantomes[ligne][col] = carte.fantome.numero
				else:
					matrice_affichage_fantomes[ligne][col] = carte.fantome

		#print('matrice des jouabilites:\n', matrice_affichage_jouabilite)
		#print('matrice des types de carte:\n', matrice_affichage_type_carte)
		#print('matrice des orientations:\n', matrice_affichage_orientation)
		print('matrice des chasseurs:\n', matrice_affichage_chasseurs)
		#print('matrice des fantomes:\n', matrice_affichage_fantomes)
		#print('matrice des surfaces\n', self.matrice_surfaces)

#		except:
#			print('Il n y a aucun jeu en cours.')
#		pass

	def inserer_carte(self,carte_inseree,position):
		"""Fonction placant la carte en argument a la position en argument
		Paramètres
		-----------
		carte_inseree : la carte JOUABLE qui va être inseree
		position: liste de coordonnées [x,y] de la place d'insertion
		"""
		x_position = int(position[0])
		y_position = int(position[1])
		dimension = self.dimension

		#On initialise un booléen permettant de savoir si on insère sur une ligne ou sur une colonne
		insertion_colonne = True
		
		#1er test: on vérifie que la position d'insertion est valide, çad que l'on veut insérer la carte 
		#sur une bordure du plateau aux endroits spécifiques d'insertions
		positions_valides= [[x_pos,y_pos] for x_pos in range(1,dimension-1,2) for y_pos in [0,dimension-1]]+[[x_pos,y_pos] for y_pos in range(1,dimension-1,2) for x_pos in [0,dimension-1]]
		# print('positions valides', positions_valides)
		#l'insertion est effectuée uniquement si la case est présente dans positions_valides
		if position in positions_valides:
			#on insère sur une colonne en partant du haut du plateau (1ere ligne)
			if x_position == 0:
				liste_a_inserer, index_carte_a_pop = self.matrice[:,y_position], -1
				# deuxieme_carte = liste_a_inserer[0] #carte sur laquelle on vient de cliquer, il va falloir lui changer l'attribut bougeable
			#on insère sur une colonne en partant du bas du plateau (dernière ligne)
			elif x_position == dimension - 1:
				liste_a_inserer, index_carte_a_pop = self.matrice[:,y_position], 0
				# deuxieme_carte = liste_a_inserer[-1]
			#on insère sur une ligne en partant de la gauche du plateau (1ere colonne)
			elif y_position == 0:
				liste_a_inserer, index_carte_a_pop = self.matrice[x_position,:], -1
				# deuxieme_carte = liste_a_inserer[0]
				insertion_colonne = False
			#on insère sur une ligne en partant de la droite du plateau (derniere colonne)
			elif y_position == dimension - 1:
				liste_a_inserer, index_carte_a_pop = self.matrice[x_position,:], 0
				# deuxieme_carte = liste_a_inserer[-1]
				insertion_colonne = False
			
			#on retire l'élément qui a coulissé en dehors du plateau
			nvelle_carte_jouable = liste_a_inserer[index_carte_a_pop]
			liste_a_inserer = np.delete(liste_a_inserer, index_carte_a_pop)	
			
			#On vérifie la présence d'un fantome ou d'un joueur sur la carte qui a été sortie du tableau
			#on initialise un booleen qui permettra d'actualiser ou non la position du chasseur
			presence_chasseur = False
			#si la carte qui est sortie du plateau avait un fantome, on le déplace sur la carte qu'on insère
			if nvelle_carte_jouable.fantome !=0:
				carte_inseree.fantome = nvelle_carte_jouable.fantome
				nvelle_carte_jouable.fantome = 0
			#puis on fait de même pour les chasseurs
			if nvelle_carte_jouable.chasseur != []:
				carte_inseree.chasseur = nvelle_carte_jouable.chasseur
				# print('test1',carte_inseree.chasseur, nvelle_carte_jouable.chasseur)
				nvelle_carte_jouable.chasseur = []
				presence_chasseur = True
				#il faudra quand même actualiser la position du chasseur
			#de même pour la pépite
			if nvelle_carte_jouable.pepite:
				carte_inseree.pepite = nvelle_carte_jouable.pepite
				nvelle_carte_jouable.pepite = False

			#On insère en début de ligne/colonne car on enlève le dernier élément
			if index_carte_a_pop == -1:
				liste_a_inserer = np.append([carte_inseree], liste_a_inserer)
				index_chasseur = 0
			else:
				liste_a_inserer = np.append(liste_a_inserer, [carte_inseree])
				index_chasseur = -1
			
			#Modification de la colonne/ligne où a été inséré la nouvelle liste
			if insertion_colonne:
				self.matrice[:,y_position] = liste_a_inserer
				if presence_chasseur:
					carte = self.matrice[index_chasseur, y_position]
					for id_chasseur in carte.chasseur:
						chasseur = self.liste_joueurs[id_chasseur-1]
						#Actualisation de la position du chasseur dans l'objet chasseur
						chasseur.position = [index_chasseur, y_position]
			else:
				self.matrice[x_position,:] = liste_a_inserer
				if presence_chasseur:
					carte = self.matrice[x_position, index_chasseur]
					for id_chasseur in carte.chasseur:
						chasseur = self.liste_joueurs[id_chasseur-1]
						#Actualisation de la position du chasseur dans l'objet chasseur
						chasseur.position = [x_position, index_chasseur]
			
			#on actualise la nouvelle carte jouable
			self.carte_jouable = nvelle_carte_jouable #carte de bout de ligne/colonne "sort"
			
			#Actualisation de la jouabilité des cartes
			carte_inseree.jouable = False
			self.carte_jouable.jouable = True

			#Actualisation de la bougeabilité des cartes
			carte_inseree.bougeable = True #nouvelle carte insérer
			
			#Actualisation de la position de la carte nouvellement insérée
			carte_inseree.position = [x_position,y_position]
			#Actualisation de la matrice des surfaces
			self.actualisation_matrice_surfaces()
			#Mise à jour des indexs des cartes de la ligne/colonne changée
			nouvel_index=0
			if insertion_colonne:
				for x in self.matrice[:,y_position]:
					# print('apres',x.position[0])
					x.position[0] = nouvel_index
					# print('apres',x.position[0])
					nouvel_index+=1
					#actualisation de la position des chasseurs
					if len(x.chasseur)>0:
						for id_chasseur in x.chasseur:
							chasseur = self.liste_joueurs[id_chasseur - 1]
							chasseur.position = x.position
			else:
				for x in self.matrice[x_position,:]:
					# print('apres',x.position[1])
					x.position[1] = nouvel_index
					# print('apres',x.position[1])
					nouvel_index+=1
					#actualisation de la position des chasseurs
					if len(x.chasseur)>0:
						for id_chasseur in x.chasseur:
							chasseur = self.liste_joueurs[id_chasseur - 1]
							chasseur.position = x.position
			#Mise à jour de la position de la carte nouvellement jouable
			self.carte_jouable.position = [None,None]
			# print("test fin d'insertion",carte_inseree.position ,carte_inseree.chasseur)

	def carte_a_cote(self, x,y,direction):
		'''Fonction renvoyant la carte à côté de la carte présente
		x,y: position de la carte de départ, x  = colonne, y = ligne (axes pygame inversés !)
		direction : char
		Direction dans laquelle on regarde, valeurs possibles : gauche, droite, haut, bas
		-->: la carte à cote de la carte(x,y) pour la direction donnée
		'''
		if direction == 'gauche':
			if x == 0:
				carte_a_cote = self.matrice[self.dimension-1,y]
			else:
				carte_a_cote = self.matrice[x-1,y]
		elif direction == 'droite':
			if x == self.dimension-1:
				carte_a_cote = self.matrice[0,y]
			else:
				carte_a_cote = self.matrice[x+1,y]
		elif direction == 'haut':
			if y == 0:
				carte_a_cote = self.matrice[x,self.dimension-1]
			else:
				carte_a_cote = self.matrice[x,y-1]
		else: #bas
			if y == self.dimension-1:
				carte_a_cote = self.matrice[x,0]
			else:
				carte_a_cote = self.matrice[x,y+1]
		return carte_a_cote
	
	def deplacement_possible(self, x_position,y_position, direction):
		'''Evalue si le déplcement est possible.
		-->: bool
		'''
		# print('dp pos acctuelle',x_position,y_position)
		direction_opposee = {'haut':'bas','bas':'haut','gauche':'droite','droite':'gauche'}
		carte_actuelle = self.matrice[x_position, y_position]
		carte_visee = self.carte_a_cote(x_position, y_position,direction)
		# print('test deplacement', carte_visee)
		# print('murs carte actuelle',carte_actuelle.murs[direction])
		# print('murs visee', carte_visee.murs[direction_opposee[direction]])
		# print('attributs de la carte visee dans deplacement possible #7', carte_visee.__dict__)
		if carte_actuelle.murs[direction] == False and carte_visee.murs[direction_opposee[direction]] == False: #s'il n(y a pas de murs sur les deux cartes)
			return True
		else: #s'il y a un mur sur l'une des deux cartes
			return False
	
	def changer_joueur(self):
		if self.joueur_actif == self.nb_joueurs :
			self.joueur_actif = 1
		else:
			self.joueur_actif += 1
		self.deplacement_fait = False
		self.insertion_carte_faite = False
		

	def deplacer_joueur(self, id_joueur, direction): 
		chasseur = self.liste_joueurs[id_joueur-1]
		# print('1a id chasseur deplacement', chasseur.id)
		# print(chasseur)
		x,y = chasseur.position[0],chasseur.position[1]
		# print('xy',x,y)
		carte_depart = self.matrice[x,y]
		carte_visee = self.carte_a_cote(x,y,direction)
		# print(carte_depart,carte_visee)
		# print('murs #6', carte_visee.__dict__)
		# print(self.deplacement_possible(x,y,direction))
		if self.deplacement_possible(x,y,direction):
			#on enlève le joueur de la carte de départ
			# print('1b test dans deplacement joueur, carte depart: ', carte_depart.chasseur, 'id_joueur: ',id_joueur)
			carte_depart.chasseur.remove(id_joueur)
			#on l'ajoute à celle d'arrivée
			carte_visee.chasseur += [id_joueur]
			#on change les attrbuts du joueur
			chasseur.position = carte_visee.position
			# chasseur.bouger(direction)
			#vérification de la présence d'une pépite
			if carte_visee.pepite:
				chasseur.attraper_pepite(carte_visee)
				pepite_attrapee = True
			else:
				pepite_attrapee = False
			# print('deplacement fait')
			return carte_visee, pepite_attrapee
		else:
			return None, False


class Carte(object):
	"""Classe des cartes constituant le plateau
	----
	jouable: Booléen qui indique si la carte est jouable ou non (i.e. si elle est hors du plateau ou pas)
	bougeable : Booléen indiquant si la carte peut être bougée
	type_carte: entier entre 1 et 3
	orientation: entier entre 0 et 3
	fantome: entier entre 0 et 21 -- la valeur 0 indique l'absence de fantôme
	pepite = booléen - True par défaut, ce qui indique la présence d'une pépite
	chasseur = entier entre 0 et 4 -- la valeur 0 indique l'absence de chasseur"""
	def __init__(self,type_carte,jouable = False, orientation = 0, presence_pepite = True, bougeable = False, position = [0,0]):
		self.position = position
		self.jouable = jouable #Booléen indiquant si la carte est jouable ou non (i.e. si elle est hors plateau ou pas)
		self.bougeable = bougeable
		self.type_carte = int(type_carte) #type de carte (1,2,3)
		self.orientation = int(orientation) #entre 0,1,2,3
		self.fantome = 0 #fantome présent sur la carte, vaut 0 si pas de fantome
		self.pepite = presence_pepite #toutes les cartes possèdent une pépite en debut de jeu, sauf la carte jouable
		self.chasseur = [] #chasseur présent sur la carte, 0 par défaut
		self.murs = {}
		self.update_murs() #présence de mur a gauche, droite, en haut et bas de la carte

	def tourner(self,direction='droite'):
		"""Permet de tourner la carte d'un sens ou de l'autre en changeant la valeur de l'attribut orientation,
		qui doit être entre 0 et 3 (4 sens possibles).
		Paramètres
		----------
		direction : char
		==> valeurs possibles : 'gauche' ou 'droite'"""
		if self.orientation == 3 and direction == 'droite':
			self.orientation = 0
		elif self.orientation == 0 and direction == 'gauche':
			self.orientation = 3
		else:
			if direction == 'droite':
				self.orientation += 1
			else:
				self.orientation -= 1
		self.update_murs()
				
	def update_murs(self):
		'''Update les positions des murs en fonction du type de carte et de la position. Utilisé lors d'une rotation de carte.
		'''
		if self.type_carte == 1:
			if self.orientation in [1,3]:
				self.murs ={'haut':True, 'droite':False,'bas':True, 'gauche':False}
			elif self.orientation in [0,2]:
				self.murs = {'haut':False,'droite':True,'bas':False,'gauche':True}

		elif self.type_carte == 2:
			if self.orientation == 0:
				self.murs = {'haut':True, 'droite':False, 'bas':False, 'gauche':True}
			if self.orientation == 1:
				self.murs = {'haut':True, 'droite':True, 'bas':False, 'gauche':False}
			if self.orientation == 2:
				self.murs = {'haut':False, 'droite':True, 'bas':True, 'gauche':False}				
			if self.orientation == 3:
				self.murs = {'haut':False, 'droite':False, 'bas':True, 'gauche':True}
				
		elif self.type_carte == 3:
			if self.orientation == 0:
				self.murs = {'haut':True, 'droite':False, 'bas':False, 'gauche':False}
			if self.orientation == 1:
				self.murs = {'haut':False, 'droite':True, 'bas':False, 'gauche':False}
			if self.orientation == 2:
				self.murs = {'haut':False, 'droite':False, 'bas':True, 'gauche':False}				  
			if self.orientation == 3:
				self.murs = {'haut':False, 'droite':False, 'bas':False, 'gauche':True}
	
class Fantome(object):
	"""Fantomes
	---
	numero: entier identifiant le fantome
	attrape: booléen indiquant si le fantome a été attrapé ou non
	"""
	def __init__(self, numero):
		self.numero = numero #numero du fantome
		self.attrape = False #attrapé ou non

class Chasseur(object):
	"""Joueurs
	---
	identifiant: 
	position: liste de coordonnees [x,y]
	mission: liste d entiers correspondant aux numéros des fantomes à ingérer
	IA: booléen -- True si c'est un ordinateur, False sinon
	pepite: entier -- nombre de pépites ramassées par le chasseur
	score: entier -- score amassé par le chasseur
	joker : Booléen -- True si le chasseur dispose encore de son joker
	fantome: liste d entiers -- correspond aux fantomes amasses par le chasseur"""
	def __init__(self, identifiant,position,mission,IA):
		self.id = identifiant
		self.position = position
		self.mission = mission
		self.IA = IA
		self.pepite = 0
		self.score = 0
		self.joker = True
		self.fantomes = []

	def bouger(self,direction):
		"""Déplace le Chasseur en changeant la valeur de son attribut position
		'/!\' FONCTION INUTILE ? EN soit on peut s'en servir dans deplacer_joueur mais elle n'ajoute pas grand chose
		"""
		if direction == 'gauche':
			self.position[0] -= 1
		elif direction == 'droite':
			self.position[0] += 1
		elif direction == 'haut':
			self.position[1] -= 1
		if direction == 'bas':
			self.position[1] += 1

	def attraper_pepite(self,Carte):
		'''Augmente le nombre de pepite attrapées par le chasseur, enleve la pepite de la carte concernee'''
		if Carte.pepite:
			x_position, y_position = self.position
			self.pepite += 1
			self.score +=1
			#Mise à jour de la valeur de la pepite sur la carte où est présent le chasseur
			Carte.pepite = False

	def utiliser_joker(self):
		######instructions utilisation joker########
		self.joker = False
		pass

	def attraper_fantome(self,Plateau):
		'''Ajoute le numero du fantome à a liste des fantomes attrapés, enlève le fantome de la carte concernée
		Paramètres
		----------
		Plateau: objet de type plateau
		'''
		x_position, y_position = self.position
		#on recupere le fantome sur la case du plateau où est situé le chasseur
		carte = Plateau.matrice[x_position,y_position]
		fantome = carte.fantome
		if fantome !=0:
			num_fantome = fantome.numero
		fantome_attrapable = 22-Plateau.fantomes_restants
		#on verifie qu'un fantome existe sur la case et qu'il correspond au fantome attrapable
		if fantome != 0 and num_fantome == fantome_attrapable:
			#ajout du numero du fantome a la liste des fantomes collectés par le chasseur
			self.fantomes += [num_fantome]
			fantome.attrape = True
			carte.fantome = 0
			#si le fantome fait partie de la mission du chasseur, le score est actualise a +20, sinon à +5
			if num_fantome in self.mission:
				self.score+= 20
				if self.mission_complete():
					self.score += 40
			else:
				self.score+=5
			Plateau.fantomes_restants-=1
			return carte
		#Renvoie False si le fantome n'est pas attrapable (ou qu'il n'y a pas de fantome)
		else:
			return False

	def mission_complete(self):
		output = True
		for fantome in self.mission:
			if fantome not in self.fantomes:
				output = False
		return output

		
	##partie test
		
#1. test de la mise en place des cartes
#test = Plateau(nb_joueurs = 4)
#test.affichage_console()
#carte = test.carte_jouable
#print(carte.jouable)
##test.inserer_carte(carte, [0,2])
#test.affichage_console()
#print(carte.jouable)
#carte = test.carte_jouable
#print(carte.jouable)

#carte = test.carte_jouable
#test.inserer_carte(carte, [0,2])
#test.affichage_console()
		
