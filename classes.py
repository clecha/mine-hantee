

class Plateau(object):
	"""Plateau de jeu"""
	def __init__(self, dimension):
		self.dimension = dimension #dimension du plateau
		
		#création de la matrice contenant les objets cartes
		self.matrice = np.eyes(dimension) 

		if dimension == 7:
		#placement des cartes fixes

		#placement des cartes aléatoires
		
		#carte restante 
		self.carte_jouable = 0 #création de la dernière carte 

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
	def __init__(self, numero,position,type_carte,orientation):
		self.numero = numero #numero d'identification de la carte
		self.position = position #liste de la position sur la matrice du aplteau [x,y]
		self.type_carte = type_carte #type de carte (1,2,3)
		self.orientation = 0 #entre 0,1,2,3
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

		self.position = [position[0],position[1]]
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


		


		