import pygame
import random
import math
import sys
import os
import time

# Inicializar Pygame
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
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

asset_icon = resource_path('assets/images/icon.png')
icon = pygame.image.load(asset_icon)

asset_sound = resource_path('assets/audios/background_music2.mp3')
pygame.mixer.music.load(asset_sound)

asset_blast = resource_path('assets/audios/blast.mp3')
blast_sound = pygame.mixer.Sound(asset_blast)

# Fuentes para los botones
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# Función para dibujar botones
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

# Función para ir a la pantalla de selección de nave
def game_start():
    main_menu = False
    while not main_menu:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        draw_button("Jugar", 300, 250, 200, 50, (0, 128, 0), (0, 255, 0), select_ship)
        draw_button("Salir", 300, 350, 200, 50, (128, 0, 0), (255, 0, 0), pygame.quit)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def select_ship():
    ship_menu = True
    while ship_menu:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        draw_button("Nave 1 (Hombre)", 100, 250, 200, 50, (0, 0, 128), (0, 0, 255), lambda: start_game(1))
        draw_button("Nave 2 (Mujer)", 500, 250, 200, 50, (128, 0, 128), (255, 0, 255), lambda: start_game(2))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def start_game(ship_type):
    print(f"Seleccionado nave {ship_type}")
    gameloop(ship_type)

# Función principal del juego
def gameloop(ship_type):
    global enemy_bullet_state, enemy_bulletX, enemy_bulletY, enemy_bulletY_change, enemy_last_shot_time, enemy_shot_interval

    # Cargar imágenes de la nave seleccionada
    if ship_type == 1:
        asset_playerimg = resource_path('assets/images/Nave.png')
    elif ship_type == 2:
        asset_playerimg = resource_path('assets/images/nave2.png')
    
    playerimg = pygame.image.load(asset_playerimg)
    
    # Cargar imagen de la bala del jugador
    asset_bulletimg = resource_path('assets/images/bullet2.jpg')
    bulletimg = pygame.image.load(asset_bulletimg)

    # Configurar el sonido y la música
    pygame.mixer.music.play(-1)

    # Variables del jugador
    playerX = 370
    playerY = 470
    playerx_change = 0

    # Variables de enemigos
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

    # Inicialización de enemigos
    for i in range(no_of_enemies):
        enemy1 = resource_path('assets/images/enemy1.png')
        enemyimg.append(pygame.image.load(enemy1))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(0, 150))
        enemyX_change.append(5)
        enemyY_change.append(20)
        enemy_bulletX.append(enemyX[i])
        enemy_bulletY.append(enemyY[i])
        enemy_bulletY_change.append(3)
        enemy_bullet_state.append("ready")
        enemy_last_shot_time.append(time.time())
        enemy_shot_interval.append(random.uniform(2, 5))

    # Inicialización de la bala del jugador
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # Inicialización de la puntuación
    score = 0

    # Función para mostrar la puntuación
    def show_score():
        score_value = font.render("SCORE : " + str(score), True, (255, 255, 0))
        screen.blit(score_value, (10, 10))

    # Función para dibujar el jugador
    def player(x, y):
        screen.blit(playerimg, (x, y))

    # Función para dibujar el enemigo
    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))

    # Función para disparar la bala del jugador
    def fire_bullet(x, y):
        global bullet_state
        blast_sound.play()
        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))

    # Función para disparar la bala del enemigo
    def fire_enemy_bullet(x, y, i):
        global enemy_bullet_state
        enemy_bulletX[i] = x
        enemy_bullet_state[i] = "fire"
        blast_sound.play()
        screen.blit(bulletimg, (x + 16, y + 10))

    # Función para verificar colisiones
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        return distance < 27

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
        y_offset = 0

        for line in lines:
            over_text = small_font.render(line, True, (255, 255, 0))
            text_rect = over_text.get_rect(center=(screen_width // 2, (screen_height // 2) + y_offset))
            screen.blit(over_text, text_rect)
            y_offset += 40

    # Bucle principal del juego
    in_game = True
    while in_game:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()

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
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                pygame.display.update()
                time.sleep(3)
                in_game = False
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            if enemy_bullet_state[i] == "ready":
                current_time = time.time()
                if current_time - enemy_last_shot_time[i] >= enemy_shot_interval[i]:
                    fire_enemy_bullet(enemyX[i], enemyY[i], i)
                    enemy_last_shot_time[i] = current_time

            if enemy_bullet_state[i] == "fire":
                enemy_bulletY[i] += enemy_bulletY_change[i]
                screen.blit(bulletimg, (enemy_bulletX[i] + 16, enemy_bulletY[i] + 10))

                if enemy_bulletY[i] >= 600:
                    enemy_bulletY[i] = enemyY[i]
                    enemy_bullet_state[i] = "ready"

                if isPlayerHit(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i]):
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                    pygame.display.update()
                    time.sleep(3)
                    in_game = False
                    break

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = 480
                bullet_state = "ready"
                score += 10
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score()
        pygame.display.update()

# Llamar a la función del menú principal
game_start()