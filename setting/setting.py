import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk


class player:
    def __init__(self):
        self.control = ""
        self.name = ""
        self.img = ""


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
        self.players = []
        self.rows = []
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
        number_plyers = self.spin_button.get_value_as_int()
        for i in range(1,number_plyers+1):
            row1 = Gtk.Box(spacing=6)
            self.rows.append(row1)
            s = "player-"+str(i)
            label = Gtk.Label(label=s)
            row1.add(label)
            combo = Gtk.ComboBox.new_with_model(self.control_list)
            combo.connect("changed", self.combo_changed)
            render_text = Gtk.CellRendererText()
            combo.pack_start(render_text, True)
            combo.add_attribute(render_text, "text", 0)
            row1.add(combo)

            self.vbox2.pack_start(row1, True, True, 0)
        button.disconnect_by_func(self.done_clicked)
        button.connect("clicked", self.player_done_clicked)
        row1 = Gtk.Box(spacing=6)
        self.rows.append(row1)
        row1.add(button)
        self.vbox2.pack_start(row1, True, True, 0)
        self.show_all()
        print(number_plyers)

    def player_done_clicked(self, button):
        print("gsadhasgjdsagjdg")
        pass

    def combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            name = model[tree_iter][:2]
            print("name = %s" % name)

win = MyWindow()
win.connect("delete_event", Gtk.main_quit)
win.show_all()
Gtk.main()
        