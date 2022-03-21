class Matrice () : #créer la classe matrice
    def __init__ (self) :
        """Définis le dictionnaire de la matrice"""
        self.matrice = {} #le dictionnaire contient les coordonées sur la grille : (si elle contient un symbople , les coordonées d'affichage)

    def __str__ (self) :
        """Retourne le dictionnaire de la matrice"""
        return str(self.matrice)
    
    def reset (self) :
        """Renitialise la matrice"""
        self.matrice.clear()

    def empty (self) :
        """Retourne True si la matrice est vide"""
        if self.matrice == [] :
            return True 
        return False

    def fill_morpion (self) :
        """remplis la matrice de coordonnées pour jouer au morpion"""
        if self.empty() == True :
            return "List already filled"
        for i in range (3) :
            for j in range (3) :
                self.matrice[(i, j)] = [None]
        return self.matrice

    def size_square (self, wi, he) :
        """Definis la taille d'une case du morpion"""
        square_wi = wi/3
        square_he = he/3
        return square_wi, square_he
    
    def case_matrice (self, pos) :
        """Retourne les coordonées pour afficher le symbole dans la case"""
        return self.matrice[pos][0]
    
    def fill_matrice_coord (self, wi, he) :
        """Remplis le dictionnaire de la matrice des coordonnées pour les symboles"""
        self.matrice[(0,0)].append ((wi/3/2, he/3/2))
        self.matrice[(0,1)].append ((wi/2, he/3/2))
        self.matrice[(0,2)].append ((wi-(wi/3/2), he/3/2))
        self.matrice[(1,0)].append ((wi/3/2, he/2))
        self.matrice[(1,1)].append ((wi/2, he/2))
        self.matrice[(1,2)].append ((wi-(wi/3/2), he/2))
        self.matrice[(2,0)].append ((wi/3/2, he - (he/3/2)))
        self.matrice[(2,1)].append ((wi/2, he - (he/3/2)))
        self.matrice[(2,2)].append ((wi-(wi/3/2), he-(he/3/2)))

