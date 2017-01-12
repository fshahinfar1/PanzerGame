# Farbod Shahinfar
# Panzer Game
# 22/10/95
# player class


class Player(object):
    def __init__(self, controller, panzer, key_map):
        # if using joystick then it should be supplied if keyboard a keyboard handler should be given
        self.controller = controller
        self.key_map = key_map
        self.panzer = panzer
        self.score = 0

    def get_panzer(self):
        return self.panzer

    def get_controller(self):
        return self.controller
