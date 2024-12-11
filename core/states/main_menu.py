import pygame
from core.states.state import State

class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render("Jurassic Car Attack", True, (255, 255, 255))
        self.subtitle = pygame.font.Font(None, 36).render("Press SPACE to Start", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.next_state = "GAMEPLAY"

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title, (200, 200))
        screen.blit(self.subtitle, (250, 300))
