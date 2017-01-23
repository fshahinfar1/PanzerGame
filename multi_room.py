# 3/11/95
# Test Room
import pygame
import room_obj
import player_class
import wall_obj
import map_obj
import fire_load
import collectable_object
import image_class
import collision_tools
import timer_obj
import my_pygame_tools as tools
from random import randrange
import sys
import key_map_sets
import socket
cp = tools.Colors()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# host = "172.17.11.170"
host = "0.0.0.0"
port = 1377
server = (host, port)
s.setblocking(0)


class MultiRoom(room_obj.Room):
    def __init__(self, screen, clock):
        room_obj.Room.__init__(self, screen, 'MultiRoom', clock=clock, caption="PanzerGame")
        # key_set = key_map_sets.KeySetOne()
        # p = player_class.Player('KeySetOne', key_set.control, key_set.key_map, "p1", None)
        key_set = key_map_sets.KeySetTwo()
        p = player_class.Player('KeySetTwo', key_set.control, key_set.key_map, "p2", None)
        message2 = '("' + p.name + '",'+'"' + p.key_set + '")'
        s.sendto(message2.encode(), server)
        data = []
        player_num = 1
        while True:
            try:
                message = s.recv(1024).decode()
                player_num = int(message[8:9])
                data = eval(message[9:])
                break
            except:
                pass
        print(data)
        # "maps/map{0}.txt".format(data[0][1])
        # data = [['name', 'key_set_name', 'full_map_add', (pos, dire), img_number], [...], ...]
        map_address = data[0][2]
        print(map_address)
        map_obj.load(map_address)
        for i in range(0, player_num):
            img = pygame.image.load('images/panzer{0}.png'.format(data[i][-1])).convert_alpha()
            if i != player_num-1:
                key_set = key_map_sets.control_map[data[i][1]]()
                player = player_class.Player(data[i][1], key_set.control, key_set.key_map, data[i][0], img)
            else:
                player = player_class.player_list[0]
                player.panzer_img = img
            pos = data[i][3][0]
            dire = data[i][3][1]
            player.ready_panzer(pos, dire, self.clock, self)
        self.mouse = tools.Mouse()
        self.timer = timer_obj.Timer(3)  # 3 sec
        self.keys = [False for i in range(400)]

    def destroy(self):
        room_obj.Room.destroy(self)
        del self.mouse
        collectable_object.clear()
        collision_tools.clear()
        fire_load.clear()
        wall_obj.clear()

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.flag_GameOver = True
                self.flag_end = True
            elif event.type == pygame.KEYDOWN:
                if event.key in player_class.player_list[0].key_map.values():
                    s.sendto(str(pygame.key.get_pressed()).encode(), server)
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                    return
                elif event.key == pygame.K_BACKSPACE:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.KEYUP:
                if event.key in player_class.player_list[0].key_map.values():
                    s.sendto(str(pygame.key.get_pressed()).encode(), server)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.event_btn_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.event_btn_released(event)

    def check_hold_self(self, key):
        # self.keys[key]
        return pygame.key.get_pressed()[key]
    
    def check_hold_other(self, key):
        # pygame.key.get_pressed()[key] or
        return self.keys[key]

    def recv_anything(self):
        try:
            message = s.recv(1024).decode()
            if 'new' in message:
                data = eval(message[9:])
                player_num = int(message[8:9])
                # data = [eval(i) for i in data]
                print(data)
                if player_num > len(player_class.player_list):
                    key_set = key_map_sets.control_map[data[-1][1]]()
                    img = pygame.image.load('images/panzer{0}.png'.format(data[-1][-1])).convert_alpha()
                    pos = data[-1][3][0]
                    dire = data[-1][3][1]
                    new_player = player_class.Player(data[-1][1], key_set.control, key_set.key_map, data[-1][0], img)
                    new_player.ready_panzer(pos, dire, self.clock, self)
            elif 'restart' in message:
                self.__init__(self.clock, "maps/map01.txt")
                return False
            else:
                data = eval(message)
                self.keys = data
                return True
        except:
            pass

    def run_logic(self):
        self.recv_anything()
        if len(player_class.player_list)>1 and player_class.active_player() < 2:
            self.timer.set_timer()
            if self.timer.is_time():
                self.change_map()
                return
        player = player_class.player_list[0]
        if player.controller_type() == "keyboard":
            # turn
            if self.check_hold_self(player.key_map['rotate_right']):
                player.get_panzer().key_right()
            elif self.check_hold_self(player.key_map['rotate_left']):
                player.get_panzer().key_left()
            # forward / backward
            if self.check_hold_self(player.key_map['forward']):
                player.get_panzer().key_up()
            elif self.check_hold_self(player.key_map['backward']):
                player.get_panzer().key_down()
            else:
                player.get_panzer().set_acceleration(0)
            # fire
            if self.check_hold_self(player.key_map['fire']):
                player.get_panzer().key_space()
        for player in player_class.player_list[1:]:
            if player.killed:
                continue
            if player.controller_type() == "keyboard":
                # turn
                if self.check_hold_other(player.key_map['rotate_right']):
                    player.get_panzer().key_right()
                elif self.check_hold_other(player.key_map['rotate_left']):
                    player.get_panzer().key_left()
                # forward / backward
                if self.check_hold_other(player.key_map['forward']):
                    player.get_panzer().key_up()
                elif self.check_hold_other(player.key_map['backward']):
                    player.get_panzer().key_down()
                else:
                    player.get_panzer().set_acceleration(0)
                # fire
                if self.check_hold_other(player.key_map['fire']):
                    player.get_panzer().key_space()
            elif player.controller_type() == "joystick":
                # turn
                hat_num = player.get_controller().get_hat(0)
                if hat_num[0] == 1:
                    player.get_panzer().key_right()
                elif hat_num[0] == -1:
                    player.get_panzer().key_left()
                # forward / backward
                if hat_num[1] == 1 or player.get_controller().get_button(5):
                    player.get_panzer().key_up()
                elif hat_num[1] == -1 or player.get_controller().get_button(4):
                    player.get_panzer().key_down()
                else:
                    player.get_panzer().set_acceleration(0)
                # fire
                if player.get_controller().get_button(2):
                    player.get_panzer().key_space()
        # mouse
        if self.mouse.is_btn_pressed(1):
            print('left_btn_pressed')
        if self.mouse.is_btn_pressed(2):
            print('right_btn_pressed')
        # object loop
        [player.get_panzer().loop() for player in player_class.player_list if not player.killed]
        [load.loop() for load in fire_load.FireLoadObjectsList]

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        [obj.draw(self.screen) for obj in collectable_object.object_list]  # draw collectable objects
        [player.get_panzer().draw(self.screen) for player in player_class.player_list if not player.killed]  # draw tanks
        [load.draw(self.screen) for load in fire_load.FireLoadObjectsList]  # draw bullets
        [wall.draw(self.screen) for wall in wall_obj.object_list]  # draw walls
        [ani.draw(self.screen) for ani in image_class.object_list]
        k = 0
        for player in player_class.player_list:
            pos = (50+k*120, 760)
            player.draw(self.screen, pos)
            k += 1
        pygame.display.update()  # update display

    def change_map(self):

        print("map_changed")
        s.sendto('finish'.encode(), server)
        [player.destroy() for player in player_class.player_list]
        player_class.player_list.clear()
        self.destroy()
        flag_restart = True
        while flag_restart:
            flag_restart = self.recv_anything()
