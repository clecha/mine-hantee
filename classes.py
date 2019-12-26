import numpy as np
import random as rd
import shelve as sh
import affichage as af
from variables import IMAGES_DICT

class Plateau(object):
	"""
	Plateau de jeu
	----
	dimension: entier impair >=7
	matrice: array de taille dimension * dimension, contenant les objets Cartes
	matrice_surfaces :  array de taille dimension * dimension, contenant les surfaces des Cartes
	carte_jouable: objet de type carte, correspond à la carte qui est hors plateau
	joueur_actif: objet de type chasseur -- indique le joueur à qui c'est le tour de jouer
	liste_joueurs:
	nb_joueurs: entier allant de 1 à 4 -- indique le nb de joueurs																  
	"""
	def __init__(self, dimension = 7, nb_joueurs = 4):
		self.dimension = dimension #dimension du plateau
		self.joueur_actif = 1
		self.liste_joueurs = []
		self.nb_joueurs = nb_joueurs
		if dimension % 2 == 1 and dimension >= 7:
		#création de la matrice contenant les objets cartes
			self.matrice = np.zeros((dimension,dimension), dtype= object)

			#placement des cartes fixes
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
			# print('t3',self.matrice[0][0].murs)

			
			#4. placement du centre
			for ligne in range(2, dimension-2, 2):
				for col in range(2, dimension-2, 2):
					orientation = rd.randint(0,3)
					self.matrice[ligne][col] = Carte(3, False, orientation, True, False,[ligne,col])

			#placement des cartes aléatoires
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
		
		#carte restante
				self.carte_jouable = Carte(liste_types[0], True, 0, False, True, [None,None])
				
				
			# placement des joueurs
			# cree la liste des joueurs
			liste_joueurs = [k for k in range(1,self.nb_joueurs + 1)]
			
			# on crée une liste des fantomes qui servira pour l'attribut des missions
			liste_fantomes = [k for k in range(0,21)]
			rd.shuffle(liste_fantomes)
			
			#liste des positions possibles, que l'on va randomiser pour attribuer aléatoirement aux joueurs
			init = dimension // 2 - 1
			liste_pos_joueurs = [[init,init],[init,init+2],[init+2,init],[init+2,init+2]]
			rd.shuffle(liste_pos_joueurs)
			
			#on parcourt la liste des joueurs pour leur attribuer une position et une mission
			for joueur in liste_joueurs:
				ligne, col = liste_pos_joueurs[joueur-1]
				self.matrice[ligne][col].chasseur = Chasseur(joueur,[ligne,col], liste_fantomes[0:3])
				self.liste_joueurs.append(self.matrice[ligne][col].chasseur)
				print(self.liste_joueurs)
				
				#On retire les fantomes déjà attribués
				liste_fantomes.pop(0),liste_fantomes.pop(1),liste_fantomes.pop(2)
				
			
			#On place les fantomes aléatoirement avec la liste des positions liste_pos_carte_alea construite précédemment
			#On randomise la liste et on ne garde que les 21 premiers elements (positions) qui vont servir positionner les fantomes
			rd.shuffle(liste_pos_carte_alea)
			liste_pos_carte_alea=liste_pos_carte_alea[0:21]
			
			#On parcourt ensuite cette liste de position pour y placer les fantomes
			for k in range(21):
				ligne, col = liste_pos_carte_alea[k]
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
		try:
			dimension = self.dimension
			matrice_affichage_jouabilite = np.zeros((dimension,dimension), dtype=object)
			matrice_affichage_type_carte = np.zeros((dimension,dimension))
			matrice_affichage_orientation = np.zeros((dimension,dimension))
			matrice_affichage_chasseurs = np.zeros((dimension,dimension))
			matrice_affichage_fantomes = np.zeros((dimension,dimension))
			for col in range(dimension):
				for ligne in range(dimension):
					carte = self.matrice[ligne][col]
					matrice_affichage_jouabilite[ligne][col] = carte.jouable
					matrice_affichage_type_carte[ligne][col] = carte.type_carte
					matrice_affichage_orientation[ligne][col] = carte.orientation
					chasseur, fantome = carte.chasseur, carte.fantome
					if type(chasseur) != int:
						matrice_affichage_chasseurs[ligne][col] = carte.chasseur.id
					else:
						matrice_affichage_chasseurs[ligne][col] = carte.chasseur
					if type(fantome) != int:
						matrice_affichage_fantomes[ligne][col] = carte.fantome.numero
					else:
						matrice_affichage_fantomes[ligne][col] = carte.fantome

			print('matrice des jouabilites:\n', matrice_affichage_jouabilite)
			print('matrice des types de carte:\n', matrice_affichage_type_carte)
			print('matrice des orientations:\n', matrice_affichage_orientation)
			print('matrice des chasseurs:\n', matrice_affichage_chasseurs)
			print('matrice des fantomes:\n', matrice_affichage_fantomes)
			print('matrice des surfaces\n', self.matrice_surfaces)

		except:
			print('Il n y a aucun jeu en cours.')
		pass

	def inserer_carte(self,carte_inseree,position):
		"""Fonction placant la carte en argument a la position en argument
		Paramètres
		-----------
		carte : la carte JOUABLE
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
			# print('d2',deuxieme_carte.__dict__)
			
			#on retire l'élément qui a coulissé en dehors du plateau
			nvelle_carte_jouable = liste_a_inserer[index_carte_a_pop]
			liste_a_inserer = np.delete(liste_a_inserer, index_carte_a_pop)	
			#du coup, si la carte à pop était en dernière position, la liste rétrécit 
			#Si elle est en premier, ça décale tout ?		
			if insertion_colonne:
				for x in self.matrice[:,y_position]:
					print('avant',x.position)
			else:
				for x in self.matrice[x_position,:]:
					print('avant',x.position)
			
			#On vérifie la présence d'un fantome ou d'un joueur sur la carte qui a été sortie du tableau
			#on initialise un booleen qui permettra d'actualiser ou non la position du chasseur
			presence_chasseur = False
			#si la carte qui est sortie du plateau avait un fantome, on le déplace sur la carte qu'on insère
			if nvelle_carte_jouable.fantome !=0:
				carte_inseree.fantome = nvelle_carte_jouable.fantome
				nvelle_carte_jouable.fantome = 0
			#puis on fait de même pour les chasseurs
			if nvelle_carte_jouable.chasseur != 0:
				carte_inseree.chasseur = nvelle_carte_jouable.chasseur
				nvelle_carte_jouable.chasseur = 0
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
					#Actualisation de la position du chasseur dans l'objet chasseur
					self.matrice[index_chasseur, y_position].chasseur.position = [index_chasseur, y_position]
			else:
				self.matrice[x_position,:] = liste_a_inserer
				if presence_chasseur:
					self.matrice[x_position, index_chasseur].chasseur.position = [x_position, index_chasseur]
			
			#on actualise la nouvelle carte jouable
			self.carte_jouable = nvelle_carte_jouable #carte de bout de ligne/colonne "sort"
			
			#Actualisation de la jouabilité des cartes
			carte_inseree.jouable = False
			self.carte_jouable.jouable = True

			# #Actualisation de la bougeabilité des cartes
			carte_inseree.bougeable = True #nouvelle carte insérer
			
			#Actualisation de la position de la carte nouvellement insérée
			carte_inseree.position = [x_position,y_position]
			#Actualisation de la matrice des surfaces
			self.actualisation_matrice_surfaces()
			for x in liste_a_inserer:
				print(x.position, x)
			nouvel_index=0
			if insertion_colonne:
				for x in self.matrice[:,y_position]:
					print('apres',x.position[0])
					x.position[0] = nouvel_index
					print('apres',x.position[0])
					nouvel_index+=1
			else:
				for x in self.matrice[x_position,:]:
					print('apres',x.position[1])
					x.position[1] = nouvel_index
					print('apres',x.position[1])
					nouvel_index+=1
			# print(self.affichage_console())
			# print('nouvelle carte inseree infos', carte_inseree.__dict__)
			
		
	def sauvegarde(self, num_sauvegarde = 1):
		""" Methode qui permet de sauvegarder un plateau dans un fichier à un instant t
		Utilise le module shelf qui store des fichiers pythons dans une sorte de dictionnaire
		---
		num_sauvegarde: entier entre 1 et 3 --- permet de creer une sauvegarde parmi les 3 fichiers de sauvegarde proposés
		"""
		filename = 'save_'+str(num_sauvegarde)
		
		#Ouverture du fichier de sauvegarde
		save = sh.open(filename)
		
		#On stocke les fichiers dans le "dictionnaire" qui sert de sauvegarde
		save['dimension'] = self.dimension
		save['matrice'] = self.matrice
		save ['carte_jouable'] = self.carte_jouable
		save ['joueur_actif'] = self.joueur_actif
		
		save.close()
		
	def charger_sauvegarde(self, num_sauvegarde = 1):
		filename = 'save_'+str(num_sauvegarde)
		save = sh.open(filename)
		self.dimension = save['dimension']
		self.matrice = save['matrice']
		self.carte_jouable = save ['carte_jouable']
		self.joueur_actif = save ['joueur_actif']
		save.close()		
	

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
		print('dp pos acctuelle',x_position,y_position)
		direction_opposee = {'haut':'bas','bas':'haut','gauche':'droite','droite':'gauche'}
		carte_actuelle = self.matrice[x_position, y_position]
		carte_visee = self.carte_a_cote(x_position, y_position,direction)
		# print('test deplacement', carte_visee)
		print('murs carte actuelle',carte_actuelle.murs[direction])
		# print('murs visee', carte_visee.murs[direction_opposee[direction]])
		print('attributs de la carte visee dans deplacement possible #7', carte_visee.__dict__)
		if carte_actuelle.murs[direction] == False and carte_visee.murs[direction_opposee[direction]] == False: #s'il n(y a pas de murs sur les deux cartes)
			return True
		else: #s'il y a un mur sur l'une des deux cartes
			return False
	
	def changer_joueur(self):
		if self.joueur_actif == self.nb_joueurs :
			self.joueur_actif = 1
		else:
			self.joueur_actif += 1

	def deplacer_joueur(self, id_joueur, direction): 
		chasseur = self.liste_joueurs[id_joueur-1]
		print(chasseur)
		x,y = chasseur.position[0],chasseur.position[1]
		print('xy',x,y)
		carte_depart = self.matrice[x,y]
		carte_visee = self.carte_a_cote(x,y,direction)
		# print(carte_depart,carte_visee)
		print('murs #6', carte_visee.__dict__)
		print(self.deplacement_possible(x,y,direction))
		if self.deplacement_possible(x,y,direction):
			#on enlève le joueur de la carte de départ
			carte_depart.chasseur = 0
			#on l'ajoute à celle d'arrivée
			carte_visee.chasseur = chasseur
			#on change les attrbuts du joueur
			chasseur.position = carte_visee.position
			print('deplacement fait')


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
		self.chasseur = 0 #chasseur présent sur la carte, 0 par défaut
		self.murs = {}
		self.update_murs() #présence de mur a gauche, droite, en haut et bas de la carte

	def tourner(self,direction='droite'):
		"""Permet de tourner la carte d'un sens ou de l'autre en changeant la valeur de l'attribut orientation,
		qui doit être entre 0 et 3 (4 sens possibles).
		Paramètres
		----------
		direction : char
		==> valeurs possibles : 'gauche' ou 'droite'"""
		if self.orientation == 3 and direction == 'gauche':
			self.orientation = 0
		elif self.orientation == 0 and direction == 'droite':
			self.orientation = 3
		else:
			if direction == 'gauche':
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
	position: liste de coordonnees [x,y]
	mission: liste d entiers correspondant aux numéros des fantomes à ingérer
	pepite: entier -- nombre de pépites ramassées par le chasseur
	score: entier -- score amassé par le chasseur
	joker : Booléen -- True si le chasseur dispose encore de son joker
	fantome: liste d entiers -- correspond aux fantomes amasses par le chasseur"""
	def __init__(self, id,position,mission):
		self.id = id
		self.position = position
		self.mission = []
		self.pepite = 0
		self.score = 0
		self.joker = True
		self.fantome = []

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
		pass
		

	def attraper_pepite(self,Plateau):
		'''Augmente le nombre de pepite attrapées par le chasseur, enleve la pepite de la carte concernee'''
		x_position, y_position = self.position
		self.pepite += 1
		self.score +=1
		#Mise à jour de la valeur de la pepite sur la carte où est présent le chasseur
		Plateau.matrice[x_position, y_position].pepite = False

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
		#ajout du numero du fantome a la liste des fantomes collectés par le chasseur
		num_fantome = fantome.numero
		self.fantome += [num_fantome]
		fantome.attrape = True
		carte.fantome = 0
		
		#si le fantome fait partie de la mission du chasseur, le score est actualise a +20, sinon à +5
		if num_fantome in self.mission:
			self.score+= 20
			self.mission.remove(num_fantome)
			if self.mission == []:
				self.score+=40
		else:
			self.score+=5


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
		
