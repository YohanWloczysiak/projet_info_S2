# -*- coding: utf-8 -*-
"""
 FONCTIONS ASSOCIEES AU DEROULEMENT DU JEU
 
"""

import copy

def fin_de_partie(plateau) :                      
    if echec_et_mat(plateau) == False :
        return None
    else :
        test, couleur = test_echec(plateau)
        if couleur == "blancs" :
            print("Victoire des noirs !!")
        else :
            print("Victoire des blancs !!")

def liste_deplacements_possibles(color, plateau) :
    liste_deplacements = []
    for piece in color :
        for a in range(0,8) :
            for b in range(0,7) :
                if deplacement(piece,a,b) != None :
                    liste_deplacements.append(a,b)
    return liste_deplacements

def liste_deplacements_piece(piece, plateau):
    liste_deplacements = []
    for a in range(0,8) :
        for b in range(0,7) :
            if deplacement(piece,a,b,plateau) != None :
                liste_deplacements.append(a,b)
    return liste_deplacements

def test_echec(plateau):
    noirs = [blabla]
    blancs = [blablabla]
    deplacaments_noirs = liste_deplacements_possibles(noirs, plateau)
    deplacements_blancs = liste_deplacements_possibles(blancs, plateau)
    if RB1[0] in deplacements_noirs :
        print("Le roi blanc est en échec")
        return True, blancs
    elif RN1[0] in deplacements_blancs :
        print("Le roi noir est en échec")
        return True, noirs
    return False    

def echec_et_mat(plateau):
    if test_echec(plateau) == False :
        pass
    else :
        test, couleur = test_echec(plateau)
        for piece in couleur :
            for couple in liste_deplacements_piece(piece, plateau):
                couple[0] = a
                couple[1] = b
                copie_plateau = copy.copy(plateau)
                deplacement(piece, a, b, copie_plateau)
                if test_echec(copie_plateau) == False :
                    return False
        return True
                    

def deplacement(p,a,b, plateau) :
    name = p[1]
    if name == "pion":
        deplacement_pion(p, a, b, plateau)
    elif name == "fou":
        deplacement_fou(p, a, b)
    elif name == "cavalier":
        deplacement_cavalier(p, a, b, plateau)
    elif name == "tour":
        deplacement_tour(p, a, b, plateau)
    elif name == "dame":
        deplacement_dame(p, a, b, plateau)
    else:
        deplacement_roi(p, a, b, plateau)
    
def game(plateau):
    print("Les blancs commencent")
    morts = []
    while fin de partie(plateau) == None :
        move_blanc = input("C'est aux blancs de jouer")
        piece = move_blanc[1]
        if piece[2] != "blanc" :
            print("Vous ne pouvez pas jouer une pièce qui n'est pas de votre couleur")
        deplacement(move_blanc, plateau)
        if echec_et_mat(morts) == None :
            return echec_et_mat(morts)
        else :
             move_noir = input("C'est aux noirs de jouer")
        piece = move_noir[1]
        if piece[2] != "noir" :
            print("Vous ne pouvez pas jouer une pièce qui n'est pas de votre couleur")
        deplacement(move_noir, plateau)
    return fin_de_partie(plateau)