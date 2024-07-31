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

# Cargar imágenes y sonidos
def load_assets():
    global background, title, seleccion, icon, blast_sound, explosion_sound
    global mala_salud, media_salud, salud, playerimg1, playercharacter1, playercharacter2
    global playerimg2, bulletimg2, bulletimg, explosion_img, over_font, font

    background = pygame.image.load(resource_path('assets/images/background.png'))
    title = pygame.image.load(resource_path('assets/images/titulo_principal.jpeg'))
    seleccion = pygame.image.load(resource_path('assets/images/selección_de_personajes.jpeg'))
    icon = pygame.image.load(resource_path('assets/images/icon.png'))
    
    pygame.mixer.music.load(resource_path('assets/audios/background_music2.mp3'))
    blast_sound = pygame.mixer.Sound(resource_path('assets/audios/blast.mp3'))
    explosion_sound = pygame.mixer.Sound(resource_path('assets/audios/explosion.mp3'))
    
    mala_salud = pygame.image.load(resource_path('assets/images/mala_salud.png'))
    media_salud = pygame.image.load(resource_path('assets/images/media_salud.png'))
    salud = pygame.image.load(resource_path('assets/images/salud.png'))
    
    playerimg1 = pygame.image.load(resource_path('assets/images/Nave.png'))
    playercharacter1 = pygame.image.load(resource_path('assets/images/Aldaris.png'))
    playercharacter2 = pygame.image.load(resource_path('assets/images/Star.png'))
    playerimg2 = pygame.image.load(resource_path('assets/images/nave2.png'))
    
    bulletimg2 = pygame.image.load(resource_path('assets/images/bullet2.jpg'))
    bulletimg = pygame.image.load(resource_path('assets/images/bullet.png'))
    
    explosion_img = pygame.image.load(resource_path('assets/images/explosion.png'))
    
    over_font = pygame.font.Font(resource_path('assets/fonts/StarJedi-DGRW.ttf'), 40)
    font = pygame.font.Font(resource_path('assets/fonts/StarJedi-DGRW.ttf'), 32)

# Cargar recursos antes de cualquier otra cosa
load_assets()

# Establecer el título de la ventana y el icono
pygame.display.set_caption("Last One of Them")
pygame.display.set_icon(icon)

# Reproducir sonido de fondo en loop
pygame.mixer.music.play(-1)

# Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Variables globales
playerX = 0
playerY = 0
playerx_change = 0
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
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 0
bullet_state = "ready"
score = 0
vidas_jugador = 3
playerimg = None

# Lista de explosiones activas
explosions = []
explosion_duration = 0.5  # Duración de la explosión en segundos

# Función para inicializar o reiniciar las variables del juego
def initialize_game():
    global playerX, playerY, playerx_change, enemyimg, enemyX, enemyY, enemyX_change, enemyY_change
    global enemy_bulletX, enemy_bulletY, enemy_bulletY_change, enemy_bullet_state, enemy_last_shot_time
    global enemy_shot_interval, no_of_enemies, bulletX, bulletY, bulletX_change, bulletY_change
    global bullet_state, score, playerimg, vidas_jugador

    playerX = 370
    playerY = 470
    playerx_change = 0

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

    for i in range(no_of_enemies):
        enemy1 = resource_path('assets/images/enemy1.png')
        enemy2 = resource_path('assets/images/enemy2.png')
        enemy3 = resource_path('assets/images/enemy3.png')

        if i % 3 == 0:
            enemyimg.append(pygame.image.load(enemy1))
        elif i % 3 == 1:
            enemyimg.append(pygame.image.load(enemy2))
        else:
            enemyimg.append(pygame.image.load(enemy3))

        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(0, 150))
        enemyX_change.append(7)
        enemyY_change.append(20)
        enemy_bulletX.append(enemyX[i])
        enemy_bulletY.append(enemyY[i])
        enemy_bulletY_change.append(8)
        enemy_bullet_state.append("ready")
        enemy_last_shot_time.append(time.time())
        enemy_shot_interval.append(random.uniform(2, 5))

    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 13
    bullet_state = "ready"

    score = 0
    playerimg = playerimg1
    vidas_jugador = 3

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

# Función para añadir explosiones a la lista
def add_explosion(x, y):
    explosions.append((x, y, time.time()))

# Función para dibujar el estado de salud del jugador
def draw_health_status():
    if vidas_jugador == 3:
        screen.blit(salud, (10, 40))
    elif vidas_jugador == 2:
        screen.blit(media_salud, (10, 40))
    elif vidas_jugador == 1:
        screen.blit(mala_salud,(10 , 40))


# Función para disparar la bala del jugador
def fire_bullet(x, y):
    global bullet_state
    blast_sound.play()
    bullet_state = "fire"
    screen.blit(bulletimg2, (x + 16, y + 10))

# Función para disparar la bala del enemigo
def fire_enemy_bullet(x, y, i):
    global enemy_bullet_state
    enemy_bulletX[i] = x
    enemy_bulletY[i] = y
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
        "La galaxia sigue a la espera de",
        "una nueva esperanza"
    ]
    y_offset = 0

    for line in lines:
        over_text = over_font.render(line, True, (255, 0, 0))
        text_rect = over_text.get_rect(center=(screen_width // 2, (screen_height // 2) + y_offset))
        screen.blit(over_text, text_rect)
        y_offset += 40

# Función para mostrar la pantalla de inicio
def game_start():
    global playerimg, character_name
    menu = True
    while menu:
        screen.fill((0, 0, 0))
        screen.blit(title, (0, 0))

        start_font = pygame.font.Font(resource_path('assets/fonts/StarJedi-DGRW.ttf'), 32)
        start_text = start_font.render("ENTER para jugar", True, (1, 75, 160))
        start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 160))
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
    global playerimg

    selected = 0
    select = True

    while select:
        screen.fill((0, 0, 0))
        screen.blit(seleccion, (0, 0))

        title_font = pygame.font.Font(resource_path('assets/fonts/StarJedi-DGRW.ttf'), 32)
        title_text = title_font.render("Elije tu personaje", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect)

        # Mostrar los personajes para la selección
        screen.blit(playercharacter1, (screen_width // 4 - playercharacter1.get_width() // 2, screen_height // 2))
        screen.blit(playercharacter2, (3 * screen_width // 4 - playercharacter2.get_width() // 2, screen_height // 2))

        # Mostrar nombres de los personajes
        name_font = pygame.font.Font(resource_path('assets/fonts/StarJedi-DGRW.ttf'), 24)
        name_text1 = name_font.render("Weddom", True, (255, 255, 255))
        name_text2 = name_font.render("Star", True, (255, 255, 255))
        name_rect1 = name_text1.get_rect(center=(screen_width // 4, screen_height // 2 + 100))
        name_rect2 = name_text2.get_rect(center=(3 * screen_width // 4, screen_height // 2 + 100))
        screen.blit(name_text1, name_rect1)
        screen.blit(name_text2, name_rect2)

        # Resaltar el personaje seleccionado
        if selected == 0:
            pygame.draw.rect(screen, (255, 255, 0), (screen_width // 4 - playercharacter1.get_width() // 2 - 5, screen_height // 2 - 5, playercharacter1.get_width() + 10, playercharacter1.get_height() + 10), 3)
        else:
            pygame.draw.rect(screen, (255, 255, 0), (3 * screen_width // 4 - playercharacter2.get_width() // 2 - 5, screen_height // 2 - 5, playercharacter2.get_width() + 10, playercharacter2.get_height() + 10), 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = 0
                if event.key == pygame.K_RIGHT:
                    selected = 1
                if event.key == pygame.K_RETURN:
                    global playerimg, character_name
                    if selected == 0:
                        playerimg = playerimg1
                        character_name = "Weddom"  # Nombre del primer personaje
                    else:
                        playerimg = playerimg2
                        character_name = "Star"  # Nombre del segundo personaje
                    select = False
                    initialize_game()  # Reinicializar el juego antes de empezar
                    game_loop()  # Iniciar el bucle principal del juego

        pygame.display.update()
        clock.tick(15)

# Función para mostrar la pantalla de Game Over y permitir volver al menú
def game_over_screen():
    while True:
        screen.fill((0, 0, 0))
        game_over_text()
        start_font = pygame.font.Font(resource_path('assets/fonts/StarJedi-DGRW.ttf'), 32)
        start_text = start_font.render("ENTER para volver al menú", True, (255, 0, 0))
        start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 160))
        screen.blit(start_text, start_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_start()

        pygame.display.update()
        clock.tick(15)

# Bucle principal del juego
def game_loop():
    global playerX, playerY, playerx_change, bulletX, bulletY, bullet_state, score, vidas_jugador

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
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

        playerX += playerx_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(no_of_enemies):
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 7
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -7
                enemyY[i] += enemyY_change[i]

            if time.time() - enemy_last_shot_time[i] >= enemy_shot_interval[i]:
                if enemy_bullet_state[i] == "ready":
                    enemy_bulletX[i] = enemyX[i]
                    enemy_bulletY[i] = enemyY[i]
                    fire_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
                    enemy_last_shot_time[i] = time.time()
                    enemy_shot_interval[i] = random.uniform(2, 5)

            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                game_over_screen()
                break

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound.play()
                add_explosion(enemyX[i], enemyY[i])  # Añadir explosión a la lista
                bulletY = 480
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            if enemy_bullet_state[i] == "fire":
                fire_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
                enemy_bulletY[i] += enemy_bulletY_change[i]

                if enemy_bulletY[i] >= 600:
                    enemy_bullet_state[i] = "ready"

                player_hit = isPlayerHit(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i])
                if player_hit:
                    explosion_sound.play()
                    vidas_jugador -= 1
                    if vidas_jugador <= 0:
                        for j in range(no_of_enemies):
                            enemyY[j] = 2000
                        game_over_screen()
                        return
                    enemy_bullet_state[i] = "ready"  # Resetea el estado de la bala enemiga

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score()
        draw_health_status()

        # Dibujar explosiones activas
        current_time = time.time()
        for explosion in explosions[:]:
            x, y, start_time = explosion
            if current_time - start_time < explosion_duration:
                screen.blit(explosion_img, (x, y))
            else:
                explosions.remove(explosion)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Comenzar el juego
game_start()