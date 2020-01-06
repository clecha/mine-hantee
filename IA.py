from math import sqrt

class Noeud():
    """Chaque case du jeu est représentée par un objet noeud qui contient :
         - sa position dans la grille
         - son cout G : distance entre elle et son ascendant + cout G de son
           ascendant
         - son cout H : distance entre elle et le noeud final
         - son cout F : somme de G et H"""
    def __init__(self,position):
        self.x_position = int(position[0])
        self.y_position = int(position[1])
        self.coutF = 0
        self.coutG = 0
        self.coutH = 0
        self.parent = self


##### Fonctions de l'algorithme ------------------------------------------------
def Algorithme(noeudDepart, noeudFinal,plateau):
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

    ###Initialistion du noeudCourant avec le noeud de départ
    noeudCourant = noeudDepart
    noeudCourant.coutH = Distance(noeudCourant,noeudFinal)
    noeudCourant.coutF = noeudCourant.coutH
    ###On le met dans la liste ouverte
    listeOuverte.append(noeudCourant)

    while (not(noeudCourant.x_position == noeudFinal.x_position and noeudCourant.y_position == noeudFinal.y_position)
           and listeOuverte != []):
        ### On choisi le meilleur noeud ce sera le noeud courant
        noeudCourant = MeilleurNoeud()
        AjouterListeFermee(noeudCourant)

        ### On va chercher les voisins du noeud courant
        AjouterCasesAdjacentes(noeudCourant,plateau)

    ### on a atteint le noeud final
    if noeudCourant.x_position == noeudFinal.x_position and noeudCourant.y_position == noeudFinal.y_position :
        RemonterListe()
    ### On a pas atteint le noeud final et il n'y a plus de noeud à explorer
    elif listeOuverte == []:
        print('===========================================')
        print('PAS DE SOLUTION'))

def MeilleurNoeud():
    """Fonction qui renvoie le meilleur noeud de la liste ouverte en fonction
    de son cout en F"""
    cout = 5000000
    noeud = None
    for n in listeOuverte:
        if n.coutF < cout:
            cout = n.coutF
            noeud = n
    return noeud

def AjouterListeFermee(noeud):
    """Ajoute un noeud à la liste fermée et le supprime de la liste ouverte"""
    global listeOuverte,listeFermee

    listeFermee.append(noeud)
    listeOuverte.remove(noeud)

def AjouterCasesAdjacentes(noeudCourant,plateau):
    """Fonction qui cherche tous les voisins possibles au noeud courant passé
    en parametre."""
    global listeOuverte,listeFermee
    dimension = plateau.dimension
    deplacements = ["gauche","droite","haut","bas"]

    for direction in deplacements:
        coordSuivante=plateau.carte_a_cote(noeudCourant.x_position,noeudCourant.y_position,direction)
        ###On vérifie qu'on sort pas de la matrice
        if coordSuivante[0] >= 0 and coordSuivante[0] <= dimension-1 and coordSuivante[1] >= 0 and coordSuivante[1] <= dimension-1:
            ###On vérifie que le voisin n'est pas un obstacle
            if plateau.deplacement_possible(x_position,y_position, direction):
                ###On crée un objet noeud au coordonnée du voisin
                noeudTemp = Noeud(coordSuivante[0],coordSuivante[1])
                ###Le noeud courant sera son parent
                noeudTemp.parent = noeudCourant
                ###On s'assure que ce voisin ne fait pas deja parti de la liste fermée
                if not DejaPresentDansListe(noeudTemp,listeFermee):
                    ###On calcule ses couts
                    noeudTemp.coutG = noeudTemp.parent.coutG + Distance(noeudTemp,noeudTemp.parent)
                    noeudTemp.coutH = Distance(noeudTemp,noeudFinal)
                    noeudTemp.coutF = noeudTemp.coutG + noeudTemp.coutH

                    n = DejaPresentDansListe(noeudTemp,listeOuverte)
                    ###Si ce voisin est deja présent dans la liste ouverte
                    if n != False:
                        ###On compare son cout G avec celui de la liste ouverte(n)
                        if noeudTemp.coutG < n.coutG:
                            ###Si il est inférieur on remplace les couts et le parent de n par ceux du voisin récemment trouvé
                            n.parent = noeudCourant
                            n.coutG = noeudTemp.coutG
                            n.coutH = noeudTemp.coutH
                            n.coutF = noeudTemp.coutF
                        ###Dans le cas contraire on ne change rien...

                    ###Ce voisin n'est pas déja présent dans le liste ouverte
                    ###donc on l'y ajoute
                    else:
                        listeOuverte.append(noeudTemp)
                        # ###animation
                        # fen.after(intervalTemps ,CasesListeOuverte(noeudTemp))
                        # fen.update()

def Distance(noeud1,noeud2):
    """Calcule des distances entre 2 noeuds suivant l'heuristique choisie"""
    a =  noeud2.x_position - noeud1.x_position
    b =  noeud2.y_position - noeud1.y_position
    if choixHeuristique == 'racineDistEucli':
        return sqrt((a*a) + (b*b))
    elif choixHeuristique == 'distanceEucli':
        return ((a*a) + (b*b))
    elif choixHeuristique == "distManhattan":
        return (abs(a)+abs(b))

def DejaPresentDansListe(noeud,liste):
    """Fonction qui cherche si un noeud est deja présent dans un liste"""
    for n in liste:
        if n.x_position == noeud.x_position and n.y_position == noeud.y_position:
            return n
    return False

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
        y_pixel = n.y_position * pixel_case + n.y_position*marge/2
        position_cercle = (int(x_pixel+pixel_case/2),int(y_pixel+pixel_case/2))
        pygame.draw.circle(gameDisplay, (70,225,70, 100), position_cercle,int(size), 8)
        n = n.parent
    chemin.append(n)
    x_pixel = espace + n.x_position * pixel_case + n.x_position*marge/2
    y_pixel = n.y_position * pixel_case + n.y_position*marge/2
    position_cercle = (int(x_pixel+pixel_case/2),int(y_pixel+pixel_case/2))
    pygame.draw.circle(gameDisplay, (70,225,70, 100), position_cercle,int(size), 8)


