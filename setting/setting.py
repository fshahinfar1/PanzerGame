import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Game-Setting")
        self.set_border_width(10)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        self.control_list = Gtk.ListStore(str)
        self.control_list.append(["KeySetOne"])
        self.control_list.append(["KeySetTwo"])
        self.control_list.append(["KeySetThree"])
        self.control_list.append(["JoystickSetOne"])
        self.player_number = 0
        self.rows = []
        self.setting_file = open('setting.txt', 'w')
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        ## Players Stack
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(spacing=6)
        self.rows.append(row1)
        label = Gtk.Label(label="Number of players")
        row1.add(label)
        adjustment = Gtk.Adjustment(0 ,0, 100, 1, 10, 0)
        self.spin_button = Gtk.SpinButton()
        self.spin_button.set_adjustment(adjustment)
        self.spin_button.set_numeric(True)
        policy = Gtk.SpinButtonUpdatePolicy.ALWAYS
        self.spin_button.set_update_policy(policy)
        row1.pack_end(self.spin_button, False, False, 0)
        self.vbox2.add(row1)
        stack.add_titled(self.vbox2, "players-setting", "Players")
        # Done Button player-setting
        row1 = Gtk.Box(spacing=6)
        self.rows.append(row1)
        button = Gtk.Button("Done")
        button.connect("clicked", self.done_clicked)
        row1.add(button)
        self.vbox2.add(row1)
        ## Screen Stack
        label = Gtk.Label(label="Screen size")
        stack.add_titled(label, "screen-setting", "Screen")
        
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)
    
    def done_clicked(self, button):
        self.spin_button.set_editable(False)
        self.rows[1].remove(button)
        del self.rows[1]
        player_count = self.spin_button.get_value_as_int()
        self.player_number = player_count
        for i in range(1, player_count+1):
            row1 = Gtk.Box(spacing=6)
            self.rows.append(row1)
            s = "player-"+str(i)
            label = Gtk.Label(label=s)
            row1.add(label)
            combo = Gtk.ComboBox.new_with_model(self.control_list)
            combo.connect("changed", self.combo_changed, i)
            render_text = Gtk.CellRendererText()
            combo.pack_start(render_text, True)
            combo.add_attribute(render_text, "text", 0)
            row1.add(combo)
            entry = Gtk.Entry()
            row1.add(entry)
            self.vbox2.pack_start(row1, True, True, 0)
        button.disconnect_by_func(self.done_clicked)
        button.connect("clicked", self.player_done_clicked)
        row1 = Gtk.Box(spacing=6)
        self.rows.append(row1)
        row1.add(button)
        self.vbox2.pack_start(row1, True, True, 0)
        self.show_all()
        self.setting_file.write("player_num: {%d}\n" % self.player_number)
        self.setting_file.write("##\n")

    def player_done_clicked(self, button):
        for i in range(self.player_number):
            self.setting_file.write("#player_%d:\n" % i)
            self.setting_file.write("start\n")
            combo = self.rows[i+1].get_children()[1]
            tree_iter = combo.get_active_iter()
            model = combo.get_model()
            control = model[tree_iter][:2][0]
            if "Joystick" in control:
                idx = self.rows[i+1].get_children()[3].get_text()
                print(idx)
                self.setting_file.write("control: {\"%s\"; %s}\n" % (control, idx))
            else:
                self.setting_file.write("control: {\"%s\"}\n" % control)
            entry = self.rows[i+1].get_children()[2]
            name = entry.get_text()
            self.setting_file.write("name: {\"%s\"}\n" % name)
            img = "images/panzer2.png"
            self.setting_file.write("image: {\"%s\"}\n" % img)
            self.setting_file.write("end\n##\n")
        self.setting_file.close()
        Gtk.main_quit()

    def combo_changed(self, combo, row):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            name = model[tree_iter][:2][0]
            row1 = self.rows[row]
            if "Joystick" in name:
                entry = Gtk.Entry()
                row1.add(entry)
                self.show_all()
            else:
                children = row1.get_children()
                if len(children) > 3:
                    row1.remove(children[3])
            

win = MyWindow()
win.connect("delete_event", Gtk.main_quit)
win.show_all()
Gtk.main()
