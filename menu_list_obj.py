# 7/10/95
# Panzer Game
# menu list obj
import label_obj
import position_class
import my_pygame_tools as tools
cp = tools.Colors()


class Menu:
    def __init__(self, pos):
        self.label_list = []
        self.count_labels = 0
        self.pos = position_class.Position(pos)
        self.size = (0, 0)
        self.padding = [10, 10, 50]  # top, left, between

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.label_list.clear()
        del self.label_list
        del self.count_labels
        del self.pos
        del self.size
        del self.padding

    def get_size(self):
        return self.size

    def add_label(self, *labels):
        # label position is not important it will be set again here
        space_top = self.padding[0]
        space_left = self.padding[1]
        space_between = self.padding[2]
        pre_w = 0
        w = 0
        h = 0
        for label in labels:
            if isinstance(label, label_obj.Label):
                new_index = self.count_labels
                new_pos = self.pos + (space_left, space_top + new_index * (space_top + space_between))
                label.change_pos(new_pos)
                self.label_list.append(label)
                self.count_labels += 1
                h += label.get_height()
                w = label.get_width()
                w = max(pre_w, w)
                pre_w = w
            else:
                raise TypeError
        self.size = (w + 2 * space_left, h + 2 * space_top + (self.count_labels - 1) * space_between)

    def what_is_label_index(self, label):
        if label in self.label_list:
            return self.label_list.index(label)
        return -1

    def change_label_index(self, index, new_index):
        tmp_label = self.label_list[index]
        self.label_list.insert(new_index, tmp_label)
        del self.label_list[index + 1]

    def get_rect(self):
        return [self.pos[0], self.pos[1], self.size[0], self.size[1]]

    def mouse_on_index(self, mp):
        if not isinstance(mp, position_class.Position):
            mp = position_class.Position(mp)
        if tools.is_in_rectangle(mp, self.get_rect()):
            for index in range(len(self.label_list)):
                if self.label_list[index].is_mouse_on():
                    return index
        return None

    def draw(self, screen):
        for label in self.label_list:
            label.draw(screen)
