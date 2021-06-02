import threading

import numpy as np
from rx import operators as ops
from rx.subject import Subject
from rx.core import Observer
from datetime import datetime
import time


# observer classes
class ResponseObserver(Observer):

    def __init__(self, max_height, min_height, command_observable, response_monitor):
        self.now = datetime.now()
        self.max_height = max_height
        self.min_height = min_height
        self.command_observable = command_observable
        self.response_monitor = response_monitor

    def check_for_automatic_control(self, height):
        if height > self.max_height:
            warning = "Drone is flying too high"
            print(warning)
            self.response_monitor.height_warning = warning
            difference = height - self.max_height
            if self.command_observable is not None:
                self.command_observable.on_next(["distance", ["down", difference]])
        elif self.min_height > height > 2:
            warning = "Drone is flying too low"
            print(warning)
            self.response_monitor.height_warning = warning
            difference = self.min_height - height
            if self.command_observable is not None:
                self.command_observable.on_next(["distance", ["up", difference]])
        elif self.response_monitor.height_warning is not None:
            self.response_monitor.height_warning = None

    def on_next(self, response_array):
        print("New readings at time: {0}\n"
              "Drone response: {1}\n"
              "Drone speed: {2}\n"
              "Drone flight time: {3}\n"
              "Drone height: {4}\n"
              "Drone battery: {5}\n"
              .format(self.now.strftime("%H:%M:%S"),
                      response_array[0],
                      response_array[1],
                      response_array[2],
                      response_array[3],
                      response_array[4]))
        if response_array[2] >= 600:
            warning = "**!!WARNING!!** Drone has been flying for 10 minutes, prepare to stop execution"
            print(warning)
            self.response_monitor.flight_warning = warning
        elif self.response_monitor.flight_warning is not None:
            self.response_monitor.flight_warning = None
        if response_array[4] <= 10:
            warning = "**!!WARNING!!** Drone battery at less than 10 percent, prepare to stop execution"
            print(warning)
            self.response_monitor.battery_warning = warning
        elif self.response_monitor.battery_warning is not None:
            self.response_monitor.battery_warning = None
        self.check_for_automatic_control(response_array[3])

    def on_completed(self):
        print("observation complete")

    def on_error(self, error):
        print("error in observation: {0}".format(error))


# class that houses an observables for monitoring all drone information
class ResponseMonitor(object):

    def __init__(self, drone, max_height, min_height, command_observable):
        # local variables
        self.drone = drone
        self.response_subject = Subject()
        self.response_observer = ResponseObserver(max_height, min_height, command_observable, self)
        self.response_array = [0, 0, 0, 0, 0]
        self.flight_warning = None
        self.battery_warning = None
        self.height_warning = None
        # subscribe to the stream
        self.response_subject.subscribe(self.response_observer)
        # start a thread that collects the frames that will later be handled by the streams
        self.stop = threading.Event()
        self.driver_loop()
        self.thread = threading.Thread(target=self.driver_loop(), args=())
        self.thread.start()

    def driver_loop(self):
        if self.drone is not None:
            while not self.stop.is_set():
                self.response_array[0] = self.drone.get_response()
                self.response_array[1] = self.drone.get_speed()
                self.response_array[2] = self.drone.get_flight_time()
                self.response_array[3] = self.drone.get_height()
                self.response_array[4] = self.drone.get_battery()
                self.response_subject.on_next(self.response_array)
                time.sleep(3)

    def __del__(self):
        self.stop.set()
        self.response_subject.dispose()
