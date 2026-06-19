from pgzero.actor import Actor
from pgzero.rect import Rect

from animation import SpriteAnimation
from movement import FlyingPatrolMovement, PatrolMovement


class Enemy:
    def __init__(self, x, y, left_limit, right_limit, speed):
        self.actor = Actor("enemy_idle_0", (x, y))
        self.animation = SpriteAnimation(
            ["enemy_idle_0", "enemy_idle_1", "enemy_idle_2", "enemy_idle_3"],
            ["enemy_walk_0", "enemy_walk_1", "enemy_walk_2", "enemy_walk_3"],
            10,
        )
        self.movement = PatrolMovement(left_limit, right_limit, speed)
        self.pause_timer = 0
        # Inimigos comuns podem ser derrotados pulando em cima deles.
        self.can_be_stomped = True
        self.is_deadly = False

    def update(self):
        if self.pause_timer > 0:
            self.pause_timer -= 1
            self.animation.set_state("idle")
        else:
            self.movement.update(self.actor)
            self.animation.set_state("move")

            # A pausa nas extremidades deixa a patrulha com um ritmo menos mecânico.
            if self.actor.x == self.movement.left_limit:
                self.pause_timer = 24

            if self.actor.x == self.movement.right_limit:
                self.pause_timer = 24

        self.animation.update()
        self.actor.image = self.animation.current_image()

    def draw(self, camera_x=0):
        real_x = self.actor.x
        self.actor.x -= camera_x
        self.actor.draw()
        self.actor.x = real_x

    def get_hitbox(self):
        return Rect(
            (self.actor.x - 17, self.actor.y - 17),
            (34, 34),
        )


class BatEnemy:
    def __init__(self, x, y, left_limit, right_limit, speed):
        self.actor = Actor("bat_fly_0", (x, y))
        self.actor.base_y = y
        self.animation = SpriteAnimation(
            ["bat_fly_0", "bat_fly_1", "bat_fly_2", "bat_fly_3"],
            ["bat_fly_0", "bat_fly_1", "bat_fly_2", "bat_fly_3"],
            7,
        )
        self.movement = FlyingPatrolMovement(left_limit, right_limit, speed, 20)
        # Morcegos são um perigo direto: não dá para derrotar pisando neles.
        self.can_be_stomped = False
        self.is_deadly = True

    def update(self):
        self.movement.update(self.actor)
        self.animation.set_state("move")
        self.animation.update()
        self.actor.image = self.animation.current_image()

    def draw(self, camera_x=0):
        real_x = self.actor.x
        self.actor.x -= camera_x
        self.actor.draw()
        self.actor.x = real_x

    def get_hitbox(self):
        return Rect(
            (self.actor.x - 20, self.actor.y - 13),
            (40, 26),
        )
