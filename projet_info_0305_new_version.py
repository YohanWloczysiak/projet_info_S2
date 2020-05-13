# -*- coding: utf-8 -*-

## Importation des modules nécessaires
import numpy
import tkinter
import copy


## Fonctions nécessaires au bon déroulement du jeu

# Fonction testant si le joueur est en situation d'échec


# Fonction testant si le joueur est en situation de mat


"""
def echec_et_mat(plateau, morts, nb_echecs):
    liste = []
    if test_echec(plateau, morts, nb_echecs) == False :
        pass
    else :
        test, couleur, nb_echecs = test_echec(plateau, morts, nb_echecs)                         # couleur = couleur mise en échec
        for piece in couleur :                                             # on teste toutes les pièces de la couleur mise en échec
            liste_prime = liste_deplacements_piece(piece, plateau, morts)        # liste des déplacements possibles pour chaque pièce
            for couple in liste_prime :
                a = couple[0]
                b = couple[1]
                copie_nb_echecs = copy.copy(nb_echecs)
                copie_plateau = copy.copy(plateau)                         # on effectue une copie du plateau pour simuler les déplacements
                deplacement(piece, a, b, copie_plateau, morts)
                if test_echec(copie_plateau, morts, copie_nb_echecs) == False :             # on teste si après un déplacement possible, le joueur peut sortir de l'échec
                    liste.append(piece, a, b) # il n'y a pas échec et mat
    if liste == []:
        return True        # il y a échec et mat
    return liste
"""

def new_echec_et_mat(plateau, morts, nb_echecs):
    print(test_echec(plateau, morts, nb_echecs))
    if test_echec(plateau, morts, nb_echecs) == False :
        pass
    else :
        test, couleur, nb_echecs = test_echec(plateau, morts, nb_echecs)                         # couleur = couleur mise en échec
        color_name = couleur[0][2]
        for piece in couleur :
            if liste_deplacements_possibles(piece, plateau, morts) != [] :
                pass
    return True, color_name


def liste_deplacements_possibles(piece, plateau, morts) :
    liste = liste_deplacements_piece(piece, plateau, morts)
    liste_finale = []
    color = piece[2]

    for couple in liste :
        copie_plateau = copy.copy(plateau)
        copie_morts = copy.copy(morts)
        copie_piece = copy.copy(piece)
        deplacement(copie_piece,couple[0],couple[1],copie_plateau, copie_morts)
        noirs, blancs = find_color(copie_plateau)

        deplacements_noirs = []
        deplacements_blancs = []

        for p in noirs:
            for elem in liste_deplacements_piece(p, copie_plateau, copie_morts):
                deplacements_noirs.append(elem)

        for p in blancs:
            for elem in liste_deplacements_piece(p, copie_plateau, copie_morts):
                deplacements_blancs.append(elem)

        new_rb = copy.copy(RB)
        new_rn = copy.copy(RN)

        if piece[1] == "roi":
            if color == "blanc":
                new_rb[0] = couple
            else:
                new_rn[0] = couple

        if color == "blanc":
            if new_rb[0] not in deplacements_noirs:
                liste_finale.append(couple)

        else :
            if new_rn[0] not in deplacements_blancs:
                liste_finale.append(couple)

    return liste_finale

def liste_deplacements_piece(piece, plateau, morts):
    liste_deplacements = []
    for a in range(0,8) :
        for b in range(0,8) :
            copie_plateau = copy.copy(plateau)
            copie_morts = copy.copy(morts)
            copie_piece = copy.copy(piece)
            try :
                deplacement(copie_piece,a,b,copie_plateau, copie_morts)
                liste_deplacements.append([a,b])
            except :
                pass
    return liste_deplacements

# Fonction qui teste si on est en situation d'échec
def test_echec(plateau, morts, nb_echecs):
    noirs, blancs = find_color(plateau)

    deplacements_noirs = []
    deplacements_blancs = []

    for p in noirs:
        for elem in liste_deplacements_piece(p, plateau, morts):
            deplacements_noirs.append(elem)

    for p in blancs:
        for elem in liste_deplacements_piece(p, plateau, morts):
            deplacements_blancs.append(elem)


    if RB[0] in deplacements_noirs :
        nb_echecs["blanc"] += 1
        print("Le roi blanc est en échec")
        return True, blancs, nb_echecs

    elif RN[0] in deplacements_blancs :
        nb_echecs["noir"] += 1
        print("Le roi noir est en échec")
        return True, noirs, nb_echecs

    return False, 0, nb_echecs

# Fonction pour déterminer les pièces de chaque couleur qui sont encore sur le plateau
def find_color(plateau):
    blancs, noirs = [], []
    for i in range(0,8):
        for j in range(0,8):
            if plateau[i,j][3] == 0 :
                pass
            else:
                piece = plateau[i,j]
                if piece[2] == "noir":
                    noirs.append(piece)
                else :
                    blancs.append(piece)
    return noirs, blancs


def deplacement(p,a,b, plateau, morts) :
    name = p[1]
    if name == "pion":
        deplacement_pion(p, a, b, plateau, morts)
    elif name == "fou":
        deplacement_fou(p, a, b, plateau, morts)
    elif name == "cavalier":
        deplacement_cavalier(p, a, b, plateau, morts)
    elif name == "tour":
        deplacement_tour(p, a, b, plateau, morts)
    elif name == "dame":
        deplacement_dame(p, a, b, plateau, morts)
    else:
        deplacement_roi(p, a, b, plateau, morts)


## Fonctions de déplacement des pièces

# Pion
def deplacement_pion(p, a, b, plateau, morts):
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if b in {Y+1, Y-1} and plateau[a,b][3] != 0 and ((a == X+1 and color == "noir") or (a == X-1 and color == "blanc")) :
        if plateau[a, b][2] != color and plateau[a, b][2] != ""  :          # élimination simple d'une pièce
            morts.append(plateau[a, b])
            plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        else :
            raise ValueError("Une autre pièce se trouve déjà sur cette case")
            return None
    elif b == Y and plateau[a,b][3] == 0 :             # déplacement simple
        if color == "noir" :                        # le pion est noir
            if (a == X+2 and X == 1 and plateau[a-1,b][3] == 0) or a == X+1 :
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a,b], plateau, morts
            else :
                raise ValueError("Le déplacement est impossible")
        else :                                       # le pion est blanc
            if (a == X-2 and X == 6 and plateau[a+1,b][3] == 0) or a == X-1:
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a,b], plateau, morts
            else :
                raise ValueError("Le déplacement est impossible")
    else :                                           # case occupée par une pièce de même couleur
             raise ValueError("Le déplacement est impossible")


# Tour
def traverse_tour(a, b, X, Y, plateau) :                         # renvoit si on peut se déplacer sans traverser de pièce
    if a != X :                                         # déplacement horizontal
            if a < X :
                for coord in range(a+1, X) :
                    if plateau[coord, b][3] != 0 :
                        return False
            else:
                for coord in range(X+1, a) :
                    if plateau[coord, b][3] != 0 :
                        return False
    elif b != Y:                                        # déplacement vertical
            if b < Y :
                for coord in range(b+1, Y) :
                    if plateau[a, coord][3] != 0 :
                        return False
            else:
                for coord in range(Y+1, b) :
                    if plateau[a, coord][3] != 0 :
                        return False
    return True

def deplacement_tour(p, a, b, plateau, morts):
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if a != X and b != Y:
        raise ValueError("Le déplacement est impossible")
    elif plateau[a,b][3] == 0 :                        # déplacement simple
        if traverse_tour(a, b, X, Y, plateau) == True :
            plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        else:
            raise ValueError("Vous traversez une pièce")
    else:
            if plateau[a,b][2] != color :             # élimination d'une pièce
                if traverse_tour(a, b, X, Y, plateau) == True :
                    morts.append(plateau[a, b])
                    plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                    p[0] = [a,b]
                    plateau[a,b] = p
                    return [a, b], plateau, morts
                else:
                    raise ValueError("Vous traversez une pièce")
            else:                                     # case occupée par une pièce de même couleur
                raise ValueError("Le déplacement est impossible")


# Cavalier
def deplacement_cavalier(p, a, b, plateau, morts) :
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    for k in range(0, 8):
        if (X - a) in {-1, 1} and (Y - b) in {-2, 2} or (X - a) in {-2, 2} and (Y - b) in {-1, 1} :
            if plateau[a,b][3] == 0 :                      # déplacement simple
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a, b], plateau, morts
            else:
                if plateau[a,b][2] != color :            # élimination d'une pièce
                    morts.append(plateau[a, b])
                    plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                    p[0] = [a,b]
                    plateau[a,b] = p
                    return [a, b], plateau, morts
                else:                                    # case occupée par une pièce de même couleur
                    raise ValueError("Une autre pièce se trouve déjà sur cette case")
        else:
            raise ValueError("Le déplacement est impossible")


# Fou
def traverse_fou(a, b, X, Y, plateau) :
    if (X - a) > 0 and (Y - b) > 0 :            # X - a = Y - b = k
        for i in range(a+1, X) :
            j = Y+i-X
            if plateau[i, j][3] != 0 :
                return False
    elif (X - a) > 0 and (Y - b) < 0 :         # X - a = k et Y - b = -k
        for i in range(X-1, a, -1) :
            j = Y-i+X
            if plateau[i, j][3] != 0 :
                return False
    elif (X - a) < 0 and (Y - b) < 0 :         # X - a = Y - b = -k
        for i in range(X+1, a) :
            j = Y+i-X
            if plateau[i, j][3] != 0 :
                return False
    elif (X - a) < 0 and (Y - b) > 0 :          # X - a = -k et Y - b = k
        for i in range(X + 1, a) :
            j = Y-i+X
            if plateau[i, j][3] != 0 :
                return False
    return True

def deplacement_fou(p, a , b, plateau, morts) :
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]

    if (Y - b) in [X-a, a-X]:
        if traverse_fou(a, b, X, Y, plateau) == False :
            raise ValueError("Vous traversez une pièce")

        if plateau[a,b][3] == 0 :                        # déplacement simple
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a, b], plateau, morts

        elif plateau[a,b][2] != color :               # élimination d'une pièce
                morts.append(plateau[a, b])
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a, b], plateau, morts

        else :                                       # case occupée par une pièce de même couleur
            raise ValueError("Une autre pièce se trouve déjà sur cette case")
    else :
        raise ValueError("Le déplacement est impossible")


# Dame
def deplacement_dame(p, a, b, plateau, morts) :
    [X, Y] = p[0]
    if a == X or b == Y :                               # déplacement selon une ligne/colonne
        deplacement_tour(p, a, b, plateau, morts)
    else:                                               # déplacement sur une diagonale
        deplacement_fou(p, a, b, plateau, morts)


# Roi
def deplacement_roi(p, a, b, plateau, morts) :
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if a in {X+1, X, X-1} and b in {Y+1, Y, Y-1} :
        if plateau[a,b][3] == 0:                       # déplacement simple
            plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        else:
            if plateau[a,b][2] != color :           # élimination d'une pièce
                morts.append(plateau[a, b])
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a, b], plateau, morts
            else:                                   # case occupée par une pièce de même couleur
                raise ValueError("Une autre pièce se trouve déjà sur cette case")
    else:
        raise ValueError("Le déplacement est impossible")


## Les coups spéciaux

# La promotion
def test_promotion(piece_selectionnee):
    liste_promotion_possible = []
    if piece_selectionnee[1] == 'pion':
        if piece_selectionnee[0][0] in {0, 7}:
            if piece_selectionnee[2] == 'noir':
                if DN in morts:
                    liste_promotion_possible.append(DN)

                if CN1 in morts or CN2 in morts :
                    liste_promotion_possible.append(CN1)

                if FN1 in morts or FN2 in morts:
                    liste_promotion_possible.append(FN1)
            else:
                if DB in morts:
                    liste_promotion_possible.append(DB)

                if CB1 in morts or CB2 in morts :
                    liste_promotion_possible.append(CB1)

                if FB1 in morts or FB2 in morts:
                    liste_promotion_possible.append(FB1)

            affiche_promotion(liste_promotion_possible)


def affiche_promotion(liste_promotion_possible):
    for elem in liste_promotion_possible:
        if elem[1] == 'dame':
            promotion_dame['state'] = 'normal'
        if elem[1] == 'fou':
            promotion_fou['state'] = 'normal'
        if elem[1] == 'cavalier':
            promotion_cavalier['state'] = 'normal'


def promotion_fou_fct(piece_promue):
    piece_promue[1] = 'fou'
    piece_promue[4] = Fou_noir

    a, b = piece_promue[0]
    ch = "case_"+str(a)+"_"+str(b)
    plateau[a,b] = piece_promue
    globals()[ch]['command'] = lambda p=piece_promue: event(p)


def promotion_dame_fct(piece_promue):
    print(piece_promue)
    piece_promue[1] = 'dame'
    piece_promue[4] = Dame_noire

    a, b = piece_promue[0]
    ch = "case_"+str(a)+"_"+str(b)
    plateau[a,b] = piece_promue
    globals()[ch]['command'] = lambda p=piece_promue: event(p)

def promotion_cavalier_fct(piece_promue):
    piece_promue[1] = 'cavalier'
    piece_promue[4] = Cavalier_noir

    a, b = piece_promue[0]
    ch = "case_"+str(a)+"_"+str(b)
    plateau[a,b] = piece_promue
    globals()[ch]['command'] = lambda p=piece_promue: event(p)



## La stratégie

def points_pieces(color):
    points = 0
    for piece in color:
        if piece[1] == "pion":
            points += 1
        elif piece[1] == "cavalier":
            points += 3
        elif piece[1] == "fou":
            points += 4
        elif piece[1] == "tour":
            points += 5
        elif piece[1] == "dame":            # dame = fou + tour
            points += 9
    return points

def evalue_plateau(blancs, noirs, plateau, nb_echecs):
    points = {"blanc" : 0, "noir" : 0}
    points["blanc"] = points_pieces(blancs)
    points["noir"] = points_pieces(noirs)
    if RB[0] != [7,4]:                                   # on enlève des points au joueur qui a déjà déplacé son roi
        points["blanc"] -= 3
    if RN[0] != [0,4]:
        points["noir"] -= 3
    Test, color, nb_echecs = test_echec(plateau, morts, nb_echecs)         # on enlève des points si le roi est actuellement en échec
    if color == "blanc" :
        points["blanc"] -= 5
        points["noir"] += 5
    if color == "noir":
        points["blanc"] += 5
        points["noir"] -= 5
    delta = int(nb_echecs["blanc"] - nb_echecs["noir"])  # on pénalise la couleur qui a subi le plus d'échecs
    if delta >= 0:
        points["blanc"] -= delta
    else:
        points["noirs"] += delta
    return points

def minmax(color_name, plateau, nb_echecs, difficulte=False):
    if difficulte == False:             # on choisit un jeu facile --> prévision du meilleur coup sans anticipation
        return meilleur_coup(color_name, plateau, nb_echecs)
    else :                               # on choisit un jeu difficile --> prévision du meilleur coup sur 2 tours
         meilleure_piece, meilleur_deplacement = 0, 0
         noirs, blancs = find_color(plateau)
         if color_name == "blanc" :
             color = blancs
             other_color_name = "noir"
             other_color = noirs
         else :
             color = noirs
             other_color_name = "blanc"
             other_color = blancs
         max_points_color = evalue_plateau(noirs, blancs, plateau, nb_echecs)[color_name]
         min_points_other_color = evalue_plateau(noirs, blancs, plateau, nb_echecs)[other_color_name]
         for piece in color :
             for couple in liste_deplacements_piece(piece, plateau, morts):
                 copie_plateau = copy.copy(plateau)
                 copie_nb_echecs = copy.copy(nb_echecs)
                 copie_piece = copy.copy(piece)
                 copie_morts = copy.copy(morts)
                 deplacement(copie_piece, couple[0], couple[1], copie_plateau, copie_morts)
                 noirs, blancs = find_color(copie_plateau)
                 for piece_adverse in other_color :
                     meilleure_piece, meilleur_deplacement = meilleur_coup(color_name, copie_plateau, copie_nb_echecs)
                     points_color_t2 = evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[color_name]
                     points_other_color_t2 = evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[other_color_name]
                     if points_color_t2 >= max_points_color and points_other_color_t2 <= min_points_other_color :
                         max_points_color = points_color_t2
                         min_points_other_color = points_other_color_t2
                         meilleure_piece = piece
                         meilleur_deplacement = couple
             return meilleure_piece, meilleur_deplacement

def meilleur_coup(color_name, plateau, nb_echecs):
    noirs, blancs = find_color(plateau)
    meilleure_piece, meilleur_deplacement = 0, 0
    if color_name == "blanc" :
        color = blancs
        other_color_name = "noir"
    else :
        color = noirs
        other_color_name = "blanc"
    max_color = evalue_plateau(noirs, blancs, plateau, nb_echecs)[color_name]
    min_other_color = evalue_plateau(noirs, blancs, plateau, nb_echecs)[other_color_name]
    for piece in color :
        for couple in liste_deplacements_piece(piece, plateau, morts):
                a, b = couple[0], couple[1]
                copie_plateau = copy.copy(plateau)
                copie_piece = copy.copy(piece)
                copie_nb_echecs = copy.copy(nb_echecs)
                copie_morts = copy.copy(morts)
                deplacement(copie_piece, a, b, copie_plateau, copie_morts)
                noirs, blancs = find_color(copie_plateau)
                if evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[color_name] >= max_color and evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[other_color_name] <= min_other_color :
                    max_color = evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[color_name]
                    min_other_color = evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[other_color_name]
                    meilleure_piece = piece
                    meilleur_deplacement = couple
    return meilleure_piece, meilleur_deplacement


## L'interface graphique

# Les variables globales nécessaires
joueur = "blanc"
liste_deplacements = []
piece_selectionnee = None
morts =[]
nb_echecs = {"blanc" :0, "noir": 0}
mode_de_jeu_choisit = "Joueur vs Ordinateur"
piece_promue = None


# Téléchargement des images
plateau_visuel = tkinter.Tk()

case_vide = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/case_vide.gif')
Dame_noire = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Dame_noire.gif')
Roi_noir = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Roi_noir.gif')
Tour_noire = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Tour_noire.gif')
Fou_noir = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Fou_noir.gif')
Cavalier_noir = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Cavalier_noir.gif')
Pion_noir = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Pion_noir.gif')
Dame_blanche = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Dame_blanche.gif')
Roi_blanc = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Roi_blanc.gif')
Tour_blanche = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Tour_blanche.gif')
Fou_blanc = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Fou_blanc.gif')
Cavalier_blanc = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Cavalier_blanc.gif')
Pion_blanc = tkinter.PhotoImage(file='C:/Users/yohan/Desktop/pieces_echecs_info/Pion_blanc.gif')


# Placement des pièces au début de la partie
PN1 =[[1,0],"pion","noir",1, Pion_noir, False]
PN2 =[[1,1],"pion","noir",2, Pion_noir, False]
PN3 =[[1,2],"pion","noir",3, Pion_noir, False]
PN4 =[[1,3],"pion","noir",4, Pion_noir, False]
PN5 =[[1,4],"pion","noir",5, Pion_noir, False]
PN6 =[[1,5],"pion","noir",6, Pion_noir, False]
PN7 =[[1,6],"pion","noir",7, Pion_noir, False]
PN8 =[[1,7],"pion","noir",8, Pion_noir, False]

TN1 = [[0,0],"tour","noir",1, Tour_noire, False]
CN1 = [[0,1],"cavalier","noir",1, Cavalier_noir, False]
FN1 = [[0,2],"fou","noir",1, Fou_noir, False]        #fou qui n'ira que sur les cases blanches
DN = [[0,3],"dame","noir",1, Dame_noire, False]
RN = [[0,4],"roi","noir",1, Roi_noir, False]
FN2 = [[0,5],"fou","noir",2, Fou_noir, False]        #fou qui n'ira que sur les cases noires
CN2 = [[0,6],"cavalier","noir",2, Cavalier_noir, False]
TN2 = [[0,7],"tour","noir",2, Tour_noire, False]

PB1 =[[6,0],"pion","blanc",1, Pion_blanc, False]
PB2 =[[6,1],"pion","blanc",2, Pion_blanc, False]
PB3 =[[6,2],"pion","blanc",3, Pion_blanc, False]
PB4 =[[6,3],"pion","blanc",4, Pion_blanc, False]
PB5 =[[6,4],"pion","blanc",5, Pion_blanc, False]
PB6 =[[6,5],"pion","blanc",6, Pion_blanc, False]
PB7 =[[6,6],"pion","blanc",7, Pion_blanc, False]
PB8 =[[6,7],"pion","blanc",8, Pion_blanc, False]

TB2 = [[7,0],"tour","blanc",2, Tour_blanche, False]
CB2 = [[7,1],"cavalier","blanc",2, Cavalier_blanc, False]
FB2 = [[7,2],"fou","blanc",2, Fou_blanc, False]       #fou qui n'ira que sur les cases noires
DB = [[7,3],"dame","blanc",1, Dame_blanche, False]
RB = [[7,4],"roi","blanc",1, Roi_blanc, False]
FB1 = [[7,5],"fou","blanc",1, Fou_blanc, False]       #fou qui n'ira que sur les cases blanches
CB1 = [[7,6],"cavalier","blanc",1, Cavalier_blanc, False]
TB1 = [[7,7],"tour","blanc",1, Tour_blanche, False]

plateau = numpy.array([[TN1,CN1,FN1,DN,RN,FN2,CN2,TN2],[PN1,PN2,PN3,PN4,PN5,PN6,PN7,PN8],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[PB1,PB2,PB3,PB4,PB5,PB6,PB7,PB8],[TB2,CB2,FB2,DB,RB,FB1,CB1,TB1]])

for i in range(2,6):
    for j in range(8):
        plateau[i,j] =  [[i,j],"case_vide","",0,case_vide]


# Création du plateau
for i in range(8):
    for j in range(8):
        if (i+j)%2 == 1:
            piece = plateau[i,j]
            img = piece[4]
            ch = "case_"+str(i)+"_"+str(j)
            globals()[ch] = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'maroon', command=lambda p=piece: event(p))
            globals()[ch].grid(row=i+1,column=j+1)

for i in range(8):
    for j in range(8):
        if (i+j)%2 == 0:
            piece = plateau[i,j]
            img = piece[4]
            ch = "case_"+str(i)+"_"+str(j)
            globals()[ch] = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'wheat', command=lambda p=piece: event(p))
            globals()[ch].grid(row=i+1,column=j+1)


# Les autres boutons (coups spéciaux et mode de jeu)
bouton_2ordis = tkinter.Button(plateau_visuel, text = "Ordinateur 1 vs Ordinateur 2", background= 'wheat', command = lambda text='bouton_2ordis': mode_de_jeu(text))
bouton_2ordis.grid(row=1,column=9)

bouton_ordi_vs_joueur = tkinter.Button(plateau_visuel, text = "Joueur vs Ordinateur", background= 'wheat', command = lambda text='bouton_ordi_vs_joueur': mode_de_jeu(text))
bouton_ordi_vs_joueur.grid(row=2,column=9)

bouton_2joueurs = tkinter.Button(plateau_visuel, text = "Joueur 1 vs Joueur 2", background= 'wheat', command =lambda text='bouton_2joueurs': mode_de_jeu(text))
bouton_2joueurs.grid(row=3,column=9)

grand_roque_bouton = tkinter.Button(plateau_visuel, text = 'Grand roque', state ='disabled', command = lambda : grand_roque())
grand_roque_bouton.grid(row=4,column=9)

petit_roque_bouton = tkinter.Button(plateau_visuel, text = 'Petit roque', state ='disabled', command = lambda : petit_roque())
petit_roque_bouton.grid(row=5,column=9)

promotion_fou = tkinter.Button(plateau_visuel, text = 'Fou', state ='disabled', background='skyblue', command = lambda p=piece_promue: promotion_fou_fct(p))
promotion_fou.grid(row=6,column=9)

promotion_cavalier = tkinter.Button(plateau_visuel, text = 'Cavalier', state ='disabled', background='skyblue', command = lambda p=piece_promue: promotion_cavalier_fct(p))
promotion_cavalier.grid(row=7,column=9)

promotion_dame = tkinter.Button(plateau_visuel, text = 'Dame', state ='disabled', background='skyblue', command = lambda p=piece_promue: promotion_dame_fct(p))
promotion_dame.grid(row=8,column=9)


# La fonction de jeu principale
def event(piece):
    global joueur
    global piece_selectionnee
    global liste_deplacements
    global mode_de_jeu_choisit
    global piece_promue

    print(piece_promue)
    a, b = piece[0]
    ch = "case_"+str(a)+"_"+str(b)
    color_fond = globals()[ch]['background']

    '''
    if mode_de_jeu_choisit == "Joueur vs Ordinateur" and joueur == 'noir':
        piece_ordi, deplacement_ordi = minmax(joueur, plateau, nb_echecs)
        a, b = deplacement_ordi[0], deplacement_ordi[1]

        print(minmax(joueur, plateau, nb_echecs))

        ch = "case_"+str(a)+"_"+str(b)
        i, j = piece_ordi[0]
        chprime = "case_"+str(i)+"_"+str(j)
        globals()[chprime]['image'] = case_vide
        piece = [[i,j],"case_vide","",0,case_vide]
        globals()[chprime]['command'] = lambda p=piece: event(p)
        deplacement(piece_ordi, a, b , plateau, morts)

        piece = plateau[a,b]
        globals()[ch]['image'] = piece_ordi[4]
        globals()[ch]['command'] = lambda p=piece: event(p)

        if joueur == "blanc":
            joueur = "noir"
        else:
            joueur = "blanc"
    '''

    if color_fond == 'green':
        i, j = piece_selectionnee[0]
        chprime = "case_"+str(i)+"_"+str(j)
        globals()[chprime]['image'] = case_vide
        piece = [[i,j],"case_vide","",0,case_vide]
        globals()[chprime]['command'] = lambda p=piece: event(p)
        deplacement(piece_selectionnee, a, b, plateau, morts)

        piece = plateau[a,b]
        globals()[ch]['image'] = piece_selectionnee[4]
        globals()[ch]['command'] = lambda p=piece: event(p)


        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 1:
                    ch = "case_"+str(i)+"_"+str(j)
                    globals()[ch]['background'] = 'maroon'

        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 0:
                    ch = "case_"+str(i)+"_"+str(j)
                    globals()[ch]['background'] = 'wheat'

        if joueur == "blanc":
            joueur = "noir"
        else:
            joueur = "blanc"

        piece_selectionnee[5] = True

        test_promotion(piece_selectionnee)

        if promotion_dame['state'] == 'normal' or promotion_cavalier['state'] == 'normal' or promotion_fou['state'] == 'normal':
            print(piece_promue)
            piece_promue = copy.copy(piece_selectionnee)
            print(piece_promue)

        liste_deplacements = []
        piece_selectionnee = None

    elif piece == piece_selectionnee:
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 1:
                    ch = "case_"+str(i)+"_"+str(j)
                    globals()[ch]['background'] = 'maroon'

        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 0:
                    ch = "case_"+str(i)+"_"+str(j)
                    globals()[ch]['background'] = 'wheat'

        liste_deplacements = []
        piece_selectionnee = None


    elif piece[3] != 0 and liste_deplacements == []:
            piece_selectionnee = piece
            if piece_selectionnee[2] == joueur:
                liste_deplacements = liste_deplacements_possibles(piece, plateau, morts)
                for i in range(8):
                    for j in range(8):
                        if [i,j] in liste_deplacements:
                            ch = "case_"+str(i)+"_"+str(j)
                            globals()[ch]['background'] = 'green'

    echec = test_echec(plateau, morts, nb_echecs)
    if echec[0] == True:
        test, color_name = new_echec_et_mat(plateau, morts, nb_echecs)
        if test == True:
            fin_de_partie(color_name)

        # On affiche la case du roi en rouge pour signaler au joueur suivant qu'il est en échec
        if joueur == 'noir':
            i, j = RN[0]
            ch = "case_"+str(i)+"_"+str(j)
            globals()[ch]['background'] = 'red'

        else:
            i, j = RB[0]
            ch = "case_"+str(i)+"_"+str(j)
            globals()[ch]['background'] = 'red'

    roque()


# Les autres fonctions de jeu
def mode_de_jeu(text):
    mode_de_jeu = text
    globals()[text]['background'] = 'yellow'

    bouton_2ordis['state']='disabled'
    bouton_ordi_vs_joueur['state']='disabled'
    bouton_2joueurs['state']='disabled'




# La fontion fin_de_partie qui s'exécute quand la partie est terminée
def fin_de_partie(joueur):
    if joueur == 'blanc':
        message = tkinter.Label(plateau_visuel, text = 'Les noirs ont gagné !')

    else:
        message = tkinter.Label(plateau_visuel, text = 'Les blancs ont gagné !')
    message.grid(row = 0, column = 1, columnspan = 8)


# Le roque
def roque() :
    global joueur

    if nb_echecs[joueur] == 0 :
        if joueur == "noir":
            a1, b1 = TN1[0]
            a2, b2 = TN2[0]
            X, Y = RN[0]
            if RN[5] == False and TN1[5] == False and traverse_tour(a1, b1, X, Y, plateau) == True:
                grand_roque_bouton['state']='normal'

            elif RN[5] == False and TN2[5] == False and traverse_tour(a2, b2, X, Y, plateau) == True:
                petit_roque_bouton['state']='normal'

        else:
            a1, b1 = TB1[0]
            a2, b2 = TB2[0]
            X, Y = RB[0]
            if RB[5] == False and TB1[5] == False and traverse_tour(a1, b1, X, Y, plateau) == True:
                petit_roque_bouton['state']='normal'

            elif RB[5] == False and TB2[5] == False and traverse_tour(a2, b2, X, Y, plateau) == True:
                grand_roque_bouton['state']='normal'


def grand_roque():
    global joueur
    if joueur == 'noir':
        piece_selectionnee1 = RN
        piece_selectionnee2 = TN1

    else:
        piece_selectionnee1 = RB
        piece_selectionnee2 = TB2

    i = piece_selectionnee1[0][0]
    ch1 = "case_"+str(i)+"_4"
    ch1prime = "case_"+str(i)+"_2"
    ch2 = "case_"+str(i)+"_0"
    ch2prime = "case_"+str(i)+"_3"

    img1 = case_vide
    piece1 = [[i,4],"case_vide","",0,case_vide]
    globals()[ch1]['command'] = lambda p=piece1: event(p)
    globals()[ch1]['image'] = img1

    img1prime = piece_selectionnee1[4]
    piece1prime = [[i,2],"roi","noir",1,piece_selectionnee1[4], True]
    globals()[ch1prime]['command'] = lambda p=piece1prime: event(p)
    globals()[ch1prime]['image'] = img1prime

    img2 = case_vide
    piece2 = [[i,0],"case_vide","",0,case_vide]
    globals()[ch2]['command'] = lambda p=piece2: event(p)
    globals()[ch2]['image'] = img2

    img2prime = piece_selectionnee2[4]
    piece2prime = [[i,3],"roi","noir",1,piece_selectionnee2[4], True]
    globals()[ch2prime]['command'] = lambda p=piece2prime: event(p)
    globals()[ch2prime]['image'] = img2prime

    plateau[i,4] = piece1
    plateau[i,3] = piece2prime
    plateau[i,2] = piece1prime
    plateau[i,0] = piece2

    if joueur == "blanc":
        joueur = "noir"
    else:
        joueur = "blanc"

    liste_deplacements = []
    piece_selectionnee = None

    grand_roque_bouton['state']='disabled'



def petit_roque():
    global joueur
    if joueur == 'noir':
        piece_selectionnee1 = RN
        piece_selectionnee2 = TN2

    else:
        piece_selectionnee1 = RB
        piece_selectionnee2 = TB1

    i = piece_selectionnee1[0][0]
    ch1 = "case_"+str(i)+"_4"
    ch1prime = "case_"+str(i)+"_6"
    ch2 = "case_"+str(i)+"_7"
    ch2prime = "case_"+str(i)+"_5"

    img1 = case_vide
    piece1 = [[i,4],"case_vide","",0,case_vide]
    globals()[ch1]['command'] = lambda p=piece1: event(p)
    globals()[ch1]['image'] = img1

    img1prime = piece_selectionnee1[4]
    piece1prime = [[i,6],"roi","noir",1,piece_selectionnee1[4], True]
    globals()[ch1prime]['command'] = lambda p=piece1prime: event(p)
    globals()[ch1prime]['image'] = img1prime

    img2 = case_vide
    piece2 = [[i,7],"case_vide","",0,case_vide]
    globals()[ch2]['command'] = lambda p=piece2: event(p)
    globals()[ch2]['image'] = img2

    img2prime = piece_selectionnee2[4]
    piece2prime = [[i,5],"roi","noir",1,piece_selectionnee2[4], True]
    globals()[ch2prime]['command'] = lambda p=piece2prime: event(p)
    globals()[ch2prime]['image'] = img2prime

    plateau[i,4] = piece1
    plateau[i,5] = piece2prime
    plateau[i,6] = piece1prime
    plateau[i,7] = piece2

    if joueur == "blanc":
        joueur = "noir"
    else:
        joueur = "blanc"

    liste_deplacements = []
    piece_selectionnee = None

    petit_roque_bouton['state']='disabled'



# Affichage du plateau
plateau_visuel.mainloop()