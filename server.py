import socket
import time
import random


def remove_title(string, title):
    """
    string = title: data
    :param string: string having data in it
    :param title: starting title of line
    :return: str
    """
    return string[len(title) + 2:]


def find_semi_colon(string, index):
    count = -1
    last_comma = 1
    for i in range(len(string)):
        if string[i] == ';' or string[i] == '}':
            count += 1
            if count == index:
                return last_comma, i
            last_comma = i + 1  # it is not simi colon's index. it is next character's index.
    # if not found
    return -1, -1


def brace_data(string, index):
    semi_colon_pos = find_semi_colon(string, index)
    data = string[semi_colon_pos[0]:semi_colon_pos[1]].strip()
    if data != '':
        return eval(data)


def get_start_points(file_add):
    points = []
    map_file = open(file_add, 'r')
    for line in map_file:
        if line[0] == '#':
            continue
        elif 'Start_Point' in line:
            data_string = remove_title(line, "Start_Point").strip()
            pos = brace_data(data_string, 0)
            dire = brace_data(data_string, 1)
            points.append((pos, dire))
    return points

count_map = 4
i = random.randrange(1, count_map+1)
map_address = "maps/map{0}.txt".format(i)
tank_start_point = get_start_points(map_address)
print(tank_start_point)

host = "0.0.0.0"
port = 1377
clients = []
clients_data = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
quitting = False
print("Server Started")
counter = 0
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            data = data.decode()
            data = eval(data)
            tmp = [data[0], data[1]]
            print(clients)
            for client in clients:
                j = random.randrange(len(tank_start_point))
                tmp.append(map_address)
                tmp.append((tank_start_point[j]))  # tuple(...)
                tmp.append(len(clients))
                clients_data.append(tmp)
                s.sendto(("new len:" + str(len(clients)) + str(clients_data)).encode(), client)
            del tank_start_point[j]
            # del tank_start_point[j]
            print(time.ctime(time.time()) + str(addr) + " : : " + "Joined and his message is :" + str(data))
        else:
            if data.decode() == 'finish':
                counter += 1
                if counter == len(clients):
                    tmp2 = clients[:]
                    clients.clear()
                    data = 'restart'.encode()
                    print(data, tmp2)
                    for client in tmp2:
                        s.sendto(data, client)
                    del tmp2
            else:
                for client in clients:
                    s.sendto(data, client)
    except:
        pass
s.close()
