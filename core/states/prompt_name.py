import pygame
from core.states.state import State

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)

# Chargement des images
background = pygame.image.load("assets/images/menu_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
jurassic_logo = pygame.image.load("assets/images/menu_logo.png")
jurassic_logo = pygame.transform.scale(jurassic_logo, (250, 200))

class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.active_button = None  # Bouton actuellement actif

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        self.active_button = button  # Activer l'animation
                        button["icon"] = button["active_icon"] or button["icon"]  # Change l'icône si disponible
            elif event.type == pygame.MOUSEBUTTONUP and self.active_button:  # Réinitialiser après le clic
                self.active_button["icon"] = icon_play  # Réinitialise l'icône du bouton "Play"
                self.active_button = None
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        self.next_state = button["label"]

    def render(self, screen):
        screen.blit(background, (0, 0))
        screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))
        draw_buttons(screen)

    def update(self):
        pass