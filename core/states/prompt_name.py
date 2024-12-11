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

class PromptName(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)


    def handle_events(self, events):



    def render(self, screen):
        screen.blit(background, (0, 0))
        screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))

    def update(self):
        pass