class SpriteAnimation:
    """Controls frame changes for idle and movement sprite animations."""

    def __init__(self, idle_frames, move_frames, frame_time):
        self.frames = {
            "idle": idle_frames,
            "move": move_frames,
        }
        self.frame_time = frame_time
        self.state = "idle"
        self.frame_index = 0
        self.timer = 0

    def set_state(self, state):
        if state == self.state:
            return

        self.state = state
        self.frame_index = 0
        self.timer = 0

    def update(self):
        current_frames = self.frames[self.state]
        self.timer += 1

        if self.timer >= self.frame_time:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(current_frames)

    def current_image(self):
        return self.frames[self.state][self.frame_index]
