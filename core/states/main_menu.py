import pygame

from core.events import handle_quit
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

# Chargement des icônes des boutons
icon_trophy = pygame.image.load("assets/images/menu_leaderboard.png")
icon_trophy = pygame.transform.scale(icon_trophy, (80, 80))
icon_play = pygame.image.load("assets/images/menu_play.png")
icon_play = pygame.transform.scale(icon_play, (80, 80))
icon_settings = pygame.image.load("assets/images/menu_settings.png")
icon_settings = pygame.transform.scale(icon_settings, (80, 80))

# Définition des boutons (avec les icônes)
buttons = [
    {"rect": pygame.Rect(300, 400, 80, 80), "icon": icon_play, "label": "GAMEPLAY"},
    {"rect": pygame.Rect(400, 400, 80, 80), "icon": icon_trophy, "label": "TROPHY"},
    {"rect": pygame.Rect(500, 400, 80, 80), "icon": icon_settings, "label": "SETTINGS"},
    {"rect": pygame.Rect(600, 400, 80, 80), "icon": icon_settings, "label": "EXIT"},
]

# Fonction pour dessiner les boutons
def draw_buttons(screen):
    for button in buttons:
        screen.blit(button["icon"], button["rect"])

class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render("Jurassic Car Attack", True, (255, 255, 255))
        self.subtitle = pygame.font.Font(None, 36).render("Select an Option", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                for button in buttons:
                    if button["label"] == "EXIT":
                        handle_quit()
                    if button["rect"].collidepoint(event.pos):
                        self.next_state = button["label"]

    def render(self, screen):
        screen.blit(background, (0, 0))
        screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))
        screen.blit(self.title, (200, 200))
        screen.blit(self.subtitle, (250, 300))
        draw_buttons(screen)

    def update(self):
        pass
