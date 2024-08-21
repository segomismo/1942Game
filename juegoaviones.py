import pygame
import random
import sys
import math


pygame.init()

WIDTH, HEIGHT = 1000, 800 # Ajusta el tamaño de la pantalla según sea necesario

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1942")

import globales_avion as g
import clases_avion as c
import inicializaciones_avion as i


def adjust_bullet_damage(bullet):
    if g.damage_level >= 1 and bullet.angle == 90:
        bullet.damage *= g.BONUS_BULLET_DAMAGE

    for level in range(1, g.damage_level):
        offset = 5 * level
        if bullet.angle == 90 - offset or bullet.angle == 90 + offset:
            bullet.damage *= g.BONUS_BULLET_DAMAGE * (g.damage_level - level)
    
    bullet.adjust_bullet_size()  # Ajusta el tamaño de la bala según su daño


def handle_input(plane, all_sprites, bullets, last_shot_time):
    keys = pygame.key.get_pressed()  
    current_time = pygame.time.get_ticks()  

    # Disparar
    if keys[pygame.K_SPACE] and current_time - last_shot_time > c.Bullet.shoot_speed:
        last_shot_time = current_time

        # Genera ángulos alternando entre izquierda y derecha
        angles = [90]
        for i in range(1, g.bullets_count):
            offset = (i + 1) // 2 * 5  # Cada paso es de 5 grados
            if i % 2 == 0:  # Si es par, se desplaza a la izquierda
                angles.insert(0, 90 - offset)  
            else:  # Si es impar, se desplaza a la derecha
                angles.append(90 + offset)

        # Aquí determinamos el daño basado en el nivel de mejora        
        for angle in angles:
            bullet = c.Bullet(plane.rect.centerx, plane.rect.top, angle)
            adjust_bullet_damage(bullet)  # Ajusta el daño de la bala según su ángulo y el nivel de poder
            
            # Rotamos la imagen de la bala según su ángulo de disparo
            bullet.image = pygame.transform.rotate(bullet.original_image, -angle + 90)
            all_sprites.add(bullet)
            bullets.add(bullet) 

    return last_shot_time


def handle_collisions(enemies, special_enemies, bullets, all_sprites, score, plane):
    hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
    hits_plane = pygame.sprite.spritecollide(plane, enemies, True)  # El 'True' significa que el enemigo será eliminado al colisionar

    for hit in hits_plane:
        plane.hp -= hit.damage_on_collision
        if plane.hp <= 0:
            # Aquí puedes manejar la lógica cuando el avión del jugador es destruido, como mostrar una animación de explosión y terminar el juego.
            explosion = c.Explosion(plane.rect.centerx, plane.rect.centery)
            all_sprites.add(explosion)
            plane.kill()  # Elimina el avión del jugador

    for hit in hits:
        for bullet in hits[hit]:
            hit.hp -= bullet.damage
            if hit.hp <= 0:
                score += 1 
                hit.kill()  # Mata al enemigo si su vida llega a 0
                explosion = c.Explosion(hit.rect.centerx, hit.rect.centery)  
                all_sprites.add(explosion) 
    
    special_hits = pygame.sprite.groupcollide(special_enemies, bullets, True, True)
    for hit in special_hits:
        explosion = c.Explosion(hit.rect.centerx, hit.rect.centery)  
        all_sprites.add(explosion)  

        if isinstance(hit, c.SpeedBoostEnemy):
            plane.speed += g.BONUS_PLANE_SPEED  # Aumenta la velocidad del avión  
        elif isinstance(hit, c.FireRateBoostEnemy):
            c.Bullet.shoot_speed = max(100, c.Bullet.shoot_speed - g.BONUS_SHOOT_SPEED)  # Aumenta la velocidad de disparo
            if c.Bullet.shoot_speed == 100:  # Si llega a 100
                g.bullets_count += 1  # Aumenta el conteo de balas
                c.Bullet.shoot_speed = g.SHOOT_SPEED  # Restablece la velocidad de disparo
        elif isinstance(hit, c.DamageBoostEnemy):
            g.damage_level += 1

    return score


def update_display(screen, background, y_background, all_sprites, score, plane, enemies):  # Añade 'plane' como un parámetro
    rect = pygame.Rect(0, y_background, WIDTH, HEIGHT)
    screen.blit(background, (0, 0), rect)
    all_sprites.update()
    all_sprites.draw(screen)

    for enemy in enemies:  # Asumiendo que 'enemies' es tu grupo de sprites de enemigos
        enemy.draw_health_bar(screen)
    
    font = pygame.font.Font(None, 36)  
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))  
    screen.blit(score_text, (10, 10))

    # Añade estos bloques para mostrar la velocidad del avión y la velocidad de disparo
    plane_speed_text = font.render(f'Plane Speed: {plane.speed}', True, (255, 255, 255))
    screen.blit(plane_speed_text, (10, 40))  # Ajusta las coordenadas según sea necesario
    shoot_speed_text = font.render(f'Shoot Speed: {c.Bullet.shoot_speed}', True, (255, 255, 255))
    screen.blit(shoot_speed_text, (10, 70))  # Ajusta las coordenadas según sea necesario
    pygame.display.flip()


def spawn_enemy(all_sprites, enemies, special_enemies):
    elapsed_time = pygame.time.get_ticks() - g.game_start_time
    strong_enemy_probability = min(g.ENEMY_LV2_INITIAL_PROB + elapsed_time * g.ENEMY_LV2_GROWTH_RATE, g.ENEMY_LV2_MAX_PROB)

    if random.random() < strong_enemy_probability:
        # Suponiendo que c.Enemylv2() es tu enemigo más fuerte
        enemy = c.Enemylv2()
        all_sprites.add(enemy)
        enemies.add(enemy)
        return

    rand_num = random.randint(1, g.RATIO_ESPECIALES)
    if rand_num == g.RATIO_ESPECIALES:
        chosen_enemy = random.choice([c.SpeedBoostEnemy, c.FireRateBoostEnemy, c.DamageBoostEnemy])
        special_enemy = chosen_enemy()
        all_sprites.add(special_enemy)
        special_enemies.add(special_enemy)
    else:
        enemy = c.Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)


def initialize_sprites():
    plane = c.Plane()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    special_enemies = pygame.sprite.Group()  # Añade esta línea
    all_sprites = pygame.sprite.Group()
    all_sprites.add(plane)
    return plane, enemies, bullets, special_enemies, all_sprites  # Añade special_enemies a la lista de retorno


def main():
    background = g.BACKGROUND_IMAGE
    bg_width, bg_height = background.get_size()
    y_background = bg_height - HEIGHT
    plane, enemies, bullets, special_enemies, all_sprites = initialize_sprites()
    clock = pygame.time.Clock()
    last_shot_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        last_shot_time = handle_input(plane, all_sprites, bullets, last_shot_time)

        # La siguiente línea maneja tanto el spawn de enemigos normales como especiales
        if random.randint(1, g.ENEMY_SPAWN_RATE) == 1: 
            spawn_enemy(all_sprites, enemies, special_enemies)  
        
        g.score = handle_collisions(enemies, special_enemies, bullets, all_sprites, g.score, plane)
        y_background -= 1  

        if y_background == 0:  
            y_background = bg_height - HEIGHT  

        update_display(screen, background, y_background, all_sprites, g.score, plane, enemies)
        clock.tick(g.FPS)


if __name__ == "__main__":
    main()