import pygame
import datetime
from core.states.state import State

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

class GameOver(State):
    def __init__(self, score=0, player_name="Player"):
        super().__init__()
        self.score = score  # Le score du joueur
        self.player_name = player_name  # Le nom du joueur
        self.save_score()  # Sauvegarde directement le score
        self.restart_message = "Press ENTER to return at Menu"
        self.blink = True

        # Chargement de l'image de fond
        self.background = pygame.image.load("assets/images/gameover.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))  # Mettre à l'échelle

        # Initialisation de la police de texte
        self.font_text = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 36)

        # Chronomètre pour gérer le clignotement
        self.last_blink_time = pygame.time.get_ticks()
        self.blink_interval = 500

        # Initialisation audio
        self.gameover_music = None
        self.is_first_update = True  # Nouveau flag pour jouer le son une seule fois

        # Charger l'image des griffures
        self.scratch_image = pygame.image.load("assets/images/griffure.png")

        # Redimensionner l'image des griffures pour la nouvelle taille plus grande
        self.scratch_image = pygame.transform.scale(self.scratch_image, (1500, 480))  # Plus grand que précédemment

        # Initialiser le chronomètre pour l'image des griffures
        self.scratch_time = None  # Temps où l'image doit apparaître
        self.image_displayed = False  # Vérifier si l'image a été affichée

    def save_score(self):
        """Sauvegarde le score actuel dans le fichier `saves/saved_scores.txt`."""
        try:
            with open("saves/saved_scores.txt", "a") as file:
                file.write(f"{self.player_name}:{self.score}\n")
            print(f"Score de {self.player_name} ({self.score}) sauvegardé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")

    def update(self):
        # Jouer le son uniquement lors du premier update
        if self.is_first_update:
            pygame.mixer.init()  # Initialiser le mixeur audio si ce n'est pas encore fait
            self.gameover_music = pygame.mixer.Sound("assets/sounds/gameover_song.mp3")
            self.gameover_music.play()
            self.is_first_update = False  # Empêche la lecture multiple du son

        # Gère le clignotement du texte
        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink_time > self.blink_interval:
            self.blink = not self.blink
            self.last_blink_time = current_time

        # Vérifier si 2 secondes sont passées pour afficher les griffures
        if self.scratch_time is None:  # Si le temps n'est pas encore défini
            self.scratch_time = current_time + 1500  # 2 secondes après le début de l'écran Game Over

        # Afficher l'image des griffures après 2 secondes
        if not self.image_displayed and current_time >= self.scratch_time:
            self.image_displayed = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Arrêter la musique avant de retourner au menu
                if self.gameover_music:
                    self.gameover_music.stop()
                self.next_state = "MAIN_MENU"

    def render(self, screen):
        # Affiche l'image de fond
        screen.blit(self.background, (0, 0))

        # Affiche le score légèrement sous le haut de l'écran
        score_text = self.font_text.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))  # Positionné juste sous le haut

        # Affiche le nom du joueur
        player_name_text = self.font_text.render(f"Player: {self.player_name}", True, (255, 255, 255))
        screen.blit(player_name_text, (WIDTH // 2 - player_name_text.get_width() // 2, 60))  # Un peu sous le score

        # Affiche l'heure actuelle
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_text = self.font_text.render(f"Time: {current_time}", True, (255, 255, 255))
        screen.blit(time_text, (WIDTH - 200, HEIGHT - 50))  # En bas à droite

        # Affiche le message clignotant légèrement au-dessus du bas de l'écran
        if self.blink:
            restart_text = self.font_text.render(self.restart_message, True, (255, 255, 255))
            screen.blit(restart_text,
                        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 100))  # Positionné juste au-dessus du bas

        # Afficher l'image des griffures si 2 secondes sont passées
        if self.image_displayed:
            # Calculer la position du texte "Game Over"
            gameover_text = self.font_text.render("GAME OVER", True, (255, 255, 255))
            gameover_rect = gameover_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))  # Centré sur l'écran

            # Calculer la position de l'image des griffures pour la centrer sur le texte
            scratch_rect = self.scratch_image.get_rect(center=gameover_rect.center)  # Centré sur le texte

            # Afficher l'image des griffures sur le texte "Game Over"
            screen.blit(self.scratch_image, scratch_rect.topleft)
