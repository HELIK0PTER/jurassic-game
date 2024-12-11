import pygame
import sys
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()  # Initialisation des polices
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Jurasic Game")
        self.clock = pygame.time.Clock()
        self.game = Game(self.screen)

    def run_menu(self):
        # Boucle du menu
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True  # Retourne True pour démarrer le jeu
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Retourne False pour quitter

            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)

            # Titre
            title = font.render("Jurasic Game", True, (255, 255, 0))
            title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
            self.screen.blit(title, title_rect)

            # Instructions
            text = font.render("Appuyez sur Entrée pour commencer", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text, text_rect)

            # Quit instruction
            quit_text = font.render("ESC pour quitter", True, (255, 255, 255))
            quit_rect = quit_text.get_rect(center=(self.screen_width // 2, 2 * self.screen_height // 3))
            self.screen.blit(quit_text, quit_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def run_game(self):
        running = True
        while running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mise à jour
            self.game.update()

            # Rendu
            self.screen.fill((0, 0, 0))  # Fond noir
            self.game.render()
            pygame.display.flip()

            # Contrôle du framerate
            self.clock.tick(60)

    def run(self):
        while True:
            # Affiche le menu et attend la décision du joueur
            if self.run_menu():
                # Si le joueur appuie sur Entrée, lance le jeu
                self.run_game()
            else:
                # Si le joueur appuie sur Escape, quitte le jeu
                break

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
    main.run()  # Appelle run() au lieu de run_game() directement