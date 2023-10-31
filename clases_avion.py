import pygame
import random
import sys
import math

import globales_avion as g


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        self.bullets_count = 1 
        super().__init__()
        self.image = g.PLANE_IMAGE
        self.image = pygame.transform.rotate(self.image, 45)  # Rotar la imagen del avion 45 grados
        self.image = pygame.transform.scale(self.image, (g.PLANE_WIDTH, g.PLANE_HEIGHT))  # Cambiar el tamaño de la imagen si es necesario
        self.rect = self.image.get_rect()
        self.rect.centerx = g.WIDTH // 2
        self.rect.bottom = g.HEIGHT - 20
        self.speed = g.PLANE_SPEED
        self.hp = g.PLANE_HP

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (self.rect.left + g.PLANE_WIDTH/2)> 1:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < g.WIDTH + g.PLANE_WIDTH/2 - g.BULLET_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < g.HEIGHT + g.PLANE_HEIGHT/2:
            self.rect.y += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = g.ENEMY_IMAGE
        self.image = pygame.transform.rotate(self.image, 135)
        self.image = pygame.transform.scale(self.image, (g.PLANE_WIDTH, g.PLANE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, g.WIDTH - g.ENEMY_WIDTH)
        self.rect.y = - g.ENEMY_HEIGHT
        self.hp = g.ENEMY_HP
        self.damage_on_collision = g.ENEMY_DAMAGE_ON_COLLISION

        variation = round(random.gauss(0, g.ENEMY_SIGMA))  # puedes ajustar el segundo argumento para cambiar la desviación
        variation = max(-2, min(variation, 2))  # esto asegura que la variación esté en el rango [-2, 2]

        self.speed = g.ENEMY_SPEED + variation

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > g.HEIGHT:
            self.kill()
    
    def draw_health_bar(self, screen):
        # Define un color para la barra de vida (verde en este caso)
        color = (0, 255, 0)
        
        # Posición y dimensiones de la barra de vida
        pos_x = self.rect.x + 10  # un poco a la derecha del enemigo
        pos_y = self.rect.y - 5  # un poco arriba del enemigo
        width = self.rect.width - 20  # un poco más pequeña que el enemigo
        fill = int(width * (self.hp / g.ENEMY_HP))
        
        # Dibuja la barra de vida "faltante"
        pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, width, 5))
        # Dibuja la barra de vida "actual"
        pygame.draw.rect(screen, color, (pos_x, pos_y, fill, 5))

    def shoot(self, all_sprites, enemy_bullets):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, -90)  # Asume que el enemigo dispara hacia abajo
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)


class Enemylv2(Enemy):  # StrongEnemy hereda de Enemy
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = g.ENEMY_IMAGE_LV2
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (g.ENEMY_LV2_WIDTH, g.ENEMY_LV2_HEIGHT))
        self.hp = g.ENEMY_LV2_HP  # Aumenta la vida del enemigo
    
    def draw_health_bar(self, screen):
        # Define un color para la barra de vida (verde en este caso)
        color = (0, 255, 0)
        
        # Posición y dimensiones de la barra de vida basadas en proporciones del tamaño del sprite
        margin_x = self.rect.width * 0.05  # Un margen del 5% del ancho del sprite
        margin_y = self.rect.height * 0.05  # Un margen del 5% del alto del sprite
        width = self.rect.width - 2 * margin_x  # La barra de vida tendrá un margen a cada lado
        fill = int(width * (self.hp / (3 * g.ENEMY_HP)))  # Usamos 3 * g.ENEMY_HP porque triplicaste la vida de Enemylv2
        
        pos_x = self.rect.x + margin_x
        pos_y = self.rect.y - margin_y - 5  # un poco arriba del enemigo
        
        # Dibuja la barra de vida "faltante"
        pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, width, 5))
        # Dibuja la barra de vida "actual"
        pygame.draw.rect(screen, color, (pos_x, pos_y, fill, 5))



class Bullet(pygame.sprite.Sprite):
    shoot_speed = g.SHOOT_SPEED  # Nuevo atributo para la velocidad de disparo
    def __init__(self, x, y, angle=90):
        super().__init__()
        self.original_image = pygame.Surface((g.BULLET_WIDTH, g.BULLET_HEIGHT))
        self.original_image.fill(g.BULLET_COLOR)
        self.rect = self.original_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        self.damage = g.BULLET_DAMAGE
        self.speed_x = g.BULLET_SPEED * math.cos(math.radians(angle))
        self.speed_y = g.BULLET_SPEED * math.sin(math.radians(angle))
        self.image = self.original_image.copy()

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle + 90)
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
        if self.rect.y < - g.BULLET_HEIGHT or self.rect.y > g.HEIGHT or self.rect.x < 0 or self.rect.x > g.WIDTH:
            self.kill()

    def adjust_bullet_size(self):
        # Aumenta el tamaño de la bala en función de su daño.
        # Por ejemplo, puedes hacer que cada aumento de daño aumente el tamaño de la bala en un 10%
        scale_factor = self.damage / g.BULLET_DAMAGE
        new_width = int(g.BULLET_WIDTH * scale_factor)
        new_height = int(g.BULLET_HEIGHT * scale_factor)
        
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.rect.center)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = g.EXPLOSION_IMAGE  # Asegúrate de tener una imagen de explosión
        self.image = pygame.transform.scale(self.image, (g.PLANE_WIDTH, g.PLANE_HEIGHT))  # Cambia (50, 50) a las dimensiones deseadas
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_count = 0  # Agrega un contador de frames para eliminar la explosión después de un tiempo

    def update(self):
        self.frame_count += 1
        if self.frame_count > 30:  # Ajusta el número según sea necesario
            self.kill()


class SpeedBoostEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = g.SPEEDBOOSTENEMY_IMAGE
        self.image = pygame.transform.scale(self.image, (g.ENEMY_WIDTH, g.ENEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, g.WIDTH - g.ENEMY_WIDTH)
        self.rect.y = - g.ENEMY_HEIGHT

    def update(self):
        self.rect.y += g.ENEMY_SPEED
        if self.rect.y > g.HEIGHT:
            self.kill()


class FireRateBoostEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = g.FIRERATEBOOSTENEMY_IMAGE
        self.image = pygame.transform.scale(self.image, (g.ENEMY_WIDTH, g.ENEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, g.WIDTH - g.ENEMY_WIDTH)
        self.rect.y = - g.ENEMY_HEIGHT

    def update(self):
        self.rect.y += g.ENEMY_SPEED
        if self.rect.y > g.HEIGHT:
            self.kill()


class DamageBoostEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = g.DAMAGEBOOSTENEMY_IMAGE
        self.image = pygame.transform.scale(self.image, (g.ENEMY_WIDTH, g.ENEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, g.WIDTH - g.ENEMY_WIDTH)
        self.rect.y = - g.ENEMY_HEIGHT

    def update(self):
        self.rect.y += g.ENEMY_SPEED
        if self.rect.y > g.HEIGHT:
            self.kill()

    def boost_damage(self):
        g.BULLET_DAMAGE += g.BONUS_BULLET_DAMAGE  # Asegúrate de tener un valor para BONUS_BULLET_DAMAGE en tus globales
