# farbod shahinfar
# timer object
# 13/10/95
import time
from exceptions import ValueError


class Timer(object):
    def __init__(self, duration):
        self.set_time = time.time()
        self.time_duration = duration  # second
        self.is_set = False

    def is_time(self):
        if self.is_set:
            if time.time() - self.set_time >= self.time_duration:
                self.is_set = False
                return True
        return False

    def set_timer(self, dont_let_over_set=True):
        if dont_let_over_set:
            if not self.is_set:
                self.set_time = time.time()
                self.is_set = True
        else:
            self.set_time = time.time()
            self.is_set = True

    def set_duration(self, value):
        if isinstance(value, (int, float)):
            self.time_duration = value
        else:
            raise ValueError
