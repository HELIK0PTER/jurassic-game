import pygame
from core.events import handle_quit

class State:
    def __init__(self):
        self.next_state = None  # État suivant
        self.player_name = None

    def handle_events(self, events):
        """
        Gère les événements pour cet état.
        """
        pass

    def update(self):
        """
        Met à jour la logique de l'état.
        """
        pass

    def render(self, screen):
        """
        Gère l'affichage de l'état.
        """
        pass
