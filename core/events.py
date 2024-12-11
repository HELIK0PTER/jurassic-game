import pygame
import sys

def handle_quit():
    """
    Gère les événements de sortie du jeu, comme la fermeture de la fenêtre.
    """
    # Si l'utilisateur ferme la fenêtre
    pygame.quit()
    exit()

def handle_mouse_click():
    """
    Récupère la position de la souris lors d'un clic gauche.
    Retourne les coordonnées (x, y) de la souris ou None si pas de clic.
    """
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            return pygame.mouse.get_pos()
    return None
