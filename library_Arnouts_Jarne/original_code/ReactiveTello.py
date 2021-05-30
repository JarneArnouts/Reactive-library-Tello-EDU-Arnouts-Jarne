from library_Arnouts_Jarne.official_sdk_files.tello import Tello
from library_Arnouts_Jarne.original_code.movement import MovementExecutor
from library_Arnouts_Jarne.original_code.status import ResponseMonitor
from library_Arnouts_Jarne.original_code.video import VideoMonitor
from library_Arnouts_Jarne.original_code.control_flow import ControlFLowController
from rx.subject import Subject
from rx.core import Observer
from PIL import Image
from PIL import ImageTk
import tkinter as tki


# observer for command stream for tello drone
class CommandObserver(Observer):

    def __init__(self, movement_executor, video_monitor, control_flow_controller):
        self.movement_executor = movement_executor
        self.video_monitor = video_monitor
        self.movement_subject = self.movement_executor.movement_subject
        self.control_flow_controller = control_flow_controller
        self.control_flow_subject = self.control_flow_controller.control_Flow_subject

    def on_next(self, value):
        if value[0] == "movement_command":
            self.movement_subject.on_next(value[1])
        elif value[0] == "adjustment_speed":
            self.movement_executor.adjust_rate_of_change(value[1])
        elif value[0] == "adjustment_degree":
            self.movement_executor.adjust_degree_of_change(value[1])
        elif value[0] == "adjust_video":
            self.video_monitor.change_analysis()
        elif value[0] == "adjust_pose_commands":
            self.video_monitor.change_pose_commands(value[1])
        elif value[0] == "add_custom_command":
            self.movement_executor.add_custom_command(value[1], value[2])
        elif value[0] == "control_flow":
            self.control_flow_subject.on_next(value[1])
        else:
            print("no such command")

    def on_completed(self):
        print("observing of commands is complete")

    def on_error(self, error):
        print("error in main command stream: {0}".format(error))


# create a wrapper for a tello drone using reactive streams
class ReactiveTello(object):

    def __init__(self, ip_address='81.83.75.219', local_port=3000, tello_ip='192.168.10.1', tello_port=8889):
        # create a tello object to interact with the drone, taken from official Tello SDK
        self.drone = Tello(local_ip=ip_address, local_port=local_port, tello_ip=tello_ip, tello_port=tello_port)

        # create a movement executor, contains an observable that controls sending commands to the
        self.movement_executor = MovementExecutor(drone=self.drone, rate_of_change=0.05, degree_of_change=45)

        # create an observable for control flow
        self.control_flow_controller = ControlFLowController(self.movement_executor)

        # create a monitoring observable that can handle drone responses
        self.response_monitor = ResponseMonitor(self.drone, 10, 200, self.movement_executor.movement_subject)

        # creating a video monitor
        # creating a panel for display with an initial frame from the droen
        frame = self.drone.read()
        image = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image)
        self.panel = tki.Label(image=image)
        self.panel.image = image
        self.panel.pack(side="left", padx=10, pady=10)
        # creating the monitor
        self.video_monitor = VideoMonitor(self.drone, self.panel, self.movement_executor)

        # create a stream to receive all possible commands
        self.command_subject = Subject()
        # create observer and subscribe to the stream
        self.command_observer = CommandObserver(self.movement_executor, self.video_monitor)
        self.command_subject.subscribe(self.command_observer)

    def accept_command_chain(self, commands):
        for com in commands:
            self.command_subject.on_next(com)

    def stop(self):
        self.drone.land()
        del self.drone
        self.drone.__del__()
        self.movement_executor.__del__()
        self.video_monitor.__del__()
        self.response_monitor.__del__()
        self.command_subject.dispose()
