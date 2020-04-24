
#définition des régles et mouvements des pièces

#importation des modules nécessaires
import numpy
import tkinter


"""
FONCTIONS ASSOCIEES AU DEROULEMENT DU JEU
"""
morts = []

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

def liste_deplacements_possibles(color, plateau) :
    liste_deplacements = []
    for piece in color :
        for a in range(0,8) :
            for b in range(0,8) :
                if deplacement(piece,a,b) != None :
                    liste_deplacements.append([a,b])
    return liste_deplacements

def liste_deplacements_piece(piece, plateau):
    liste_deplacements = []
    for a in range(0,8) :
        for b in range(0,8) :
            if deplacement(piece,a,b,plateau, morts) != None :
                liste_deplacements.append([a,b])
    return liste_deplacements

def test_echec(plateau):
    noirs, blancs = find_color(plateau)
    deplacements_noirs = liste_deplacements_possibles(noirs, plateau)
    deplacements_blancs = liste_deplacements_possibles(blancs, plateau)
    if RB1[0] in deplacements_noirs :
        print("Le roi blanc est en échec")
        return True, blancs
    elif RN1[0] in deplacements_blancs :
        print("Le roi noir est en échec")
        return True, noirs
    return False


def find_color(plateau):
    blancs, noirs = [], []
    for i in range(0,8):
        for j in range(0,8):
            if plateau[i,j] == 0 :
                pass
            else:
                piece = plateau[i,j]
                if piece[2] == "noir":
                    noirs.append(piece)
                else :
                    blancs.append(piece)
    return noirs, blancs


def echec_et_mat(plateau):
    if test_echec(plateau) == False :
        pass
    else :
        test, couleur = test_echec(plateau)                         # couleur = couleur mise en échec
        for piece in couleur :                                      # on teste toutes les pièces de la couleur mise en échec
            liste = liste_deplacements_piece(piece, plateau)        # liste des déplacements possibles pour chaque pièce
            for couple in liste :
                a = couple[0]
                b = couple[1]
                copie_plateau = copy.copy(plateau)                  # on effectue une copie du plateau pour simuler les déplacements
                deplacement(piece, a, b, copie_plateau)
                if test_echec(copie_plateau) == False :             # on teste si après un déplacement possible, le joueur peut sortir de l'échec
                    return False
                return True


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

def game(plateau):
    print("Les blancs commencent")
    morts = []
    while fin_de_partie(plateau) == None :
        move_blanc = input("C'est aux blancs de jouer")
        piece = move_blanc[1]
        if piece[2] != "blanc" :
            print("Vous ne pouvez pas jouer une pièce qui n'est pas de votre couleur")
        deplacement(move_blanc, plateau)
        if echec_et_mat(plateau) == None :
            return echec_et_mat(plateau)
        else :
             move_noir = input("C'est aux noirs de jouer")
        piece = move_noir[1]
        if piece[2] != "noir" :
            print("Vous ne pouvez pas jouer une pièce qui n'est pas de votre couleur")
        deplacement(move_noir, plateau)
    return fin_de_partie(plateau)



"""
REGLES DU JEU D'ECHECS - FONCTIONS DE DEPLACEMENTS DES PIECES
"""

def deplacement_pion(p, a, b, plateau, morts):
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if (a == 0 and color == "blanc") or (a == 7 and color == "noir"):
        piece = input("Choisissez une pièce pour échanger votre pion : dame, cavalier, fou")
        p = promotion(p, piece, plateau, morts)
    else :
        pass
    if b in {Y+1, Y-1} and plateau[a,b][3] != 0 :
        dead = prise_en_passant(p, a, b, plateau)
        if dead != None :                         # prise en passant
            morts.append(dead)
            plateau[X,Y] = CV
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        elif plateau[a, b][2] != color :          # élimination simple d'une pièce
            morts.append(plateau[a, b])
            plateau[X,Y] = CV
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        else :
            print("Une autre pièce se trouve déjà sur cette case")
            return None
    elif b == Y and plateau[a,b][3] == 0 :             # déplacement simple
        if color == "noir" :                        # le pion est noir
            if a == X+2 and X!= 1 :
                print("Le déplacement est impossible")
                return None
            elif a == X+1 or b == X+2 :
                plateau[X,Y] = CV
                p[0] = [a,b]
                plateau[a,b] = p
                return [a,b], plateau, morts
            else :
                print("Le déplacement est impossible")
                return None
        else :                                       # le pion est blanc
            if a == X-2 and X != 1 :
                print("Le déplacement est impossible")
                return None
            elif a == X-1 or a == X-2 :
                plateau[X,Y] = CV
                p[0] = [a,b]
                plateau[a,b] = p
                return [a,b], plateau, morts
    else :                                           # case occupée par une pièce de même couleur
             print("Le déplacement est impossible")
             return None


def deplacement_tour(p, a, b, plateau, morts):
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if a != X and b != Y:
        print("Le déplacement est impossible")
        return None
    elif plateau[a,b][3] == 0 :                        # déplacement simple
        if traverse_tour(a, b, X, Y, plateau) == True :
            plateau[X,Y] = CV
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        else:
            print("Vous traversez une pièce")
            return None
    else:
            if plateau[a,b][2] != color :             # élimination d'une pièce
                if traverse_tour(a, b, X, Y, plateau) == True :
                    morts.append(plateau[a, b])
                    plateau[X,Y] = CV
                    p[0] = [a,b]
                    plateau[a,b] = p
                    return [a, b], plateau, morts
                else:
                    print("Vous traversez une pièce")
                    return None
            else:                                     # case occupée par une pièce de même couleur
                print("Le déplacement est impossible")
                return None

def deplacement_roi(p, a, b, plateau, morts) :
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if a in {X+1, X, X-1} and b in {Y+1, Y, Y-1} :
        if plateau[a,b][3] == 0:                       # déplacement simple
            plateau[X,Y] = CV
            p[0] = [a,b]
            plateau[a,b] = p
            return [a, b], plateau, morts
        else:
            if plateau[a,b][2] != color :           # élimination d'une pièce
                morts.append(plateau[a, b])
                plateau[X,Y] = CV
                p[0] = [a,b]
                plateau[a,b] = p
                return [a, b], plateau, morts
            else:                                   # case occupée par une pièce de même couleur
                print("Une autre pièce se trouve déjà sur cette case")
                return None
    else:
        print("Le déplacement est impossible")
        return None

def deplacement_fou(p, a , b, plateau, morts) :
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]
    if traverse_fou(a, b, X, Y, plateau) == False :
        print("Vous traversez une pièce")
        return None
    else:
        for k in range(0, 8) :
            if (X - a) in {k, -k} and (Y - b) in {k, -k}:
                if plateau[a,b][3] == 0 :                        # déplacement simple
                    plateau[X,Y] = CV
                    p[0] = [a,b]
                    plateau[a,b] = p
                    return [a, b], plateau, morts
                elif plateau[a,b][2] != color :               # élimination d'une pièce
                    morts.append(plateau[a, b])
                    plateau[X,Y] = CV
                    p[0] = [a,b]
                    plateau[a,b] = p
                    return [a, b], plateau, morts
                else :                                       # case occupée par une pièce de même couleur
                    print("Une autre pièce se trouve déjà sur cette case")
                    return None
            else :
                print("Le déplacement est impossible")
                return None

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
                plateau[X,Y] = CV
                p[0] = [a,b]
                plateau[a,b] = p
                return [a, b], plateau, morts
            else:
                if plateau[a,b][2] != color :            # élimination d'une pièce
                    morts.append(plateau[a, b])
                    plateau[X,Y] = CV
                    p[0] = [a,b]
                    plateau[a,b] = p
                    return [a, b], plateau, morts
                else:                                    # case occupée par une pièce de même couleur
                    print("Une autre pièce se trouve déjà sur cette case")
                    return None
        else:
            print("Le déplacement est impossible")
            return None


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
    if nb_echecs > 0 :
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
                    plateau[0,4], plateau[0,0] = CV, CV
                    return roi, tour, plateau
                else :                          # petit roque
                    roi[0] = [0, 6]
                    tour[0] = [0, 5]
                    plateau[0,6], plateau[0,5] = roi, tour
                    plateau[0,4], plateau[0,7] = CV, CV
                    return roi, tour, plateau
        else :                                  # roque noir
            if roi[0] != [7, 4] and tour[0] not in {[7, 0], [7, 7]} :
                raise ValueError("Roque impossible. L'une des pièces a déjà été déplacée")
            else :
                if tour[3] == 2 :               # grand roque
                    roi[0] = [7, 2]
                    tour[0] = [7, 3]
                    plateau[7,2], plateau[7,3] = roi, tour
                    plateau[7,4], plateau[7,0] = CV, CV
                    return roi, tour, plateau
                else :                          # petit roque
                    roi[0] = [7, 6]
                    tour[0] = [7, 5]
                    plateau[7,6], plateau[7,5] = roi, tour
                    plateau[7,4], plateau[7,7] = CV, CV
                    return roi, tour, plateau

def promotion(p, piece, plateau, morts) :
    color = p[2]
    if piece == "dame":
        if color == "noir":
            if DN1 in morts :
                DN1[0] = pion[0]
                morts[indice[DN1, morts]] = p
                return DN1, morts
            else :
                raise ValueError("promotion impossible")
        else :
            if DB1 in morts :
                DB1[0] = pion[0]
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
            return plateau[a-1, b]
        else :
            return None



#initialsation du jeu

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

PN1 =[[1,0],"pion","noir",1, Pion_noir]
PN2 =[[1,1],"pion","noir",2, Pion_noir]
PN3 =[[1,2],"pion","noir",3, Pion_noir]
PN4 =[[1,3],"pion","noir",4, Pion_noir]
PN5 =[[1,4],"pion","noir",5, Pion_noir]
PN6 =[[1,5],"pion","noir",6, Pion_noir]
PN7 =[[1,6],"pion","noir",7, Pion_noir]
PN8 =[[1,7],"pion","noir",8, Pion_noir]

TN1 = [[0,0],"tour","noir",1, Tour_noire]
CN1 = [[0,1],"cavalier","noir",1, Cavalier_noir]
FN1 = [[0,2],"fou","noir",1, Fou_noir]        #fou qui n'ira que sur les cases blanches
DN = [[0,3],"dame","noir",1, Dame_noire]
RN = [[0,4],"roi","noir",1, Roi_noir]
FN2 = [[0,5],"fou","noir",2, Fou_noir]        #fou qui n'ira que sur les cases noires
CN2 = [[0,6],"cavalier","noir",2, Cavalier_noir]
TN2 = [[0,7],"tour","noir",2, Tour_noire]

PB1 =[[6,0],"pion","blanc",1, Pion_blanc]
PB2 =[[6,0],"pion","blanc",2, Pion_blanc]
PB3 =[[6,0],"pion","blanc",3, Pion_blanc]
PB4 =[[6,0],"pion","blanc",4, Pion_blanc]
PB5 =[[6,0],"pion","blanc",5, Pion_blanc]
PB6 =[[6,0],"pion","blanc",6, Pion_blanc]
PB7 =[[6,0],"pion","blanc",7, Pion_blanc]
PB8 =[[6,0],"pion","blanc",8, Pion_blanc]

TB2 = [[7,0],"tour","blanc",2, Tour_blanche]
CB2 = [[7,1],"cavalier","blanc",2, Cavalier_blanc]
FB2 = [[7,2],"fou","blanc",2, Fou_blanc]       #fou qui n'ira que sur les cases noires
DB = [[7,3],"dame","blanc",1, Dame_blanche]
RB = [[7,4],"roi","blanc",1, Roi_blanc]
FB1 = [[7,5],"fou","blanc",1, Fou_blanc]       #fou qui n'ira que sur les cases blanches
CB1 = [[7,6],"cavalier","blanc",1, Cavalier_blanc]
TB1 = [[7,7],"tour","blanc",1, Tour_blanche]

CV = [[0,0],"case_vide","",0,case_vide]

plateau = numpy.array([[TN1,CN1,FN1,DN,RN,FN2,CN2,TN2],[PN1,PN2,PN3,PN4,PN5,PN6,PN7,PN8],[CV,CV,CV,CV,CV,CV,CV,CV],[CV,CV,CV,CV,CV,CV,CV,CV],[CV,CV,CV,CV,CV,CV,CV,CV],[CV,CV,CV,CV,CV,CV,CV,CV],[PB1,PB2,PB3,PB4,PB5,PB6,PB7,PB8],[TB1,CB1,FB2,DB,RB,FB1,CB2,TB2]])


def event(piece):
    print("piece")
    if piece[3] != 0:
            liste_deplacements = liste_deplacements_piece(piece, plateau)
            for i in range(8):
                for j in range(8):
                    if [i,j] in liste_deplacements:
                        case_i_j = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'green', command=lambda evt, p=piece: event(p))
                        case_i_j.grid(row=i+1,column=j+1)


for i in range(8):
    for j in range(8):
        if (i+j)%2 == 1:
            piece = plateau[i,j]
            img = piece[4]
            case_i_j = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'maroon', command=lambda evt, p=piece: event(p))
            case_i_j.grid(row=i+1,column=j+1)

for i in range(8):
    for j in range(8):
        if (i+j)%2 == 0:
            piece = plateau[i,j]
            img = piece[4]
            case_i_j = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'wheat', command=lambda evt, p=piece: event(p))
            case_i_j.grid(row=i+1,column=j+1)

plateau_visuel.mainloop()

