from grille import *
from random import randint
import time

class IA () :
    
    def __init__ (self) :
        self.c1 = None #c1 = premier coup du bot
        self.oppod = None #oppod = le coup en diagonal de c1 ex : c1 = (0,0) oppod = (2,2)
        self.oppo_l = None #oppol_l = le coup à l'opposé sur la même ligne que c1 ex : c1 = (0,0) oppo_l = (0,2)

    def opposate (self) :
        """Définis les opposés du premier coup"""
        if self.c1 == (0,0) :
            self.oppod = (2,2)
            self.oppo_l = (0,2)
        elif self.c1 == (0,2) :
            self.oppod = (2,0)
            self.oppo_l = (0,0)
        elif self.c1 == (2,0) :
            self.oppod = (0,2) 
            self.oppo_l = (2,2)
        else :
            self.oppod = (0,0)
            self.oppo_l = (2,0)
        

    def play_random (self, matrice, symbol) :
        """Le bot joue un coup aléatoirement"""
        i = randint (0, 2)
        j = randint (0, 2)
        coord = (i,j)
        while matrice[coord][0] != None :
              i = randint (0, 2)
              j = randint (0, 2)
              coord = (i,j)
        time.sleep(0.2)
        matrice[coord][0] = symbol
        return coord, matrice

    def search_None (self, matrice) :
        """Remplis la liste l_None de toutes les case vides"""
        l_None = []
        for i in range (3) :
            for j in range (3) :
                if matrice[(i,j)][0] == None :
                    l_None.append ((i,j))
        return l_None

    def search_not_None (self, matrice) :
        """remplis la liste l_not_None de toutes les case non vides"""
        l_not_None = []
        for i in range (3) :
            for j in range (3) :
                if matrice[(i,j)][0] != None :
                    l_not_None.append ((i,j))
        return l_not_None

    def bot_check_win (self, coord, symbol, m) :
        """Fonction permettant d'explorer toute la matrice pour savoir si un joueur a gagné"""
        m.matrice[coord][0] = symbol
        for i in range (3) : #détecte si trois cases sur une ligne sont identiques
            if m.matrice[(i, 0)][0] == m.matrice[(i, 1)][0] == m.matrice[(i, 2)][0] and m.matrice[(i, 0)][0] != None : 
                return coord
        for i in range (3) : #regarde si trois case une colonne sont identiques
            if m.matrice[(0, i)][0] == m.matrice[(1, i)][0] == m.matrice[(2, i)][0] and m.matrice[(0, i)][0] != None : 
                return coord
        if m.matrice[(0, 0)][0] == m.matrice[(1, 1)][0] == m.matrice[(2, 2)][0] and m.matrice[(0, 0)][0] != None : #regarde si il y a trois même symbole dans la diagonale gauche
            return coord
        if m.matrice[(0, 2)][0] == m.matrice[(1, 1)][0] == m.matrice[(2, 0)][0] and m.matrice[(0, 2)][0] != None :#regarde si il y a trois m^me symbole dans la diagonale droite
            return coord
    
    def play_i (self, matrice, symbol) :
        """Premier test de jeu intelligent (incomplet)"""
        coord= None
        
        lst = [[], [], []]
        l_None = []
        count_sy = 0
        
        for i in range (3) :
            for j in range (3) :
                lst[i].append ((matrice[(i,j)][0]))
                
        for i in range (len(lst)) :
            for j in range (len(lst[i])) :
                if lst[i][j] == symbol :
                    count_sy += 1
                elif lst[i][j] == None :
                    l_None.append ((i,j))
            if count_sy == 2 :
                coord = l_None[0]
                matrice[coord][0] = symbol
                print ("choix intelligent")
                return coord, matrice
            count_sy = 0
            l_None.clear()
        
        return coord, matrice

    def play_i2_win (self,co_empty, m, symbol, index, res) :
        """recherche récursivement si le bot peut gagner en un coup"""
        if res != None :
            m.matrice[res][0] = symbol
            return res, m.matrice
        if index == len(co_empty) :
            return None, m.matrice
        res = self.bot_check_win(co_empty[index], symbol, m)
        m.matrice[co_empty[index]][0] = None

        return self.play_i2_win(co_empty, m, symbol, index + 1, res)
   
    def play_i2_defend (self,co_empty, m, symbol, index, res) :
        """recherche récursivement si le bot doit défendre pour ne pas perdre"""
        if res != None :
            m.matrice[res][0] = symbol
            return res, m.matrice
        if index == len(co_empty) :
            return None, m.matrice
        res = self.bot_check_win(co_empty[index], "circle", m)
        m.matrice[co_empty[index]][0] = None

        return self.play_i2_defend(co_empty, m, symbol, index + 1, res)

    def play_iop (self, co_empty,m, symbol, res) :
        """condition de coup logique pour ne pas perdre"""
        """Possibilité de faire un arbre.."""
        if res == None :
            if len(co_empty) == 9 : #Premier coup joué dans un coin
                choice = [(0,0), (0,2), (2,0), (2,2)]
                res = choice[randint(0, len(choice)-1)]
                self.c1 = res
                self.opposate()
            elif len(co_empty) == 8 : #si bot joue en deuxième
                not_None = self.search_not_None(m.matrice)[0]
                if not_None == (0,0) :
                    res = (2,2)
                elif not_None == (2,2) :
                    res = (0,0)
                elif not_None == (0,2) :
                    res = (2,0)
                elif not_None == (2,0) :
                    res = (0,2)
                else:
                    choice = [(0,0), (0,2), (2,0), (2,2)]
                    res = choice[randint(0, len(choice)-1)] 
                    while res in not_None :
                        res = choice[randint(0, len(choice)-1)] 
                self.c1 = res
                self.opposate() 
            elif (1,1) in co_empty : #prend le centre
                res = (1,1)
            elif self.oppod in co_empty : 
                res = self.oppod
            elif self.oppo_l in co_empty :
                res = self.oppo_l
                if (self.c1[0],self.c1[1]+1) not in co_empty and (self.c1[0],self.c1[1]-1) not in co_empty :
                    if (self.c1[0]+1,self.c1[1]) in co_empty  :
                        res = (self.c1[0]+1,self.c1[1])
                    elif  (self.c1[0]-1, self.c1[1]) in co_empty :
                        res = (self.c1[0]-1,self.c1[1])
            else :
                res = co_empty[0] #joue la dernière case vide
            m.matrice[res][0] = symbol #remplis la matrice
        return res, m.matrice
        
    