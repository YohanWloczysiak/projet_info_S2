# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 18:53:52 2020

@author: marie
"""
import copy

def points_pieces(color):
    points = 0
    for piece in color:
        if piece[3] == "pion":
            points += 1
        elif piece[3] == "cavalier":
            points += 3
        elif piece[3] == "fou":
            points += 4
        elif piece[3] == "tour":
            points += 5
        elif piece[3] == "dame":            # dame = fou + tour
            points += 9
    return points

def evalue_plateau(blancs, noirs, plateau, nb_echecs):  
    points = {"blanc" : 0, "noir" : 0}
    points["blanc"] = points_pieces(blancs) 
    points["noir"] = points_pieces(noirs)
    roi_noir = noirs[indice(RN)]
    roi_blanc = blancs[indice(RB)]
    if roi_blanc[0] != [7,4]:                                   # on enlève des points au joueur qui a déjà déplacé son roi
        points["blanc"] -= 3
    if roi_noir[0] != [0,4]:
        points["noir"] -= 3  
    Test, color, nb_echecs = test_echec(plateau, morts, nb_echecs)         # on enlève des points si le roi est actuellement en échec
    if color == "blanc" :
        points["blanc"] -= 5
        points["noir"] += 5
    if color == "noir":
        points["blanc"] += 5
        points["noir"] -= 5 
    delta = nb_echecs["blanc"] - nb_echecs["noir"] :    # on pénalise la couleur qui a subi le plus d'échecs
    if delta >= 0:
        points["blanc"] -= delta
    else:
        points["noirs"] += delta
    return points

def minmax(plateau, nb_echecs): #ops la couleur de l'ordinateur est noire
    noirs, blancs = find_color(plateau)
    maximum = evalue_plateau(noirs, blancs, plateau, nb_echecs)["noir"]
    minimum = evalue_plateau(noirs, blancs, plateau, nb_echecs)["blanc"]
    coup = []
    piece_choisie = CV
    for piece in noirs:
        for couple in liste_deplacements_piece(piece, plateau, morts):
            a, b = couple[0], couple[1]
            copie_plateau = copy.copy(plateau)
            copie_nb_echecs = copy.copy(nb_echecs)
            copie_morts = copy.copy(morts)
            deplacement(piece, a, b, copie_plateau, copie_morts)
            noirs, blancs = find_color(copie_plateau)                     # on actualise la liste des pièces restantes sur le plateau selon le coup possible réalisé
            if evalue_plateau(noirs, blancs, copy_plateau, copie_nb_echecs)["noir"] >= maximum and evalue_plateau(noirs, blancs, copy_plateau, copie_nb_echecs)["blanc"] <= minimum :
                piece_choisie = piece
                coup = [a, b]
                maximum = evalue_plateau(noirs, blancs, plateau, nb_echecs)["noir"]
                minimum = evalue_plateau(noirs, blancs, plateau, nb_echecs)["blanc"]
    return piece_choisie, coup

