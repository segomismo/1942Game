import pygame
import random
import sys
import math

# Configuración de la pantalla
import globales_avion as g

WIDTH, HEIGHT = 1000, 800 # Ajusta el tamaño de la pantalla según sea necesario
FPS = 60 # Ajusta la velocidad del juego según sea necesario
game_start_time = pygame.time.get_ticks()


# Configuración del avión
PLANE_WIDTH = 80 # Ajusta el tamaño del avión según sea necesario
PLANE_HEIGHT = 80 # Ajusta el tamaño del avión según sea necesario
PLANE_HP = 1000.0 # Ajusta la salud del avión según sea necesario


#Barra de vida:
LIFE_BAR_WIDTH = 200
LIFE_BAR_HEIGHT = 20
LIFE_BAR_POS_X = (g.WIDTH - LIFE_BAR_WIDTH) / 2  # Centra la barra de vida en la pantalla
LIFE_BAR_POS_Y = 10  # Una pequeña margen desde el borde superior de la pantalla
LIFE_BAR_COLOR = (0, 255, 0)  # Color verde
LIFE_BAR_BG_COLOR = (255, 0, 0)  # Color rojo para representar la vida perdida


# Configuración de los enemigos
ENEMY_WIDTH = 40 # Ajusta el tamaño de los enemigos según sea necesario
ENEMY_HEIGHT = 40   # Ajusta el tamaño de los enemigos según sea necesario
ENEMY_SIGMA = 1 # Ajusta la desviación estándar de la distribución gaussiana según sea necesario
ENEMY_SPEED = 5 # Ajusta la velocidad de los enemigos según sea necesario
ENEMY_SPAWN_RATE = 25 # Cuanto más alto sea el número, menos enemigos aparecerán
ENEMY_HP = 15.0 # Ajusta la salud de los enemigos según sea necesario
ENEMY_DAMAGE_ON_COLLISION = 10


ENEMY_LV2_MAX_PROB = 0.7 #0.5 es 50% de probabilidad de que aparezca un enemigo de nivel 2
ENEMY_LV2_GROWTH_RATE =  1 / 1000000  # Este valor determina qué tan rápido crece la probabilidad con el tiempo.
ENEMY_LV2_INITIAL_PROB = 0.1 # Probabilidad inicial de que aparezca un enemigo de nivel 2
ENEMY_LV2_HP = 50.0
ENEMY_LV2_WIDTH = 50 # Ajusta el tamaño de los enemigos según sea necesario
ENEMY_LV2_HEIGHT = 50   # Ajusta el tamaño de los enemigos según sea necesario


# Configuración de las balas
BULLET_COLOR = (255,255,0) # Ajusta el color de las balas según sea necesario
BULLET_WIDTH = 2 # Ajusta el tamaño de las balas según sea necesario
BULLET_HEIGHT = 10 # Ajusta el tamaño de las balas según sea necesario
BULLET_SPEED = 10 # Ajusta la velocidad de las balas según sea necesario
BULLET_DAMAGE = 10.0
BULLET_ANGLE_VARIATION = 5 # Ajusta la variación del ángulo de las balas según sea necesario
bullets_count = 1 # Ajusta el número de balas según sea necesario
damage_level = 0 # Ajusta el nivel de daño según sea necesario


SHOOT_SPEED = 200 # Ajusta la velocidad de disparo según sea necesario
PLANE_SPEED = 2 # Ajusta la velocidad del avión según sea necesario


# Bonuses:
BONUS_SHOOT_SPEED = 100 # Ajusta la velocidad de disparo del bonus según sea necesario  
BONUS_PLANE_SPEED = 1 # Ajusta la velocidad del bonus según sea necesario
BONUS_BULLET_DAMAGE = 1.5

RATIO_ESPECIALES = 2 # Ajusta la probabilidad de que aparezcan enemigos especiales según sea necesario (1/RATIO_ESPECIALES)


# Imágenes:
#Avion principal
PLANE_IMAGE = pygame.image.load("imagenes/plane1.png").convert_alpha()
#Fondo del juego:
BACKGROUND_IMAGE = pygame.image.load("imagenes/fondo-des-pantalla-1.png").convert()
#Enemigos:
ENEMY_IMAGE = pygame.image.load("imagenes/enemy1.png").convert_alpha()
ENEMY_IMAGE_LV2 = pygame.image.load("imagenes/enemy2.png").convert_alpha()
SPEEDBOOSTENEMY_IMAGE = pygame.image.load("imagenes/enemy-fire-1.png").convert_alpha()
FIRERATEBOOSTENEMY_IMAGE = pygame.image.load("imagenes/enemy-speed-1.png").convert_alpha()
DAMAGEBOOSTENEMY_IMAGE = pygame.image.load("imagenes/enemy-damage-1.png").convert_alpha()


#Animaciones
EXPLOSION_IMAGE = pygame.image.load("imagenes/explosion1.png").convert_alpha()


#Puntuaciones:
enemies_killed = 0
bullets_shot = 0
special_enemies_killed = 0
score = 0
dies = 0


