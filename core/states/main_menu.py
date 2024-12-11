import pygame
from core.states.state import State
import sys

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jurassic Park Menu")

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
    {"rect": pygame.Rect(300, 400, 80, 80), "icon": icon_play, "label": "Play"},
    {"rect": pygame.Rect(400, 400, 80, 80), "icon": icon_trophy, "label": "Trophy"},
    {"rect": pygame.Rect(500, 400, 80, 80), "icon": icon_settings, "label": "Menu"},
]

# Fonction pour dessiner les boutons
def draw_buttons():
    for button in buttons:
        screen.blit(button["icon"], button["rect"])

class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render("Jurassic Car Attack", True, (255, 255, 255))
        self.subtitle = pygame.font.Font(None, 36).render("Press SPACE to Start", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # clear events and change state
                events.clear()
                self.next_state = "GAMEPLAY"

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title, (200, 200))
        screen.blit(self.subtitle, (250, 300))

# Boucle principale
running = True
main_menu = MainMenu()
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    main_menu.handle_events(events)

    # Affichage de l'arrière-plan
    screen.blit(background, (0, 0))

    # Affichage du logo
    screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))

    # Dessin des boutons
    draw_buttons()

    # Affichage du menu principal
    main_menu.render(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()
