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
    delta = nb_echecs["blanc"] - nb_echecs["noir"]    # on pénalise la couleur qui a subi le plus d'échecs
    if delta >= 0:
        points["blanc"] -= delta
    else:
        points["noirs"] += delta
    return points

def minmax(color_name, plateau, nb_echecs, difficulte): 
    if difficulte == False:             # on choisit un jeu facile --> prévision du meilleur coup sans anticipation
        return meilleur_coup(color_name, plateau, nb_echecs)
    else :                               # on choisit un jeu difficile --> prévision du meilleur coup sur 3 tours
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
                 a, b = couple[0], couple[1]
                 copie_plateau = copy.copy(plateau)
                 copie_nb_echecs = copy.copy(nb_echecs)
                 copie_morts = copy.copy(morts)
                 deplacement(piece, a, b, copie_plateau, copie_morts)
                 noirs, blancs = find_color(copie_plateau)
                 for piece_adverse in other_color :
                     deplacement(piece, couple[0], couple[1], copie_plateau, copie_nb_echecs)
                     meilleure_piece, meilleur_deplacement = meilleur_coup(color_name, copie_plateau, copie_nb_echecs)
                     points_color_t2 = evalue_plateau(noirs, blancs, plateau, nb_echecs)[color_name]
                     points_other_color_t2 = evalue_plateau(noirs, blancs, plateau, nb_echecs)[other_color_name]
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
                copie_nb_echecs = copy.copy(nb_echecs)
                copie_morts = copy.copy(morts)
                deplacement(piece, a, b, copie_plateau, copie_morts)
                noirs, blancs = find_color(copie_plateau)
                if evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[color_name] >= max_color and evalue_plateau(noirs, blancs, copie_plateau, copie_nb_echecs)[other_color_name] <= min_other_color :
                    max_color = evalue_plateau(noirs, blancs, plateau, nb_echecs)[color_name]
                    min_other_color = evalue_plateau(noirs, blancs, plateau, nb_echecs)[other_color_name]
                    meilleure_piece = piece
                    meilleur_deplacement = couple
    return meilleure_piece, meilleur_deplacement
    