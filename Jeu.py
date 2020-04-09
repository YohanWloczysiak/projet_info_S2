# -*- coding: utf-8 -*-
"""
 FONCTIONS ASSOCIEES AU DEROULEMENT DU JEU
 
"""

def echec_et_mat(morts) :                       # il y a échec et mat ssi on élimine l'un des rois
    if RN1 in morts : 
        return "Fin de partie - Victoire des blancs"
    elif RB1 in morts :
        return "Fin de partie - Victoire des noirs"
    else:
        return None
        
def deplacement(p,a,b):
    name = p[1]
    if name == "pion":
        deplacement_pion(p, a, b)
    elif name == "fou":
        deplacement_fou(p, a, b)
    elif name == "cavalier":
        deplacement_cavalier(p, a, b)
    elif name == "tour":
        deplacement_tour(p, a, b)
    elif name == "dame":
        deplacement_dame(p, a, b)
    else:
        deplacement_roi(p, a, b)
    
def game(plateau):
    print("Les blancs commencent")
    morts = []
    while echec_et_mat(morts) == None :
        move_blanc = input("C'est aux blancs de jouer")
        piece = move_blanc[1]
        if piece[2] != "blanc" :
            print("Vous ne pouvez pas jouer une pièce qui n'est pas de votre couleur")
        deplacement(move_blanc)
        if echec_et_mat(morts) == None :
            return echec_et_mat(morts)
        else :
             move_noir = input("C'est aux noirs de jouer")
        piece = move_noir[1]
        if piece[2] != "noir" :
            print("Vous ne pouvez pas jouer une pièce qui n'est pas de votre couleur")
        deplacement(move_noir)
    return echec_et_mat(morts)