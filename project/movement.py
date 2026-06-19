GRAVITY = 0.7
MAX_FALL_SPEED = 14


class PlatformMovement:
    def __init__(self, speed, jump_strength):
        self.speed = speed
        self.jump_strength = jump_strength
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

    def read_input(self, keyboard):
        # A velocidade horizontal é recalculada a cada frame conforme o teclado.
        self.velocity_x = 0

        if keyboard.left or keyboard.a:
            self.velocity_x = -self.speed
            self.facing_right = False

        if keyboard.right or keyboard.d:
            self.velocity_x = self.speed
            self.facing_right = True

        if (keyboard.up or keyboard.w or keyboard.space) and self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY

        # Limita a queda para manter o controle e evitar atravessar plataformas.
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

    def is_moving(self):
        return self.velocity_x != 0


class PatrolMovement:
    def __init__(self, left_limit, right_limit, speed):
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = speed
        self.direction = 1

    def update(self, actor):
        actor.x += self.speed * self.direction

        # Ao bater no limite da patrulha, corrige a posição e inverte o lado.
        if actor.x < self.left_limit:
            actor.x = self.left_limit
            self.direction = 1

        if actor.x > self.right_limit:
            actor.x = self.right_limit
            self.direction = -1

        actor.flip_x = self.direction < 0


class FlyingPatrolMovement:
    def __init__(self, left_limit, right_limit, speed, wave_height):
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = speed
        self.wave_height = wave_height
        self.direction = 1
        self.timer = 0

    def update(self, actor):
        self.timer += 1
        actor.x += self.speed * self.direction
        # O voo usa a posição inicial como referência para uma onda vertical.
        actor.y = actor.base_y + self._wave_offset()

        if actor.x < self.left_limit:
            actor.x = self.left_limit
            self.direction = 1

        if actor.x > self.right_limit:
            actor.x = self.right_limit
            self.direction = -1

        actor.flip_x = self.direction < 0

    def _wave_offset(self):
        phase = self.timer % 80

        # O movimento é feito em trechos lineares para ficar simples e previsível.
        if phase < 20:
            return -self.wave_height * phase / 20

        if phase < 60:
            return -self.wave_height + self.wave_height * (phase - 20) / 20

        return self.wave_height - self.wave_height * (phase - 60) / 20
