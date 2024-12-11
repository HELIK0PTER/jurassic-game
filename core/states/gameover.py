import pygame
import datetime
from core.states.state import State

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

class GameOver(State):
    def __init__(self, score=0):
        super().__init__()
        # Chargement de l'image de fond
        self.background = pygame.image.load("assets/images/gameover.jpg")
        self.background = pygame.transform.scale(self.background, (800, 600))  # Ajuste à la taille de l'écran

        # Chargement de la police thématique
        self.font_text = pygame.font.Font("assets/fonts/SpecialElite-Regular.ttf", 36)

        # Textes
        self.score = score
        self.restart_message = "Press ENTER to return at Menu"
        self.blink = True  # État pour le clignotement de la phrase

        # Chronomètre pour gérer le clignotement
        self.last_blink_time = pygame.time.get_ticks()
        self.blink_interval = 500  # Intervalle de clignotement (en millisecondes)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next_state = "MAIN_MENU"  # Retour au menu principal

    def render(self, screen):
        # Affiche l'image de fond
        screen.blit(self.background, (0, 0))

        # Affiche le score légèrement sous le haut de l'écran
        score_text = self.font_text.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))  # Positionné juste sous le haut

        # Affiche l'heure actuelle
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_text = self.font_text.render(f"Time: {current_time}", True, (255, 255, 255))
        screen.blit(time_text, (WIDTH - 200, HEIGHT - 50))  # En bas à droite

        # Affiche le message clignotant légèrement au-dessus du bas de l'écran
        if self.blink:
            restart_text = self.font_text.render(self.restart_message, True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 100))  # Positionné juste au-dessus du bas

    def update(self):
        # Gère le clignotement du texte
        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink_time > self.blink_interval:
            self.blink = not self.blink  # Change l'état de clignotement
            self.last_blink_time = current_time
