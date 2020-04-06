# -*- coding: utf-8 -*-
"""
REGLES DU JEU D'ECHECS - FONCTIONS DE DEPLACEMENTS DES PIECES

"""
    
def déplacement_pion(p, a, b):
    (X, Y) = p[0]
    color = p[2]
    if a in {X+1, X-1} and plateau[a, b] != 0 :     # élimination d'une pièce
        if plateau[a, b][2] != color:
            return (a, b),  plateau[a, b]
        else:
            raise ValueError("Le déplacement est impossible")  
    elif a == X and plateau[a,b] == 0:                # déplacement simple
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
  
        
def deplacement_tour(p, a, b):
    (X, Y) = p[0]
    color = p[2]
    if a != X and b != Y:
        raise ValueError("Le déplacement est impossible") 
    else :                                           
        if plateau[a,b] == 0:                       # déplacement simple
            return (a, b)
        else:                                       
            if plateau[a,b][2] != color:                # élimination d'une pièce
                return (a, b),  plateau[a, b]
            else:                                   # case occupée par une pièce de même couleur
                raise ValueError("Le déplacement est impossible")
                
def deplacement_roi(p, a, b):
    (X, Y) = p[0]
    color = p[2]
    if a in {X+1, X, X-1} and b in {Y+1, Y, Y-1}:
        if plateau[a,b] == 0:                       # déplacement simple
            return (a, b)
        else:
            if plateau[a,b][2] != color:            # élimination d'une pièce
                return (a, b),  plateau[a, b]
            else:                                   # case occupée par une pièce de même couleur
                raise ValueError("Le déplacement est impossible")
    else:
        raise ValueError("Le déplacement est impossible")
        
def deplacement_fou(p, a , b):
    (X, Y) = p[0]
    color = p[2]
    for k in range(0, 8):   
        if X - a in {k, -k} and Y - b in {k, -k}: 
            if plateau[a,b] == 0:
                return (a, b)                           # déplacement simple
            else:
                if plateau[a,b][2] != color:            # élimination d'une pièce
                    return (a, b),  plateau[a, b]
                else:                                       # case occupée par une pièce de même couleur
                    raise ValueError("Le déplacement est impossible")   
        else:
            raise ValueError("Le déplacement est impossible")
        
def deplacement_reine(p, a, b):
    (X, Y) = p[0]
    if a == X or b == Y :                               # déplacement selon une ligne/colonne
        deplacement_tour(p, a, b)                       
    else:                                               # déplacement sur une diagonale
        deplacement_fou(p, a, b)
    
def deplacement_cavalier(p, a, b):
    for k in range(0, 8):   
        if (X - a in {-1, 1} and Y - b in {-2, 2}) or (X - a in {-2, 2} and Y - b in {-1, 1}) 
            if plateau[a,b] == 0:
                return (a, b)                           # déplacement simple
            else:
                if plateau[a,b][2] != color:            # élimination d'une pièce
                    return (a, b),  plateau[a, b]
            else:                                       # case occupée par une pièce de même couleur
                raise ValueError("Le déplacement est impossible")   
        else:
            raise ValueError("Le déplacement est impossible")
    
        

        
  