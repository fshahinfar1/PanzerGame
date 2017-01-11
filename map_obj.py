# Farbod Shahinfar
# 16/10/95
# map_obj

class Map:
    def __init__(self, file_add):
        map_file = open(file_add, 'r')
        for line in map_file:
            if line[0] == '#':
                continue
            if 'Size' in line:
                line = line[5:]
                line = line.strip()
                t = line.split()
                self.size =