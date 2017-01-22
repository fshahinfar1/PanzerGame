# 7/10/95
# position class


class Position(object):

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    # todo overload this function
    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y

    def __str__(self):
        return '[{0},{1}]'.format(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, (Position, tuple, list)):
            new_x = self.x + other[0]
            new_y = self.y + other[1]
            return Position((new_x, new_y))
        else:
            print("Type Error")
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, (Position, tuple, list)):
            new_x = self.x - other[0]
            new_y = self.y - other[1]
            return Position((new_x, new_y))
        else:
            print("Type Error")
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, (Position, tuple, list,)):
            new_x = self.x * other[0]
            new_y = self.y * other[1]
            return Position((new_x, new_y))
        elif isinstance(other, (int, float)):
            new_x = self.x * other
            new_y = self.y * other
            return Position((new_x, new_y))
        else:
            print("Type Error")
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_x = self.x / other
            new_y = self.y / other
            return Position((new_x, new_y))
        else:
            print("Type Error")
            raise TypeError

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            print("Index out of range")
            raise TypeError

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            print("Index out of range")
            raise TypeError

    def __iter__(self):
        for i in range(2):
            yield self[i]

    def __len__(self):
        return 2

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get(self):
        return self.x, self.y

    def set(self, new_pos, rel=False):
        if rel:
            self.x += new_pos[0]
            self.y += new_pos[1]
        else:
            self.x, self.y = new_pos

    def int_cordinates(self):
        return int(self[0]), int(self[1])

    def __copy__(self):
        return Position(self)
