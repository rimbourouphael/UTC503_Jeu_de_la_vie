from tkinter import *
from grille import Grille

frame = Tk()
frameWidth = 700
frameHeight =600
frame.geometry(f"{frameWidth}x{frameHeight}")

#---------------------------------------------------------------------------------------------------

def center_window(w:int,h:int):
    "Cette fonction permer de positionner le cadre au centre de l'écran"
    # obtenir la largeur et la longueur de l'ecran
    ws = frame.winfo_screenwidth()
    hs = frame.winfo_screenheight()
    # calculer x et y pour qu'on puisse mettre au centre le tkinter window
    x = int((ws/2) - (w/2))  
    y = int((hs/2) - (h/2))
    frame.geometry(f"{w}x{h}+{x}+{y}")
    
#---------------------------------------------------------------------------------------------------

def start():
    grille.generations()
    start.pack_forget()
    stop.pack(side =LEFT, padx =3, pady =3)
    go.pack_forget()
    restart.pack_forget()

#---------------------------------------------------------------------------------------------------

def stop():
    grille.stop()
    start.pack_forget()
    stop.pack_forget()
    go.pack(side =LEFT, padx =3, pady =3)
    restart.pack(side =LEFT, padx =3, pady =3)
    go.configure(state= "normal")
    restart.configure(state= "normal")

#---------------------------------------------------------------------------------------------------

def go():
    grille.go()
    grille.generations()
    start.pack_forget()
    stop.pack(side =LEFT, padx =3, pady =3)
    go.pack_forget()
    restart.pack_forget()

#---------------------------------------------------------------------------------------------------

def restart():
    grille.restart()
    start.pack(side =LEFT, padx =3, pady =3)
    stop.pack_forget()
    go.pack_forget()
    restart.pack_forget()

#---------------------------------------------------------------------------------------------------

#Création de la grille
grille = Grille(frame)
grille2 = grille.getGrille()

#---------------------------------------------------------------------------------------------------

#Création des bouttons
start = Button(frame, text ='Start' ,width=10,command = start)
stop = Button(frame, text ='Stop' ,width=10 , command = stop)
go = Button(frame, text ='Go' ,width=10 , command = go)
restart = Button(frame, text ='Restart' ,width=10 , command = restart)

#---------------------------------------------------------------------------------------------------

#Création du cadre contenant les coordonnée des lignes et colonnes lors du survol de la souris
L_infos      = LabelFrame(frame)

L_Coord = LabelFrame(L_infos,text = " Coordonnées ")
C_Coord = Label(L_Coord, textvariable = grille.Var_coord)

#Création de l'espace de changement de la vittesse
L_vitesse = LabelFrame(L_infos,text = " Vitesse ")
entree = Entry(L_vitesse)
entree.bind("<Return>", lambda event: grille.change_vit(event,entree))
chaine = Label(L_vitesse)
chaine.configure(text = "Attente entre les étapes (ms) : ")

#---------------------------------------------------------------------------------------------------
#Ajout du LabelFrame
L_infos.pack()
L_Coord.pack(side=LEFT,padx = 4, pady = 4,expand = YES, fill = X)
C_Coord.pack(side=LEFT,padx = 4, expand = YES, fill = X)

#Ajout de l'entrée de vitesse
L_vitesse.pack(side=LEFT,padx = 4, pady = 4,expand = YES, fill = X)
entree.pack(side=RIGHT,padx = 4, expand = YES, fill = X)
chaine.pack(side=RIGHT,padx = 4, expand = YES, fill = X)
#Ajout des elements au frame
grille2.place(relx=0.5, rely=0.5, anchor=CENTER)
grille2.pack()

#Ajout du boutton Start
start.pack(side =LEFT, padx =3, pady =3)

#---------------------------------------------------------------------------------------------------
#Centrer notre window
center_window(frameWidth , frameHeight)
#changement du titre du window
frame.title("Jeu De La Vie")
#changement du background
frame['bg']= "#f2f2f2" 

#---------------------------------------------------------------------------------------------------

frame.mainloop()