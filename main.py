import pygame
from core.states.main_menu import MainMenu
from core.states.gameplay import Gameplay
from core.states.gameover import GameOver

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jurassic Car Attack")
clock = pygame.time.Clock()

# Gestion des états
states = {
    "MAIN_MENU": MainMenu(),
    "GAMEPLAY": Gameplay(),
    "GAMEOVER": GameOver(0)
}
current_state = states["MAIN_MENU"]

# Boucle principale
while True:
    events = pygame.event.get()
    current_state.handle_events(events)
    current_state.update()

    # Vérifier si on doit changer d'état
    if current_state.next_state:
        if current_state.next_state == "GAMEOVER":
            states["GAMEOVER"] = GameOver(states["GAMEPLAY"].score)
        current_state = states[current_state.next_state]

    current_state.render(screen)
    pygame.display.flip()
    clock.tick(60)
