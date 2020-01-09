import pygame
import os, sys, glob
from variables import *
from main import *
import classes as cl
from math import *
import copy

## A*
def a_star(plateau,noeudFinal):
    """Boucle while principale :
        - on met le meilleur noeud de la liste ouverte dans la liste fermée
        et on appelle la fonction qui va chercher ses voisins
        - lorsque le meilleur noeud correspond au noeud final on sort de la
        boucle pour afficher le chemin
        - si le noeud final n'est pas atteint et si la liste des noeud à
        explorer est vide : retourne le chemin qui se rapproche le plus du noeud final
        """
    global listeOuverte,listeFermee,noeudCourant

    listeOuverte = []
    listeFermee = []
    chasseur = plateau.liste_joueurs[plateau.joueur_actif-1] #chasseur actif
    noeudDepart=cl.Noeud(chasseur.position)
    # id_fantome=int(21-plateau.fantomes_restants)
    # fantome_position=position_fantome(plateau,id_fantome)
    # print(fantome_position[0])
    # noeudFinal=cl.Noeud(position_fantome(plateau,id_fantome))

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
    #RemonterListe()
    return(listeFermee)

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
#
# def RemonterListe():
#     """Le but est atteint, cette fonction remonte le chemin d'ascendant en
#     ascendant en partant du dernier noeud courant choisi"""
#     chemin = []
#     n = listeFermee[-1]
#     chemin.append(n)
#     n = n.parent
#     # on crée des ronds pour chaque noeud appartenant au chemin gagnant
#     while n.parent != n:
#         chemin.append(n)
#     n = n.parent
#     chemin.append(n)
#     return(chemin)


def position_fantome(plateau, id_fantome):
    """Fonction qui renvoie la position du fantome étant donné son id"""
    dimension=plateau.dimension
    for x in range (dimension):
        for y in range (dimension):
            fantome = plateau.matrice[x,y].fantome
            if fantome != 0:
                num_fantome=fantome.numero
                if fantome == id_fantome:
                    return [x,y]

### Insertion carte

def a_star_insertion(plateau):
    """Réalise l'insertion de la carte jouable à toutes les positions possibles et ce pour les 4 orientation possibles. Puis pour chacune de ces insertions détermine le meilleur chemin pour atteindre le fantome à attraper. Tous ces chemins sont enregistrés et l'algorithme retourne la meilleure insertion et le meilleur chemin pour atteindre le fantome.
    """
    dimension = plateau.dimension
    carte_a_inserer = plateau.carte_jouable
    positions_possibles_insertion= [[x_pos,y_pos] for x_pos in range(1,dimension-1,2) for y_pos in [0,dimension-1]]+[[x_pos,y_pos] for y_pos in range(1,dimension-1,2) for x_pos in [0,dimension-1]]
    orientations_possibles=[0,1,2,3]
    dico_insertions ={}
    #copie du plateau sur lequel on va effectuer des modifs
    plateau_rch_chemin = copy.deepcopy(plateau)
    id_fantome=int(22-plateau.fantomes_restants)
    #Parcours des insertions possibles
    for position in positions_possibles_insertion:
        x_position=position[0]
        y_position=position[1]
        for orientation in orientations_possibles:
            carte_a_inserer.orientation=orientation
            dico_insertions[(x_position,y_position,orientation)] = 0
            plateau_rch_chemin.inserer_carte(carte_a_inserer,position)
            #definition du noeud final
            print(position_fantome(plateau_rch_chemin,id_fantome))
            noeudFinal=cl.Noeud(position_fantome(plateau_rch_chemin,id_fantome))
            chemin=a_star(plateau_rch_chemin,noeudFinal)
            point_arrivee=chemin[-1]
            if point_arrivee.x_position==noeudFinal.x_position and point_arrivee.y_position==noeudFinal.y_position:
                cout=-len(chemin)
            else :
                cout=Distance(point_arrivee,noeudFinal,plateau_rch_chemin)
            dico_insertions[(x_position,y_position,orientation)] += cout
    #recuperation de la meilleure insertion
    clef_dico_suggeree = min(dico_insertions, key = dico_insertions.get)
    position_insertion_optimale = [clef_dico_suggeree[0],clef_dico_suggeree[1]]
    orientation_optimale = clef_dico_suggeree[2]
    carte_a_inserer.orientation=orientation_optimale

    #recupeartion de la liste de deplacements pour y parvenir
    plateau_optimal=copy.deepcopy(plateau)
    plateau_optimal.inserer_carte(carte_a_inserer,position_insertion_optimale)
    noeudFinal=cl.Noeud(position_fantome(plateau_optimal,id_fantome))
    deplacement_optimal=a_star(plateau_optimal,noeudFinal)

    return(position_insertion_optimale, orientation_optimale, deplacement_optimal)

## Affichage plateau
    """Fonction qui affiche le déplacement à réaliser"""
def dessine_chemin(deplacement_optimal):
    size = 20
    for elem in deplacement_optimal:
        x_pixel = espace + elem.x_position * pixel_case + elem.x_position*marge/2
        x=int(x_pixel+pixel_case/2)
        y_pixel = elem.y_position * pixel_case + elem.y_position*marge/2
        y=int(y_pixel+pixel_case/2)
        pygame.draw.circle(gameDisplay, (70,225,70,100), (x,y),int(size), 8)
