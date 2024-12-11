import pygame
from core.states.state import State

class GameOver(State):
    def __init__(self, score = 0):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.message = self.font.render("Game Over!", True, (255, 0, 0))
        self.score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (255, 255, 255))
        self.restart_message = pygame.font.Font(None, 36).render("Press ENTER", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next_state = "MAIN_MENU"  # Demande de revenir à l'écran d'accueil

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.message, (200, 200))
        screen.blit(self.score_text, (250, 300))
        screen.blit(self.restart_message, (250, 400))  # Ajoute une instruction pour revenir à l'accueil
