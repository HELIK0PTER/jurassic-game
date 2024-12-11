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

# Fichier de sauvegarde des scores et pseudos
SAVED_SCORES_FILE = "saved_scores.txt"


class PromptName(State):
    def __init__(self):
        super().__init__()
        # Applique la police personnalisée
        self.font = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 74)
        self.font_theme = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 32)  # Police pour le texte d'information
        self.blink_timer = 0  # Chronomètre pour le clignotement
        self.show_text = True  # Contrôle si le texte doit être affiché ou non
        self.player_name = ""  # Initialisation du nom du joueur
        self.score = 0  # Initialisation du score (par défaut à 0)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Permettre à l'utilisateur d'entrer son nom
                if event.key == pygame.K_RETURN and self.player_name != "":  # Confirmer l'entrée
                    self.save_player_score(self.player_name, self.score)  # Sauvegarder le nom et le score
                    self.next_state = "GAMEPLAY"  # Passer au gameplay une fois le nom et le score sauvegardés
                elif event.key == pygame.K_ESCAPE:
                    self.next_state = "MAIN_MENU"  # Retourner au menu principal si ESC est pressé

                elif event.key == pygame.K_BACKSPACE:
                    # Supprimer un caractère du nom
                    self.player_name = self.player_name[:-1]
                elif event.key <= 127:  # Vérifie si le caractère est valide (lettres, chiffres, etc.)
                    # Ajouter le caractère tapé au nom du joueur
                    self.player_name += event.unicode

    def render(self, screen):
        # Afficher le fond
        screen.blit(background, (0, 0))
        screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))

        # Afficher le texte qui remplace "Enter your name" avec ce que le joueur tape
        if self.player_name == "":
            text = self.font.render("Enter your name", True, WHITE)  # Si aucun nom n'est tapé, afficher "Enter your name"
        else:
            text = self.font.render(self.player_name, True, WHITE)  # Si un nom est tapé, afficher le nom

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300))

        # Affiche la phrase clignotante (par exemple pour "Press ESC to return to Main Menu")
        if self.show_text:
            exit_text = self.font_theme.render("Press ESC to return to Main Menu", True, WHITE)
            screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 450))  # Position sous le texte du nom

    def update(self):
        # Met à jour le clignotement du texte
        self.blink_timer += 1
        if self.blink_timer % 60 == 0:  # Change toutes les 30 frames (si 60 FPS)
            self.show_text = not self.show_text  # Alterner l'affichage du texte

    def save_player_score(self, name, score):
        """ Sauvegarde le nom du joueur et son score dans un fichier texte. """
        try:
            with open(SAVED_SCORES_FILE, "a") as file:
                file.write(f"{name}:{score}\n")  # Enregistrer le nom et le score, séparés par un ':'
            print(f"Nom du joueur '{name}' avec score '{score}' sauvegardé.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du nom et du score : {e}")

    def load_player_scores(self):
        """ Charge les pseudos et les scores sauvegardés depuis le fichier texte. """
        try:
            with open(SAVED_SCORES_FILE, "r") as file:
                scores = file.readlines()
            # Séparer chaque ligne en nom et score, puis les retourner sous forme de liste de tuples
            return [line.strip().split(":") for line in scores]
        except FileNotFoundError:
            return []  # Aucun nom et score si le fichier n'existe pas
