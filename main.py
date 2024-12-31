import pygame as pg
from os import path
import random


def run():
    # Constants
    MAIN_PATH = path.join("./")
    FPS = 18
    START_SPEED = 8
    SCREEN_SIZE = {"x": 1000, "y": 400}
    THEME = ("light", "dark")
    THEME_TRIGGERS = ((0, 300), (500, 800))
    BG_COLOR = {THEME[0]: (255, 255, 255), THEME[1]: (0, 0, 0)}
    FONT_COLOR = (120, 120, 120)
    QUIT_FZ = 16
    QUIT_MARGIN = 10
    SCORE_FZ = 24
    SCORE_MARGIN = 20
    GAME_OVER_FZ = 36
    GAME_OVER_MARGIN = 50
    GROUND_SCALE = 3
    MOON_SCALE = 3
    HUBBLE_SCALE = 1.3
    PLAYER_SCALE = 2.5
    PTERO_SCALE = 2
    MAX_JUMP = 8
    MAX_DWN = 8
    STAR_MAX_SCALE = 3

    theme = THEME[0]
    game_speed = START_SPEED
    game_score = 0
    total_score = 0

    def get_theme(score):
        if THEME_TRIGGERS:
            for trigger in THEME_TRIGGERS:
                if score >= trigger[0] and score < trigger[1]:
                    return THEME[1]
        return THEME[0]

    # Initialize Pygame
    pg.init()
    pg.display.set_caption("T-Rex Game")
    # screen = pg.display.set_mode([SCR_WIDTH, SCR_HEIGHT], flags=pg.NOFRAME)
    screen = pg.display.set_mode(list(SCREEN_SIZE.values()))
    clock = pg.time.Clock()

    # Game Over
    is_game_over = False
    gameover_sound = pg.mixer.Sound(path.join(MAIN_PATH, "sound", "game_over.mp3"))

    # Timer
    cloud_mills = 0
    enemy_mills = 0
    cloud_timer = pg.USEREVENT + 1
    enemy_timer = pg.USEREVENT + 2

    # Icon
    icon = pg.image.load(path.join(MAIN_PATH, "img", "icon.png")).convert_alpha()
    pg.display.set_icon(icon)

    # Font
    quit_font = pg.font.Font(path.join(MAIN_PATH, "font", "Pixellari.ttf"), QUIT_FZ)
    score_font = pg.font.Font(path.join(MAIN_PATH, "font", "Pixellari.ttf"), SCORE_FZ)
    game_over_font = pg.font.Font(
        path.join(MAIN_PATH, "font", "Pixellari.ttf"), GAME_OVER_FZ
    )

    # Ground image
    ground_image = pg.image.load(
        path.join(MAIN_PATH, "img", "ground.png")
    ).convert_alpha()
    ground = pg.transform.scale_by(ground_image, GROUND_SCALE)
    ground_x = 0
    ground_y = 311

    # Hubble image
    hubble_ingame = []
    hubble = {
        THEME[0]: pg.transform.scale_by(
            pg.image.load(path.join(MAIN_PATH, "img", "hubble.png")).convert_alpha(),
            HUBBLE_SCALE,
        ),
        THEME[1]: pg.transform.scale_by(
            pg.image.load(
                path.join(MAIN_PATH, "img", "hubble_dark.png")
            ).convert_alpha(),
            HUBBLE_SCALE,
        ),
    }
    hubble_x = SCREEN_SIZE["x"]
    hubble_y = ground_y - hubble[THEME[0]].get_height() + 3

    # Moon image
    moon_image = pg.image.load(path.join(MAIN_PATH, "img", "moon.png")).convert_alpha()
    moon = pg.transform.scale_by(moon_image, MOON_SCALE)
    moon_x = SCREEN_SIZE["x"]
    moon_y = 50

    # Star image
    star_ingame = []
    star_image = pg.image.load(path.join(MAIN_PATH, "img", "star.png")).convert_alpha()
    star_x = (20, SCREEN_SIZE["x"] - 20)
    star_y = (20, 150)

    def star_add():
        star_scale = random.randint(15, STAR_MAX_SCALE * 10) / 10

        current_star_x = random.randint(*star_x)
        current_star_y = random.randint(*star_y)
        star_rect = star_image.get_rect(topleft=(current_star_x, current_star_y))
        star_ingame.append({"rect": star_rect, "scale": star_scale})

    # Cloud image
    cloud_ingame = []
    cloud_image = pg.image.load(
        path.join(MAIN_PATH, "img", "cloud.png")
    ).convert_alpha()
    cloud_x = SCREEN_SIZE["x"]
    cloud_y = 150

    def clouds_add():
        clouds_scale = random.randint(15, 30) / 10

        cloud = pg.transform.scale_by(cloud_image, clouds_scale)
        current_cloud_y = cloud_y - clouds_scale * 30 - cloud.get_height()
        cloud_rect = cloud.get_rect(topleft=(cloud_x, current_cloud_y))
        cloud_speed = clouds_scale * 2
        cloud_ingame.append({"image": cloud, "rect": cloud_rect, "speed": cloud_speed})

    # Player images
    player_images_dict = {
        "play": {
            "up": [
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_01.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_02.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_03.png")
                ).convert_alpha(),
            ],
            "dwn": [
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_dwn_01.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_dwn_02.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_dwn_03.png")
                ).convert_alpha(),
            ],
        },
        "gameover": {
            "up": [
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_fine_01.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_fine_02.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_fine_03.png")
                ).convert_alpha(),
            ],
            "dwn": [
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_dwn_fine_01.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_dwn_fine_02.png")
                ).convert_alpha(),
                pg.image.load(
                    path.join(MAIN_PATH, "img", "player_dwn_fine_03.png")
                ).convert_alpha(),
            ],
        },
    }
    player_index = 0
    player_x = 150
    player_y_dict = {"up": 260, "dwn": 280}

    # Player jumping
    jump_sound = pg.mixer.Sound(path.join(MAIN_PATH, "sound", "jump.mp3"))
    is_jump = False
    is_dwn = False
    jump_value = 0
    jump_count = MAX_JUMP
    dwn_count = MAX_DWN

    # Enemies
    ## Kaktus
    kaktuses_ingame = []
    kaktus_images = [
        pg.image.load(path.join(MAIN_PATH, "img", "kaktus1.png")).convert_alpha(),
        pg.image.load(path.join(MAIN_PATH, "img", "kaktus2.png")).convert_alpha(),
        pg.image.load(path.join(MAIN_PATH, "img", "kaktus3.png")).convert_alpha(),
    ]
    kaktus_index = 0
    kaktus_x = SCREEN_SIZE["x"]
    kaktus_y = 280

    def kaktus_add(kaktus_index):
        for i in range(random.randint(1, 3)):
            kaktus_scale = random.randint(12, 16) / 10

            kaktus = pg.transform.scale_by(kaktus_images[kaktus_index], kaktus_scale)
            kaktus_y = ground_y - kaktus.get_height()
            kaktus_x = SCREEN_SIZE["x"] + i * 15
            kaktus_rect = kaktus.get_rect(topleft=(kaktus_x, kaktus_y))
            kaktuses_ingame.append({"image": kaktus, "rect": kaktus_rect})
            kaktus_index = (kaktus_index + 1) % len(kaktus_images)

        return kaktus_index

    ## Ptero
    pteros_ingame = []
    ptero_images = [
        pg.transform.scale_by(
            pg.image.load(path.join(MAIN_PATH, "img", "ptero_01.png")).convert_alpha(),
            PTERO_SCALE,
        ),
        pg.transform.scale_by(
            pg.image.load(path.join(MAIN_PATH, "img", "ptero_02.png")).convert_alpha(),
            PTERO_SCALE,
        ),
    ]
    ptero_index = 0
    ptero_x = SCREEN_SIZE["x"]
    ptero_y = 230

    def ptero_add():
        ptero_rect = ptero_images[0].get_rect(topleft=(ptero_x, ptero_y))
        pteros_ingame.append({"rect": ptero_rect})

    # Game loop
    game_run = True
    while game_run:
        keys = pg.key.get_pressed()
        theme = get_theme(game_score)
        player_y = player_y_dict["dwn" if is_dwn else "up"]
        player_images = player_images_dict["gameover" if is_game_over else "play"][
            "dwn" if is_dwn else "up"
        ]

        if is_game_over:
            if keys[pg.K_SPACE]:
                is_game_over = False
                is_jump = False
                is_dwn = False
                hubble_ingame = []
                star_ingame = []
                cloud_ingame = []
                kaktuses_ingame = []
                pteros_ingame = []
                ground_x = 0
                moon_x = SCREEN_SIZE["x"]
                game_speed = START_SPEED
                game_score = 0
        else:
            game_speed += 0.001
            player_index = (
                0 if player_index == len(player_images) - 1 else player_index + 1
            )

            # Jumping
            if is_jump:
                if jump_count >= -MAX_JUMP:
                    neg = 1 if jump_count > 0 else -1
                    player_index = 1 if jump_count > 0 else 2

                    if jump_count % 3:
                        jump_value += (jump_count**2) * 0.7 * neg

                    player_y -= jump_value
                    jump_count -= 1
                else:
                    is_jump = False
            elif is_dwn:
                if dwn_count >= -MAX_DWN:
                    dwn_count -= 1
                else:
                    is_dwn = False
            else:
                if keys[pg.K_UP]:
                    is_jump = True
                    jump_sound.play()
                    jump_value = 0
                    jump_count = MAX_JUMP

                if keys[pg.K_DOWN] and not is_jump:
                    is_dwn = True
                    jump_sound.play()
                    dwn_count = MAX_DWN

        # ----- Draw -----
        screen.fill(BG_COLOR[theme])

        # Quit helper
        quit_label = quit_font.render("QUIT[Q]", False, FONT_COLOR)
        quit_x = SCREEN_SIZE["x"] - quit_label.get_width() - QUIT_MARGIN
        quit_y = SCREEN_SIZE["y"] - quit_label.get_height() - QUIT_MARGIN
        screen.blit(quit_label, (quit_x, quit_y))

        # Ground
        screen.blit(ground, (ground_x, ground_y))
        screen.blit(ground, (ground_x + ground.get_width(), ground_y))
        if not is_game_over:
            ground_x = 0 if ground_x <= -ground.get_width() else ground_x - game_speed

        # Hubble
        hubble_rand = random.randint(0, 200) / 10
        if 1.2 <= hubble_rand <= 1.4:
            hubble_rect = hubble[theme].get_rect(topleft=(hubble_x, hubble_y))
            hubble_ingame.append({"rect": hubble_rect})

        if hubble_ingame:
            hubble_ingame = [
                el for el in hubble_ingame if el["rect"].x >= -el["rect"].width
            ]

            for el in hubble_ingame:
                screen.blit(hubble[theme], el["rect"])
                if not is_game_over:
                    el["rect"].x -= game_speed

        # Moon
        if theme == THEME[0]:
            moon_x = SCREEN_SIZE["x"]
        else:
            screen.blit(moon, (moon_x, moon_y))
            if not is_game_over:
                moon_x = (
                    moon_x - 0.1 if moon_x > -moon.get_width() else SCREEN_SIZE["x"]
                )

        # Star movement
        if star_ingame:
            if theme == THEME[0]:
                star_ingame = []
            else:
                star_ingame = [el for el in star_ingame if el["scale"] > 0]

                for el in star_ingame:
                    star = pg.transform.scale_by(star_image, el["scale"])

                    screen.blit(star, el["rect"])
                    if not is_game_over:
                        el["scale"] -= 0.01

        # Clouds movement
        if cloud_ingame:
            cloud_ingame = [
                el for el in cloud_ingame if el["rect"].x >= -el["rect"].width
            ]

            for el in cloud_ingame:
                screen.blit(el["image"], el["rect"])
                if not is_game_over:
                    el["rect"].x -= el["speed"]

        # Score
        if not is_game_over:
            game_score += 0.1

        total_score = total_score if total_score > game_score else game_score
        score_label = score_font.render(
            f"HI {int(total_score):05} | {int(game_score):05}", False, FONT_COLOR
        )
        score_x = SCREEN_SIZE["x"] - score_label.get_width() - SCORE_MARGIN
        screen.blit(score_label, (score_x, SCORE_MARGIN))

        # Player
        player = pg.transform.scale_by(player_images[player_index], PLAYER_SCALE)
        player_rect = player.get_rect(topleft=(player_x, player_y))
        screen.blit(player, (player_x, player_y))

        # Kaktus movement
        if kaktuses_ingame:
            kaktuses_ingame = [
                el for el in kaktuses_ingame if el["rect"].x >= -el["rect"].width
            ]

            for el in kaktuses_ingame:
                screen.blit(el["image"], el["rect"])
                if not is_game_over:
                    el["rect"].x -= game_speed

                # ----- GAME OVER -----
                if player_rect.colliderect(el["rect"]):
                    gameover_sound.play()
                    is_game_over = True

        # Ptero movement
        if pteros_ingame:
            pteros_ingame = [
                el for el in pteros_ingame if el["rect"].x >= -el["rect"].width
            ]

            for el in pteros_ingame:
                if not is_game_over:
                    el["rect"].x -= game_speed
                    ptero_index = random.randint(0, 100) % 2

                ptero = ptero_images[ptero_index]
                screen.blit(ptero, el["rect"])

                # ----- GAME OVER -----
                if player_rect.colliderect(el["rect"]):
                    gameover_sound.play()
                    is_game_over = True

        # Game over screen
        if is_game_over:
            game_over_label = game_over_font.render(
                "Press Space to reload", False, FONT_COLOR
            )
            game_over_x = (SCREEN_SIZE["x"] - game_over_label.get_width()) / 2
            game_over_y = (
                SCREEN_SIZE["y"] - game_over_label.get_height()
            ) / 2 - GAME_OVER_MARGIN
            screen.blit(game_over_label, (game_over_x, game_over_y))

        # Events
        if not cloud_mills:
            cloud_mills = random.randint(2500, 5000)
            pg.time.set_timer(cloud_timer, cloud_mills)
        if not enemy_mills:
            enemy_mills = random.randint(1500, 2500)
            pg.time.set_timer(enemy_timer, enemy_mills)

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                game_run = False
                pg.quit()
                exit()
            elif event.type == cloud_timer and not is_game_over:
                cloud_mills = 0
                clouds_add()
                if theme == THEME[1]:
                    star_add()
            elif event.type == enemy_timer and not is_game_over:
                enemy_mills = 0

                if random.randint(0, 100) / 10 % 2:
                    kaktus_index = kaktus_add(kaktus_index)
                else:
                    ptero_add()

        # Update screen
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
