# -*- coding: utf-8 -*-
"""
REGLES DU JEU D'ECHECS - FONCTIONS DE DEPLACEMENTS DES PIECES
"""
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
            if (a == X+2 and X == 1) or a == X+1 :
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a,b], plateau, morts
            else :
                raise ValueError("Le déplacement est impossible")
        else :                                       # le pion est blanc
            if (a == X-2 and X == 6) or a == X-1:
                plateau[X,Y] = [[X,Y],"case_vide","",0,case_vide]
                p[0] = [a,b]
                plateau[a,b] = p
                return [a,b], plateau, morts
            else :
                raise ValueError("Le déplacement est impossible")
    else :                                           # case occupée par une pièce de même couleur
             raise ValueError("Le déplacement est impossible")


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

def deplacement_fou(p, a , b, plateau, morts) :
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if traverse_fou(a, b, X, Y, plateau) == False :
        raise ValueError("Vous traversez une pièce")
    else:
        for k in range(0, 8) :
            if (X - a) in {k, -k} and (Y - b) in {k, -k}:
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

def deplacement_dame(p, a, b, plateau, morts) :
    [X, Y] = p[0]
    if a == X or b == Y :                               # déplacement selon une ligne/colonne
        deplacement_tour(p, a, b, plateau, morts)
    else:                                               # déplacement sur une diagonale
        deplacement_fou(p, a, b, plateau, morts)

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

def traverse_fou(a, b, X, Y, plateau) :
    if (X - a) > 0 and (Y - b) > 0 :            # X - a = Y - b = k
        for i in range(a, X) :
            for j in range (b, Y) :
                if plateau[i, j][3] != 0 :
                    return False
    elif (X - a) > 0 and (Y - b) < 0 :         # X - a = k et Y - b = -k
        for i in range(X-1, a, -1) :
            for j in range (Y+1, b) :
                if plateau[i, j][3] != 0 :
                    return False
    elif (X - a) < 0 and (Y - b) < 0 :         # X - a = Y - b = -k
        for i in range(X+1, a) :
            for j in range (Y+1, b) :
                if plateau[i, j][3] != 0 :
                    return False
    elif (X - a) < 0 and (Y - b) > 0 :          # X - a = -k et Y - b = k
        for i in range(X + 1, a) :
            for j in range (Y-1, b, -1) :
                if plateau[i, j][3] != 0 :
                    return False
    return True

def roque(roi, tour, plateau, nb_echecs) :
    assert roi[2] == tour[2]
    color = roi[2]
    if nb_echecs[color] > 0 :
        raise ValueError("Roque impossible. Le roi a déjà été mis en échec.")
    else:
        if roi[2] == "noir":                    # roque noir
            if roi[0] != [0, 4] and tour[0] not in {[0, 0], [0, 7]} :
                raise ValueError("Roque impossible. L'une des pièces a déjà été déplacée")
            else :
                if tour[3] == 1 :               # grand roque
                    roi[0] = [0, 2]
                    tour[0] = [0, 3]
                    plateau[0,2], plateau[0,3] = roi, tour
                    plateau[0,4], plateau[0,0] = [[0,4],"case_vide","",0,case_vide], [[0,0],"case_vide","",0,case_vide]
                    return roi, tour, plateau
                else :                          # petit roque
                    roi[0] = [0, 6]
                    tour[0] = [0, 5]
                    plateau[0,6], plateau[0,5] = roi, tour
                    plateau[0,4], plateau[0,7] = [[0,4],"case_vide","",0,case_vide], [[0,7],"case_vide","",0,case_vide]
                    return roi, tour, plateau
        else :                                  # roque noir
            if roi[0] != [7, 4] and tour[0] not in {[7, 0], [7, 7]} :
                raise ValueError("Roque impossible. L'une des pièces a déjà été déplacée")
            else :
                if tour[3] == 2 :               # grand roque
                    roi[0] = [7, 2]
                    tour[0] = [7, 3]
                    plateau[7,2], plateau[7,3] = roi, tour
                    plateau[7,4], plateau[7,0] = [[7,4],"case_vide","",0,case_vide], [[7,0],"case_vide","",0,case_vide]
                    return roi, tour, plateau
                else :                          # petit roque
                    roi[0] = [7, 6]
                    tour[0] = [7, 5]
                    plateau[7,6], plateau[7,5] = roi, tour
                    plateau[7,4], plateau[7,7] = [[7,4],"case_vide","",0,case_vide], [[7,7],"case_vide","",0,case_vide]
                    return roi, tour, plateau

def promotion(p, piece, plateau, morts) :
    color = p[2]
    if piece == "dame":
        if color == "noir":
            if DN in morts :
                DN[0] = pion[0]
                morts[indice[DN1, morts]] = p
                return DN1, morts
            else :
                raise ValueError("promotion impossible")
        else :
            if DB in morts :
                DB[0] = pion[0]
                morts[indice[DB1, morts]] = p
                return DB1, morts
            else :
                raise ValueError("promotion impossible")
    elif piece == "cavalier":
        if color == "noir" :
            if CN1 in morts :
                CN1[0] = pion[0]
                morts[indice[CN1, morts]] = p
                return CN1, morts
            elif CN2 in morts :
                CN2[0] = pion[0]
                morts[indice[CN2, morts]] = p
                return CN2, morts
            else :
                raise ValueError("promotion impossible")
        else :
            if CB1 in morts :
                CB1[0] = pion[0]
                morts[indice[CB1, morts]] = p
                return CB1, morts
            elif CB2 in morts :
                CB2[0] = pion[0]
                morts[indice[CB2, morts]] = p
                return CB2, morts
            else :
                raise ValueError("promotion impossible")
    elif piece == "fou":
        if color == "noir" :
            if FN1 in morts :
                FN1[0] = pion[0]
                morts[indice[FN1, morts]] = p
                return FN1, morts
            elif FN2 in morts :
                FN2[0] = pion[0]
                morts[indice[FN2, morts]] = p
                return FN2, morts
            else :
                raise ValueError("promotion impossible")
        else :
            if FB1 in morts :
                FB1[0] = pion[0]
                morts[indice[FB1, morts]] = p
                return FB1, morts
            elif FB2 in morts :
                FB2[0] = pion[0]
                morts[indice[FB2, morts]] = p
                return FB2, morts
            else :
                raise ValueError("promotion impossible")

def indice(x, liste) :
    indice = 0
    while liste[indice] != x and indice <= len(liste):
        indice += 1
    if indice == len(liste):
        return None
    return indice

def prise_en_passant(p, a, b, plateau) :
    color = p[2]
    if color == "noir" :
        if plateau[a-1, b][1] == "pion" and plateau[a-1, b][2] == "blanc" :
            return plateau[a-1, b]
        else :
            return None
    else :
        if plateau[a+1, b][1] == "pion" and plateau[a+1, b][2] == "noir" :
            return plateau[a+1, b]
        else :
            return None
