## RESUME DE NOTRE PROJET

'''Notre projet d'informatique porte sur l'implémentation d'un jeu d'échecs et de stratégies relatives à ce jeu. Avant de réfléchir à une quelconque stratégie, l'un d'entre nous s'est chargé de coder l'ensemble des règles du jeu d'échecs, en commençant par les règles de déplacements des pièces, puis en programmant le reste (comment vérifier si un joueur est en échec, comment caractériser l'échec et mat...). Nous avons également ajouté les règles moins essentielles du jeu, telles que le roque et la promotion d'un pion. En parallèle, l'autre membre de notre binôme s'est occupé de l'interface graphique de notre projet. En effet, nous sommes soucieux d'avoir un programme qui puisse être joué de manière assez simple, en cliquant sur une pièce puis sur la case sur laquelle on veut la déplacer. Il a donc fallu créer le visuel du plateau ainsi que des boutons cliquables sur chaque case de ce dernier. Enfin, nous nous sommes tous deux penchés sur une stratégie à adopter afin que l'utilisateur puisse jouer contre l'ordinateur. L'implémentation de cette stratégie consiste à créer une fonction d'évaluation du plateau qui attribue à chaque joueur un certain nombre de points, puis à renvoyer le déplacement qui maximise ce nombre de points. Nous avons prévu deux niveaux de difficulté pour l'ordinateur, avec deux types de stratégies différentes. '''

## IMPORTATION DES MODULES NECESSAIRES
import numpy
import tkinter
import copy
import random

## IMPLEMENTATION DES REGLES DE DEPLACEMENT
''' Dans chaque fonction de déplacement suivante, p représentera une pièce. Cette pièce est représentée sous la forme d'une liste [[X,Y], type, couleur, numero, image, bool] où [X,Y] seront les coordonnées de cette pièce sur le plateau, type le type de pièce (roi, dame...), couleur la couleur à laquelle appartient la pièce (noirs ou blancs), numero permet de distinguer les pièces qui sont identiques, image correspond à la représentation graphique de la pièce sur l'interface et bool indique si la pièce a déjà bougé ou non. Cette dernière variable est utile pour le roque.
a, b sont les coordonnées de la case où on déplace p.
Le plateau est quant à lui représenté par une matrice. plateau[a,b] renvoie la pièce qui se trouve sur les coordonnées (a,b) du plateau. On caractérisera les cases vides par CV, définie par : [[X,Y],"case_vide","",0,case_vide, False], où case_vide correspond à l'image de la case vide sur l'interface graphique.
La variable morts en argument de chaque fonction correspond à la liste des pièces éliminées au cours de la partie. '''

## Pion

''' Le pion se déplace en avançant d'une case (ou deux s'il n'a pas encore avancé et élimine des pièces en avançant d'une case en diagonale.'''

def deplacement_pion(p, a, b, plateau, morts):
    # On vérifie que la case choisie est bien sur le plateau
    assert 0 <= a <= 7
    assert 0 <= b <= 7
    [X, Y] = p[0]
    color = p[2]

    if b in {Y+1, Y-1} and plateau[a,b][3] != 0 and ((a == X+1 and color == "noirs") or (a == X-1 and color == "blancs")) :
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
        if color == "noirs" :                        # le pion est noir
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


## Tour

''' Pour se déplacer avec la tour, il est nécessaire de créer une fonction qui indique si le déplacement que l'on souhaite n'implique pas de traverser une pièce, auquel cas ce déplacement est impossible.'''

def traverse_tour(a, b, X, Y, plateau) :                         # renvoie si on peut se déplacer sans traverser de pièce
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

''' La tour se déplace horizontalement ou verticalement donc pour que la tour puisse se déplacer dans les règles, l'une des coordonnées choisies doit être égale à l'une de ses coordonnées d'origine.'''

def deplacement_tour(p, a, b, plateau, morts):
    # On vérifie que la case choisie est bien sur le plateau
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


## Cavalier

''' Le cavalier se déplace en formant un L, donc il faut que la différence en valeur absolue entre la coordonnée choisie et la coordonnée initiale selon le premier axe soit égale à 2 (respectivement 1) et que l'autre différence entre les valeurs des coordonnées sur le second axe soit alors égale en valeur absolue à 1 (respectivement 2).'''

def deplacement_cavalier(p, a, b, plateau, morts) :
    # On vérifie que la case choisie est bien sur le plateau
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


## Fou

''' Pour se déplacer avec le fou, il est nécessaire de créer une fonction qui indique si le déplacement que l'on souhaite n'implique pas de traverser une pièce, auquel cas ce déplacement est impossible. '''

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


''' Le fou se déplace sur les diagonales donc il faut que la différence Y-b soit égale en valeur absolue à X-a.'''

def deplacement_fou(p, a , b, plateau, morts) :
    # On vérifie que la case choisie est bien sur le plateau
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


## Dame

'''La dame peut se déplacer verticalement et horizontalement, comme la tour, mais également en diagonale, comme le fou. Donc selon les valeurs de a et b, on déplace la dame par l'intermédiaire de la fonction deplacement_tour ou deplacement_fou.'''


def deplacement_dame(p, a, b, plateau, morts) :
    [X, Y] = p[0]
    if a == X or b == Y :                               # déplacement selon une ligne/colonne
        deplacement_tour(p, a, b, plateau, morts)
    else:                                               # déplacement sur une diagonale
        deplacement_fou(p, a, b, plateau, morts)


## Roi

''' Le roi peut se déplacer d'une case dans toutes les directions à partir de sa case d'origine.'''

def deplacement_roi(p, a, b, plateau, morts) :
    # On vérifie que la case choisie est bien sur le plateau
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


## Utilisation des fonctions de déplacements dans le jeu

''' La fonction suivante permet d'effectuer le déplacement de la pièce choisie selon les règles de déplacements qui lui sont propres.'''

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


## LES COUPS SPECIAUX

''' Maintenant que nous avons établi des règles sur les déplacements de chaque type de pièce, il reste encore à pouvoir effectuer un roque (petit ou grand) et également la promotion d'un pion.'''

## La promotion

''' La fonction test_promotion prend en argument la dernière pièce jouée et vérifie si la promotion de cette pièce est possible. Elle exécute la fonction affiche_promotion le cas échéant. '''

def test_promotion(piece_selectionnee):
    liste_promotion_possible = []

    if piece_selectionnee[1] == 'pion':
        if piece_selectionnee[0][0] in {0, 7}: # On vérifie si le pion est sur la dernière ligne du plateau : cette condition suffit car il est impossible pour un pion blanc (respectivement noir) de se retrouver sur la ligne d'indice 7 (respectivement d'indice 0) car les pions ne reculent pas
            # On vérifie ensuite les pièces disponibles
            if piece_selectionnee[2] == 'noirs':
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


''' La fonction affiche_promotion s'exécute si la promotion de la dernière pièce jouée est possible. Elle prend en argument la liste des promotions possibles et active les boutons permettant au joueur de sélectionner la pièce qui remplacera son pion. '''

def affiche_promotion(liste_promotion_possible):
    for elem in liste_promotion_possible:
        if elem[1] == 'dame':
            promotion_dame['state'] = 'normal'
        if elem[1] == 'fou':
            promotion_fou['state'] = 'normal'
        if elem[1] == 'cavalier':
            promotion_cavalier['state'] = 'normal'


''' La fonction promotion_fou_fct s'exécute quand un joueur clique sur le bouton "fou". Elle permet le remplacement d'un pion en un fou. '''

def promotion_fou_fct():
    global piece_promue
    # Remplacement du type de pièce
    piece_promue[1] = 'fou'

    # Remplacement de l'image de la pièce
    if piece_promue[2] == "noirs":
        piece_promue[4] = Fou_noir
    else:
        piece_promue[4] = Fou_blanc

    # Mise à jour de la case_a_b du plateau
    a, b = piece_promue[0]
    ch = "case_"+str(a)+"_"+str(b)
    plateau[a,b] = piece_promue
    globals()[ch]['image'] = piece_promue[4]
    globals()[ch]['command'] = lambda p=piece_promue: event(p)

    reinitialisation_bouton_promotion()


''' La fonction promotion_dame_fct s'exécute quand un joueur clique sur le bouton "dame". Elle permet le remplacement d'un pion en une dame. '''

def promotion_dame_fct():
    global piece_promue
    piece_promue[1] = 'dame'

    if piece_promue[2] == "noirs":
        piece_promue[4] = Dame_noire
    else:
        piece_promue[4] = Dame_blanche

    a, b = piece_promue[0]
    ch = "case_"+str(a)+"_"+str(b)
    plateau[a,b] = piece_promue
    globals()[ch]['image'] = piece_promue[4]
    globals()[ch]['command'] = lambda p=piece_promue: event(p)

    reinitialisation_bouton_promotion()


''' La fonction promotion_cavalier_fct s'exécute quand un joueur clique sur le bouton "cavalier". Elle permet le remplacement d'un pion en un cavalier. '''

def promotion_cavalier_fct():
    global piece_promue
    piece_promue[1] = 'cavalier'

    if piece_promue[2] == "noirs":
        piece_promue[4] = Cavalier_noir
    else:
        piece_promue[4] = Cavalier_blanc

    a, b = piece_promue[0]
    ch = "case_"+str(a)+"_"+str(b)
    plateau[a,b] = piece_promue
    globals()[ch]['image'] = piece_promue[4]
    globals()[ch]['command'] = lambda p=piece_promue: event(p)

    reinitialisation_bouton_promotion()


## Le roque

''' La fonction test_roque indique si le roque est possible au début du tour du joueur. Le cas échéant, le bouton petit_roque_bouton ou grand_roque_bouton s'active en fonction du roque possible.'''

def test_roque():
    global joueur
    # On réinitialise les boutons de roque
    petit_roque_bouton['state']='disabled'
    grand_roque_bouton['state']='disabled'

    # Pour effectuer un roque il faut dans un premier temps que le joueur n'ait jamais été mis en échec.
    if nb_echecs[joueur] == 0:
        if joueur == "noirs":
            a1, b1 = TN1[0]
            a2, b2 = TN2[0]
            X, Y = RN[0]

            # Pour effectuer un roque, il faut également qu'aucune des deux pièces concernées par le roque n'ait effectué de mouvement depuis le début de la partie. En outre, les cases situées entre les deux pièces doivent être vides.
            if RN[5] == False and TN1[5] == False and traverse_tour(a1, b1, X, Y, plateau) == True:
                grand_roque_bouton['state']='normal'

            if RN[5] == False and TN2[5] == False and traverse_tour(a2, b2, X, Y, plateau) == True:
                petit_roque_bouton['state']='normal'

        else:
            a1, b1 = TB1[0]
            a2, b2 = TB2[0]
            X, Y = RB[0]
            if RB[5] == False and TB1[5] == False and traverse_tour(a1, b1, X, Y, plateau) == True:
                petit_roque_bouton['state']='normal'

            if RB[5] == False and TB2[5] == False and traverse_tour(a2, b2, X, Y, plateau) == True:
                grand_roque_bouton['state']='normal'

''' Les fonctions suivantes permettent d'effectuer un roque (petit ou grand). Dans les deux cas, on prend les deux pièces concernées et on effectue deux déplacements ce qui crée deux cases vides.'''

def grand_roque():
    global joueur

    # Sélection des pièces en fonction de la couleur du joueur
    if joueur == 'noirs':
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

    # Modification des quatres cases concernées par le roque
    img1 = case_vide
    piece1 = [[i,4],"case_vide","",0,case_vide]
    globals()[ch1]['command'] = lambda p=piece1: event(p)
    globals()[ch1]['image'] = img1

    img1prime = piece_selectionnee1[4]
    piece1prime = [[i,2],"roi",joueur,1,piece_selectionnee1[4], True]
    globals()[ch1prime]['command'] = lambda p=piece1prime: event(p)
    globals()[ch1prime]['image'] = img1prime

    img2 = case_vide
    piece2 = [[i,0],"case_vide","",0,case_vide]
    globals()[ch2]['command'] = lambda p=piece2: event(p)
    globals()[ch2]['image'] = img2

    img2prime = piece_selectionnee2[4]
    piece2prime = [[i,3],"tour",joueur,1,piece_selectionnee2[4], True]
    globals()[ch2prime]['command'] = lambda p=piece2prime: event(p)
    globals()[ch2prime]['image'] = img2prime

    plateau[i,4] = piece1
    plateau[i,3] = piece2prime
    plateau[i,2] = piece1prime
    plateau[i,0] = piece2

    # Le roque compte comme un déplacement donc on passe au joueur suivant.
    if joueur == "blancs":
        joueur = "noirs"
    else:
        joueur = "blancs"

    m.set("C'est aux "+ joueur +" de jouer")
    liste_deplacements = []
    piece_selectionnee = None

    # On réinitialise les boutons de roque
    grand_roque_bouton['state']='disabled'
    petit_roque_bouton['state']='disabled'


def petit_roque():
    global joueur

    if joueur == 'noirs':
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
    piece1prime = [[i,6],"roi",joueur,1,piece_selectionnee1[4], True]
    globals()[ch1prime]['command'] = lambda p=piece1prime: event(p)
    globals()[ch1prime]['image'] = img1prime

    img2 = case_vide
    piece2 = [[i,7],"case_vide","",0,case_vide]
    globals()[ch2]['command'] = lambda p=piece2: event(p)
    globals()[ch2]['image'] = img2

    img2prime = piece_selectionnee2[4]
    piece2prime = [[i,5],"tour",joueur,1,piece_selectionnee2[4], True]
    globals()[ch2prime]['command'] = lambda p=piece2prime: event(p)
    globals()[ch2prime]['image'] = img2prime

    plateau[i,4] = piece1
    plateau[i,5] = piece2prime
    plateau[i,6] = piece1prime
    plateau[i,7] = piece2

    if joueur == "blancs":
        joueur = "noirs"
    else:
        joueur = "blancs"
    m.set("C'est aux "+ joueur +" de jouer")

    liste_deplacements = []
    piece_selectionnee = None

    grand_roque_bouton['state']='disabled'
    petit_roque_bouton['state']='disabled'


## Les fonctions nécessaires au bon déroulement du jeu

''' La fonction mode_de_jeu prend en argument le texte du bouton pressé et enregistre ainsi le mode de jeu choisi par l'utilisateur. '''

def mode_de_jeu(text):
    global mode_de_jeu_choisi

    # On indique le mode de jeu choisi
    mode_de_jeu_choisi = text
    globals()[text]['background'] = 'yellow'

    # Dans le cas où le joueur joue contre l'ordi, on lui propose de choisir la difficulté
    if mode_de_jeu_choisi == 'bouton_ordi_vs_joueur':
        difficulte_facile['state'] = 'normal'
        difficulte_difficile['state'] = 'normal'

    # On désactive le choix du mode de jeu
    bouton_2ordis['state']='disabled'
    bouton_ordi_vs_joueur['state']='disabled'
    bouton_2joueurs['state']='disabled'

    # On indique que la partie peut commencer
    m.set("C'est aux blancs de jouer")


'''La fonction find_color permet d'obtenir la liste des pièces de chaque couleur à n'importe quel moment du jeu en prenant en compte les pièces déjà éliminées, stockées dans la liste morts.'''

def find_color(plateau, morts):
    blancs = [PB1,PB2,PB3,PB4,PB5,PB6,PB7,PB8,TB2,CB2,FB2,DB,RB,FB1,CB1,TB1]
    noirs = [TN1,CN1,FN1,DN,RN,FN2,CN2,TN2,PN1,PN2,PN3,PN4,PN5,PN6,PN7,PN8]

    for elem in morts:
        if elem in blancs:
            blancs.remove(elem)
        elif elem in noirs:
            noirs.remove(elem)

    return noirs, blancs


''' Au cours de la partie, il sera nécessaire d'avoir accès à la liste des déplacements que peut effectuer chacune des pièces (par exemple pour tester si le roi est en échec). Ainsi, grâce à try: except:, la fonction suivante peut tester tous les déplacements possibles sur le plateau mais en conservant uniquement ceux qui ne déclencheront pas d'erreur.'''

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


''' Cependant, cette fonction ne prend pas en compte le fait que le déplacement d'une pièce puisse être compromis car il impliquerait de mettre le roi en échec. Par conséquent, nous avons codé la fonction suivante, qui prend cet aspect en compte et renvoie la nouvelle liste de déplacements possibles par pièce, sans y compter les déplacements qui mettraient le roi en échec.'''

def liste_deplacements_possibles(piece, plateau, morts) :
    liste = liste_deplacements_piece(piece, plateau, morts)
    liste_finale = []
    color = piece[2]

    for couple in liste :       # on simule le déplacement sur une copie du plateau pour en voir les effets
        copie_plateau = copy.copy(plateau)
        copie_morts = copy.copy(morts)
        copie_piece = copy.copy(piece)
        deplacement(copie_piece,couple[0],couple[1],copie_plateau, copie_morts)
        noirs, blancs = find_color(copie_plateau, copie_morts)

        deplacements_noirs = []
        deplacements_blancs = []

        for p in noirs:        # on regroupe tous les déplacements possibles des pièces noires dans une même liste
            for elem in liste_deplacements_piece(p, copie_plateau, copie_morts):
                deplacements_noirs.append(elem)

        for p in blancs:      # on regroupe tous les déplacements possibles des pièces blanches dans une même liste
            for elem in liste_deplacements_piece(p, copie_plateau, copie_morts):
                deplacements_blancs.append(elem)

        # on copie les pièces relatives aux deux rois
        new_rb = copy.copy(RB)
        new_rn = copy.copy(RN)

        if piece[1] == "roi":
            if color == "blancs":
                new_rb[0] = couple
            else:
                new_rn[0] = couple

        # on teste si les coordonnées d'un des rois sont atteintes par l'une des pièces opposées, i.e. si ses coordonnées se trouvent dans la liste des déplacements de la couleur opposée
        if color == "blancs":
            if new_rb[0] not in deplacements_noirs:
                liste_finale.append(couple)

        else :
            if new_rn[0] not in deplacements_blancs:
                liste_finale.append(couple)

    return liste_finale


''' A chaque tour de jeu, il est nécessaire de savoir si un joueur est en échec ou non. Pour savoir cela, nous avons créé la fonction test_echec qui prend en argument la matrice du plateau, la liste des morts et le nombre d'échecs de chaque joueur depuis le début de la partie. test_echec renvoie un booléen, la liste des pièces mises en échec s'il y a échec et le nombre d'échecs actualisé.'''

def test_echec(plateau, morts, nb_echecs):
    noirs, blancs = find_color(plateau, morts)

    deplacements_noirs = []
    deplacements_blancs = []

    for p in noirs:
        for elem in liste_deplacements_piece(p, plateau, morts):
            deplacements_noirs.append(elem)

    for p in blancs:
        for elem in liste_deplacements_piece(p, plateau, morts):
            deplacements_blancs.append(elem)

    # comme pour la fonction liste_deplacements_possibles, on teste si les coordonnées sur lesquelles se trouve le roi peuvent être atteintes par une pièce adverse.
    if RB[0] in deplacements_noirs :
        nb_echecs["blancs"] += 1
        return True, blancs, nb_echecs

    elif RN[0] in deplacements_blancs :
        nb_echecs["noirs"] += 1
        return True, noirs, nb_echecs

    return False, 0, nb_echecs


'''La fonction echec_et_mat teste tout d'abord s'il y a échec. Dans ce cas, elle va tester s'il existe un déplacement qui permettrait de sortir de l'échec.'''

def echec_et_mat(plateau, morts, nb_echecs):
    if test_echec(plateau, morts, nb_echecs) == False :
        pass
    else :
        test, couleur, nb_echecs = test_echec(plateau, morts, nb_echecs)       # couleur = couleur mise en échec
        color_name = couleur[0][2]
        for piece in couleur :
            if liste_deplacements_possibles(piece, plateau, morts) != [] :    # il existe un déplacement possible pour le joueur de cette couleur : il peut sortir de l'échec donc n'est pas mat
                return False, color_name
    return True, color_name

## Les fonctions pour choisir la difficulté si on joue contre l'ordinateur

def difficulte_facile_fct():
    global difficulte
    difficulte = False
    difficulte_facile['background'] = 'yellow'

    difficulte_facile['state'] = 'disabled'
    difficulte_difficile['state'] = 'disabled'

def difficulte_difficile_fct():
    global difficulte
    difficulte = True
    difficulte_difficile['background'] = 'yellow'

    difficulte_facile['state'] = 'disabled'
    difficulte_difficile['state'] = 'disabled'


## La fonction de jeu principale

''' Lorsque le joueur clique sur une case du plateau, la fonction event s'exécute. Cette fonction va réaliser plusieurs choses en fonction du cas de figure. '''

def event(piece):
    global joueur
    global piece_selectionnee
    global liste_deplacements
    global mode_de_jeu_choisi
    global piece_promue
    global difficulte

    if mode_de_jeu_choisi == None:
        m.set('Veuillez choisir un mode de jeu')

    else:
        # On réinitialise le message d'information
        m.set('')

        a, b = piece[0]
        ch = "case_"+str(a)+"_"+str(b)
        color_fond = globals()[ch]['background']

        # On distingue les cas en fonction du mode_de_jeu_choisi
        if mode_de_jeu_choisi == "bouton_ordi_vs_joueur" and joueur == 'noirs':
            if difficulte == None:
                m.set('Choississez une difficulté')
            else:
                # Dans le cas où c'est à un joueur ordi de jouer on utilise la fonction stratégie
                piece_ordi, deplacement_ordi = strategie(plateau, nb_echecs, morts, difficulte)
                a, b = deplacement_ordi[0], deplacement_ordi[1]
                ch = "case_"+str(a)+"_"+str(b)
                piece_selectionnee = piece_ordi

                deplacement_effectif(a, b, ch)
                m.set("C'est aux "+ joueur +" de jouer")

        elif mode_de_jeu_choisi == "bouton_2ordis":
            if joueur == 'blancs':
                piece_ordi, deplacement_ordi = strategie(plateau, nb_echecs, morts, False)          #stratégie MinMax
            else :
                piece_ordi, deplacement_ordi = strategie(plateau, nb_echecs, morts, True)          #stratégie meilleur_coup_fct
            a, b = deplacement_ordi[0], deplacement_ordi[1]
            ch = "case_"+str(a)+"_"+str(b)
            piece_selectionnee = piece_ordi

            deplacement_effectif(a, b, ch)
            m.set("C'est aux "+ joueur +" de jouer")

        else: # Cas où c'est à un joueur non ordi de jouer
            if color_fond == 'green': # Cas où la case sélectionnée est verte (ie le déplacement de la pièce précédemment sélectionnée est possible)
                deplacement_effectif(a, b, ch)


            elif piece == piece_selectionnee: # Si la case sélectionnée est la même que précédemment, on réinitialise tout
                liste_deplacements = []
                piece_selectionnee = None
                reinitialisation_couleur_plateau()


            elif piece[3] != 0 and liste_deplacements == []: # Si la case sélectionnée n'est pas vide et qu'il n'y a pas de pièce sélectionnée pour le moment, on recherche les déplacements possibles pour la pièce située sur la case sélectionnée et on les affiche en vert
                    reinitialisation_bouton_promotion()
                    piece_selectionnee = piece
                    if piece_selectionnee[2] == joueur:
                        liste_deplacements = liste_deplacements_possibles(piece, plateau, morts)
                        for i in range(8):
                            for j in range(8):
                                if [i,j] in liste_deplacements:
                                    ch = "case_"+str(i)+"_"+str(j)
                                    globals()[ch]['background'] = 'green'

            test_roque()
            m.set("C'est aux "+ joueur +" de jouer")

        # On teste si le joueur suivant est en échec après le déplacement effectif d'une pièce adverse
        echec = test_echec(plateau, morts, nb_echecs)
        if echec[0] == True:
            # On teste s'il y a mat
            test, color_name = echec_et_mat(plateau, morts, nb_echecs)
            if test == True:
                if joueur == 'noirs':
                    m.set('Les blancs ont gagné !')
                else:
                    m.set('Les noirs ont gagné !')

            # On affiche la case du roi en rouge pour signaler au joueur suivant qu'il est en échec
            if joueur == 'noirs':
                i, j = RN[0]
                ch = "case_"+str(i)+"_"+str(j)
                globals()[ch]['background'] = 'red'

            else:
                i, j = RB[0]
                ch = "case_"+str(i)+"_"+str(j)
                globals()[ch]['background'] = 'red'






''' La fonction suivante s'exécute dans le cas où le joueur a cliqué sur une case verte. Elle va effectuer le déplacement de la pièce sélectionnée sur le plateau. '''

def deplacement_effectif(a, b, ch):
    global joueur
    global piece_selectionnee
    global liste_deplacements
    global piece_promue

    i, j = piece_selectionnee[0]
    chprime = "case_"+str(i)+"_"+str(j)
    globals()[chprime]['image'] = case_vide
    piece = [[i,j],"case_vide","",0,case_vide]
    globals()[chprime]['command'] = lambda p=piece: event(p)
    deplacement(piece_selectionnee, a, b, plateau, morts)

    piece = plateau[a,b]
    globals()[ch]['image'] = piece_selectionnee[4]
    globals()[ch]['command'] = lambda p=piece: event(p)

    # On indique que la pièce a bougé
    piece_selectionnee[5] = True

    # On vérifie si la promotion de la pièce est possible. Le cas échéant on propose au joueur de promouvoir sa pièce.
    test_promotion(piece_selectionnee)

    if promotion_dame['state'] == 'normal' or promotion_cavalier['state'] == 'normal' or promotion_fou['state'] == 'normal':
        piece_promue = copy.copy(piece_selectionnee)


    # On change de joueur et on réinitialise la liste des déplacements, la pièce sélectionnée et les couleurs des cases du plateau.
    if joueur == "blancs":
        joueur = "noirs"
    else:
        joueur = "blancs"

    liste_deplacements = []
    piece_selectionnee = None

    reinitialisation_couleur_plateau()


''' Les deux fonctions suivantes sont des fonctions permettant de réinitialiser certains paramètres'''

def reinitialisation_couleur_plateau():
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


def reinitialisation_bouton_promotion():
    promotion_dame['state'] = 'disabled'
    promotion_fou['state'] = 'disabled'
    promotion_cavalier['state'] = 'disabled'


## IMPLEMENTATION DE LA STRATEGIE
# Evaluation du plateau

'''Afin d'implémenter une stratégie, il est nécessaire de créer une fonction qui évalue le plateau pour chaque joueur et qui attribue à chacun un certain nombre de points. '''

''' Tout d'abord, on attribue à chaque pièce une certaine valeur. Cette fonction sera utilisée lorsqu'il faudra par exemple compter les points des joueurs, en fonction des pièces qui ont été éliminées.'''

def points_piece(piece):
    points = 0
    if piece[1] == "pion":
            points = 2
    elif piece[1] == "cavalier":
            points = 6
    elif piece[1] == "fou":
            points = 8
    elif piece[1] == "tour":
            points = 10
    elif piece[1] == "dame":            # dame = fou + tour
            points = 18
    elif piece[1] == "roi":
            points = 6
    return points


''' La fonction suivante prend en argument la liste des pièces éliminées d'une certaine couleur et renvoie la somme des points perdus par le joueur.'''

def points_morts(color):
    points = 0
    if color != []:
        for piece in color:
            points += points_piece(piece)
    return points


''' Avec ces premières attributions de points, nous pouvons alors définir une fonction d'évaluation du plateau .'''

def evalue_plateau(plateau, nb_echecs, morts):
    points = {"blancs" : 0, "noirs" : 0}
    morts_blancs = []
    morts_noirs = []
    for p in morts :
        if p[2] == "blancs":
            morts_blancs.append(p)
        else:
            morts_noirs.append(p)
    # on initialise les points perdus par chacun des joueurs en soustrayant le nombre de points perdus à cause des pièces qui se sont fait éliminer
    points["blancs"] -= points_morts(morts_noirs)
    points["noirs"] -= points_morts(morts_noirs)
    Test, color, _ = test_echec(plateau, morts, nb_echecs)         # on enlève des points si le roi est actuellement en échec
    if color == "blancs" :
        points["blancs"] -= 2
        points["noirs"] += 2
    if color == "noirs":
        points["blancs"] += 2
        points["noirs"] -= 2

    return points


# Première stratégie : 1er niveau de difficulté

''' Dans cette première fonction, on cherche à maximiser les points du joueur sans anticiper grandement les déplacements futurs du joueur adverse. Ainsi, cette fonction renvoie la pièce à choisir et le coup à effectuer pour avoir un maximum de points. Pour avoir des choix de déplacements plus pertinents, on va attribuer des points bonus et malus selon si le coup choisi permet d'éliminer une pièce, d'en menacer une, ou bien mène à l'élimination de la pièce ayant effectué le coup. Ces bonus/malus sont alors déterminés à partir de la fonction points_piece de sorte que l'algorithme veuille sacrifier un pion pour éliminer une pièce forte comme une dame ou un fou. '''

def meilleur_coup_fct(color_name, plateau, nb_echecs, morts):
    noirs, blancs = find_color(plateau, morts)

    meilleure_piece, meilleur_deplacement = 0, 0

    if color_name == "noirs":
        other_color_name = "blancs"
        color, other_color = noirs, blancs
    else :
        other_color_name = "noirs"
        other_color, color = noirs, blancs

    init_point = -100                          # on initialise à une valeur très petite pour être sur qu'un meilleur déplacement est possible

    for piece in color :
        for couple in liste_deplacements_possibles(piece, plateau, morts):
            points_bonus = 0
            a, b = couple[0], couple[1]
            copie_plateau = copy.copy(plateau)
            copie_piece = copy.copy(piece)
            copie_nb_echecs = copy.copy(nb_echecs)
            copie_morts = copy.copy(morts)
            deplacement(copie_piece, a, b, copie_plateau, copie_morts)

            if copie_morts != morts:
                points_bonus += 6*points_piece(copie_morts[-1]) # on récompense le fait que la pièce en élimine une autre

            noirs, blancs = find_color(copie_plateau, copie_morts) # on actualise le plateau
            if color_name == "noirs":
                color, other_color = noirs, blancs
            else :
                other_color, color = noirs, blancs

            for piece_ennemie in other_color :
                liste = liste_deplacements_possibles(copie_piece, copie_plateau, copie_morts)
                liste_adverse = liste_deplacements_possibles(piece_ennemie, copie_plateau, copie_morts)

                if copie_piece[0] in liste_adverse:                        # on sanctionne le fait que la pièce se fasse éliminer
                    points_bonus -= 6*points_piece(copie_piece)
                if piece_ennemie[0] in liste :                                # on récompense le fait que la pièce menace une pièce adverse
                    points_bonus += 4*points_piece(copie_piece)

            points = evalue_plateau(copie_plateau, copie_nb_echecs, copie_morts)[color_name] + points_bonus

            if points > init_point :
                init_point = points
                meilleure_piece = piece
                meilleur_deplacement = couple

    if meilleure_piece == 0 and meilleur_deplacement == 0:  # si aucun déplacement n'est satisfaisant, on en choisit un au hasard
        liste = []
        for piece in color:
            if liste_deplacements_possibles(piece, plateau, morts) != []:
                liste.append(piece)
        meilleure_piece = liste[random.randint(0, len(liste) - 1)]
        meilleurs_coups_possibles = liste_deplacements_possibles(meilleure_piece, plateau, morts)
        meilleur_deplacement = meilleurs_coups_possibles[random.randint(0, len(meilleurs_coups_possibles)-1)]

    return meilleure_piece, meilleur_deplacement


# Seconde stratégie : 2nd niveau de difficulté

'''Pour cette seconde stratégie, nous avons décidé d'implémenter l'algorithme MinMax. Il s'applique bien ici car le jeu d'échecs est un jeu à somme nulle. Dans notre cas, cet algorithme consiste à simuler chaque noeud possible pour le joueur, i.e. chaque combinaison pièce/coup qu'il puisse jouer. Au sein de chaque noeud, on simule chaque noeud adverse, puis on évalue le plateau pour le premier joueur. L'adversaire cherchant le coup qui minimise le nombre de points du premier joueur, on conserve alors pour chaque noeud du joueur le minimum des points qu'il puisse avoir à la suite du coup de son adversaire. Enfin, parmi la liste de ces minima, le joueur choisira le coup pour lequel il obtient le maximum de cette liste. Par conséquent, l'algorithme MinMax renverra le meilleur coup qu'il puisse effectuer. Là encore, pour avoir plus de précisions dans le calcul des points, on met en place des points bonus/malus qui viendront s'ajouter au total du nombre de points du joueurs donné par la fonction evalue_plateau.'''

def minmax(color_name, plateau, nb_echecs, morts):
    noirs, blancs = find_color(plateau, morts)
    meilleure_piece, meilleur_coup = 0, 0
    liste_min_node = []         # pour chaque noeud du joueur, l'adversaire veut minimiser les points du joueurs : on conservera les minima de chaque noeud, que l'on stockera dans la variable suivante
    liste_max_node = []         # étant donné le jeu de l'adversaire, le joueur veut maximiser ses points :  il choisira donc le coup qui rapporte le plus de points parmi cette liste

    if color_name == "noirs":
        other_color_name = "blancs"
        color, other_color = noirs, blancs
    else :
        other_color_name = "noirs"
        other_color, color = noirs, blancs

    for node_piece in color :           # chaque combinaison piece/couple est un noeud de l'arbre de jeu
        for node_couple in liste_deplacements_possibles(node_piece, plateau, morts):
            points_bonus = 0
            a, b = node_couple[0], node_couple[1]
            copie_plateau = copy.copy(plateau)
            copie_piece = copy.copy(node_piece)
            copie_nb_echecs = copy.copy(nb_echecs)
            copie_morts = copy.copy(morts)
            deplacement(copie_piece, a, b, copie_plateau, copie_morts)

            if copie_morts != morts:
                points_bonus += 6*points_piece(copie_morts[-1]) #on récompense le fait que la pièce en élimine une autre
            noirs, blancs = find_color(copie_plateau, copie_morts) # on actualise le plateau

            if color_name == "noirs":        # on actualise le plateau si éventuellement le déplacement simulé a éliminé une pièce adverse
                other_color_name = "blancs"
                color, other_color = noirs, blancs
            else :
                other_color_name = "noirs"
                other_color, color = noirs, blancs

            for piece_adverse in other_color:
                liste = liste_deplacements_possibles(copie_piece, copie_plateau, copie_morts)
                liste_adverse = liste_deplacements_possibles(piece_adverse, copie_plateau, copie_morts)

                if copie_piece[0] in liste_adverse:                        # on sanctionne le fait que la pièce se fasse éliminer
                    points_bonus -= 6*points_piece(copie_piece)
                if piece_adverse[0] in liste :                                # on récompense le fait que la pièce menace une pièce adverse
                    points_bonus += 4*points_piece(copie_piece)

                for coup_adverse in liste_adverse:
                    c, d = coup_adverse[0], coup_adverse[1]
                    copie2_plateau = copy.copy(copie_plateau)
                    copie_piece_adverse = copy.copy(piece_adverse)
                    copie2_nb_echecs = copy.copy(copie_nb_echecs)
                    copie2_morts = copy.copy(copie_morts)
                    deplacement(copie_piece_adverse, c, d, copie2_plateau, copie2_morts)

                    points = evalue_plateau(copie2_plateau, copie2_nb_echecs, copie2_morts)[color_name] + points_bonus
                    liste_min_node.append(points)       # on n'a pas besoin de stocker les déplacements de la pièce adverse, il faut juste stocker les points du joueur après le déplacement de la pièce adverse
            min_node = min(liste_min_node)

            liste_max_node.append([node_piece, node_couple, min_node])

    max_node = max(elem[2] for elem in liste_max_node)  # le joueur choisit le déplacement qui maximise ses points

    for elem in liste_max_node:
        if elem[2] == max_node:
            choix = elem
    meilleure_piece = choix[0]
    meilleur_coup = choix[1]
    return meilleure_piece, meilleur_coup

''' Après avoir confronté les deux stratégies, nous nous sommes rendu compte que bien que l'algorithme MinMax soit plus élaboré, la stratégie qui y est associée n'est pas plus efficace que l'algorithme de meilleur_coup_fct. Ce constat résulte sûrement d'une évaluation du plateau peut-être pas aussi complète que ce qu'elle devrait être pour que l'algorithme soit vraiment efficace. Par conséquent, on considérera par la suite que cette stratégie correspond à un niveau de difficulté faible. '''

# Choix de la stratégie

''' Enfin, on résume ces deux fonctions de stratégie dans une seule. La variable difficulté est un booléen. Si ce booléen vaut False, alors on renvoie la stratégie MinMax. Sinon on renvoie la stratégie donnée par meilleur_coup_fct. Pour éviter tout problème, dans le cas où aucun déplacement n'est satisfaisant, on renverra un coup aléatoire.'''

def strategie(plateau, nb_echecs, morts, difficulte):
    global joueur
    color_name = copy.copy(joueur)

    if difficulte == False :
        meilleure_piece, meilleur_coup = minmax(color_name, plateau, nb_echecs, morts)
    elif difficulte == True:
        meilleure_piece, meilleur_coup =  meilleur_coup_fct(color_name, plateau, nb_echecs, morts)
    if meilleure_piece == 0 and meilleur_coup == 0:  # si aucun déplacement n'est satisfaisant, on en choisit un au hasard
        liste = []
        for piece in color:
            if liste_deplacements_possibles(piece, plateau, morts) != []:
                liste.append(piece)
        meilleure_piece = liste[random.randint(0, len(liste) - 1)]
        meilleurs_coups_possibles = liste_deplacements_possibles(meilleure_piece, plateau, morts)
        meilleur_coup = meilleurs_coups_possibles[random.randint(0, len(meilleurs_coups_possibles)-1)]

    return meilleure_piece, meilleur_coup

## L'INTERFACE GRAPHIQUE

## Les variables globales nécessaires

joueur = "blancs"
liste_deplacements = []
piece_selectionnee = None
morts =[]
nb_echecs = {"blancs" :0, "noirs": 0}
mode_de_jeu_choisi = None
piece_promue = None
difficulte = None


## Création du widget plateau_visuel

plateau_visuel = tkinter.Tk()

## Téléchargement des images des pièces

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


# Initialisation des pièces
PN1 =[[1,0],"pion","noirs",1, Pion_noir, False]
PN2 =[[1,1],"pion","noirs",2, Pion_noir, False]
PN3 =[[1,2],"pion","noirs",3, Pion_noir, False]
PN4 =[[1,3],"pion","noirs",4, Pion_noir, False]
PN5 =[[1,4],"pion","noirs",5, Pion_noir, False]
PN6 =[[1,5],"pion","noirs",6, Pion_noir, False]
PN7 =[[1,6],"pion","noirs",7, Pion_noir, False]
PN8 =[[1,7],"pion","noirs",8, Pion_noir, False]
TN1 = [[0,0],"tour","noirs",1, Tour_noire, False]
CN1 = [[0,1],"cavalier","noirs",1, Cavalier_noir, False]
FN1 = [[0,2],"fou","noirs",1, Fou_noir, False]        #fou qui n'ira que sur les cases blanches
DN = [[0,3],"dame","noirs",1, Dame_noire, False]
RN = [[0,4],"roi","noirs",1, Roi_noir, False]
FN2 = [[0,5],"fou","noirs",2, Fou_noir, False]        #fou qui n'ira que sur les cases noires
CN2 = [[0,6],"cavalier","noirs",2, Cavalier_noir, False]
TN2 = [[0,7],"tour","noirs",2, Tour_noire, False]
PB1 =[[6,0],"pion","blancs",1, Pion_blanc, False]
PB2 =[[6,1],"pion","blancs",2, Pion_blanc, False]
PB3 =[[6,2],"pion","blancs",3, Pion_blanc, False]
PB4 =[[6,3],"pion","blancs",4, Pion_blanc, False]
PB5 =[[6,4],"pion","blancs",5, Pion_blanc, False]
PB6 =[[6,5],"pion","blancs",6, Pion_blanc, False]
PB7 =[[6,6],"pion","blancs",7, Pion_blanc, False]
PB8 =[[6,7],"pion","blancs",8, Pion_blanc, False]
TB2 = [[7,0],"tour","blancs",2, Tour_blanche, False]
CB2 = [[7,1],"cavalier","blancs",2, Cavalier_blanc, False]
FB2 = [[7,2],"fou","blancs",2, Fou_blanc, False]       #fou qui n'ira que sur les cases noires
DB = [[7,3],"dame","blancs",1, Dame_blanche, False]
RB = [[7,4],"roi","blancs",1, Roi_blanc, False]
FB1 = [[7,5],"fou","blancs",1, Fou_blanc, False]       #fou qui n'ira que sur les cases blanches
CB1 = [[7,6],"cavalier","blancs",1, Cavalier_blanc, False]
TB1 = [[7,7],"tour","blancs",1, Tour_blanche, False]

# Création de la matrice du plateau
plateau = numpy.array([[TN1,CN1,FN1,DN,RN,FN2,CN2,TN2],[PN1,PN2,PN3,PN4,PN5,PN6,PN7,PN8],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[PB1,PB2,PB3,PB4,PB5,PB6,PB7,PB8],[TB2,CB2,FB2,DB,RB,FB1,CB1,TB1]])

# Initialisation des cases vides
for i in range(2,6):
    for j in range(8):
        plateau[i,j] =  [[i,j],"case_vide","",0,case_vide, False]

# Initialisation du message d'avertissement à l'utilisateur
m = tkinter.StringVar()
message = tkinter.Label(plateau_visuel, textvariable = m)
message.grid(row = 0, column = 1, columnspan = 8)

# Création du visuel du plateau
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


# Création des boutons connexes au plateau
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

promotion_fou = tkinter.Button(plateau_visuel, text = 'Fou', state ='disabled', background='skyblue', command = lambda : promotion_fou_fct())
promotion_fou.grid(row=6,column=9)

promotion_cavalier = tkinter.Button(plateau_visuel, text = 'Cavalier', state ='disabled', background='skyblue', command = lambda : promotion_cavalier_fct())
promotion_cavalier.grid(row=7,column=9)

promotion_dame = tkinter.Button(plateau_visuel, text = 'Dame', state ='disabled', background='skyblue', command = lambda : promotion_dame_fct())
promotion_dame.grid(row=8,column=9)

difficulte_facile = tkinter.Button(plateau_visuel, text = 'Facile', state ='disabled', command = lambda : difficulte_facile_fct())
difficulte_facile.grid(row=1,column=10)

difficulte_difficile = tkinter.Button(plateau_visuel, text = 'Difficile', state ='disabled', command = lambda : difficulte_difficile_fct())
difficulte_difficile.grid(row=2,column=10)

# Affichage du plateau
plateau_visuel.mainloop()