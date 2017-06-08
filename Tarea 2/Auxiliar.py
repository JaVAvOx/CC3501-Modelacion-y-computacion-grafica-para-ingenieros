from constants import *
class Aux:

    """clase que guarda las variables del juego"""

    def __init__(self):

        self.current_points = 1
        self.extra_ball_c = 0
        self.mouse_state = True
        self.generate = True
        self.can_play = True
        self.position_s = False
        self.pointer_init = WS / 2
        self.counter = 0

    def increase_points(self):
        self.current_points += 1

    def increase_balls(self):
        self.extra_ball_c += 1

    def get_pointer(self):
        return self.pointer_init

    def mouse_change(self):
        self.mouse_state = not self.mouse_state

    def get_points_ammount(self):
        return self.current_points

    def get_extra_balls(self):
        return self.extra_ball_c

    def get_mouse_state(self):
        return self.mouse_state

    def reset(self):
        self.current_points = 1
        self.extra_ball_c = 0
        self.mouse_state = True
        self.generate = True
        self.can_play = True
        self.position_s = False
        self.pointer_init = WS / 2
        self.counter = 0
