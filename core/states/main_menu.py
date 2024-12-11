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

# Chargement des icônes des boutons
icon_trophy = pygame.image.load("assets/images/menu_leaderboard.png")
icon_trophy = pygame.transform.scale(icon_trophy, (80, 80))
icon_trophy_on = pygame.image.load("assets/images/menu_leaderboard_up.png")  # Image animée
icon_trophy_on = pygame.transform.scale(icon_trophy_on, (80, 80))
icon_play = pygame.image.load("assets/images/menu_play.png")
icon_play = pygame.transform.scale(icon_play, (80, 80))
icon_play_on = pygame.image.load("assets/images/menu_play_up.png")  # Image animée
icon_play_on = pygame.transform.scale(icon_play_on, (80, 80))
icon_settings = pygame.image.load("assets/images/menu_settings.png")
icon_settings = pygame.transform.scale(icon_settings, (80, 80))
icon_settings_on = pygame.image.load("assets/images/menu_settings_up.png")  # Image animée
icon_settings_on = pygame.transform.scale(icon_settings_on, (80, 80))
icon_exit = pygame.image.load("assets/images/menu_exit.png")
icon_exit = pygame.transform.scale(icon_exit, (80, 80))
icon_exit_on = pygame.image.load("assets/images/menu_exit_up.png")  # Image animée
icon_exit_on = pygame.transform.scale(icon_exit_on, (80, 80))

# Définition des boutons (avec les icônes)
buttons = [
    {"rect": pygame.Rect(300, 350, 80, 80), "icon": icon_play,"icon_on": icon_play_on ,"active_icon": icon_play_on, "label": "GAMEPLAY"},
    {"rect": pygame.Rect(440, 350, 80, 80), "icon": icon_trophy,"icon_on": icon_trophy_on ,"active_icon": icon_trophy_on, "label": "TROPHY"},
    {"rect": pygame.Rect(300, 450, 80, 80), "icon": icon_settings,"icon_on": icon_settings_on ,"active_icon": icon_settings_on, "label": "SETTINGS"},
    {"rect": pygame.Rect(440, 450, 80, 80), "icon": icon_exit,"icon_on": icon_exit_on , "active_icon": icon_exit_on, "label": "EXIT"},
]

# Fonction pour dessiner les boutons
def draw_buttons(screen):
    for button in buttons:
        screen.blit(button["icon"], button["rect"])

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