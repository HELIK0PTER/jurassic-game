import pygame
import os
from core.states.state import State

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Chemin du fichier des scores
SCORES_FILE = "saves/saved_scores.txt"

# Chargement des images
background = pygame.image.load("assets/images/menu_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
jurassic_logo = pygame.image.load("assets/images/menu_logo.png")
jurassic_logo = pygame.transform.scale(jurassic_logo, (250, 200))

class Leaderboard(State):
    def __init__(self):
        super().__init__()
        # Police de thème
        self.font_theme = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 32)
        self.font_title = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 64)

        # Charger les scores depuis le fichier
        self.scores = self.load_scores()

        # Variable pour gérer le clignotement du texte
        self.blink_timer = 0
        self.show_text = True

    def load_scores(self):
        """Charge les scores depuis `saved_scores.txt` et retourne une liste triée."""
        if not os.path.exists(SCORES_FILE):
            print(f"Fichier {SCORES_FILE} introuvable. Aucun score chargé.")
            return []

        try:
            with open(SCORES_FILE, "r") as file:
                lines = file.readlines()

            # Convertir les données en une liste de tuples (nom, score)
            score_data = []
            for line in lines:
                try:
                    name, score = line.strip().split(":")
                    score_data.append((name, int(score)))
                except ValueError:
                    continue

            # Trier les scores par ordre décroissant
            score_data.sort(key=lambda x: x[1], reverse=True)
            return score_data
        except Exception as e:
            print(f"Erreur lors du chargement des scores : {e}")
            return []

    def render(self, screen):
        """Affiche l'écran du leaderboard."""
        # Fond
        screen.blit(background, (0, 0))

        # Logo Jurassic
        screen.blit(jurassic_logo, (WIDTH // 2 - jurassic_logo.get_width() // 2, 50))

        # Titre "Leaderboard"
        title = self.font_title.render("Leaderboard", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 270))

        # Afficher les scores
        y_offset = 350
        for rank, (name, score) in enumerate(self.scores[:4], start=1):  # Top 5
            score_text = self.font_theme.render(f"{rank}. {name}: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
            y_offset += 50

        # Texte de retour clignotant
        if self.show_text:
            exit_text = self.font_theme.render("Press ESC to return to Menu", True, WHITE)
            screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 550))

    def update(self):
        """Met à jour le clignotement du texte."""
        self.blink_timer += 1
        if self.blink_timer % 60 == 0:  # Change toutes les 60 frames
            self.show_text = not self.show_text

    def handle_events(self, events):
        """Gère les événements utilisateur."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MAIN_MENU"
