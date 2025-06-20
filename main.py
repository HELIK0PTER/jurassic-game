import pygame

from core.events import handle_quit
from core.states.main_menu import MainMenu
from core.states.gameplay import Gameplay
from core.states.gameover import GameOver
from core.states.settings import Settings
from core.states.prompt_name import PromptName
from core.states.leaderboard import Leaderboard

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jurassic Car Attack")
clock = pygame.time.Clock()

# Charger l'image du curseur
cursor_image = pygame.image.load("assets/images/player/crosshair-Photoroom.png")  # Chemin de l'image
cursor_image = pygame.transform.scale(cursor_image, (20, 20))  # Ajuste la taille si nécessaire

# Masquer le curseur par défaut
pygame.mouse.set_visible(False)

# Gestion des états
states = {
    "MAIN_MENU": MainMenu(),
    "GAMEPLAY": Gameplay(),
    "GAMEOVER": GameOver(),
    "SETTINGS": Settings(),
    "PROMPT_NAME": PromptName(),
    "Leaderboard": Leaderboard(),
    }
current_state = states["MAIN_MENU"]
current_state.play_welcome_and_background()

previous_state = "MAIN_MENU"

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
            if previous_state == "GAMEOVER":
                previous_state = "MAIN_MENU"
                current_state.play_welcome_and_background()
        elif current_state.next_state == "GAMEPLAY":
            states["GAMEPLAY"] = Gameplay(states["PROMPT_NAME"].player_name)
            current_state = states["GAMEPLAY"]
            if previous_state == "MAIN_MENU":
                previous_state = "GAMEPLAY"
        elif current_state.next_state == "GAMEOVER":
            states["GAMEOVER"] = GameOver(states["GAMEPLAY"].score, current_state.player_name)
            current_state = states["GAMEOVER"]
            if previous_state == "GAMEPLAY":
                previous_state = "GAMEOVER"
        elif current_state.next_state == "EXIT":
            handle_quit()
        elif current_state.next_state == "SETTINGS":
            states["SETTINGS"] = Settings()
            current_state = states["SETTINGS"]
        elif current_state.next_state == "PROMPT_NAME":
            states["PROMPT_NAME"] = PromptName()
            current_state = states["PROMPT_NAME"]
        elif current_state.next_state == "Leaderboard":
            states["Leaderboard"] = Leaderboard()
            current_state = states["Leaderboard"]
        else:
            current_state = states[current_state.next_state]

    # Gérer les événements de sortie
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    current_state.render(screen)

    # Dessiner le curseur personnalisé
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_image, (mouse_x - cursor_image.get_width() // 2, mouse_y - cursor_image.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

