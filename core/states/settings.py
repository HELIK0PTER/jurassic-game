import pygame
import datetime

from core.states.state import State

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)

# Chargement des images
background = pygame.image.load("assets/images/menu_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
jurassic_logo = pygame.image.load("assets/images/menu_logo.png")
jurassic_logo = pygame.transform.scale(jurassic_logo, (250, 200))  # Taille ajustée du logo

class Settings(State):
    def __init__(self):
        super().__init__()
        # Chargement d'une police thématique pour tous les textes
        self.font_theme = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 32)  # Remplacez par une police d'aventure/dinosaures
        self.font_title = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 64)  # Version plus grande pour le titre
        self.volume = 50  # Volume initial (entre 0 et 100)
        self.volume_bar_rect = pygame.Rect(300, 400, 200, 20)  # Rectangle pour la barre de volume

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.next_state = "MAIN_MENU"  # Retour au menu principal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si la souris clique sur la barre de volume
                if self.volume_bar_rect.collidepoint(event.pos):
                    self.update_volume(event.pos[0])  # Met à jour le volume en fonction de la position X

            elif event.type == pygame.MOUSEMOTION:
                # Si la souris est enfoncée, mettre à jour le volume
                if pygame.mouse.get_pressed()[0]:  # Bouton gauche maintenu
                    if self.volume_bar_rect.collidepoint(event.pos):
                        self.update_volume(event.pos[0])

    def update_volume(self, mouse_x):
        # Met à jour le volume en fonction de la position X sur la barre
        relative_x = mouse_x - self.volume_bar_rect.x
        self.volume = max(0, min(100, int((relative_x / self.volume_bar_rect.width) * 100)))

    def render(self, screen):
        # Affiche le background
        screen.blit(background, (0, 0))

        # Affiche le logo Jurassic Park
        screen.blit(jurassic_logo, (WIDTH // 2 - jurassic_logo.get_width() // 2, 50))

        # Affiche le titre "Settings"
        title = self.font_title.render("Settings", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 270))  # Position sous le logo

        # Affiche la barre de volume
        pygame.draw.rect(screen, GREY, self.volume_bar_rect)  # Fond de la barre
        pygame.draw.rect(screen, GREEN, (self.volume_bar_rect.x, self.volume_bar_rect.y,
                                         self.volume_bar_rect.width * (self.volume / 100), self.volume_bar_rect.height))  # Volume
        volume_label = self.font_theme.render(f"Volume: {self.volume}%", True, WHITE)
        screen.blit(volume_label, (self.volume_bar_rect.x, self.volume_bar_rect.y - 40))

        # Affiche l'heure actuelle
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_text = self.font_theme.render(f"Time: {current_time}", True, WHITE)
        screen.blit(time_text, (WIDTH - 200, HEIGHT - 50))  # En bas à droite

    def update(self):
        pass
