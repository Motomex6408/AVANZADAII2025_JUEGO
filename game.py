import pygame
import random
import math
import sys
import os
import time

# Inicializar el juego
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

# Cargar imagen del titulo principal
asset_title = resource_path('assets/images/titulo_principal.jpeg')
title = pygame.image.load(asset_title)

# Cargar imagen de seleccion de personajes
asset_seleccion = resource_path('assets/images/selección_de_personajes.jpeg')
seleccion = pygame.image.load(asset_seleccion)

# Cargar icono de ventana
asset_icon = resource_path('assets/images/icon.png')
icon = pygame.image.load(asset_icon)

# Cargar sonido de fondo
asset_sound = resource_path('assets/audios/background_music2.mp3')
pygame.mixer.music.load(asset_sound)

# Cargar sonido de bala
asset_blast = resource_path('assets/audios/blast.mp3')
blast_sound = pygame.mixer.Sound(asset_blast)

# Cargar sonido de bala
asset_explosion = resource_path('assets/audios/explosion.mp3')
explosion_sound = pygame.mixer.Sound(asset_explosion)

# Cargar imagen del jugador
asset_playerimg1 = resource_path('assets/images/Nave.png')
playerimg1 = pygame.image.load(asset_playerimg1)

# Cargar personaje del personaje Weddom
asset_playercharacter1 = resource_path('assets/images/Aldaris.png')
playercharacter1 = pygame.image.load(asset_playercharacter1)

# Cargar personaje de la personaje Star
asset_playercharacter2 = resource_path('assets/images/Star.png')
playercharacter2 = pygame.image.load(asset_playercharacter2)

# Imagen del jugador 2 (si tienes un segundo jugador)
asset_playerimg2 = resource_path('assets/images/nave2.png')
playerimg2 = pygame.image.load(asset_playerimg2)

# Cargar imagen de la bala del jugador
asset_bulletimg2 = resource_path('assets/images/bullet2.jpg')
bulletimg2 = pygame.image.load(asset_bulletimg2)

# Cargar imagen de la bala del enemigo
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# Cargar fuente para texto de game over
asset_over_font = resource_path('assets/fonts/StarJedi-DGRW.ttf')
over_font = pygame.font.Font(asset_over_font, 40)

# Cargar fuente para texto de puntaje
asset_font = resource_path('assets/fonts/StarJedi-DGRW.ttf')
font = pygame.font.Font(asset_font, 32)

# Cargar imágenes de explosión
asset_explosion = resource_path('assets/images/explosion.png')
explosion_img = pygame.image.load(asset_explosion)

# Establecer el título de la ventana
pygame.display.set_caption("Last One of Them")

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
enemy_bulletX = []
enemy_bulletY = []
enemy_bulletY_change = []
enemy_bullet_state = []
enemy_last_shot_time = []
enemy_shot_interval = []
no_of_enemies = 6

# Se inicializan las variables para guardar las posiciones de los enemigos
for i in range(no_of_enemies):
    enemy1 = resource_path('assets/images/enemy1.png')
    enemy2 = resource_path('assets/images/enemy2.png')
    enemy3 = resource_path('assets/images/enemy3.png')

    # Alternar entre las imágenes de los enemigos
    if i % 3 == 0:
        enemyimg.append(pygame.image.load(enemy1))
    elif i % 3 == 1:
        enemyimg.append(pygame.image.load(enemy2))
    else:
        enemyimg.append(pygame.image.load(enemy3))

    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(7)  # Aumentar la velocidad del enemigo
    enemyY_change.append(20)
    enemy_bulletX.append(enemyX[i])
    enemy_bulletY.append(enemyY[i])
    enemy_bulletY_change.append(8)
    enemy_bullet_state.append("ready")
    enemy_last_shot_time.append(time.time())
    enemy_shot_interval.append(random.uniform(2, 5))

# Se inicializan las variables para guardar la posición de la bala
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 13
bullet_state = "ready"

# Se inicializa la puntuación en 0
score = 0

# Variable global para la imagen del jugador
playerimg = playerimg1

# Función para mostrar la puntuación en la pantalla
def show_score():
    score_value = font.render("PTS : " + str(score), True, (255, 255, 0))
    screen.blit(score_value, (10, 10))

# Función para dibujar el jugador en la pantalla 
def player(x, y):
    screen.blit(playerimg, (x, y))

# Función para dibujar el enemigo en la pantalla
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Función para disparar la bala del jugador
def fire_bullet(x, y):
    global bullet_state
    blast_sound.play()
    bullet_state = "fire"
    screen.blit(bulletimg2, (x + 16, y + 10))

# Función para disparar la bala del enemigo
def fire_enemy_bullet(x, y, i):
    global enemy_bullet_state
    enemy_bulletX[i] = x  # Asegurarse de que la bala aparezca desde la posición actual del enemigo
    enemy_bullet_state[i] = "fire"
    blast_sound.play()
    screen.blit(bulletimg, (x + 16, y + 10))

# Función para verificar si hubo colisión entre la bala y el enemigo
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Función para verificar si hubo colisión entre la bala enemiga y el jugador
def isPlayerHit(playerX, playerY, bulletX, bulletY):
    distance = math.sqrt((math.pow(playerX - bulletX, 2)) + (math.pow(playerY - bulletY, 2)))
    return distance < 27

# Función para mostrar el texto de game over
def game_over_text():
    lines = [
        "El Jedi defensor ha caído",
        "El lado oscuro triunfó.",
        "La galaxia sigue esperando",
        "una nueva esperanza"
    ]
    y_offset = 0  # Desplazamiento inicial en y

    for line in lines:
        over_text = over_font.render(line, True, (255, 255, 0))
        text_rect = over_text.get_rect(center=(screen_width // 2, (screen_height // 2) + y_offset))
        screen.blit(over_text, text_rect)
        y_offset += 40  # Aumenta el desplazamiento en y para la siguiente línea

# Función del menú principal
def game_start():
    menu = True
    while menu:
        screen.fill((0, 0, 0))
        screen.blit(title, (0, 0))

        start_font = pygame.font.Font(asset_font, 32)
        start_text = start_font.render("ENTER para empezar", True, (0,0,0))
        start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_text, start_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    character_selection()

        pygame.display.update()
        clock.tick(15)

# Función para la selección de personajes
def character_selection():
    selected = 0
    select = True
    
    # Variable para el nombre del personaje
    while select:
        screen.fill((0, 0, 0))
        screen.blit(seleccion, (0, 0))
        
        title_font = pygame.font.Font(asset_font, 64)
        title_text = title_font.render("Elige tu personaje", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect)

        ships = [playercharacter1, playercharacter2]
        ship_names = ["Weddom", "Star"]

        for i, ship in enumerate(ships):
            x_pos = screen_width // 2 + (i - 1) * 200
            y_pos = screen_height // 2

            if i == selected:
                border_color = (0, 0, 255)
                name_color = (0, 0, 255)
            else:
                border_color = (255, 255, 255)
                name_color = (255, 255, 255)

            # Rectángulo del borde alrededor de la imagen seleccionada
            border_rect = ship.get_rect(center=(x_pos, y_pos))
            pygame.draw.rect(screen, border_color, border_rect.inflate(20, 20), 3)

            # Imagen del personaje
            screen.blit(ship, border_rect)

            # Nombre del personaje
            name_font = pygame.font.Font(asset_font, 32)
            name_text = name_font.render(ship_names[i], True, name_color)
            name_rect = name_text.get_rect(center=(x_pos, y_pos + 70))
            screen.blit(name_text, name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(ships)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(ships)
                elif event.key == pygame.K_RETURN:
                    select = False

        pygame.display.update()
        clock.tick(15)
    
    global playerimg
    playerimg = playerimg1 if selected == 0 else playerimg2

# Variables para la explosión
explosion_image = pygame.image.load(asset_explosion)
explosion_visible = False
explosion_x = 0
explosion_y = 0
EXPLOSION_DURATION = 500  # Duración de la explosión en milisegundos
explosion_timer = 0

# Bucle principal del juego
game_start()
running = True
while running:
    # Color de fondo
    screen.fill((0, 0, 0))

    # Fondo del juego
    screen.blit(background, (0, 0))

    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -7
            if event.key == pygame.K_RIGHT:
                playerx_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerX += playerx_change

    # Limitar el movimiento del jugador dentro de los bordes de la pantalla
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimiento del enemigo
    for i in range(no_of_enemies):
        # Fin del juego
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]

        # Disparar balas enemigas con intervalos aleatorios
        current_time = time.time()
        if current_time - enemy_last_shot_time[i] > enemy_shot_interval[i]:
            fire_enemy_bullet(enemyX[i], enemyY[i], i)
            enemy_last_shot_time[i] = current_time
            enemy_shot_interval[i] = random.uniform(2, 5)  # Ajustar el intervalo

        # Movimiento de la bala enemiga
        if enemy_bullet_state[i] == "fire":
            screen.blit(bulletimg, (enemy_bulletX[i], enemy_bulletY[i]))
            enemy_bulletY[i] += enemy_bulletY_change[i]

        # Resetear la bala enemiga si sale de la pantalla
        if enemy_bulletY[i] >= screen_height:
            enemy_bulletY[i] = enemyY[i]
            enemy_bullet_state[i] = "ready"

        # Verificar si el jugador fue golpeado
        if isPlayerHit(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i]):
            explosion_x = playerX
            explosion_y = playerY
            explosion_visible = True
            explosion_timer = pygame.time.get_ticks()  # Guarda el tiempo actual
            explosion_sound.play()  # Reproducir el sonido de explosión

            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            running = False
            break

        # Colisión entre bala y enemigo
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Mostrar explosión
            explosion_x = enemyX[i]
            explosion_y = enemyY[i]
            explosion_visible = True
            explosion_timer = pygame.time.get_ticks()  # Guarda el tiempo actual
            explosion_sound.play()  # Reproducir el sonido de explosión

            # Resetear la bala y actualizar la puntuación
            bulletY = 480
            bullet_state = "ready"
            score += 1

            # Reiniciar la posición del enemigo
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Dibujar el enemigo
        enemy(enemyX[i], enemyY[i], i)

    # Movimiento de la bala del jugador
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score()

    # Mostrar la explosión si es necesario
    if explosion_visible:
        screen.blit(explosion_image, (explosion_x, explosion_y))
        if pygame.time.get_ticks() - explosion_timer > EXPLOSION_DURATION:
            explosion_visible = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
