import pygame
import datetime
import os

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

# Fichier de configuration pour les paramètres
SETTINGS_FILE = "volume_config.txt"


class Settings(State):
    def __init__(self):
        super().__init__()
        # Chargement d'une police thématique pour tous les textes
        self.font_theme = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 32)
        self.font_title = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 64)

        # Charger les paramètres de volume depuis le fichier de configuration
        self.load_settings()

        # Rectangle pour la barre de volume
        self.volume_bar_rect = pygame.Rect(300, 400, 200, 20)

        # Variable pour gérer le clignotement du texte
        self.blink_timer = 0
        self.show_text = True

        # Initialisation de la musique et des sons
        self.background_music = pygame.mixer.music
        self.gameover_music = None  # Musique de game over
        self.welcome_music = None  # Musique de bienvenue

    def load_settings(self):
        # Si le fichier settings.txt existe, on charge les paramètres
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                # Charger le volume depuis le fichier texte (le fichier contient une seule valeur)
                try:
                    self.volume = int(file.read().strip())
                except ValueError:
                    self.volume = 50  # Valeur par défaut en cas d'erreur
        else:
            self.volume = 50  # Valeur par défaut si le fichier n'existe pas

        # Applique le volume initial à la musique et aux sons
        self.apply_volume_to_sounds()

    def save_settings(self):
        # Sauvegarde les paramètres dans settings.txt
        with open(SETTINGS_FILE, "w") as file:
            file.write(str(self.volume))  # Sauvegarde la valeur du volume sous forme de chaîne

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.next_state = "MAIN_MENU"  # Retour au menu principal
                self.save_settings()  # Sauvegarde les paramètres avant de quitter
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

        # Applique le volume à la musique et aux sons
        self.apply_volume_to_sounds()

        # Sauvegarde immédiatement le volume après la modification
        self.save_settings()

    def apply_volume_to_sounds(self):
        # Applique le volume aux différentes musiques et sons
        volume_level = self.volume / 100.0  # Convertir le volume en valeur entre 0 et 1
        pygame.mixer.music.set_volume(volume_level)  # Appliquer au fond sonore

        # Enlève ces vérifications si tu n'as pas d'autres musiques
        # Si tu souhaites utiliser gameover_music et welcome_music à l'avenir, assure-toi qu'elles sont définies
        # if self.gameover_music:
        #     self.gameover_music.set_volume(volume_level)  # Appliquer à la musique de Game Over
        # if self.welcome_music:
        #     self.welcome_music.set_volume(volume_level)  # Appliquer à la musique de bienvenue

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
                                         self.volume_bar_rect.width * (self.volume / 100),
                                         self.volume_bar_rect.height))  # Volume
        volume_label = self.font_theme.render(f"Volume: {self.volume}%", True, WHITE)
        screen.blit(volume_label, (self.volume_bar_rect.x, self.volume_bar_rect.y - 40))

        # Affiche la phrase clignotante sous la barre de volume
        if self.show_text:
            exit_text = self.font_theme.render("Press ESC to exit Settings", True, WHITE)
            screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 450))  # Position sous la barre

        # Affiche l'heure actuelle
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_text = self.font_theme.render(f"Time: {current_time}", True, WHITE)
        screen.blit(time_text, (WIDTH - 200, HEIGHT - 50))  # En bas à droite

    def update(self):
        # Met à jour le clignotement du texte
        self.blink_timer += 1
        if self.blink_timer % 60 == 0:  # Change toutes les 30 frames
            self.show_text = not self.show_text
