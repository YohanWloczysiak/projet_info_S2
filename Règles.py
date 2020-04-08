# -*- coding: utf-8 -*-
"""
REGLES DU JEU D'ECHECS - FONCTIONS DE DEPLACEMENTS DES PIECES

"""
    
def deplacement_pion(p, a, b):
    assert 0 <= a < 7
    assert 0 <= b <= 7
    (X, Y) = p[0]
    color = p[2]
    if a in {X+1, X-1} and plateau[a, b] != 0 :     # élimination d'une pièce
        if plateau[a, b][2] != color:
            return (a, b),  plateau[a, b]
        else:
            raise ValueError("Une autre pièce se trouve déjà sur cette case")  
    elif a == X and plateau[a,b] == 0:              # déplacement simple
        if color == "noir" :                        # le pion est noir
            if b == Y+2 and Y!= 1 :
                raise ValueError("Le déplacement est impossible") 
            elif b == Y+1 or b == Y+2 :     
                return (X,b)
            else:
                raise ValueError("Le déplacement est impossible") 
        else:                                       # le pion est blanc
            if b == Y-2 and Y!= 6:
                pass
            elif b == Y-1 or b == Y-2 :
                return (X,b)  
    else:                                           # case occupée par une pièce de même couleur
             raise ValueError("Le déplacement est impossible") 
  
        
def deplacement_tour(p, a, b):   ## inclure traverse_tour
    assert 0 <= a < 7
    assert 0 <= b <= 7
    (X, Y) = p[0]
    color = p[2]
    if a != X and b != Y:
        raise ValueError("Le déplacement est impossible") 
    elif plateau[a, b] == 0 :                        # déplacement simple                          
        if traverse_tour(a, b, X, Y) == True :
            return (a, b)
        else:
            raise ValueError("Vous traversez une pièce")
    else:                                       
            if plateau[a,b][2] != color :             # élimination d'une pièce
                if traverse_tour(a, b, X, Y) == True :
                    return (a, b),  plateau[a, b]
                else:
                    raise ValueError("Vous traversez une pièce")
            else:                                     # case occupée par une pièce de même couleur
                raise ValueError("Le déplacement est impossible")
                
def deplacement_roi(p, a, b) :
    assert 0 <= a < 7
    assert 0 <= b <= 7
    (X, Y) = p[0]
    color = p[2]
    if a in {X+1, X, X-1} and b in {Y+1, Y, Y-1} :
        if plateau[a,b] == 0:                       # déplacement simple
            return (a, b)
        else:
            if plateau[a,b][2] != color :           # élimination d'une pièce
                return (a, b),  plateau[a, b]
            else:                                   # case occupée par une pièce de même couleur
                raise ValueError("Une autre pièce se trouve déjà sur cette case")
    else:
        raise ValueError("Le déplacement est impossible")
        
def deplacement_fou(p, a , b) :        ## écrire traverse_fou 
    assert 0 <= a < 7
    assert 0 <= b <= 7
    (X, Y) = p[0]
    color = p[2]
    if traverse_fou(a, b, X, Y) == False :
        raise ValueError("Vous traversez une pièce")
    else:
        for k in range(0, 8) :
            if (X - a) in {k, -k} and (Y - b) in {k, -k}: 
                if plateau[a,b] == 0 :                        # déplacement simple
                    return (a, b)                          
                elif plateau[a,b][2] != color :               # élimination d'une pièce
                        return (a, b),  plateau[a, b]
                    else :                                       # case occupée par une pièce de même couleur
                        raise ValueError("Une autre pièce se trouve déjà sur cette case")   
            else :
                raise ValueError("Le déplacement est impossible")
        
def deplacement_dame(p, a, b) :
    (X, Y) = p[0]
    if a == X or b == Y :                               # déplacement selon une ligne/colonne
        deplacement_tour(p, a, b)                       
    else:                                               # déplacement sur une diagonale
        deplacement_fou(p, a, b)
    
def deplacement_cavalier(p, a, b) :
    assert 0 <= a < 7
    assert 0 <= b <= 7
    (X, Y) = p[0]
    color = p[2]
    for k in range(0, 8):   
        if (X - a in {-1, 1} and Y - b in {-2, 2}) or (X - a in {-2, 2} and Y - b in {-1, 1}) 
            if plateau[a,b] == 0 :
                return (a, b)                           # déplacement simple
            else:
                if plateau[a,b][2] != color :            # élimination d'une pièce
                    return (a, b),  plateau[a, b]
                else:                                       # case occupée par une pièce de même couleur
                    raise ValueError("Une autre pièce se trouve déjà sur cette case")   
        else:
            raise ValueError("Le déplacement est impossible")
    
        
def traverse_tour(a, b, X, Y) :                         # renvoit si on peut se déplacer sans traverser de pièce
    if a != X :                                  # déplacement horizontal
            if a < X :
                for coord in range(a+1, X) :
                    if plateau[coord, b] != 0 :
                        return False
            else:
                for coord in range(X+1, a) :
                    if plateau[coord, b] != 0 :
                        return False
    elif b != Y:                                 # déplacement vertical
            if b < Y :
                for coord in range(b+1, Y) :
                    if plateau[a, coord] != 0 :
                        return False
            else:
                for coord in range(Y+1, b) :
                    if plateau[a, coord] != 0 :
                        return False
    return True

def traverse_fou(a, b, X, Y) :
    if (X - a) > 0 and (Y - b) > 0 :            # X - a = Y - b = k
        for i in range(X + 1, a) :
            for j in range (Y + 1, b) :
                if plateau[i, j] != 0 :
                    return False
    elif (X - a) > 0 and (Y - b ) < 0 :         # X - a = k et Y - b = -k
        for i in range(X + 1, a) :
            for j in range (b + 1, Y, -1) :
                if plateau[i, j] != 0 :
                    return False
    elif (X - a) < 0 and (Y - b ) < 0 :         # X - a = Y - b = -k
        for i in range(a + 1, X, -1) :
            for j in range (b + 1, Y, -1) :
                if plateau[i, j] != 0 :
                    return False
    elif (X - a) < 0 and (Y - b) > 0 :          # X - a = -k et Y - b = k
        for i in range(a + 1, X, -1) :
            for j in range (Y + 1, b) :
                if plateau[i, j] != 0 :
                    return False
    return True
    