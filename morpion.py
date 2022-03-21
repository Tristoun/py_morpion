import pygame
from sympy import true
from grille import *
from ia import IA
import time

pygame.init()

wi = 900
he = 800

machine = False #False = Le bot ne commence pas / True = le bot commence
two_player = False #définis si le bot joue ou non False = un seul joueur contre le bot
#machine et two player ne peuvent pas tout les deux être = True
machine_start = machine
tp_start = two_player
bot = IA() #objet IA (bot)
        
m = Matrice() #objet matrice (grille)
m.fill_morpion()
m.fill_matrice_coord(wi, he)

case = m.size_square(wi, he) 

symbol = True #permet d'alterner en True et False pour savoir quel symbole afficher avec deux joueurs
count = 0

screen = pygame.display.set_mode((wi, he), pygame.RESIZABLE)
clock = pygame.time.Clock()

color = {"white" : (255, 255, 255), "black" : (0, 0, 0), "red" : (255,0,0), "blue" : (0,232,255), "green" : (0,150,0)} #définis un panel de couleur (dictionnaire)

run = True 
res = None
etat_click = True

def define_font () :
    """Definis la taille de la police pour les croix"""
    if wi >= he :
        font_size = int(280*case[1]/266) #produit en croix
    else :
        font_size = int(280*case[0]/266) #produit en croix
    font = pygame.font.SysFont("Arial", font_size)
    return font_size, font

font_size, font = define_font()

    
def create_screen_morpion () :
    """Dessine la matrice sur l'interface"""
    screen.fill(color["black"])
    x = 1
    for i in range (2) :
        pygame.draw.line(screen, color["white"], (x*wi/3, 0), (x*wi/3, he), 5)
        pygame.draw.line(screen, color["white"], (0, x*he/3), (wi, x*he/3), 5)
        x = x + 1

create_screen_morpion()


def draw_circle (coord) :
    """Dessine un cercle sur l'interface"""
    if wi >= he : 
        pygame.draw.circle(screen, color["green"], m.matrice[coord][1], 100*case[1]/266, 5) #produit en croix
    else  :
        pygame.draw.circle(screen, color["green"], m.matrice[coord][1], 100*case[0]/266, 5) #produit en croix


def draw_cross (coord) :  
    """Dessine une croix sur l'interface"""
    txt = font.render ("X", True, color["blue"])
    if wi >= he :  
        screen.blit (txt, (m.matrice[coord][1][0] - (1/4*font_size), m.matrice[coord][1][1] - 20 - (1/2*font_size)))
    else :
        screen.blit (txt, (m.matrice[coord][1][0] - (1/4*font_size), m.matrice[coord][1][1] - 20 - (1/2*font_size)))



def detect_case (pos) :
    """Detecte où est posé le symbole"""
    if pos[1] < he /3 :
        coord = (0, detect_case_wi(pos))
    elif pos[1] >= he/3 and pos[1] <= 2*he/3 :
        coord = (1, detect_case_wi(pos))
    elif pos[1] > 2 * he/3 :
        coord = (2, detect_case_wi(pos))

    return coord

def detect_case_wi (pos) :
    """Detecte ou est placé le symbole sur l'axe des abscisses"""
    if pos[0] < wi/3 :
        return 0
    elif pos[0] >= wi/3 and pos[0] <= 2*wi/3 :
        return 1
    elif pos[0] > 2*wi/3 :
        return 2
    
def print_symbol_player (symbol, machine, count, m) :
    """Affiche le symbole du joueur (croix, cercle)"""
    if symbol == True :
        draw_circle(coord)
        if two_player == True :
            symbol = False
        m.matrice[coord][0] = "circle"
    elif symbol == False : 
        draw_cross (coord)
        symbol = True
        m.matrice[coord][0] = "cross"
    if two_player == False :
        machine = True
    count += 1
    return symbol, machine, count

def print_symbol_bot (machine, count, m) :
    """Affiche le symbole du bot (croix)"""
    time.sleep(0.8) #le bot réflechit...
    co_empty = bot.search_None(m.matrice)
    coord, m.matrice = bot.play_i2_win(co_empty, m, "cross", 0, None)
    
    if coord == None :
        coord, m.matrice = bot.play_i2_defend(co_empty, m, "cross",0, None)

    if coord == None :
        coord, m.matrice = bot.play_iop(co_empty, m, "cross", None)

    if coord == None :
        coord, m.matrice = bot.play_random(m.matrice, "cross")
    draw_cross(coord)
    machine = False
    count += 1
    return machine, count

def check_win () :
    """Fonction permettant d'explorer toute la matrice pour savoir si un joueur a gagné"""
    for i in range (3) : #détecte si trois cases sur une ligne sont identiques
        if m.matrice[(i, 0)][0] == m.matrice[(i, 1)][0] == m.matrice[(i, 2)][0] and m.matrice[(i, 0)][0] != None : 
            return m.matrice[(i, 0)][0]
    for i in range (3) : #regarde si trois case une colonne sont identiques
        if m.matrice[(0, i)][0] == m.matrice[(1, i)][0] == m.matrice[(2, i)][0] and m.matrice[(0, i)][0] != None : 
            return m.matrice[(0, i)][0]
    if m.matrice[(0, 0)][0] == m.matrice[(1, 1)][0] == m.matrice[(2, 2)][0] and m.matrice[(0, 0)][0] != None : #regarde si il y a trois même symbole dans la diagonale gauche
        return m.matrice[(0, 0)][0]
    if m.matrice[(0, 2)][0] == m.matrice[(1, 1)][0] == m.matrice[(2, 0)][0] and m.matrice[(0, 2)][0] != None :#regarde si il y a trois m^me symbole dans la diagonale droite
        return m.matrice[(0, 2)][0]   


def screen_end (wl) :
    """Affiche qui a gagné"""
    screen.fill(color["black"])
    font_txt = pygame.font.SysFont("Arial", 80)
    if wl == "Match nul" :
        txt = font_txt.render(wl, True, color["white"])  
    else :
        txt = font_txt.render(wl + " " + "win !!", True, color["white"])   
    screen.blit(txt, (wi//3.5,he//2))

while run : #boucle pygame
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False
            
        if event.type == pygame.KEYDOWN : #appuie sur la touche entrée rénitialise la partie
            create_screen_morpion()
            count = 0
            m = Matrice()
            m.fill_morpion()
            m.fill_matrice_coord(wi, he)
            bot = IA()
            
            case = m.size_square(wi, he)
            
            symbol = True
            etat_click = True
            machine = machine_start
            two_player = tp_start
            
        if machine == False and etat_click == True:
            if event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed() == (1, 0, 0) :
                        position = pygame.mouse.get_pos()
                        coord = detect_case(position)
                        if m.matrice[coord][0] == None :
                            symbol, machine, count = print_symbol_player(symbol, machine, count, m)  
                                       
        elif machine == True :
            machine, count = print_symbol_bot(machine, count, m)
    
    res = check_win()
    if res != None :
        wl = res
        etat_click = screen_end(wl)
    elif count == 9 :
        wl = "Match nul"
        etat_click = screen_end(wl)
    
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()