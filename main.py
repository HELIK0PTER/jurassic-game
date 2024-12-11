import pygame

from core.events import handle_quit
from core.states.main_menu import MainMenu
from core.states.gameplay import Gameplay
from core.states.gameover import GameOver
from core.states.settings import Settings

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jurassic Car Attack")
clock = pygame.time.Clock()

# Gestion des états
states = {
    "MAIN_MENU": MainMenu(),
    "GAMEPLAY": Gameplay(),
    "GAMEOVER": GameOver(),
    "SETTINGS": Settings(),
    }
current_state = states["MAIN_MENU"]

# Boucle principale
while True:
    events = pygame.event.get()
    current_state.handle_events(events)
    current_state.update()

    # Vérifier si on doit changer d'état
    if current_state.next_state:
        if current_state.next_state == "MAIN_MENU":
            states["MAIN_MENU"] = MainMenu()  # Réinitialise l'écran principal
            current_state = states["MAIN_MENU"]
        elif current_state.next_state == "GAMEPLAY":
            states["GAMEPLAY"] = Gameplay()
            current_state = states["GAMEPLAY"]
        elif current_state.next_state == "GAMEOVER":
            states["GAMEOVER"] = GameOver(states["GAMEPLAY"].score)
            current_state = states["GAMEOVER"]
        elif current_state.next_state == "EXIT":
            handle_quit()
        elif current_state.next_state == "SETTINGS":
            states["SETTINGS"] = Settings()
            current_state = states["SETTINGS"]
        else:
            current_state = states[current_state.next_state]

    # Gérer les événements de sortie
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    current_state.render(screen)
    pygame.display.flip()
    clock.tick(60)
