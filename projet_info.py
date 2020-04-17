
#définition des régles et mouvements des pièces

#importation des modules nécessaires
import numpy
import tkinter

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
    if piece[3] != 0:
            liste_deplacements = liste_deplacements_piece(piece, plateau)
            for i in range(8):
                for j in range(8):
                    if [i,j] in liste_deplacements:
                        case_i_j = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'green', command=event(piece))
                        case_i_j.grid(column=i+1,row=j+1)


for i in range(8):
    for j in range(8):
        if (i+j)%2 == 1:
            piece = plateau[i,j]
            img = piece[4]
            case_i_j = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'maroon', command=event(piece))
            case_i_j.grid(column=i+1,row=j+1)

for i in range(8):
    for j in range(8):
        if (i+j)%2 == 0:
            piece = plateau[i,j]
            img = piece[4]
            case_i_j = tkinter.Button(plateau_visuel, image=img, height = 90, width = 90, background= 'wheat', command=event(piece))
            case_i_j.grid(column=i+1,row=j+1)

plateau_visuel.mainloop()




