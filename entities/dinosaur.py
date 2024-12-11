import pygame
import random

class Dinosaur:
    def __init__(self):
        self.image = pygame.image.load("assets/images/dino1.png")  # Image du dinosaure
        self.rect = self.image.get_rect()
        self.random_spawn()  # Position aléatoire
        self.speed = 2  # Vitesse de déplacement
        self.health = 100  # Santé actuelle
        self.max_health = 100  # Santé maximale

    def random_spawn(self):
        """
        Positionne le dinosaure à une position aléatoire en dehors de l'écran.
        """
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.rect.x = -self.rect.width - 10
            self.rect.y = random.randint(0, 600)
        elif side == "right":
            self.rect.x = 800 + 10
            self.rect.y = random.randint(0, 600)
        elif side == "top":
            self.rect.x = random.randint(0, 800)
            self.rect.y = -self.rect.height - 10
        elif side == "bottom":
            self.rect.x = random.randint(0, 800)
            self.rect.y = 600 + 10

    def move_towards_player(self, player_rect):
        """
        Déplace le dinosaure vers le joueur.
        """
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed

    def take_damage(self, amount):
        """
        Inflige des dégâts au dinosaure. Retourne True si le dinosaure est détruit.
        """
        self.health -= amount
        if self.health <= 0:
            return True  # Indique que le dinosaure est mort
        return False

    def draw(self, screen):
        """
        Dessine le dinosaure et sa barre de santé.
        """
        # Afficher l'image du dinosaure
        screen.blit(self.image, self.rect)

        # Dessiner la barre de santé
        health_bar_width = 50
        health_ratio = self.health / self.max_health
        # Barre verte (santé restante)
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))
        # Barre rouge (santé perdue)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x + health_bar_width * health_ratio, self.rect.y - 10, health_bar_width * (1 - health_ratio), 5))
