import numpy as np
import random as rd

class Plateau(object):
	"""
    Plateau de jeu
    """
	def __init__(self, dimension=7):
		self.dimension = dimension #dimension du plateau
		
		if dimension % 2 == 1 and dimension >= 7:
        #création de la matrice contenant les objets cartes
			self.matrice = np.zeros((dimension,dimension), dtype= object)

			#placement des cartes fixes
			
			#1. placement des bords - sur les lignes
			orientation=0
			for ligne in range(0,dimension, dimension-1):
				for col in range(2, dimension, 2):
					self.matrice[ligne][col] = carte([ligne,col], 3, orientation)
				orientation+=2
				
			#2. placement des bords - sur les colonnes
			orientation=3
			for col in range(0,dimension, dimension-1):
				for ligne in range(2, dimension, 2):
					self.matrice[ligne][col] = carte([ligne,col], 3, orientation)
				orientation-=2
					
			#3. placement des coins
			orientation=0
			for ligne in range(0,dimension, dimension-1):
				for col in range(0,dimension, dimension-1):
					self.matrice[ligne][col] = carte([ligne,col], 2, orientation)
					orientation+=1
			
			#4. placement du centre
			for ligne in range(2, dimension-2, 2):
				for col in range(2, dimension-2, 2):
					orientation = rd.randint(0,3)
					self.matrice[ligne][col] = carte([ligne,col], 3, orientation)

			#placement des cartes aléatoires
			nb_cartes_fixes = ((dimension +  1)/2)**2
			nb_cartes_alea = dimension**2 - nb_cartes_fixes + 1
		
			nb_type_1= round(nb_cartes_alea*0.38)
			nb_type_2= round(nb_cartes_alea*0.44)
			nb_type_3= int(nb_cartes_alea - nb_type_1 - nb_type_2)
		
			#on initialise une liste contenant les types de cartes, pour simuler le tirage aléatoire
			liste_types = [1 for k in range(nb_type_1)] + [2 for k in range(nb_type_2)] + [3 for k in range(nb_type_3)]
			cpt_cartes_alea = nb_cartes_alea - 1
		
			#On parcourt les cases pour leur assigner aléatoirement un type de carte
			#1. parcours des lignes à rang pair (0,2,4 ..)
			for ligne in range(0, dimension, 2):
				for col in range(1, dimension, 2):
					#on choisit un élément aléatoire de la liste
					alea = rd.randint(0,cpt_cartes_alea)
					type_carte = liste_types.pop(alea)
					orientation = rd.randint(0,3)
					self.matrice[ligne][col] = carte([ligne,col], type_carte, orientation)
					cpt_cartes_alea-=1
		
			#2. parcours des lignes à rang impair (1,3,5 ..)
			for ligne in range(1, dimension, 2):
				for col in range(0, dimension, 1):
					#on choisit un élément aléatoire de la liste
					alea = rd.randint(0,cpt_cartes_alea)
					type_carte = liste_types.pop(alea)
					orientation = rd.randint(0,3)
					self.matrice[ligne][col] = carte([ligne,col], type_carte, orientation)
					cpt_cartes_alea-=1
		
		#carte restante
				self.carte_jouable = carte(None, liste_types[0], 0)
			
		else:
			print("Veuillez rentrer un nombre de cartes impair et supérieur à 7.")
	
	#affichage consol
	def affichage_console(self):
		"""Fonction qui créée un affichage console du plateau en cours
		"""
		try:
			dimension = self.dimension
			matrice_affichage_positions=np.zeros((dimension,dimension), dtype=object)
			matrice_affichage_type_carte=np.zeros((dimension,dimension))
			matrice_affichage_orientation=np.zeros((dimension,dimension))
			for ligne in range(dimension):
				for col in range(dimension):
					carte = self.matrice[ligne][col]
					matrice_affichage_positions[ligne][col] = carte.position
					matrice_affichage_type_carte[ligne][col] = carte.type_carte
					matrice_affichage_orientation[ligne][col] = carte.orientation
					print('matrice des positions:', matrice_affichage_positions)
					print('matrice des types de carte:', matrice_affichage_type_carte)
					print('matrice des orientations:', matrice_affichage_orientation)
		except:
			print('Il n y a aucun jeu en cours.')
		pass

	def inserer_carte(self,carte,position):
		"""Fonction placant la carte en argument a la position en argument
		Paramètres
		-----------
		carte : int"""

	#Changement de carte jouable (celle en bout de la ligne/colonne qui bouge devient la nouvelle carte jouable)

	#Déplacement de la ligne/colonne

	#Insertion de la carte au la position en argument

	pass
		

class Carte(object):
	"""Classe des cartes constituant le plateau"""
	def __init__(self,position,type_carte,orientation = 0):
		self.position = position #liste de la position sur la matrice du aplteau [x,y]
		self.type_carte = int(type_carte) #type de carte (1,2,3)
		self.orientation = int(orientation) #entre 0,1,2,3
		self.fantome = 0 #numero du fantome présent sur la carte, vaut 0 si pas de fantome
		self.pepite = True #toutes les cartes possèdent une pépite en debut de jeu 
		self.chasseur = 0 #id du chasseur présent sur la carte, 0 par défaut

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
	
class Fantome(object):
	"""Fantomes"""
	def __init__(self, numero,position):
		self.numero = numero #numero du fantome
		self.position = position #liste [x,y] de sa position sur la matrice du plateau
		self.attrape = False #attrapé ou non

class Chasseur(object):
	"""Joueurs"""
	def __init__(self, id,position):
		self.id = id

		self.position = position
		self.mission = []
		self.pepite = 0
		self.score = 0
		self.joker = True
		self.fantome = []
		self.mouv_possibles = [] #à deduire du type et de l'orientation de la carte


	def bouger(self,direction):
		"""Déplace le Chasseur en changeant la valeur de son attribut position"""
		if direction == 'gauche':
			self.position[0] -= 1
		elif direction == 'droite':
			self.position[0] += 1
		elif direction == 'haut':
			self.position[1] -= 1
		if direction == 'bas':
			self.position[1] += 1
		

	def attraper_pepite(self,carte):
		'''Augmente le nombre de pepite attrapées par le chasseur, enleve la pepite de la carte concernee'''
		self.pepite += 1
		self.score +=1
		carte.pepite = False

	def utiliser_joker(self):
		######instructions utilisation joker########
		self.joker = False

	def attraper_fantome(self,numero_fantome,Plateau):
		'''Ajoute le numero du fantome à a liste des fantomes attrapés, enlève le fantome de la carte concernée
		Paramètres
		----------
		numero_fantome : int 
		==> Numéro du fantome attrapé
		carte : Carte()  
		==> Carte sur laquelle le joueur est
		'''
		self.fantome += fantome.numero
		Plateau.matrice[self.position] = 0


##partie test
test = plateau()
test.affichage_console()
		


		
