# -*- coding: utf-8 -*-
"""
FONCTIONS ASSOCIEES AU DEROULEMENT DU JEU
"""
import copy

def fin_de_partie(plateau) :
    if echec_et_mat(plateau) == False :
        return None
    else :                                                    # il y a échec et mat
        test, couleur = test_echec(plateau)                   # la couleur perdante est celle mise en échec
        if couleur == "blancs" :
            print("Victoire des noirs !!")
        else :
            print("Victoire des blancs !!")

def liste_deplacements_possibles(color, plateau, morts) :
    liste_deplacements = []
    for piece in color :
        for a in range(0,8) :
            for b in range(0,8) :
                try :
                    deplacement(piece,a,b,plateau, morts)
                    liste_deplacements.append([a,b])
                except :
                    pass
    return liste_deplacements

def liste_deplacements_piece(piece, plateau, morts):
    liste_deplacements = []
    for a in range(0,8) :
        for b in range(0,8) :
            try :
                deplacement(piece,a,b,plateau, morts)
                liste_deplacements.append([a,b])
            except :
                pass
    return liste_deplacements

def test_echec(plateau, morts, nb_echecs):
    noirs, blancs = find_color(plateau)
    deplacements_noirs = liste_deplacements_possibles(noirs, plateau, morts)
    deplacements_blancs = liste_deplacements_possibles(blancs, plateau, morts)
    if RB[0] in deplacements_noirs :
        nb_echecs["blanc"] += 1
        print("Le roi blanc est en échec")
        return True, blancs, nb_echecs
    elif RN[0] in deplacements_blancs :
        nb_echecs["noir"] += 1
        print("Le roi noir est en échec")
        return True, noirs, nb_echecs
    return False


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


def echec_et_mat(plateau, morts, nb_echecs):
    if test_echec(plateau, morts) == False :
        pass
    else :
        test, couleur, nb_echecs = test_echec(plateau, morts, nb_echecs)                         # couleur = couleur mise en échec
        for piece in couleur :                                             # on teste toutes les pièces de la couleur mise en échec
            liste = liste_deplacements_piece(piece, plateau, morts)        # liste des déplacements possibles pour chaque pièce
            for couple in liste :
                a = couple[0]
                b = couple[1]
                copie_nb_echecs = copy.copy(nb_echecs)
                copie_plateau = copy.copy(plateau)                         # on effectue une copie du plateau pour simuler les déplacements
                deplacement(piece, a, b, copie_plateau, morts)
                if test_echec(copie_plateau, morts, copie_nb_echecs) == False :             # on teste si après un déplacement possible, le joueur peut sortir de l'échec
                    return False   # il n'y a pas échec et mat
                return True        # il y a pas échec et mat


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