import pgzrun
from pgzero.rect import Rect

from level import Level
from menu import MainMenu
from player import Player

WIDTH = 1280
HEIGHT = 720
TITLE = "Shadow Escape"

# Estados principais do jogo. Manter esses nomes centralizados evita strings soltas
# espalhadas pelos eventos, pelo update e pela tela de desenho.
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_LEVEL_INTRO = "level_intro"
STATE_WON = "won"
STATE_GAME_OVER = "game_over"
MAX_LEVEL = 3

game_state = STATE_MENU
audio_enabled = True
background_audio_started = False
mouse_pos = (0, 0)
camera_x = 0
level_intro_timer = 0
current_level = 1
level = None
player = None
total_crystals_collected = 0
enemies_defeated = 0
play_frames = 0
menu = MainMenu(WIDTH, HEIGHT)


def new_game():
    global enemies_defeated, play_frames, total_crystals_collected

    # Reinicia os dados da partida inteira, não apenas da fase atual.
    enemies_defeated = 0
    play_frames = 0
    total_crystals_collected = 0
    start_level(1, 3)


def start_level(level_number, lives):
    global camera_x, current_level, game_state, level, level_intro_timer, player

    # O jogador é recriado em cada fase, mas preserva as vidas que sobraram.
    current_level = level_number
    level = Level(current_level)
    player = Player(80, 590)
    player.lives = lives
    camera_x = 0
    level_intro_timer = 90
    game_state = STATE_LEVEL_INTRO


def update():
    global camera_x, enemies_defeated, game_state, play_frames
    global total_crystals_collected

    ensure_background_audio()

    if game_state == STATE_LEVEL_INTRO:
        level_intro_timer_update()
        return

    if game_state != STATE_PLAYING:
        return

    # A partir daqui roda apenas a lógica de partida: movimento, coletas,
    # colisões, avanço de fase e câmera.
    play_frames += 1
    player.update(keyboard, level.platforms, level.width)

    level.update()
    collected = level.collect_crystals(player)

    if collected > 0 and audio_enabled:
        sounds.collect.play()

    total_crystals_collected += collected

    if level.collect_whip_item(player) and audio_enabled:
        sounds.collect.play()

    defeated_by_whip = level.hit_enemies_with_whip(player)

    if defeated_by_whip > 0:
        enemies_defeated += defeated_by_whip

        if audio_enabled:
            sounds.stomp.play()

    enemy_contact = level.handle_enemy_contact(player)

    # Cada tipo de contato tem uma consequência diferente: pisar derrota,
    # morcego mata direto e encostar nos inimigos comuns tira vida.
    if enemy_contact == "stomp":
        enemies_defeated += 1

        if audio_enabled:
            sounds.stomp.play()
    elif enemy_contact == "deadly":
        player.lives = 0

        if audio_enabled:
            sounds.bat.play()

        game_state = STATE_GAME_OVER
    elif enemy_contact == "hit":
        was_hit = player.hit()

        if was_hit and audio_enabled:
            sounds.hit.play()

        if player.lives <= 0:
            game_state = STATE_GAME_OVER

    if player.actor.y > HEIGHT + 140:
        # Dá uma pequena margem abaixo da tela para evitar morte instantânea
        # quando o personagem só encosta na borda inferior da câmera.
        was_hit = player.hit()

        if was_hit and audio_enabled:
            sounds.hit.play()

        if player.lives <= 0:
            game_state = STATE_GAME_OVER

    if level.player_reached_exit(player):
        if current_level < MAX_LEVEL:
            if audio_enabled:
                sounds.door.play()

            start_level(current_level + 1, player.lives)
        else:
            game_state = STATE_WON

            if audio_enabled:
                sounds.win.play()

    update_camera()


def level_intro_timer_update():
    global game_state, level_intro_timer

    level_intro_timer -= 1

    if level_intro_timer <= 0:
        game_state = STATE_PLAYING


def update_camera():
    global camera_x

    # A câmera segue o jogador com suavização, mas fica presa aos limites da fase.
    target_x = player.actor.x - WIDTH // 2
    target_x = max(0, min(target_x, level.width - WIDTH))
    camera_x += (target_x - camera_x) * 0.12


def draw():
    screen.clear()

    if game_state == STATE_MENU:
        menu.draw(screen, mouse_pos)
    elif game_state == STATE_LEVEL_INTRO:
        draw_game()
        draw_level_intro()
    elif game_state == STATE_PLAYING:
        draw_game()
    elif game_state == STATE_WON:
        draw_victory_screen()
    elif game_state == STATE_GAME_OVER:
        draw_end_screen("FIM DE JOGO", "Clique para tentar de novo pelo menu.")


def draw_game():
    # A ordem importa: cenário primeiro, jogador por cima e HUD sempre na frente.
    level.draw(screen, camera_x)
    player.draw(camera_x)
    draw_hud()


def draw_hud():
    screen.draw.text(
        "Vidas: " + str(player.lives),
        topleft=(26, 22),
        fontsize=32,
        color="white",
    )
    screen.draw.text(
        "Cristais: " + str(player.score) + " / " + str(level.total_crystals),
        topleft=(26, 58),
        fontsize=32,
        color=(134, 226, 255),
    )
    screen.draw.text(
        "Fase: " + str(current_level) + " / " + str(MAX_LEVEL),
        topleft=(26, 94),
        fontsize=32,
        color=(210, 232, 194),
    )
    screen.draw.text(
        "Chicote: " + str(player.whip_charges),
        topleft=(26, 130),
        fontsize=32,
        color=(255, 196, 132),
    )


def draw_level_intro():
    screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (4, 6, 12))
    screen.draw.text(
        "FASE " + str(current_level),
        center=(WIDTH // 2, HEIGHT // 2 - 52),
        fontsize=72,
        color="white",
    )
    screen.draw.text(
        level.name,
        center=(WIDTH // 2, HEIGHT // 2 + 18),
        fontsize=42,
        color=(134, 226, 255),
    )
    screen.draw.text(
        "Colete os diamantes e procure a porta.",
        center=(WIDTH // 2, HEIGHT // 2 + 76),
        fontsize=28,
        color=(210, 232, 194),
    )


def draw_end_screen(title, subtitle):
    screen.fill((12, 15, 23))
    screen.draw.text(
        title,
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=74,
        color="white",
    )
    screen.draw.text(
        subtitle,
        center=(WIDTH // 2, HEIGHT // 2 + 35),
        fontsize=32,
        color=(154, 174, 204),
    )


def draw_victory_screen():
    restart_button = get_restart_button()
    screen.fill((12, 15, 23))
    screen.draw.text(
        "VOCE ESCAPOU",
        center=(WIDTH // 2, 210),
        fontsize=74,
        color="white",
    )
    screen.draw.text(
        "Diamantes coletados: " + str(total_crystals_collected),
        center=(WIDTH // 2, 315),
        fontsize=34,
        color=(134, 226, 255),
    )
    screen.draw.text(
        "Inimigos derrotados: " + str(enemies_defeated),
        center=(WIDTH // 2, 360),
        fontsize=34,
        color=(255, 196, 132),
    )
    screen.draw.text(
        "Vidas restantes: " + str(player.lives),
        center=(WIDTH // 2, 405),
        fontsize=34,
        color=(210, 232, 194),
    )
    screen.draw.text(
        "Tempo total: " + str(play_frames // 60) + "s",
        center=(WIDTH // 2, 450),
        fontsize=34,
        color=(232, 244, 255),
    )
    screen.draw.filled_rect(restart_button, (38, 45, 66))
    screen.draw.rect(restart_button, (134, 226, 255))
    screen.draw.text(
        "Jogar Novamente",
        center=restart_button.center,
        fontsize=34,
        color="white",
    )


def get_restart_button():
    return Rect((WIDTH // 2 - 170, 520), (340, 58))


def on_mouse_move(pos):
    global mouse_pos

    mouse_pos = pos


def on_mouse_down(pos):
    global audio_enabled, game_state

    if game_state == STATE_MENU:
        action = menu.button_at(pos)

        # O menu devolve uma ação simples, e a tela principal decide o que fazer.
        if action == "start":
            if audio_enabled:
                sounds.click.play()

            new_game()
        elif action == "audio":
            audio_enabled = not audio_enabled
            menu.set_audio_text(audio_enabled)
            update_audio()
        elif action == "quit":
            raise SystemExit
    elif game_state == STATE_WON:
        if get_restart_button().collidepoint(pos):
            new_game()
        else:
            game_state = STATE_MENU
    elif game_state == STATE_GAME_OVER:
        game_state = STATE_MENU


def on_key_down(key):
    global game_state

    if key.name == "ESCAPE":
        game_state = STATE_MENU

    if game_state == STATE_MENU and key.name == "RETURN":
        new_game()

    if game_state == STATE_PLAYING:
        if key.name in ("UP", "W", "SPACE") and player.movement.on_ground:
            if audio_enabled:
                sounds.jump.play()

        if key.name in ("X", "K"):
            if player.start_whip_attack() and audio_enabled:
                sounds.whip.play()


def update_audio():
    global background_audio_started

    # O Pygame Zero usa o objeto sounds também para música curta em loop.
    if audio_enabled:
        sounds.shadow_theme.set_volume(0.18)
        sounds.shadow_theme.play(-1)
        background_audio_started = True
    else:
        sounds.shadow_theme.stop()
        background_audio_started = False


def ensure_background_audio():
    if audio_enabled and not background_audio_started:
        update_audio()


new_game()
game_state = STATE_MENU
pgzrun.go()
