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

# Chargement des icônes des boutons
icon_trophy = pygame.image.load("assets/images/menu_leaderboard.png")
icon_trophy = pygame.transform.scale(icon_trophy, (80, 80))
icon_trophy_on = pygame.image.load("assets/images/menu_leaderboard_up.png")  # Image animée
icon_trophy_on = pygame.transform.scale(icon_trophy_on, (80, 80))
icon_play = pygame.image.load("assets/images/menu_play.png")
icon_play = pygame.transform.scale(icon_play, (80, 80))
icon_play_on = pygame.image.load("assets/images/menu_play_up.png")  # Image animée
icon_play_on = pygame.transform.scale(icon_play_on, (80, 80))
icon_settings = pygame.image.load("assets/images/menu_settings.png")
icon_settings = pygame.transform.scale(icon_settings, (80, 80))
icon_settings_on = pygame.image.load("assets/images/menu_settings_up.png")  # Image animée
icon_settings_on = pygame.transform.scale(icon_settings_on, (80, 80))
icon_exit = pygame.image.load("assets/images/menu_exit.png")
icon_exit = pygame.transform.scale(icon_exit, (80, 80))
icon_exit_on = pygame.image.load("assets/images/menu_exit_up.png")  # Image animée
icon_exit_on = pygame.transform.scale(icon_exit_on, (80, 80))

class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.current_button = None

        self.play_button = Button(300, 350, 80, 80, icon_play, icon_play_on, "GAMEPLAY")
        self.trophy_button = Button(440, 350, 80, 80, icon_trophy, icon_trophy_on, "TROPHY")
        self.settings_button = Button(300, 450, 80, 80, icon_settings, icon_settings_on, "SETTINGS")
        self.exit_button = Button(440, 450, 80, 80, icon_exit, icon_exit_on, "EXIT")

        self.buttons = [self.play_button, self.trophy_button, self.settings_button, self.exit_button]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:  # Clic
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        button.active = True  # Activer l'animation
                        self.current_button = button
            elif event.type == pygame.MOUSEBUTTONUP :  # Réinitialiser après le clic
                self.current_button.active = False
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        self.next_state = button.get_label()

                if self.current_button is not None:
                    self.current_button.active = False
                    self.current_button = None

    def render(self, screen):
        screen.blit(background, (0, 0))
        screen.blit(jurassic_logo, (WIDTH // 2 - 125, 50))
        for button in self.buttons:
            button.draw()

    def update(self):
        pass

class Button:
    def __init__(self, x, y, width, height, image, image_on, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.image_on = image_on
        self.label = label
        self.active = False

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image_on if self.active else self.image, self.rect)
        pygame.display.update(self.rect)

    def check_collision(self, pos):
        self.active = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def set_active(self, active):
        self.active = active

    def get_label(self):
        return self.label