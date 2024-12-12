import pygame
from core.states.state import State

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Chargement des images
background = pygame.image.load("assets/images/menu_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
jurassic_logo = pygame.image.load("assets/images/menu_logo.png")
jurassic_logo = pygame.transform.scale(jurassic_logo, (250, 200))

class Leaderboard(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.scores = self.load_scores()  # Charger les scores depuis le fichier

    def load_scores(self):
        """Charge les scores depuis `saved_scores.txt` et retourne une liste triée."""
        try:
            with open("saved_scores.txt", "r") as file:
                lines = file.readlines()

            # Convertir les données en une liste de tuples (nom, score)
            score_data = []
            for line in lines:
                try:
                    name, score = line.strip().split(":")
                    score_data.append((name, int(score)))
                except ValueError:
                    print(f"Ligne mal formatée ignorée : {line.strip()}")

            # Trier les scores par ordre décroissant
            score_data.sort(key=lambda x: x[1], reverse=True)
            return score_data
        except FileNotFoundError:
            print("Fichier 'saved_scores.txt' introuvable. Aucun score chargé.")
            return []  # Retourner une liste vide si le fichier est introuvable

    def render(self, screen):
        """Affiche l'écran du leaderboard."""
        screen.blit(background, (0, 0))
        screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))

        title = self.font.render("Leaderboard", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        # Afficher les scores
        y_offset = 200
        for rank, (name, score) in enumerate(self.scores[:10], start=1):  # Top 10 seulement
            score_text = self.font.render(f"{rank}. {name}: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
            y_offset += 40

    def update(self):
        """Met à jour l'état."""
        pass

    def handle_events(self, events):
        """Gère les événements utilisateur."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MAIN_MENU"
