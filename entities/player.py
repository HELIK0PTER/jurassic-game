import pygame
from entities.projectile import Projectile, FireAnimation
import math

player_sprite_paths = {
    'default': {
        'up': 'assets/images/player/player_up.png',
        'down': 'assets/images/player/player_down.png',
        'left': 'assets/images/player/player_left.png',
        'right': 'assets/images/player/player_right.png',
        'upleft': 'assets/images/player/player_upleft.png',
        'upright': 'assets/images/player/player_upright.png',
        'downleft': 'assets/images/player/player_downleft.png',
        'downright': 'assets/images/player/player_downright.png',
    },
    'speed': {
        'up': 'assets/images/player-bonus1/player_up.png',
        'down': 'assets/images/player-bonus1/player_down.png',
        'left': 'assets/images/player-bonus1/player_left.png',
        'right': 'assets/images/player-bonus1/player_right.png',
        'upleft': 'assets/images/player-bonus1/player_upleft.png',
        'upright': 'assets/images/player-bonus1/player_upright.png',
        'downleft': 'assets/images/player-bonus1/player_downleft.png',
        'downright': 'assets/images/player-bonus1/player_downright.png',
    },
    'fire_rate': {
        'up': 'assets/images/player-bonus2/player_up.png',
        'down': 'assets/images/player-bonus2/player_down.png',
        'left': 'assets/images/player-bonus2/player_left.png',
        'right': 'assets/images/player-bonus2/player_right.png',
        'upleft': 'assets/images/player-bonus2/player_upleft.png',
        'upright': 'assets/images/player-bonus2/player_upright.png',
        'downleft': 'assets/images/player-bonus2/player_downleft.png',
        'downright': 'assets/images/player-bonus2/player_downright.png',
    }
}

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Rectangle représentant le joueur
        self.speed = 5  # Vitesse de déplacement
        self.is_dead = False  # Indique si la voiture est morte
        self.sprites = self.load_sprites(player_sprite_paths['default'])

        # Image de la voiture cassée
        self.dead_sprite = pygame.image.load("assets/images/player/player_break.png").convert_alpha()
        self.dead_sprite = pygame.transform.scale(self.dead_sprite, (60, 60))  # Ajuste la taille si nécessaire

        # Son de l'explosion
        self.dead_sound = pygame.mixer.Sound("assets/sounds/ExploCar.mp3")
        self.dead_sound.set_volume(0.5)  # Ajuste le volume à ton goût

        # Initialiser les projectiles et les animations de feu
        self.projectiles = []  # Liste des projectiles tirés par le joueur
        self.fires = []  # Liste des animations de feu
        self.shoot_cooldown = 0  # Compteur de temps de recharge pour le tir (en frames)
        self.default_cooldown = 30
        self.is_dead = False  # Indique si le joueur est mort
        self.active_bonus = 'default'  # Bonus actif (par défaut : aucun)

        # Charger les sprites
        self.sprites = self.load_all_sprites()
        self.current_sprite = self.sprites['default']['down']  # Sprite initial
        self.direction = 'down'

        # Animation d'explosion
        self.explosion_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/player/ExploCar{i}.png").convert_alpha(),
                (60, 60)  # Remplacez par la taille souhaitée
            ) for i in range(1, 4)
        ]
        self.explosion_frame = 0  # Pour gérer la progression de l'animation
        self.explosion_timer = 0  # Timer pour changer de sprite

    def load_all_sprites(self):
        """
        Charge tous les sprites pour les états par défaut, speed et fire_rate.
        """
        return {
            bonus: {
                direction: pygame.image.load(path).convert_alpha()
                for direction, path in sprite_paths.items()
            } for bonus, sprite_paths in player_sprite_paths.items()
        }

    def load_sprites(self, sprite_paths):
        """Charge les images de sprites à partir des chemins donnés."""
        return {
            direction: pygame.image.load(path).convert_alpha()
            for direction, path in sprite_paths.items()
        }

    def move(self, keys):
        """
        Gère le déplacement et la direction.
        """
        dx, dy = 0, 0
        if keys[pygame.K_z]:  # Haut
            dy -= self.speed
        if keys[pygame.K_s]:  # Bas
            dy += self.speed
        if keys[pygame.K_q]:  # Gauche
            dx -= self.speed
        if keys[pygame.K_d]:  # Droite
            dx += self.speed

        # Mise à jour de la position
        self.rect.x += dx
        self.rect.y += dy

        # Déterminer la direction en fonction du mouvement
        if dx > 0 and dy < 0:
            self.direction = 'upright'
        elif dx > 0 and dy > 0:
            self.direction = 'downright'
        elif dx < 0 and dy < 0:
            self.direction = 'upleft'
        elif dx < 0 and dy > 0:
            self.direction = 'downleft'
        elif dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

        # Mettre à jour le sprite courant
        self.current_sprite = self.sprites[self.active_bonus][self.direction]

    def apply_bonus(self, bonus_type):
        """
        Applique un bonus au joueur et change son sprite.
        """
        self.active_bonus = bonus_type
        if bonus_type == 'speed':
            self.speed += 2
        elif bonus_type == 'fire_rate':
            self.shoot_cooldown = max(1, self.shoot_cooldown // 5)

    def reset_bonus(self):
        """
        Réinitialise les bonus et revient au sprite par défaut.
        """
        if self.active_bonus == 'speed':
            self.speed = 5
        elif self.active_bonus == 'fire_rate':
            self.shoot_cooldown = self.default_cooldown
        self.active_bonus = 'default'
        self.current_sprite = self.sprites['default'][self.direction]

    def shoot(self, mouse_pos, sound):
        """
        Tire un projectile en direction de la souris.
        """
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
            self.shoot_cooldown = self.default_cooldown

            # Jouer le son de tir
            sound.play()

    def update_fires(self):
        """
        Met à jour les animations de feu.
        """
        for fire in self.fires[:]:  # Itérer sur une copie pour supprimer en toute sécurité
            fire.update()
            if fire.animation_done:
                self.fires.remove(fire)

    def update_projectiles(self):
        """
        Met à jour les projectiles et les feux.
        """
        for projectile in self.projectiles[:]:  # Itérer sur une copie pour éviter les erreurs de modification
            projectile.move()

            # Décrémenter la durée de vie du projectile
            projectile.life_duration -= 1

            # Supprimer le projectile si sa durée de vie est écoulée
            if projectile.life_duration <= 0:
                self.projectiles.remove(projectile)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Mettre à jour les feux
        self.update_fires()

    def draw(self, screen, mouse_pos):
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

        # Dessiner le curseur
        # self.draw_cursor(screen, mouse_pos)

        # Calcul de l'angle vers la souris
        dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)

        # Rayon pour la pointe du triangle (distance du joueur)
        radius = 50  # Diminuez cette valeur pour rapprocher la pointe

        # Rayon pour la base du triangle
        base_radius = radius - 10  # Déplace légèrement la base en retrait
        base_width = 20  # Réduisez cette valeur pour diminuer la largeur de la base

        # Position de la pointe du triangle (sur le cercle)
        tip_x = self.rect.centerx + math.cos(angle) * radius
        tip_y = self.rect.centery + math.sin(angle) * radius

        # Position du centre de la base (légèrement en retrait)
        base_center_x = self.rect.centerx + math.cos(angle) * base_radius
        base_center_y = self.rect.centery + math.sin(angle) * base_radius

        # Points de la base du triangle
        base_left_x = base_center_x + math.cos(angle + math.pi / 2) * base_width / 2
        base_left_y = base_center_y + math.sin(angle + math.pi / 2) * base_width / 2

        base_right_x = base_center_x + math.cos(angle - math.pi / 2) * base_width / 2
        base_right_y = base_center_y + math.sin(angle - math.pi / 2) * base_width / 2

        # Dessiner le triangle
        pygame.draw.polygon(screen, (255, 0, 0), [
            (tip_x, tip_y),  # Pointe du triangle
            (base_left_x, base_left_y),  # Base gauche
            (base_right_x, base_right_y)  # Base droite
        ])


    def die(self):
        """Méthode appelée quand le joueur meurt."""
        if not self.is_dead:  # Empêche de rejouer l'animation si déjà mort
            self.is_dead = True
            self.dead_sound.play()  # Jouer le son d'explosion
            self.explosion_frame = 0  # Réinitialiser l'animation
            self.explosion_timer = 0

# Correction dans le gameplay (ajouter mouse_pos à l'appel de draw)
def render(self, screen):
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()  # Obtenez la position actuelle de la souris
    self.player.draw(screen, mouse_pos)  # Passez la position de la souris
