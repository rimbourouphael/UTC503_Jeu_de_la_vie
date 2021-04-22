from tkinter import *
from random import randint

class Grille:
    def __init__(self , fenetre):
        self.Var_coord = IntVar()
        #initialisation des données à utiliser
        self.initialisation()

        #initialisation de la grille
        self.grille = Canvas(fenetre, bg = "#f0ffff", height = self.canvasHeight, 
            width = self.canvasWidth,highlightthickness=1, highlightbackground="black")

        self.activationEvenements()
        self.getGrille()

    #---------------------------------------------------------------------------------------------------

    def activationEvenements(self):
        self.grille.bind("<Motion>", self.souris_survol)
        self.grille.bind("<Button-1>", self.creerCellule)
        self.grille.bind("<Button-3>", self.supprimercellule)

    #---------------------------------------------------------------------------------------------------

    def initialisation(self):
        '''
            Initialisation des variables à utiliser 
        '''
        
        self.vitesse = 50
        self.drap=1 # pour pemettre de commencer et d'arreter le jeu

        self.tailleCellule = 10 #taille de la cellule
        self.canvasWidth = 450 # largeur de la grille
        self.canvasHeight = 400 #longueur de la grille
        self.nb_cellules = int(self.canvasWidth / self.tailleCellule)  #nombre total de cellule

        #dictionnaires des cellules
        self.cellule_en_vie ={} #dictionnaire des cellule en vie
        self.cellule_en_vie_t1 = {}      #dictionnaire des cellules en vie au temps t+1
        self.examen = {}            #dictionnaire des cellules deje examinees
        self.cell_voisines = {}     #dictionnaire des cellules voisines de chaque cellule en vie

    #---------------------------------------------------------------------------------------------------

    def getGrille(self) :
        "Cette fonction retourne le canvas déjà créé"
        self.creerGrille()
        return self.grille

    def creerGrille(self):
        '''
            Création de la grille et de ces colonnes
        '''
        #creer ligne verticale
        celluleX = 0
        for _ in range(self.canvasWidth):
            self.grille.create_line(celluleX, 0, celluleX, self.canvasHeight, width=1,fill = "black")
            celluleX += self.tailleCellule

        #creer ligne horizontale
        celluleY = 0
        for _ in range(self.canvasHeight):
            self.grille.create_line(0,celluleY,self.canvasWidth,celluleY,width=1,fill='black')
            celluleY+=self.tailleCellule
  
    #---------------------------------------------------------------------------------------------------

    def coords_lig_col(self,event):
        '''
        Calcul des coordonnees x,y et des numeros de ligne et colonne
        '''
        x = event.x - (event.x % self.tailleCellule)
        y = event.y - (event.y % self.tailleCellule)
        lig = int(y / self.tailleCellule)
        col = int(x / self.tailleCellule)
        return x, y, lig, col
    
    #---------------------------------------------------------------------------------------------------

    def creerCellule(self,event):
        '''
        Creation d'une cellule vivante et la mettre dans le dictionnaire cellule_en_vie
        '''
        x, y, lig, col = self.coords_lig_col(event)

        if lig <= self.nb_cellules and col <= self.nb_cellules:
            if not (lig, col) in self.cellule_en_vie:
                self.cellule_en_vie.setdefault((lig, col))
                self.grille.create_rectangle(x, y, x + self.tailleCellule, y + self.tailleCellule,
                    fill = "#ff9999", tags = ((lig, col), "vie"))

    #---------------------------------------------------------------------------------------------------
    
    def supprimercellule(self, event):
        '''
        Supprimer la cellule de la grille et du dictionnaire cellule_en_vie
        '''
        #Suppression de la cellule sur la grille
        x, y, lig, col = self.coords_lig_col(event)
        self.grille.delete((lig, col))

        #Suppression de la cellule du dictionnaire des cellules en vie
        if (lig, col) in self.cellule_en_vie:
            del self.cellule_en_vie[(lig, col)]
    
    #---------------------------------------------------------------------------------------------------

    def scan_cell_voisines(self, lig, col, test):
        '''
        Recherche des cellules voisines et compter le nombre des cellules en vie.
        Les cles des cellules voisines sont stockees dans <self.cell_voisines>
        Les Parametre <test>:
            - True si on recherche les voisines des cellules en vie
            - False si on recherche les voisines des voisines des cellules en vie
        '''
        cpt_cell_en_vie = 0   #Compteur cellules voisines et en vie

        for voisine in ((lig - 1, col - 1), #Nord Ouest
                        (lig - 1, col),     #Nord
                        (lig - 1, col + 1), #Nord Est
                        (lig,     col - 1), #Ouest
                        (lig,     col + 1), #Est
                        (lig + 1, col - 1), #Sud Ouest
                        (lig + 1, col),     #Sud
                        (lig + 1, col + 1)):#Sud Est

            if test:
                self.cell_voisines.setdefault(voisine)

            #Si la cellule voisine est en vie
            if voisine in self.cellule_en_vie:
                cpt_cell_en_vie += 1

        return cpt_cell_en_vie
    
    #---------------------------------------------------------------------------------------------------
    def decision_vie_mort(self, cpt_cell_en_vie, lig, col):
        '''
        Application des regles de vie ou de mort:
        - 0 ou 1 cellule voisine  en vie = mort par isolement
        - 4 a 8 cellules voisines en vie = mort par surpopulation
          Dans ces cas la cellule n'est pas ecrite dans <cellule_en_vie_t1>
         '''
        #2 cellules voisines en vie = survie (pas de changement)
        if cpt_cell_en_vie == 2:
            #Si la cellule etait en vie au temps T
            if (lig, col) in self.cellule_en_vie:
                self.cellule_en_vie_t1.setdefault((lig, col))

        #3 cellules voisines en vie = survie ou naissance
        elif cpt_cell_en_vie == 3:
            self.cellule_en_vie_t1.setdefault((lig, col))
    
    #---------------------------------------------------------------------------------------------------

    def change_vit(self,event,entree): 
        '''
        fonction pour changer la vitesse(l'attente en ms entre chaque étape d'évolution)
        '''
        self.vitesse = int(eval(entree.get()))
    
    #---------------------------------------------------------------------------------------------------

    def souris_survol(self, event):
        '''
        Afficher les coordonnées ligne/colonne de la souris lors de son survol au-dessus de la grille 
        '''
        x, y, lig, col = self.coords_lig_col(event)

        if lig < self.nb_cellules and col < self.nb_cellules:
            self.Var_coord.set("Lig:%d  Col:%d" %(lig, col))

    #---------------------------------------------------------------------------------------------------
    
    def start(self):
        self.drap = 1
        if (not self.cellule_en_vie):
            for i in range(1,320): 
                x = randint(i,self.canvasWidth)
                for j in range(1,320):
                    y= randint(j,self.canvasWidth)
                    lig = int(y / self.tailleCellule)
                    col = int(x / self.tailleCellule)
                    if lig <= self.nb_cellules and col <= self.nb_cellules:
                        if not (lig, col) in self.cellule_en_vie:
                            self.cellule_en_vie.setdefault((lig, col))
                            self.grille.create_rectangle(x, y, x + self.tailleCellule, y + self.tailleCellule,
                                fill = "#ff9999", tags = ((lig, col), "vie"))
        self.go()
    
    #---------------------------------------------------------------------------------------------------

    def go(self):
        if self.cellule_en_vie!=0:
            if self.drap ==0:
                self.drap =1
                self.generations()

    #---------------------------------------------------------------------------------------------------
    
    def generations(self):
        '''
        Examiner si la cellule doit mourir ou non 
        ''' 
        if(self.drap==1):
            self.start()

            #Examen de chaque cellule en vie
            for lig, col in self.cellule_en_vie.keys():
                self.examen.setdefault((lig, col))

                #Comptage des cellules voisines de la cellule en vie
                cpt_cell_en_vie = self.scan_cell_voisines(lig, col, True)
                self.decision_vie_mort(cpt_cell_en_vie, lig, col)

            #Examen des cellules voisines de chaque cellule en vie
            for lig, col in self.cell_voisines.keys():
                if not (lig, col) in self.examen:
                    self.examen.setdefault((lig, col))
                    cpt_cell_en_vie = self.scan_cell_voisines(lig, col, False)
                    self.decision_vie_mort(cpt_cell_en_vie, lig, col)

            

            self.grille.delete("vie")  #Suppression des cellules en vie au temps "t"

            #Creation des cellules en vie au temps "t+1"
            for lig, col in self.cellule_en_vie_t1:
                x = (col * self.tailleCellule)
                y = (lig * self.tailleCellule)
                self.grille.create_rectangle(x, y, x + self.tailleCellule, y + self.tailleCellule,
                    fill = "#ff9999", tags = ((lig, col), "vie"))

            #La generation "t+1" devient la generation "t"
            self.cellule_en_vie = dict(self.cellule_en_vie_t1)
            self.cellule_en_vie_t1 = {}
            self.examen = {}
            self.cell_voisines = {}
            if self.drap != 0: 
                self.grille.after(self.vitesse,self.generations)

    #---------------------------------------------------------------------------------------------------

    def stop(self):
        "arrêt de l'animation"  
        self.drap =0

    #---------------------------------------------------------------------------------------------------
    
    def restart(self):
        self.grille.delete("all")
        self.initialisation()
        return self.getGrille()