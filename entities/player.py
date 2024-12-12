import pygame
import math
from entities.projectile import Projectile, FireAnimation

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
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5
        self.projectiles = []
        self.fires = []
        self.shoot_cooldown = 0
        self.default_cooldown = 30
        self.is_dead = False
        self.direction = 'down'
        self.active_bonus = 'default'
        self.speed_bonus = False
        self.fire_rate_bonus = False
        self.bonus_timers = {
            'speed': 0,
            'fire_rate': 0
        }  # Timers pour chaque bonus


        # Chargement des sprites
        self.sprites = self.load_all_sprites()
        self.current_sprite = self.sprites['default']['down']

        # Sprite de voiture cassée et animation d'explosion
        self.dead_sprite = pygame.image.load("assets/images/player/player_break.png").convert_alpha()
        self.dead_sprite = pygame.transform.scale(self.dead_sprite, (60, 60))
        self.explosion_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/player/ExploCar{i}.png").convert_alpha(),
                (60, 60)
            ) for i in range(1, 4)
        ]
        self.explosion_frame = 0
        self.explosion_timer = 0

        # Son d'explosion
        self.dead_sound = pygame.mixer.Sound("assets/sounds/ExploCar.mp3")
        self.dead_sound.set_volume(0.5)

    def load_all_sprites(self):
        """Charge tous les sprites pour chaque bonus."""
        return {
            bonus: {
                direction: pygame.image.load(path).convert_alpha()
                for direction, path in sprite_paths.items()
            }
            for bonus, sprite_paths in player_sprite_paths.items()
        }

    def move(self, keys):
        """Gère le déplacement et la direction."""
        dx, dy = 0, 0
        if keys[pygame.K_z]:  # Haut
            dy -= self.speed
        if keys[pygame.K_s]:  # Bas
            dy += self.speed
        if keys[pygame.K_q]:  # Gauche
            dx -= self.speed
        if keys[pygame.K_d]:  # Droite
            dx += self.speed

        self.rect.x += dx
        self.rect.y += dy

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

        self.current_sprite = self.sprites[self.active_bonus][self.direction]

    def shoot(self, mouse_pos, sound):
        """Tire un projectile en direction de la souris."""
        if self.shoot_cooldown == 0:
            dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
            angle = math.atan2(dy, dx)

            projectile = Projectile(self.rect.centerx, self.rect.centery, angle)
            self.projectiles.append(projectile)

            fire = FireAnimation(self.rect.centerx, self.rect.top)
            self.fires.append(fire)

            self.shoot_cooldown = self.default_cooldown
            sound.play()

    def update_projectiles(self):
        """Met à jour les projectiles et les animations de feu."""
        for projectile in self.projectiles[:]:
            projectile.move()
            projectile.life_duration -= 1
            if projectile.life_duration <= 0:
                self.projectiles.remove(projectile)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.update_fires()

    def update_fires(self):
        """Met à jour les animations de feu."""
        for fire in self.fires[:]:
            fire.update()
            if fire.animation_done:
                self.fires.remove(fire)

    def draw(self, screen, mouse_pos):
        """Dessine le joueur, les projectiles, et les animations."""
        if self.is_dead:
            if self.explosion_frame < len(self.explosion_sprites):
                screen.blit(self.explosion_sprites[self.explosion_frame], (self.rect.x, self.rect.y))
                self.explosion_timer += 1
                if self.explosion_timer >= 10:
                    self.explosion_frame += 1
                    self.explosion_timer = 0
            else:
                screen.blit(self.dead_sprite, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.current_sprite, (self.rect.x, self.rect.y))
        for projectile in self.projectiles:
            projectile.draw(screen)
        for fire in self.fires:
            fire.draw(screen)

    def die(self):
        """Déclenche la mort du joueur."""
        if not self.is_dead:
            self.is_dead = True
            self.dead_sound.play()
            self.explosion_frame = 0
            self.explosion_timer = 0

    def apply_bonus(self, bonus_type):
        """
        Applique un bonus au joueur et met à jour ses caractéristiques.
        """
        self.active_bonus = bonus_type  # Change le bonus actif pour changer le sprite
        if bonus_type == 'speed':
            self.speed = 7
            self.bonus_timers['speed'] = 60*5  # Durée de 5 secondes
        elif bonus_type == 'fire_rate':
            self.default_cooldown = max(10, self.default_cooldown // 2)
            self.bonus_timers['fire_rate'] = 60*5  # Durée de 5 secondes

        # Mettre à jour le sprite actuel
        self.active_bonus = bonus_type
        self.current_sprite = self.sprites[self.active_bonus][self.direction]

    def reset_speed_bonus(self):
        """Réinitialise le bonus de vitesse."""
        self.speed = 5

    def reset_fire_rate_bonus(self):
        """Réinitialise le bonus de cadence de tir."""
        self.default_cooldown = 30

    def update_bonus(self):
        """
        Vérifie si les bonus doivent être réinitialisés.
        """
        # Réduction des timers
        if self.bonus_timers['speed'] > 0:
            self.bonus_timers['speed'] -= 1
        else:
            self.reset_speed_bonus()
            self.bonus_timers['speed'] = 0

        if self.bonus_timers['fire_rate'] > 0:
            self.bonus_timers['fire_rate'] -= 1
        else:
            self.reset_fire_rate_bonus()
            self.bonus_timers['fire_rate'] = 0

        # Détermine le sprite en fonction des bonus actifs
        if self.bonus_timers['speed'] > 0:
            self.active_bonus = 'speed'
        elif self.bonus_timers['fire_rate'] > 0:
            self.active_bonus = 'fire_rate'
        else:
            self.active_bonus = 'default'

        # Mettre à jour le sprite actuel
        self.current_sprite = self.sprites[self.active_bonus][self.direction]
