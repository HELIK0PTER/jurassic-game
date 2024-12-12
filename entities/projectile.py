import pygame
import math


class FireAnimation:
    def __init__(self, x, y):
        # Charger les images du feu
        try:
            self.images = [
                pygame.image.load("assets/images/Feu_tir1.png"),
                pygame.image.load("assets/images/Feu_tir2.png")
            ]
        except pygame.error as e:
            print(f"Erreur de chargement des images du feu : {e}")
            self.images = [pygame.Surface((50, 50)), pygame.Surface((50, 50))]  # Placeholder

        # Redimensionner les images si nécessaire
        self.images = [pygame.transform.scale(img, (50, 50)) for img in self.images]

        # Position initiale du feu (à côté de la voiture)
        self.x = x
        self.y = y

        # Gestion de l'animation
        self.current_image_index = 0
        self.animation_timer = 0
        self.animation_speed = 5  # Durée entre chaque changement d'image
        self.animation_done = False  # Indique si l'animation est terminée

    def update(self):
        # Mettre à jour l'animation si elle n'est pas terminée
        if not self.animation_done:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                # Passer à l'image suivante
                self.current_image_index += 1
                if self.current_image_index >= len(self.images):
                    self.animation_done = True  # L'animation est terminée

    def draw(self, screen):
        # Dessiner le feu si l'animation n'est pas terminée
        if not self.animation_done:
            current_image = self.images[self.current_image_index]
            screen.blit(current_image, (self.x, self.y))


class Projectile:
    def __init__(self, x, y, angle):
        # Charger l'image du projectile
        try:
            self.image = pygame.image.load("assets/images/Projectile.png")
        except pygame.error as e:
            print(f"Erreur de chargement de l'image du projectile : {e}")
            self.image = pygame.Surface((50, 50))  # Placeholder

        # Redimensionner l'image si nécessaire
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Faire une rotation initiale de l'image selon l'angle
        self.image = pygame.transform.rotate(self.image, -math.degrees(angle))

        # Utiliser le rect de l'image pour les coordonnées
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 20
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

        # Gérer la durée de vie d'un projectile
        self.life_duration = 60 * 3  # Durée de vie en frames (1 seconde = 60 frames)

    def move(self):
        # Déplacer le projectile en fonction de sa direction
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen):
        # Dessiner l'image du projectile sur l'écran
        screen.blit(self.image, self.rect)
