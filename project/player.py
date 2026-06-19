from pgzero.actor import Actor
from pgzero.rect import Rect

from animation import SpriteAnimation
from movement import PlatformMovement


class Player:
    def __init__(self, x, y):
        self.actor = Actor("hero_idle_0", (x, y))
        self.animation = SpriteAnimation(
            ["hero_idle_0", "hero_idle_1", "hero_idle_2", "hero_idle_3"],
            ["hero_run_0", "hero_run_1", "hero_run_2", "hero_run_3"],
            8,
        )
        self.movement = PlatformMovement(4.6, 13)
        self.lives = 3
        self.spawn_x = x
        self.spawn_y = y
        self.invincible_timer = 0
        self.score = 0
        self.whip_charges = 0
        # O chicote tem uma janela curta de ataque; isso evita acertar o mesmo
        # golpe várias vezes enquanto a animação ainda está acontecendo.
        self.whip_timer = 0
        self.whip_hit_done = False

    def update(self, keyboard, platforms, level_width):
        # Resolve o eixo X e depois o Y para deixar a colisão com plataformas
        # mais previsível, principalmente nas quinas.
        self.movement.read_input(keyboard)
        self.movement.apply_gravity()
        self.actor.x += self.movement.velocity_x
        self._solve_horizontal_collision(platforms)
        self.actor.y += self.movement.velocity_y
        self._solve_vertical_collision(platforms)
        self._keep_inside_level(level_width)
        self._update_animation()

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.whip_timer > 0:
            self.whip_timer -= 1

            if self.whip_timer == 0:
                self.whip_hit_done = False

    def draw(self, camera_x=0):
        # Durante a invencibilidade o personagem pisca, deixando claro para o
        # jogador que ainda está protegido por alguns frames.
        if self.invincible_timer > 0 and self.invincible_timer % 8 < 4:
            return

        real_x = self.actor.x
        self.actor.x -= camera_x
        self.actor.draw()
        self.actor.x = real_x
        self._draw_whip(camera_x)

    def hit(self):
        if self.invincible_timer > 0:
            return False

        # Ao tomar dano, volta para o ponto inicial da fase e ganha um tempo
        # curto de proteção para não perder todas as vidas de uma vez.
        self.lives -= 1
        self.invincible_timer = 90
        self.reset_position()
        return True

    def reset_position(self):
        self.actor.pos = (self.spawn_x, self.spawn_y)
        self.movement.velocity_x = 0
        self.movement.velocity_y = 0

    def bounce_after_stomp(self):
        self.movement.velocity_y = -9
        self.movement.on_ground = False

    def collect_whip(self):
        self.whip_charges = 3

    def start_whip_attack(self):
        if self.whip_charges <= 0 or self.whip_timer > 0:
            return False

        # Cada uso consome uma carga; a fase controla quando novas cargas aparecem.
        self.whip_charges -= 1
        self.whip_timer = 18
        self.whip_hit_done = False
        return True

    def is_whipping(self):
        return self.whip_timer > 0

    def can_hit_with_whip(self):
        # O golpe só causa dano no meio da animação, quando o sprite do chicote
        # já está visualmente estendido.
        return self.whip_timer > 0 and not self.whip_hit_done and self.whip_timer <= 12

    def finish_whip_hit(self):
        self.whip_hit_done = True

    def get_whip_hitbox(self):
        # A caixa de ataque acompanha o lado para onde o personagem está virado.
        if self.movement.facing_right:
            return Rect((self.actor.x + 10, self.actor.y - 26), (86, 52))

        return Rect((self.actor.x - 96, self.actor.y - 26), (86, 52))

    def get_hitbox(self):
        return Rect(
            (self.actor.x - 17, self.actor.y - 24),
            (34, 48),
        )

    def _update_animation(self):
        if self.is_whipping():
            # A animação do chicote é curta e tem prioridade sobre idle/corrida.
            frame = (18 - self.whip_timer) // 6
            self.actor.image = "hero_whip_" + str(min(2, frame))
            self.actor.flip_x = not self.movement.facing_right
            return

        if self.movement.is_moving():
            self.animation.set_state("move")
        else:
            self.animation.set_state("idle")

        self.animation.update()
        self.actor.image = self.animation.current_image()
        self.actor.flip_x = not self.movement.facing_right

    def _solve_horizontal_collision(self, platforms):
        for platform in platforms:
            if not self.actor.colliderect(platform):
                continue

            if self.movement.velocity_x > 0:
                self.actor.right = platform.left
            elif self.movement.velocity_x < 0:
                self.actor.left = platform.right

    def _solve_vertical_collision(self, platforms):
        self.movement.on_ground = False

        for platform in platforms:
            if not self.actor.colliderect(platform):
                continue

            if self.movement.velocity_y > 0:
                # Caindo sobre uma plataforma: trava no topo e libera novo pulo.
                self.actor.bottom = platform.top
                self.movement.velocity_y = 0
                self.movement.on_ground = True
            elif self.movement.velocity_y < 0:
                self.actor.top = platform.bottom
                self.movement.velocity_y = 0

    def _keep_inside_level(self, level_width):
        if self.actor.left < 0:
            self.actor.left = 0

        if self.actor.right > level_width:
            self.actor.right = level_width

    def _draw_whip(self, camera_x):
        if not self.is_whipping():
            return

        frame = min(2, (18 - self.whip_timer) // 6)
        image = "whip_attack_" + str(frame)
        offset = 52

        if self.movement.facing_right:
            whip = Actor(image, (self.actor.x + offset - camera_x, self.actor.y))
        else:
            whip = Actor(image, (self.actor.x - offset - camera_x, self.actor.y))
            whip.flip_x = True

        whip.draw()
