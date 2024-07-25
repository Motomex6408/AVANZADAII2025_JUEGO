import pygame
import random
import math
import sys
import os

# Inicializar el game
pygame.init()

# Establecer el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Función para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar imagen de fondo
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

# Cargar icono de ventana
asset_icon = resource_path('assets/images/icon.png')
icon = pygame.image.load(asset_icon)

# Cargar sonido de fondo
asset_sound = resource_path('assets/audios/background_music2.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

#  Cargar sonido de disparo
asset_blast = resource_path('assets/audios/blast.mp3')
blast_sound = pygame.mixer.Sound(asset_blast)

# Cargar imagen del jugador
asset_playerimg = resource_path('assets/images/Nave.png')
playerimg = pygame.image.load(asset_playerimg)

# Cargar imagen del jugador 2
asset_playerimg2 = resource_path('assets/images/Nave2.png')
playerimg2 = pygame.image.load(asset_playerimg2)

# Cargar imagen de la bala enemiga
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# Cargar imagen de la bala aliada
asset_bulletimg2 = resource_path('assets/images/bullet2.jpg')
bulletimg2 = pygame.image.load(asset_bulletimg2)

# Cargar fuente para texto de game over
asset_over_font = resource_path('assets/fonts/StarJediHollow-A4lL.ttf')
over_font = pygame.font.Font(asset_over_font, 40)

# Cargar fuente para texto de puntaje
asset_font = resource_path('assets/fonts/StarJediHollow-A4lL.ttf')
font = pygame.font.Font(asset_font, 32)

# Establecer el título de la ventana
pygame.display.set_caption("The Last One Of Them")

# Establecer el icono de la ventana
pygame.display.set_icon(icon)

# Reproducir sonido de fondo en loop
pygame.mixer.music.play(-1)

# Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Posición inicial del jugador
playerX = 370
playerY = 470
playerx_change = 0

# Lista para almacenar posiciones de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

# Se inicializan las variables para guardar las posiciones de los enemigos
for i in range(no_of_enemies):
    # Se cargan las imágenes de los enemigos
    enemy1 = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))
    enemy2 = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))
    enemy3 = resource_path('assets/images/enemy3.png')
    enemyimg.append(pygame.image.load(enemy3))

    # Se asigna una posición aleatoria en x y en y para el enemigo
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))

    # Se establece la velocidad de movimiento del enemigo en X y en Y
    enemyX_change.append(5)
    enemyY_change.append(20)

# Se inicializan las variables para guardar la posición de la bala
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Se inicializa la puntuación en 0
score = 0

# Función para mostrar la puntuación en la pantalla
def show_score():
    score_value = font.render("SCORE : " + str(score), True, (255, 255, 0))
    screen.blit(score_value, (10, 10))

# Función para dibujar el jugador en la pantalla 
def player(x, y):
    screen.blit(playerimg, (x, y))

# Función para dibujar el enemigo en la pantalla
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Función para disparar la bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    blast_sound.play()
    screen.blit(bulletimg2, (x + 16, y + 10))

# Función para verificar si hubo colisión entre la bala y el enemigo
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Función para mostrar el texto de game over
def game_over_text():
    lines = [
        "El Jedi defensor ha caído",
        "El lado oscuro triunfó",
        "La galaxia sigue esperando",
        "Una Nueva esperanza."
    ]
    y_offset = 0  # Desplazamiento inicial en y

    for line in lines:
        over_text = over_font.render(line, True, (255, 255, 0))
        text_rect = over_text.get_rect(center=(screen_width // 2, (screen_height // 2) + y_offset))
        screen.blit(over_text, text_rect)
        y_offset += 40  # Aumenta el desplazamiento en Y para la siguiente línea

#Funcion para introduccion del juego
def game_introduction():
    lines = [
        "Es periodo de conflicto",
        "La galaxia ha sido atacada",
        "Palpatine ha ejecutado la orden 66",
        " ",
        
    ]
    
# Función principal del juego
def gameloop():
    global score, playerX, playerx_change, bulletX, bulletY, bullet_state
    in_game = True
    while in_game:
        # Limpiar la pantalla
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Maneja la movilidad del jugador y la bala
                if event.key == pygame.K_LEFT:
                    playerx_change = -5

                if event.key == pygame.K_RIGHT:
                    playerx_change = 5

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerx_change = 0

        # Aca se actualiza la posicion del jugador
        playerX += playerx_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Bucle que se ejecuta para cada enemigo
        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            # Aca se verifica si hay colision entre el enemigo y la bala   
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY < 0:
            bulletY = 454
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score()

        pygame.display.update()
        clock.tick(120)

gameloop()
