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
        }

        self.sprites = self.load_all_sprites()
        self.current_sprite = self.sprites['default']['down']

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

        self.dead_sound = pygame.mixer.Sound("assets/sounds/ExploCar.mp3")
        self.dead_sound.set_volume(0.5)

    def load_all_sprites(self):
        return {
            bonus: {
                direction: pygame.image.load(path).convert_alpha()
                for direction, path in sprite_paths.items()
            }
            for bonus, sprite_paths in player_sprite_paths.items()
        }

    def move(self, keys, borders=None, map_coords=None, obstacles=None):
        dx, dy = 0, 0
        intended_dx, intended_dy = 0, 0

        if keys[pygame.K_z]:
            dy -= self.speed
            intended_dy -= 1
        if keys[pygame.K_s]:
            dy += self.speed
            intended_dy += 1
        if keys[pygame.K_q]:
            dx -= self.speed
            intended_dx -= 1
        if keys[pygame.K_d]:
            dx += self.speed
            intended_dx += 1

        if dx != 0 and dy != 0:
            diagonal_factor = math.cos(math.pi / 4)
            dx *= diagonal_factor
            dy *= diagonal_factor

        if map_coords:
            map_left, map_top, map_right, map_bottom = map_coords
            if self.rect.left + dx < map_left:
                dx = map_left - self.rect.left
            if self.rect.right + dx > map_right:
                dx = map_right - self.rect.right
            if self.rect.top + dy < map_top:
                dy = map_top - self.rect.top
            if self.rect.bottom + dy > map_bottom:
                dy = map_bottom - self.rect.bottom

        if borders:
            if "right" in borders and dx > 0:
                dx = 0
            if "left" in borders and dx < 0:
                dx = 0
            if "down" in borders and dy > 0:
                dy = 0
            if "up" in borders and dy < 0:
                dy = 0

        # Test de collision avec obstacles
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy

        if obstacles:
            for obs in obstacles:
                if new_rect.colliderect(obs.rect):
                    # Collision détectée, annule le déplacement
                    dx = 0
                    dy = 0
                    break

        self.rect.x += dx
        self.rect.y += dy

        # Direction
        if intended_dx > 0 and intended_dy < 0:
            self.change_direction('upright')
        elif intended_dx > 0 and intended_dy > 0:
            self.change_direction('downright')
        elif intended_dx < 0 and intended_dy < 0:
            self.change_direction('upleft')
        elif intended_dx < 0 and intended_dy > 0:
            self.change_direction('downleft')
        elif intended_dx > 0:
            self.change_direction('right')
        elif intended_dx < 0:
            self.change_direction('left')
        elif intended_dy > 0:
            self.change_direction('down')
        elif intended_dy < 0:
            self.change_direction('up')

    def change_direction(self, direction):
        self.direction = direction
        self.current_sprite = self.sprites[self.active_bonus][self.direction]

    def shoot(self, mouse_pos, sound):
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
        for projectile in self.projectiles[:]:
            projectile.move()
            projectile.life_duration -= 1
            if projectile.life_duration <= 0:
                self.projectiles.remove(projectile)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.update_fires()

    def update_fires(self):
        for fire in self.fires[:]:
            fire.update()
            if fire.animation_done:
                self.fires.remove(fire)

    def draw(self, screen, mouse_pos):
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
        if not self.is_dead:
            self.is_dead = True
            self.dead_sound.play()
            self.explosion_frame = 0
            self.explosion_timer = 0

    def apply_bonus(self, bonus_type):
        self.active_bonus = bonus_type
        if bonus_type == 'speed':
            self.speed = 7
            self.bonus_timers['speed'] = 60*5
        elif bonus_type == 'fire_rate':
            self.default_cooldown = max(10, self.default_cooldown // 2)
            self.bonus_timers['fire_rate'] = 60*5
        self.current_sprite = self.sprites[self.active_bonus][self.direction]

    def reset_speed_bonus(self):
        self.speed = 5

    def reset_fire_rate_bonus(self):
        self.default_cooldown = 30

    def update_bonus(self):
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

        if self.bonus_timers['speed'] > 0:
            self.active_bonus = 'speed'
        elif self.bonus_timers['fire_rate'] > 0:
            self.active_bonus = 'fire_rate'
        else:
            self.active_bonus = 'default'

        self.current_sprite = self.sprites[self.active_bonus][self.direction]
