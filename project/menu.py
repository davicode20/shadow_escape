from pgzero.rect import Rect


class Button:
    def __init__(self, text, center, width, height):
        self.text = text
        self.rect = Rect((0, 0), (width, height))
        self.rect.center = center

    def draw(self, screen, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        # Uma troca discreta de cor já deixa claro qual botão está selecionado.
        fill_color = (74, 93, 130) if hovered else (38, 45, 66)
        border_color = (151, 219, 201) if hovered else (95, 114, 151)

        screen.draw.filled_rect(self.rect, fill_color)
        screen.draw.rect(self.rect, border_color)
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=34,
            color="white",
        )

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class MainMenu:
    def __init__(self, width, height):
        center_x = width // 2
        # Os botões ficam centralizados para funcionar bem em uma tela fixa.
        self.start_button = Button("Iniciar Jogo", (center_x, 335), 340, 58)
        self.audio_button = Button("Musica e Sons: ON", (center_x, 415), 340, 58)
        self.quit_button = Button("Sair", (center_x, 495), 340, 58)
        self.buttons = [
            self.start_button,
            self.audio_button,
            self.quit_button,
        ]
        self.width = width
        self.height = height

    def set_audio_text(self, enabled):
        if enabled:
            self.audio_button.text = "Musica e Sons: ON"
        else:
            self.audio_button.text = "Musica e Sons: OFF"

    def draw(self, screen, mouse_pos):
        screen.fill((12, 15, 23))
        screen.draw.text(
            "SHADOW ESCAPE",
            center=(self.width // 2, 170),
            fontsize=78,
            color=(232, 244, 255),
        )
        screen.draw.text(
            "Colete os cristais azuis e alcance a saida.",
            center=(self.width // 2, 235),
            fontsize=30,
            color=(154, 174, 204),
        )

        for button in self.buttons:
            button.draw(screen, mouse_pos)

    def button_at(self, pos):
        # Traduz o clique em uma ação para o main.py tratar o fluxo do jogo.
        if self.start_button.clicked(pos):
            return "start"

        if self.audio_button.clicked(pos):
            return "audio"

        if self.quit_button.clicked(pos):
            return "quit"

        return None
