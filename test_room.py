# farbod shahinfar
# 7/10/95
# Test Room
import pygame
import room_obj
import panzer_obj
import wall_obj
import collision_tools
import my_pygame_tools as tools
cp = tools.Colors()


class TestRoom(room_obj.Room):
    def __init__(self, clock):
        room_obj.Room.__init__(self, 'Test', clock=clock)  # create room with name Test
        panzer_img = pygame.image.load("images/panzer.png")
        self.panzer = panzer_obj.Panzer((80, 80), panzer_img, (54, 54), self.clock, self)
        self.wall_list = []
        self.wall_init()
        self.fire_load_list = []
        self.mouse = tools.Mouse()

    def wall_init(self):
        wall_img = pygame.image.load("images/wall.png")
        wall = wall_obj.Wall(wall_img, (54, 14), (250, 250), direction=90)
        wall2 = wall_obj.Wall(wall_img, (54, 14), (303, 250), direction=90)
        wall3 = wall_obj.Wall(wall_img, (54, 14), (400, 250), direction=0)
        self.wall_list += [wall, wall2, wall3]

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.flag_GameOver = True
                self.flag_end = True
            elif event.type == pygame.KEYDOWN:
                self.panzer.keyboard.get_event(event)
            elif event.type == pygame.KEYUP:
                self.panzer.keyboard.get_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.event_btn_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.event_btn_released(event)

    def run_logic(self):
        # keyboard
        # turn
        if self.panzer.keyboard.is_key_hold('right'):
            self.panzer.key_right()
        elif self.panzer.keyboard.is_key_hold('left'):
            self.panzer.key_left()
        # forward / backward
        if self.panzer.keyboard.is_key_hold('up'):
            self.panzer.key_up()
        elif self.panzer.keyboard.is_key_hold('down'):
            self.panzer.key_down()
        else:
            self.panzer.set_acceleration(0)
        # fire
        if self.panzer.keyboard.is_key_hold('space'):
            load = self.panzer.key_space()
            if load is not None:
                self.fire_load_list.append(load)
                load.link_holder(self.fire_load_list)
        # mouse
        if self.mouse.is_btn_pressed(1):
            pass
        # collision logic
        if self.panzer.collision_obj.is_colliding_with(self.wall_list[0].collision_obj):
            self.panzer.set_speed(0)
            self.panzer.set_acceleration(0)
            self.panzer.set_position(self.panzer.collision_obj.move_to_edge(self.wall_list[0].collision_obj, self.panzer.direction))
            print(self.wall_list[0].pos)
            print(self.panzer.position)
            print('Collision ***')
        # object loop
        self.panzer.loop()
        [load.loop() for load in self.fire_load_list]
        # for load in self.fire_load_list:
        #     temp = load.loop()
        #     if temp:
        #         load.destroy()
        #         self.fire_load_list.remove(load)

        collision_tools.update_collidable_objects_list_position()

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        self.panzer.draw(self.screen)
        [wall.draw(self.screen) for wall in self.wall_list]
        [load.draw(self.screen) for load in self.fire_load_list]
        pygame.display.flip()  # update display
