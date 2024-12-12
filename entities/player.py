import pygame
from entities.projectile import Projectile, FireAnimation
import math

player_sprite_paths = {
    'up': 'assets/images/player/player_up.png',
    'down': 'assets/images/player/player_down.png',
    'left': 'assets/images/player/player_left.png',
    'right': 'assets/images/player/player_right.png',
    'upleft': 'assets/images/player/player_upleft.png',
    'upright': 'assets/images/player/player_upright.png',
    'downleft': 'assets/images/player/player_downleft.png',
    'downright': 'assets/images/player/player_downright.png',
}

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Rectangle représentant le joueur
        self.speed = 5  # Vitesse de déplacement
        self.is_dead = False  # Indique si la voiture est morte
        self.sprites = self.load_sprites(player_sprite_paths)
        self.current_sprite = self.sprites['down']  # Sprite initial
        self.direction = 'down'

        # Image de la voiture cassée
        self.dead_sprite = pygame.image.load("assets/images/player/player_break.png").convert_alpha()
        self.dead_sprite = pygame.transform.scale(self.dead_sprite, (60, 60))  # Ajuste la taille si nécessaire

        # Son de l'explosion
        self.dead_sound = pygame.mixer.Sound("assets/sounds/ExploCar.mp3")
        self.dead_sound.set_volume(0.5)  # Ajuste le volume à ton goût

        # Initialiser les projectiles et les animations de feu
        self.projectiles = []  # Liste des projectiles tirés par le joueur
        self.fires = []  # Liste des animations de feu
        self.shoot_cooldown = 0  # Temps de recharge pour le tir (en frames)

        # Animation d'explosion
        self.explosion_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/player/ExploCar{i}.png").convert_alpha(),
                (60, 60)  # Remplacez par la taille souhaitée
            ) for i in range(1, 4)
        ]
        self.explosion_frame = 0  # Pour gérer la progression de l'animation
        self.explosion_timer = 0  # Timer pour changer de sprite

    def load_sprites(self, sprite_paths):
        """Charge les images de sprites à partir des chemins donnés."""
        return {
            direction: pygame.image.load(path).convert_alpha()
            for direction, path in sprite_paths.items()
        }

    def move(self, keys):
        if not self.is_dead:  # Ne pas déplacer la voiture si elle est morte
            dx, dy = 0, 0
            if keys[pygame.K_z]:
                dy -= self.speed
            if keys[pygame.K_s]:
                dy += self.speed
            if keys[pygame.K_q]:
                dx -= self.speed
            if keys[pygame.K_d]:
                dx += self.speed

            self.rect.x += dx
            self.rect.y += dy

            # Déterminer la direction en fonction du mouvement
            directions = {
                (1, -1): 'upright',
                (1, 1): 'downright',
                (-1, -1): 'upleft',
                (-1, 1): 'downleft',
                (1, 0): 'right',
                (-1, 0): 'left',
                (0, 1): 'down',
                (0, -1): 'up'
            }
            self.direction = directions.get((dx // self.speed, dy // self.speed), self.direction)

            # Mettre à jour le sprite courant
            self.current_sprite = self.sprites[self.direction]

    def shoot(self, mouse_pos, sound):
        """Tire un projectile en direction de la souris."""
        if self.shoot_cooldown == 0:
            dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
            angle = math.atan2(dy, dx)

            # Ajouter un projectile
            projectile = Projectile(self.rect.centerx, self.rect.centery, angle)
            self.projectiles.append(projectile)

            # Ajouter une animation de feu
            fire = FireAnimation(self.rect.centerx, self.rect.top)  # Ajuster la position si nécessaire
            self.fires.append(fire)

            # Activer le cooldown
            self.shoot_cooldown = 60 // 2

            # Jouer le son de tir
            sound.play()

    def update_fires(self):
        """Met à jour les animations de feu."""
        for fire in self.fires[:]:  # Itérer sur une copie pour supprimer en toute sécurité
            fire.update()
            if fire.animation_done:
                self.fires.remove(fire)

    def update_projectiles(self):
        """Met à jour les projectiles et les feux."""
        for projectile in self.projectiles[:]:
            projectile.move()
            if (projectile.rect.bottom < 0 or projectile.rect.top > 600 or
                projectile.rect.left > 800 or projectile.rect.right < 0):
                self.projectiles.remove(projectile)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Mettre à jour les feux
        self.update_fires()

    def draw(self, screen):
        """Dessine le sprite actuel, les projectiles et les animations de feu."""
        if self.is_dead:
            if self.explosion_frame < len(self.explosion_sprites):
                # Affiche l'image actuelle de l'explosion
                explosion_sprite = self.explosion_sprites[self.explosion_frame]
                screen.blit(explosion_sprite, (self.rect.x, self.rect.y))

                # Met à jour le timer de l'explosion
                self.explosion_timer += 1
                if self.explosion_timer >= 10:  # Change de frame toutes les 10 frames
                    self.explosion_frame += 1
                    self.explosion_timer = 0
            else:
                # Une fois l'animation terminée, affiche la voiture cassée
                screen.blit(self.dead_sprite, (self.rect.x, self.rect.y))
        else:
            # Dessine la voiture si elle est encore en vie
            screen.blit(self.current_sprite, (self.rect.x, self.rect.y))

        # Dessiner les projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

        # Dessiner les animations de feu
        for fire in self.fires:
            fire.draw(screen)

    def die(self):
        """Méthode appelée quand le joueur meurt."""
        if not self.is_dead:  # Empêche de rejouer l'animation si déjà mort
            self.is_dead = True
            self.dead_sound.play()  # Jouer le son d'explosion
            self.explosion_frame = 0  # Réinitialiser l'animation
            self.explosion_timer = 0