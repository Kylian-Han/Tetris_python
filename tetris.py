#!/usr/bin/python3
# -*- coding: utf-8 -*-



"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "votre nom"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "Kylian HANIQUET"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "haniquet"
__email__ = "haniquet.pro@gmail.com"

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import constantes as cons
import sys

# Classe Tetris
class Jeu:
    """
    [Il manque la documentation de la classe]
    """
    def __init__(self ):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(cons.TAILLE_FENETRE)
        self.fonts = {
            'defaut': pygame.font.Font('freesansbold.ttf', cons.FONT_SIZE),
            'titre': pygame.font.Font('freesansbold.ttf', cons.TITLE_FONT_SIZE),
        }
        pygame.display.set_caption('Application Tetris')

    def start(self) -> None:
        """Ecran de demarrage, affiche le titre 'Teris' et attends une touche
        """
        self._afficher_texte('Tetris', cons.CENTRE_FENETRE, font = 'titre')
        self._afficher_texte('Appuyer sur une touche...', cons.POS)
        self._attente()

    def stop(self) -> None:
        """Ecran de defaite, attends, puis ferme l'app
        """
        self._afficher_texte('Perdu', cons.CENTRE_FENETRE, font='titre')
        self._attente()
        self._quitter()

    def _afficher_texte(self, text : str, position : tuple[int, int], couleur : int = 9, font : str = 'defaut') -> None:
        """
          Affiche un texte sur la surface à une position donnée avec une couleur et une police spécifiées.

            text (str): Texte à afficher.
            position (tuple[int, int]): Position (x, y) du centre du texte sur la surface.
            couleur (int, optional): Identifiant de la couleur à utiliser. Par défaut 9.
            font (str, optional): Nom de la police à utiliser. Par défaut 'defaut'.

        Returns:
            None
        """
        # print("Afficher Texte")
        font = self.fonts.get(font, self.fonts['defaut'])
        couleur = cons.COULEURS.get(couleur, cons.COULEURS[9])
        rendu = font.render(text, True, couleur)
        rect = rendu.get_rect()
        rect.center = position
        self.surface.blit(rendu, rect)
    def _get_event(self):
        """Récupère et traite les événements pygame.

        Parcourt la file d'événements pygame et gère les événements de fermeture de fenêtre
        et d'appui sur la touche Échap. Retourne la touche pressée lors d'un événement KEYDOWN,
        sauf si c'est la touche Échap.

        Retourne :
            int ou None : Code de la touche pressée lors d'un événement KEYDOWN, ou None si aucun événement pertinent.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self._quitter()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._quitter()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                return event.key
                
    def _quitter(self) -> None:
        """
        Termine proprement le jeu en fermant la fenêtre Pygame et en quittant le programme.
        """
        print("Quitter")
        pygame.quit()
        sys.exit()
  
    def _rendre(self) -> None:
        """
        Met à jour l'affichage du jeu et régule la vitesse d'exécution.
        Cette méthode utilise pygame.display.update() pour rafraîchir l'écran,
        puis appelle self.clock.tick() afin de contrôler le nombre d'images par seconde.
        """
        pygame.display.update()
        self.clock.tick()
    def _attente(self) -> None:
        """
        Attend qu'un événement utilisateur soit détecté.
        Cette méthode affiche le message "Attente" dans la console, puis entre dans une boucle
        où elle attend qu'un événement soit reçu via la méthode `_get_event()`. Tant qu'aucun
        événement n'est détecté (c'est-à-dire que `_get_event()` retourne None), la méthode
        continue de rendre l'affichage en appelant `_rendre()`.
        Utilisé pour mettre le jeu en pause jusqu'à une interaction de l'utilisateur.
        """
        print("Attente")
        while self._get_event() == None:
            self._rendre()
    def _get_piece(self) -> dict:
        """
        Sélectionne et retourne une pièce de Tetris aléatoire.
        Cette méthode choisit une clé au hasard parmi les clés disponibles dans cons.PIECES_KEYS,
        puis retourne la pièce correspondante depuis le dictionnaire cons.PIECES.
        Retour:
            dict: La pièce de Tetris sélectionnée aléatoirement.
        """
        
        return cons.PIECES.get(random.choice(cons.PIECES_KEYS))
    def _get_current_piece_color(self) -> int:
        """
        Retourne la couleur de la pièce courante.
        Parcourt la matrice représentant la pièce courante et retourne la première valeur non nulle,
        qui correspond à la couleur de la pièce. Si aucune couleur n'est trouvée, retourne 0.
        Retour:
            int: La couleur de la pièce courante, ou 0 si aucune couleur n'est présente.
        """
     
        for l in self.current[0]:
            for c in l:
                if c != 0:
                    return c
        return 0
    def _calculer_donnes_piece_courante(self) -> None:
        """
        Calcule et met à jour les coordonnées de la pièce courante sur la grille.
        Cette méthode parcourt la matrice représentant la forme actuelle de la pièce
        (en fonction de sa rotation) et détermine les positions absolues de chaque
        bloc de la pièce sur la grille de jeu, en tenant compte de la position
        actuelle de la pièce. Les coordonnées calculées sont stockées dans
        l'attribut `self.coordonnees`.
        Aucun paramètre n'est requis.
        Ne retourne rien.
        """
        
        m = self.current[self.position[2]]
        coords = []
        for i, l in enumerate(m):
            for j, k in enumerate(l):
                if k != 0:
                    coords.append([i+self.position[0], j+self.position[1]])
        self.coordonnees = coords
    def _est_valide(self, x : int=0, y:int=0, r:int=0) -> bool:
        """
        Vérifie si la position actuelle ou une position donnée (avec décalage x, y et rotation r) de la pièce est valide sur le plateau de jeu.
        Args:
            x (int, optionnel): Décalage horizontal à appliquer à la position de la pièce. Par défaut à 0.
            y (int, optionnel): Décalage vertical à appliquer à la position de la pièce. Par défaut à 0.
            r (int, optionnel): Nombre de rotations à appliquer à la pièce. Par défaut à 0 (aucune rotation).
        Returns:
            bool: True si la position est valide (dans les limites du plateau et non occupée), False sinon.
        """
        
        max_x, max_y = cons.DIM_PLATEAU
        if r == 0:
            coordonnees = self.coordonnees
        else:
            m = self.current[(self.position[2]+r)%len(self.current)]
            coords = []
            for i, l in enumerate(m):
                for j, k in enumerate(l):
                    if k != 0:
                        coords.append([i+self.position[0], j+self.position[1]])
            coordonnees = coords
#			print("Rotation testée: %s" % coordonnees)
        for cx, cy in coordonnees:
            if not 0 <= x + cx < max_x:
                #				print("Non valide en X: cx=%s, x=%s" % (cx, x))
                return False
            elif cy < 0:
                continue
            elif y + cy >= max_y:
                #				print("Non valide en Y: cy=%s, y=%s" % (cy, y))
                return False
            else:
                if self.plateau[cy + y][cx + x] != 0:
                    #					print("Position occupée sur le plateau")
                    return False


#		print("Position testée valide: x=%s, y=%s" % (x, y))
        return True
    def _poser_piece(self) -> None:
        """
        Pose la pièce courante sur le plateau, met à jour l'état du jeu et calcule le score.
        Cette méthode effectue les opérations suivantes :
        - Vérifie si la pièce est posée en haut du plateau pour déterminer si la partie est perdue.
        - Ajoute la pièce courante sur le plateau avec sa couleur.
        - Détecte et supprime les lignes complètes, puis insère des lignes vides en haut du plateau.
        - Met à jour le nombre de lignes complétées, le score et le niveau du joueur.
        - Gère le cas particulier du "Tetris" (quatre lignes complétées simultanément) et augmente le score en conséquence.
        - Termine le travail avec la pièce courante en la réinitialisant.
        Aucun paramètre n'est attendu.
        Ne retourne rien.
        """
        
        print("La pièce est posée")
        if self.position[1] <= 0:
            self.perdu = True
        # Ajout de la pièce parmi le plateau
        couleur = self._get_current_piece_color()
        for cx, cy in self.coordonnees:
            self.plateau[cy][cx] = couleur
        completees = []
        # calculer les lignes complétées
        for i, line in enumerate(self.plateau[::-1]):
            for case in line:
                if case == 0:
                    break
            else:
                print(self.plateau)
                print(">>> %s" % (cons.DIM_PLATEAU[1]-1-i))
                completees.append(cons.DIM_PLATEAU[1]-1-i)
        lignes = len(completees)
        for i in completees:
            self.plateau.pop(i)
        for i in range(lignes):
            self.plateau.insert(0, [0] * cons.DIM_PLATEAU[0])
        # calculer le score et autre
        self.lignes += lignes
        self.score += lignes * self.niveau
        self.niveau = int(self.lignes / 10) + 1
        if lignes >= cons.NOMBRE_DE_LIGNES_SCORE_MULTIPLIE:
            self.tetris +=1
            self.score += self.niveau * self.tetris
        # Travail avec la pièce courante terminé
        self.current = None
    def _first(self) -> None:
        """
        Initialise les variables principales du jeu Tetris.
        Cette méthode configure le plateau de jeu, réinitialise le score, le nombre de pièces jouées,
        le nombre de lignes complétées, le nombre de tetris réalisés et le niveau du joueur.
        Elle prépare également la prochaine pièce à jouer et indique que la partie n'est pas perdue.
        Attributs modifiés :
            - plateau : matrice représentant le plateau de jeu.
            - score : score actuel du joueur.
            - pieces : nombre de pièces jouées.
            - lignes : nombre de lignes complétées.
            - tetris : nombre de tetris réalisés.
            - niveau : niveau actuel du joueur.
            - current : pièce courante (initialisée à None).
            - next : prochaine pièce à jouer.
            - perdu : état de la partie (False = partie en cours).
        """
        
        self.plateau = [[0] * cons.DIM_PLATEAU[0] for i in range(cons.DIM_PLATEAU[1])]
        self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
        self.current, self.next, self.perdu = None, self._get_piece(), False
    def _next(self) -> None:
        """
        Prépare la pièce suivante dans le jeu.
        Cette méthode effectue les opérations suivantes :
        - Affiche un message indiquant le passage à la pièce suivante.
        - Met à jour la pièce courante avec la prochaine pièce et génère une nouvelle pièce suivante.
        - Incrémente le compteur de pièces.
        - Réinitialise la position de la pièce courante au centre supérieur du plateau.
        - Calcule les données associées à la nouvelle pièce courante.
        - Met à jour les timestamps du dernier mouvement et de la dernière chute.
        """
        
        print("Piece suivante")
        self.current, self.next = self.next, self._get_piece()
        self.pieces += 1
        self.position = [int(cons.DIM_PLATEAU[0] / 2)-2, -4, 0]
        self._calculer_donnes_piece_courante()
        self.dernier_mouvement = self.derniere_chute = time.time()
    def _gerer_evenemet(self) -> None:
        """
        Gère les événements de contrôle du jeu Tetris.
        Cette méthode récupère l'événement utilisateur courant et effectue l'action correspondante :
        - Met le jeu en pause si la touche 'P' est pressée.
        - Déplace la pièce vers la gauche, la droite ou le bas selon les flèches directionnelles, si le mouvement est valide.
        - Effectue une rotation de la pièce avec la flèche du haut, si la rotation est valide.
        - Fait chuter la pièce instantanément avec la barre d'espace.
        Après chaque action, les données de la pièce courante sont recalculées.
        Retourne:
            None
        """
        
        event = self._get_event()
        if event == K_p:
            print("Pause")
            self.surface.fill(cons.COULEURS.get(0))
            self._afficher_texte('Pause', cons.CENTRE_FENETRE, font='titre')
            self._afficher_texte('Appuyer sur une touche...', cons.POS)
            self._attente()
        elif event == K_LEFT:
            print("Mouvement vers la gauche")
            if self._est_valide(x=-1):
                self.position[0] -= 1
        elif event == K_RIGHT:
            print("Mouvement vers la droite")
            if self._est_valide(x=1):
                self.position[0] += 1
        elif event == K_DOWN:
            print("Mouvement vers le bas")
            if self._est_valide(y=1):
                self.position[1] += 1
        elif event == K_UP:
            print("Mouvement de rotation")
            if self._est_valide(r=1):
                self.position[2] = (self.position[2] + 1) %len(self.current)
        elif event == K_SPACE:
            print("Mouvement de chute %s / %s" % (self.position, self.coordonnees))
            if self.position[1] <=0:
                self.position[1] = 1
                self._calculer_donnes_piece_courante()
            a = 0
            while self._est_valide(y=a):
                a+=1
            self.position[1] += a-1
        self._calculer_donnes_piece_courante()
    def _gerer_gravite(self) -> None:
        """
        Gère la gravité du jeu en déplaçant la pièce courante vers le bas à intervalles réguliers.
        Si le temps écoulé depuis la dernière chute dépasse la valeur de gravité définie, la méthode tente de déplacer la pièce vers le bas :
        - Si la position actuelle est invalide, la pièce est remontée d'une ligne, ses données sont recalculées et elle est posée sur le plateau.
        - Si la position actuelle est valide mais qu'elle ne le serait pas en descendant d'une ligne, la pièce est posée sur le plateau.
        - Sinon, la pièce est déplacée d'une ligne vers le bas et ses données sont recalculées.
        Cette méthode permet de simuler la chute automatique des pièces dans le jeu de Tetris.
        """
        
        if time.time() - self.derniere_chute > cons.GRAVITE:
            self.derniere_chute = time.time()
            if not self._est_valide():
                print ("On est dans une position invalide")
                self.position[1] -= 1
                self._calculer_donnes_piece_courante()
                self._poser_piece()
            elif self._est_valide() and not self._est_valide(y=1):
                self._calculer_donnes_piece_courante()
                self._poser_piece()
            else:
                print("On déplace vers le bas")
                self.position[1] += 1
                self._calculer_donnes_piece_courante()
    def _dessiner_plateau(self) -> None:
        """
        Dessine le plateau de jeu de Tetris sur la surface graphique.
        Cette méthode effectue les opérations suivantes :
        - Remplit la surface avec la couleur de fond.
        - Dessine la bordure du plateau.
        - Dessine chaque bloc du plateau selon sa couleur.
        - Dessine la pièce courante si elle existe.
        - Affiche les informations du jeu (score, nombre de pièces, lignes, tetris, niveau).
        - Rend la surface à l'écran.
        Aucun paramètre n'est requis.
        Ne retourne rien.
        """
        
        self.surface.fill(cons.COULEURS.get(0))
        pygame.draw.rect(self.surface, cons.COULEURS[8], cons.START_PLABORD+cons.TAILLE_PLABORD, cons.BORDURE_PLATEAU)
        for i, ligne in enumerate(self.plateau):
            for j, case in enumerate(ligne):
                couleur = cons.COULEURS[case]
                position = j, i
                coordonnees = tuple([cons.START_PLATEAU[k] + position[k] * cons.TAILLE_BLOC[k] for k in range(2)])
                pygame.draw.rect(self.surface, couleur, coordonnees + cons.TAILLE_BLOC)
        if self.current is not None:
            for position in self.coordonnees:
                couleur = cons.COULEURS.get(self._get_current_piece_color())
                coordonnees = tuple([cons.START_PLATEAU[k] + position[k] * cons.TAILLE_BLOC[k] for k in range(2)])
                pygame.draw.rect(self.surface, couleur, coordonnees + cons.TAILLE_BLOC)
        self.score, self.pieces, self.lignes, self.tetris, self.niveau#TODO
        self._afficher_texte('Score: >%s' % self.score, cons.POSITION_SCORE)
        self._afficher_texte('Pièces: %s' % self.pieces, cons.POSITION_PIECES)
        self._afficher_texte('Lignes: %s' % self.lignes, cons.POSITION_LIGNES)
        self._afficher_texte('Tetris: %s' % self.tetris, cons.POSITION_TETRIS)
        self._afficher_texte('Niveau: %s' % self.niveau, cons.POSITION_NIVEAU)

        self._rendre()
  
    def play(self) -> None:
        """
        Démarre et gère la boucle principale du jeu Tetris.
        Cette méthode initialise la surface de jeu, affiche le message de démarrage,
        puis exécute la boucle principale tant que le joueur n'a pas perdu.
        À chaque itération, elle gère l'apparition d'une nouvelle pièce, les événements utilisateur,
        la gravité des pièces et le dessin du plateau de jeu.
        Retour:
            None
        """
        
        print("Jouer")
        self.surface.fill(cons.COULEURS.get(0))
        self._first()
        while not self.perdu:
            if self.current is None:
                self._next()
            self._gerer_evenemet()
            self._gerer_gravite()
            self._dessiner_plateau()

if __name__ == '__main__':
    j = Jeu()
    print("Jeu prêt")
    j.start()
    print("Partie démarée")
    j.play()
    print("Partie terminée")
    j.stop()
    print("Arrêt du programme")
