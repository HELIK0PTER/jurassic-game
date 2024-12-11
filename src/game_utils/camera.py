import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scroll_margin = 100
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def should_move(self, player_rect, screen_width, screen_height):
        """Détermine dans quelles directions la caméra doit bouger:
            conditions :
                - le joueur est à moins de scroll_margin pixels du bord de l'écran
                - la touche du bord correspondant est activée
        """

        self.moving_left = (player_rect.left <= self.scroll_margin) & pygame.key.get_pressed()[pygame.K_LEFT]
        self.moving_right = (player_rect.right >= screen_width - self.scroll_margin) & pygame.key.get_pressed()[pygame.K_RIGHT]
        self.moving_up = (player_rect.top <= self.scroll_margin) & pygame.key.get_pressed()[pygame.K_UP]
        self.moving_down = (player_rect.bottom >= screen_height - self.scroll_margin) & pygame.key.get_pressed()[pygame.K_DOWN]

        return (self.moving_left, self.moving_right,
                self.moving_up, self.moving_down)

    def move_world(self, speed):
        """Déplace la caméra (et donc le monde) selon les directions actives"""
        if self.moving_left:
            self.x -= speed
        if self.moving_right:
            self.x += speed
        if self.moving_up:
            self.y -= speed
        if self.moving_down:
            self.y += speed