import tkinter as tki
import tkinter.ttk as ttk
from tkinter import Scale, Toplevel
from library_Arnouts_Jarne.original_code.ReactiveTello import ReactiveTello


# buttons for flips + adding custom command, that is it
class BasicApplication(object):

    def __init__(self):
        # setting up a tkinter root
        self.root = tki.Tk()
        self.root.geometry('750x100')
        self.root.wm_title("Simple tello app Arnouts Jarne")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        # setting up the drone and retrieving it's panel
        self.reactive_drone = ReactiveTello()
        self.panel = self.reactive_drone.panel
        # setting up for changing the pose mode
        self.pose_mode = None
        self.pose_mode_btn = None

        self.main_label = tki.Label(
            self.root,
            text="Open the different windows wit the buttons to control the drone and more"
        )
        self.main_label.grid(row=0, column=1)

        # buttons for opening the different modules
        self.control_window_btn = tki.Button(
            self.root,
            text="Open control window",
            relief="raised",
            command=lambda: self.open_control_window())
        self.control_window_btn.grid(row=1, column=0)

        self.control_flow_window_btn = tki.Button(
            self.root,
            text="Open control flow window",
            relief="raised",
            command=lambda: self.open_control_flow_window())
        self.control_flow_window_btn.grid(row=2, column=0)

        self.command_window_btn = tki.Button(
            self.root,
            text="Open commands window",
            relief="raised",
            command=lambda: self.open_command_window()
        )
        self.command_window_btn.grid(row=3, column=0)

        self.pose_window_btn = tki.Button(
            self.root,
            text="Open pose analysis window",
            relief="raised",
            command=lambda: self.open_pose_window())
        self.pose_window_btn.grid(row=1, column=1)

        # create button for changing the analysis mode
        self.pose_mode_btn = tki.Button(
            self.root,
            text="Change pose mode, currently: OFF",
            relief="raised",
            command=lambda: self.set_pose_mode())

        self.pose_mode_btn.grid(row=2, column=1)

        self.settings_window_btn = tki.Button(
            self.root,
            text="Open settings window",
            relief="raised",
            command=lambda: self.open_settings_window())
        self.settings_window_btn.grid(row=3, column=1)

        # buttons for takeoff and landing
        self.takeoff_btn = tki.Button(
            self.root,
            text="Takeoff",
            relief="raised",
            command=lambda: self.send_command(["movement_command", ["regular", "takeoff"]]))
        self.takeoff_btn.grid(row=1, column=2)

        self.land_btn = tki.Button(
            self.root,
            text="land",
            relief="raised",
            command=lambda: self.send_command(["movement_command", ["regular", "land"]]))
        self.land_btn.grid(row=2, column=2)

        self.root.mainloop()

    # what to do when closing the root window
    def on_close(self):
        self.reactive_drone.stop()
        self.root.quit()

    # sending commands to the drone
    def send_command(self, command):
        print("command accepted from GUI: {0}".format(command))
        self.reactive_drone.command_subject.on_next(command)

    # function for starting/stopping the analysation of the video stream
    def set_pose_mode(self):
        if self.pose_mode:
            self.pose_mode = False
            self.send_command(["adjust_video"])
            self.pose_mode_btn.config(text='Change pose mode, currently: OFF')

        else:
            self.pose_mode = True
            self.send_command(["adjust_video"])
            self.pose_mode_btn.config(text='Change pose mode, currently: ON')

    # opens window for regular movement
    def open_control_window(self):
        panel = Toplevel(self.root)
        panel.wm_title("Command Panel")

        # create text input entry
        text_controls = tki.Label(panel, text='Control the drone with the keyboard: controls are as follows')
        text_actual_controls = tki.Label(panel, text='   Z - Move up\t\t\tArrow Up - Move forward\n'
                                                     '        S - Move down\t\tArrow Down - Move backward\n'
                                                     'Q - Rotate counter-clockwise\tArrow Left - Move left\n'
                                                     '   D - Rotate clockwise\t\tArrow Right - Move right')
        text_controls.grid(row=0)
        text_actual_controls.grid(row=1)

        # create buttons for flips
        flipl_button = tki.Button(panel,
                                  text="flip left",
                                  relief="raised",
                                  command=lambda: self.send_command(["movement_command", ["regular", "flipl"]]))
        flipr_button = tki.Button(panel,
                                  text="flip right",
                                  relief="raised",
                                  command=lambda: self.send_command(["movement_command", ["regular", "flipr"]]))
        flipf_button = tki.Button(panel,
                                  text="flip forward",
                                  relief="raised",
                                  command=lambda: self.send_command(["movement_command", ["regular", "flipf"]]))
        flipb_button = tki.Button(panel,
                                  text="flip backward",
                                  relief="raised",
                                  command=lambda: self.send_command(["movement_command", ["regular", "flipb"]]))
        flipl_button.grid(row=2)
        flipr_button.grid(row=3)
        flipf_button.grid(row=4)
        flipb_button.grid(row=5)

        # binding arrow keys to drone control, intended for AZERTY keyboard
        tmp_f = tki.Frame(panel, width=100, height=2)
        tmp_f.bind('<KeyPress-z>', lambda arg: self.send_command(["movement_command", ["regular", "up"]]))
        tmp_f.bind('<KeyPress-s>', lambda arg: self.send_command(["movement_command", ["regular", "down"]]))
        tmp_f.bind('<KeyPress-q>', lambda arg: self.send_command(["movement_command", ["regular", "left"]]))
        tmp_f.bind('<KeyPress-d>', lambda arg: self.send_command(["movement_command", ["regular", "right"]]))
        tmp_f.bind('<KeyPress-Up>', lambda arg: self.send_command(["movement_command", ["regular", "forward"]]))
        tmp_f.bind('<KeyPress-Down>', lambda arg: self.send_command(["movement_command", ["regular", "backward"]]))
        tmp_f.bind('<KeyPress-Left>', lambda arg: self.send_command(["movement_command", ["regular", "left"]]))
        tmp_f.bind('<KeyPress-Right>', lambda arg: self.send_command(["movement_command", ["regular", "right"]]))
        tmp_f.grid(row=6)
        tmp_f.focus_set()

    def open_pose_window(self):
        panel = Toplevel(self.root)
        panel.wm_title("Pose and analysis panel")
        panel.geometry("500x75")

        # create button to change commands for certain poses
        command_label = tki.Label(panel, text="change pose command")
        command_label.grid(row=1)
        variable = tki.StringVar()
        pose_selector = ttk.Combobox(panel, width=10, textvariable=variable)
        pose_selector['values'] = ('select Pose',
                                   'flat',
                                   'V',
                                   'up',
                                   'down',
                                   'upStraight',
                                   'downStraight')
        pose_selector.current(0)
        pose_selector.grid(row=1, column=1)
        new_pose_text_area = tki.Entry(panel)
        new_pose_text_area.grid(row=1, column=2)
        pose_button = tki.Button(panel,
                                 text="Change command",
                                 relief="raised",
                                 command=lambda: self.send_command(["adjust_pose_commands",
                                                                    [pose_selector.get(), new_pose_text_area.get()]]))
        pose_button.grid(row=1, column=3)

    def open_control_flow_window(self):
        panel = Toplevel(self.root)
        panel.wm_title("Control flow ")

        label = tki.Label(panel, text="Control flow")
        label.grid(row=0, column=0)

        label_if = tki.Label(panel, text="if")
        label_if.grid(row=1)
        expression_if = tki.Entry(panel)
        expression_if.grid(row=1, column=1)
        label_then = tki.Label(panel, text="then")
        label_then.grid(row=1, column=2)
        command_then = tki.Entry(panel)
        command_then.grid(row=1, column=3)
        label_else = tki.Label(panel, text="else")
        label_else.grid(row=1, column=4)
        command_else = tki.Entry(panel)
        command_else.grid(row=1, column=5)
        if_button = tki.Button(panel,
                               text="start if",
                               relief="raised",
                               command=lambda: self.send_command(
                                   ["control_flow",
                                    ["if", expression_if.get(), command_then.get(), command_else.get()]]))
        if_button.grid(row=2)

        label_for = tki.Label(panel, text="for i in range(")
        label_for.grid(row=4)
        expression_for = tki.Entry(panel)
        expression_for.grid(row=4, column=1)
        label_for2 = tki.Label(panel, text="):")
        label_for2.grid(row=4, column=2)
        command_for = tki.Entry(panel)
        command_for.grid(row=5, column=1)
        if_button = tki.Button(panel,
                               text="start for",
                               relief="raised",
                               command=lambda: self.send_command(
                                   ["control_flow", ["for", expression_for.get(), command_for.get()]]))
        if_button.grid(row=6, column=0)

    def create_sequence(self, commands):
        new_list = []
        for command in commands:
            new_list.append(["regular", command])
        return new_list

    def open_command_window(self):
        # creates a panel for sending commands directly
        panel = Toplevel(self.root)
        panel.wm_title("Commands with distance")

        label = tki.Label(panel, text="Give basic command with distance")
        label.grid(row=0, column=1)

        label_format = tki.Label(panel, text="Format = [\"command\", distance]")
        label_format.grid(row=2, column=1)

        label_command = tki.Label(panel, text="drone.send_command(")
        label_command.grid(row=3)
        text_area = tki.Entry(panel)
        text_area.grid(row=3, column=1)
        command_close = tki.Label(panel, text=")")
        command_close.grid(row=3, column=2)

        command_button = tki.Button(panel,
                                    text="Send command",
                                    relief="raised",
                                    command=lambda: self.send_command(
                                        ["movement_command", ["distance", eval(text_area.get())]]))
        command_button.grid(row=4, column=1)

        label_nd = tki.Label(panel, text="Give command without distance")
        label_nd.grid(row=6, column=1)
        label_command_nd = tki.Label(panel, text="drone.send_command(")
        label_command_nd.grid(row=7)
        text_area_nd = tki.Entry(panel)
        text_area_nd.grid(row=7, column=1)
        command_close_nd = tki.Label(panel, text=")")
        command_close_nd.grid(row=7, column="2")
        command_button_nd = tki.Button(panel,
                                       text="Send command",
                                       relief="raised",
                                       command=lambda: self.send_command(
                                           ["movement_command", ["regular", eval(text_area.get())]]))
        command_button_nd.grid(row=8, column=1)

        label_new_com = tki.Label(panel, text="Create new commands")
        label_new_com.grid(row=10, column=1)
        label_com = tki.Label(panel, text="Command name")
        label_com.grid(row=11, column=0)
        com_area = tki.Entry(panel)
        com_area.grid(row=11, column=1)
        label_sequence = tki.Label(panel, text="Sequence")
        label_format = tki.Label(panel, text="Format = [\"command1\", \"command2\","
                                             "...]")
        label_sequence.grid(row=13, column=0)
        label_format.grid(row=12, column=1)
        sequence_area = tki.Entry(panel)
        sequence_area.grid(row=13, column=1)
        new_command_button = tki.Button(panel,
                                        text="create new command",
                                        relief="raised",
                                        command=lambda: self.send_command(["add_custom_command",
                                                                           com_area.get(),
                                                                           self.create_sequence(eval(sequence_area.get()))
                                                                           ]))
        new_command_button.grid(row=14, column=1)

    def open_settings_window(self):
        panel = Toplevel(self.root)
        panel.wm_title("Settings Panel")

        # changing distance and degree of change
        # distance
        distance_label = tki.Label(panel, text="Distance").grid(row=0)
        distance_bar = Scale(panel, from_=0.02, to=5, tickinterval=0.01, digits=3, resolution=0.01)
        distance_bar.set(0.05)
        distance_bar.grid(row=0, column=1)
        btn_distance = tki.Button(panel,
                                  text="Apply new distance",
                                  relief="raised",
                                  command=lambda: self.send_command(["adjustment_speed", distance_bar.get()]))
        btn_distance.grid(row=0, column=2)

        # degree
        degree_label = tki.Label(panel, text="Degree").grid(row=1)
        degree_bar = Scale(panel, from_=1, to=360, tickinterval=10)
        degree_bar.set(35)
        degree_bar.grid(row=1, column=1)
        btn_degree = tki.Button(panel,
                                text="Apply new degree",
                                relief="raised",
                                command=lambda: self.send_command(["adjustment_degree", degree_bar.get()]))
        btn_degree.grid(row=1, column=2)


BasicApplication()
