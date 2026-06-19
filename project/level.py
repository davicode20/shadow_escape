from pgzero.actor import Actor
from pgzero.rect import Rect

from enemy import BatEnemy, Enemy


class Level:
    def __init__(self, number=1):
        self.number = number
        self.name = "Ruas Sombrias"
        self.width = 1800
        self.platforms = []
        self.enemies = []
        self.crystals = []
        self.collect_effects = []
        self.whip_item = None
        self.whip_collected = False
        self.exit = Rect((1715, 570), (45, 80))
        self.sky_color = (12, 15, 23)
        self.platform_color = (42, 43, 55)
        self.platform_edge_color = (94, 179, 151)
        self.crystal_timer = 0
        self.build()
        # Guarda o total inicial para o HUD continuar mostrando a meta da fase.
        self.total_crystals = len(self.crystals)

    def build(self):
        # Cada fase fica em seu próprio método para facilitar ajustes de layout.
        if self.number == 2:
            self._build_level_two()
        elif self.number == 3:
            self._build_level_three()
        else:
            self._build_level_one()

    def _build_level_one(self):
        self.width = 1800
        self.name = "Ruas Sombrias"
        self.sky_color = (12, 15, 23)
        self.platform_color = (42, 43, 55)
        self.platform_edge_color = (94, 179, 151)
        self.platforms = [
            Rect((0, 650), (1800, 70)),
            Rect((190, 555), (220, 24)),
            Rect((500, 485), (210, 24)),
            Rect((790, 415), (240, 24)),
            Rect((1120, 530), (210, 24)),
            Rect((1430, 445), (250, 24)),
        ]
        self.enemies = [
            Enemy(330, 520, 225, 385, 1.4),
            Enemy(610, 450, 530, 690, 1.2),
            Enemy(915, 380, 820, 1010, 1.6),
            Enemy(1220, 495, 1145, 1305, 1.5),
            Enemy(1540, 410, 1460, 1660, 1.8),
        ]
        self.crystals = [
            Rect((260, 510), (24, 24)),
            Rect((590, 440), (24, 24)),
            Rect((940, 370), (24, 24)),
            Rect((1210, 485), (24, 24)),
            Rect((1565, 400), (24, 24)),
        ]
        self.exit = Rect((1715, 570), (45, 80))

    def _build_level_two(self):
        self.width = 1900
        self.name = "Telhados Verdes"
        self.sky_color = (11, 24, 30)
        self.platform_color = (35, 53, 57)
        self.platform_edge_color = (91, 207, 181)
        self.platforms = [
            Rect((0, 650), (1900, 70)),
            Rect((210, 570), (220, 24)),
            Rect((500, 510), (200, 24)),
            Rect((790, 455), (220, 24)),
            Rect((1085, 510), (220, 24)),
            Rect((1370, 465), (220, 24)),
            Rect((1630, 545), (230, 24)),
        ]
        self.enemies = [
            Enemy(340, 535, 240, 405, 1.7),
            Enemy(610, 475, 525, 680, 1.3),
            Enemy(910, 420, 820, 995, 1.8),
            Enemy(1195, 475, 1115, 1290, 1.5),
            Enemy(1485, 430, 1390, 1575, 2.0),
            BatEnemy(1020, 340, 900, 1220, 1.7),
        ]
        self.crystals = [
            Rect((300, 525), (24, 24)),
            Rect((590, 465), (24, 24)),
            Rect((910, 410), (24, 24)),
            Rect((1210, 465), (24, 24)),
            Rect((1490, 420), (24, 24)),
            Rect((1730, 500), (24, 24)),
        ]
        self.whip_item = Rect((145, 585), (32, 32))
        self.exit = Rect((1810, 570), (45, 80))

    def _build_level_three(self):
        self.width = 2000
        self.name = "Torre da Noite"
        self.sky_color = (20, 16, 29)
        self.platform_color = (49, 39, 68)
        self.platform_edge_color = (184, 130, 255)
        self.platforms = [
            Rect((0, 650), (2000, 70)),
            Rect((170, 560), (180, 24)),
            Rect((430, 500), (200, 24)),
            Rect((710, 440), (220, 24)),
            Rect((1030, 500), (220, 24)),
            Rect((1330, 445), (210, 24)),
            Rect((1660, 520), (230, 24)),
        ]
        self.enemies = [
            Enemy(275, 525, 190, 335, 1.6),
            Enemy(535, 465, 455, 615, 1.8),
            Enemy(840, 405, 745, 920, 1.5),
            Enemy(1160, 465, 1070, 1250, 2.0),
            Enemy(1445, 410, 1365, 1530, 1.7),
            Enemy(1770, 485, 1685, 1875, 2.1),
            BatEnemy(670, 330, 540, 820, 1.8),
            BatEnemy(1525, 335, 1370, 1710, 2.0),
        ]
        self.crystals = [
            Rect((245, 515), (24, 24)),
            Rect((530, 455), (24, 24)),
            Rect((850, 395), (24, 24)),
            Rect((1165, 455), (24, 24)),
            Rect((1450, 400), (24, 24)),
            Rect((1785, 475), (24, 24)),
        ]
        self.exit = Rect((1920, 570), (45, 80))

    def update(self):
        self.crystal_timer += 1

        # O timer dos cristais também serve para pequenos efeitos visuais da fase.
        for enemy in self.enemies:
            enemy.update()

        self._update_collect_effects()

    def draw(self, screen, camera_x):
        self._draw_background(screen, camera_x)

        # Tudo que pertence ao mundo é deslocado pela câmera antes de ser desenhado.
        for platform in self.platforms:
            visible = platform.move(-camera_x, 0)
            screen.draw.filled_rect(visible, self.platform_color)
            screen.draw.filled_rect(
                Rect((visible.x, visible.y), (visible.width, 8)),
                self.platform_edge_color,
            )

        crystal_image = "diamond_" + str((self.crystal_timer // 8) % 4)

        for crystal in self.crystals:
            visible = crystal.move(-camera_x, 0)
            diamond = Actor(crystal_image, visible.center)
            diamond.draw()

        self._draw_whip_item(camera_x)
        self._draw_collect_effects(screen, camera_x)

        visible_exit = self.exit.move(-camera_x, 0)
        door_ready = len(self.crystals) == 0
        door_color = (88, 43, 132) if door_ready else (58, 28, 89)
        edge_color = (244, 213, 125) if door_ready else (164, 120, 255)

        if door_ready:
            # Quando todos os cristais foram coletados, a porta ganha um brilho
            # simples para chamar o jogador sem precisar de texto extra.
            pulse = 4 + (self.crystal_timer // 6) % 4
            glow = visible_exit.inflate(pulse * 5, pulse * 4)
            screen.draw.rect(glow, (244, 213, 125))

        screen.draw.filled_rect(visible_exit, door_color)
        screen.draw.rect(visible_exit, edge_color)
        screen.draw.text(
            "EXIT",
            center=visible_exit.center,
            fontsize=22,
            color="white" if door_ready else (154, 174, 204),
        )

        for enemy in self.enemies:
            enemy.draw(camera_x)

    def collect_crystals(self, player):
        collected = 0
        remaining = []

        # Monta uma nova lista com o que não foi coletado; assim evitamos remover
        # itens enquanto estamos percorrendo a lista original.
        for crystal in self.crystals:
            if player.actor.colliderect(crystal):
                collected += 1
                self._add_collect_effect(crystal.center)
            else:
                remaining.append(crystal)

        self.crystals = remaining
        player.score += collected
        return collected

    def collect_whip_item(self, player):
        if self.whip_item is None or self.whip_collected:
            return False

        if player.actor.colliderect(self.whip_item):
            self.whip_collected = True
            player.collect_whip()
            self._add_collect_effect(self.whip_item.center)
            return True

        return False

    def hit_enemies_with_whip(self, player):
        if not player.can_hit_with_whip():
            return 0

        # O ataque do chicote usa uma hitbox separada do personagem.
        attack_box = player.get_whip_hitbox()
        defeated = 0
        remaining_enemies = []

        for enemy in self.enemies:
            if attack_box.colliderect(enemy.get_hitbox()):
                defeated += 1
                self._add_collect_effect(enemy.actor.pos)
            else:
                remaining_enemies.append(enemy)

        self.enemies = remaining_enemies
        player.finish_whip_hit()
        return defeated

    def handle_enemy_contact(self, player):
        player_hitbox = player.get_hitbox()
        remaining_enemies = []
        stomped_enemy = False
        player_was_hit = False
        player_was_killed = False

        for enemy in self.enemies:
            enemy_hitbox = enemy.get_hitbox()

            if player_hitbox.colliderect(enemy_hitbox):
                if enemy.is_deadly:
                    # Alguns inimigos, como morcegos, encerram a tentativa na hora.
                    player_was_killed = True
                    remaining_enemies.append(enemy)
                    continue

                player_is_falling = player.movement.velocity_y > 0
                player_is_above_enemy = player.actor.bottom <= enemy.actor.y + 14

                # Só conta como pisão quando o jogador vem de cima e está caindo.
                if enemy.can_be_stomped and player_is_falling and player_is_above_enemy:
                    stomped_enemy = True
                    continue

                player_was_hit = True

            remaining_enemies.append(enemy)

        self.enemies = remaining_enemies

        if player_was_killed:
            return "deadly"

        if stomped_enemy:
            player.bounce_after_stomp()

        if player_was_hit:
            return "hit"

        if stomped_enemy:
            return "stomp"

        return None

    def player_touched_enemy(self, player):
        return self.handle_enemy_contact(player) == "hit"

    def player_reached_exit(self, player):
        return player.actor.colliderect(self.exit) and len(self.crystals) == 0

    def _add_collect_effect(self, center):
        self.collect_effects.append(
            {
                "x": center[0],
                "y": center[1],
                "timer": 24,
            }
        )

    def _update_collect_effects(self):
        active_effects = []

        # Os efeitos sobem e somem depois de alguns frames.
        for effect in self.collect_effects:
            effect["timer"] -= 1
            effect["y"] -= 1

            if effect["timer"] > 0:
                active_effects.append(effect)

        self.collect_effects = active_effects

    def _draw_collect_effects(self, screen, camera_x):
        for effect in self.collect_effects:
            age = 24 - effect["timer"]
            radius = 6 + age // 2
            center = (effect["x"] - camera_x, effect["y"])
            screen.draw.circle(center, radius, (120, 245, 255))
            screen.draw.filled_circle(center, 2, (255, 255, 255))

    def _draw_whip_item(self, camera_x):
        if self.whip_item is None or self.whip_collected:
            return

        # O item flutua um pouco para se destacar dos cristais comuns.
        frame = (self.crystal_timer // 8) % 4
        bob = -4 + (self.crystal_timer // 6) % 9
        visible = self.whip_item.move(-camera_x, bob)
        item = Actor("whip_item_" + str(frame), visible.center)
        item.draw()

    def _draw_background(self, screen, camera_x):
        screen.fill(self.sky_color)

        # Camadas com velocidades diferentes criam uma sensação leve de profundidade.
        moon_x = 1080 - (camera_x * 0.08) % 1300
        screen.draw.filled_circle((moon_x, 105), 38, (204, 219, 224))
        screen.draw.filled_circle((moon_x + 16, 93), 35, self.sky_color)

        for index in range(12):
            star_x = index * 173 - (camera_x * 0.15) % 173
            star_y = 58 + (index * 37) % 155
            screen.draw.filled_circle((star_x, star_y), 2, (205, 230, 238))

        for index in range(8):
            x = index * 280 - (camera_x * 0.35) % 280
            screen.draw.filled_rect(
                Rect((x, 210), (130, 440)),
                (22, 27, 40),
            )
            screen.draw.filled_rect(
                Rect((x + 18, 250), (18, 24)),
                (65, 82, 107),
            )
            screen.draw.filled_rect(
                Rect((x + 74, 325), (18, 24)),
                (65, 82, 107),
            )

        for index in range(9):
            x = index * 230 - (camera_x * 0.55) % 230
            screen.draw.filled_rect(
                Rect((x, 520), (150, 130)),
                (17, 21, 31),
            )
