from dige_stl.basic_library.base_data_type import SwitchState


class ColorDelay:
    def __init__(self, delay=10):
        self.delay = delay
        self.color_keep = SwitchState.OFF
        self.time = 0

    def run(self, color):
        if color == SwitchState.ON and self.color_keep == SwitchState.OFF:
            self.color_keep = color
            self.time = 0
        elif self.color_keep == SwitchState.ON and self.time <= self.delay:
            self.time += 1
        elif self.time > self.delay:
            self.color_keep = SwitchState.OFF
        return self.color_keep


