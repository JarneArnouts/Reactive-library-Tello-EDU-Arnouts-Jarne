from rx import operators as ops
from rx.subject import Subject
from rx.core import Observer
import time


# handling movement by passing it to the drone object of the official SDK

# takeoff and landing
def handle_altitude_command(command, drone, response_subject):
    if "takeoff" in command:
        response_subject.on_next(drone.takeoff())
    elif "land" in command:
        response_subject.on_next(drone.land())


# regular movement
def handle_regular_command(command, drone, rate_of_change, response_subject, subject):
    if "up" in command:
        response_subject.on_next(drone.move_up(rate_of_change))
    elif "down" in command:
        response_subject.on_next(drone.move_down(rate_of_change))
    elif "left" in command:
        response_subject.on_next(drone.move_left(rate_of_change))
    elif "right" in command:
        response_subject.on_next(drone.move_right(rate_of_change))
    elif "forward" in command:
        response_subject.on_next(drone.move_forward(rate_of_change))
    elif "backward" in command:
        response_subject.on_next(drone.move_backward(rate_of_change))
    else:
        handle_custom_command(command, subject)


# custom commands
commands_dict = {'flipTwice': [["regular", "flipl"], ["regular", "flipr"]]}


def handle_custom_command(command, movement_subject):
    command_chain = commands_dict[command]
    if command_chain:
        for command_to_execute in command_chain:
            movement_subject.on_next(command_to_execute)
    else:
        print("command not found")


# rotation movement
def handle_rotation_command(command, drone, degree, response_subject):
    if "rotate_cw" in command:
        response_subject.on_next(drone.rotate_cw(degree))
    elif "rotate_ccw" in command:
        response_subject.on_next(drone.rotate_cw(degree))


# trick movement (ex: flips)
def handle_trick_command(command, drone, response_subject):
    direction = command[4]
    response_subject.on_next(drone.flip(direction))


# observers for the command data stream
class BasicMovementExecutionObserver(Observer):

    def __init__(self, drone, rate_of_change, response_subject, subject):
        self.drone = drone
        self.rate_of_change = rate_of_change
        self.response_subject = response_subject
        self.subject = subject

    def on_next(self, value):
        handle_regular_command(value, self.drone, self.rate_of_change, self.response_subject, self.subject)
        time.sleep(0.5)

    def on_completed(self):
        print("execution process completed")

    def on_error(self, error):
        print("error in regular movement: {0}".format(error))


class DistanceMovementExecutionObserver(Observer):

    def __init__(self, drone, response_subject, creator):
        self.drone = drone
        self.response_subject = response_subject
        self.creator = creator

    def on_next(self, value):
        handle_regular_command(value[0], self.drone, value[1], self.response_subject, self.creator)
        time.sleep(0.5)

    def on_completed(self):
        print("execution process completed")

    def on_error(self, error):
        print("error in regular movement: {0}".format(error))


class RotationMovementExecutionObserver(Observer):

    def __init__(self, drone, response_subject, degree_of_change):
        self.drone = drone
        self.response_subject = response_subject
        self.degree_of_change = degree_of_change

    def on_next(self, value):
        handle_rotation_command(value, self.drone, self.response_subject, self.degree_of_change)
        time.sleep(0.5)

    def on_completed(self):
        print("execution process completed")

    def on_error(self, error):
        print("error in rotation movement: {0}".format(error))


class AltitudeMovementExecutionObserver(Observer):

    def __init__(self, drone, response_subject):
        self.drone = drone
        self.response_subject = response_subject

    def on_next(self, value):
        handle_altitude_command(value, self.drone, self.response_subject)
        time.sleep(0.5)

    def on_completed(self):
        print("execution process completed")

    def on_error(self, error):
        print("error in altitude movement: {0}".format(error))


class TrickMovementExecutionObserver(Observer):

    def __init__(self, drone, response_subject):
        self.drone = drone
        self.response_subject = response_subject

    def on_next(self, value):
        handle_trick_command(value, self.drone, self.response_subject)
        time.sleep(0.5)

    def on_completed(self):
        print("execution process completed")

    def on_error(self, error):
        print("error in trick movement: {0}".format(error))


class LogObserver(Observer):

    def on_next(self, value):
        print(value)

    def on_completed(self):
        print("log process completed")

    def on_error(self, error):
        print("error in logging: {0}".format(error))


# class to be exported to command the drone using reactive streams
class MovementExecutor(object):

    def __init__(self, drone, rate_of_change, degree_of_change):
        # basic subject for movement commands and responses
        self.movement_subject = Subject()
        self.response_subject = Subject()
        # original split
        self.movement_subject_no_distance = self.movement_subject.pipe(ops.filter(lambda command:
                                                                                  "regular" in command[0]),
                                                                       ops.map(lambda command:
                                                                               command[1]))
        self.movement_subject_distance = self.movement_subject.pipe(ops.filter(lambda command:
                                                                               "distance" in command[0]),
                                                                    ops.map(lambda command:
                                                                            command[1]))
        # further filtering the
        self.trick_movement_subject = self.movement_subject_no_distance.pipe(ops.filter(lambda command:
                                                                                        "flip" in command))
        self.rotation_subject = self.movement_subject_no_distance.pipe(ops.filter(lambda command:
                                                                                  "rotate_ccw" in command or
                                                                                  "rotate_cw" in command))
        self.altitude_movement_subject = self.movement_subject_no_distance.pipe(ops.filter(lambda command:
                                                                                           "Takeoff" in command or
                                                                                           "Land" in command))
        self.regular_movement_subject = self.movement_subject_no_distance.pipe(ops.filter(lambda command:
                                                                                          not ("takeoff" in command or
                                                                                               "land" in command or
                                                                                               "flip" in command or
                                                                                               "rotate_ccw" in command or
                                                                                               "rotate_cw" in command)))
        # observer instances
        self.altitude_observer = AltitudeMovementExecutionObserver(drone, self.response_subject)
        self.regular_observer = BasicMovementExecutionObserver(drone, rate_of_change,
                                                               self.response_subject,
                                                               self.movement_subject)
        self.distance_observer = DistanceMovementExecutionObserver(drone, self.response_subject, self)
        self.rotation_observer = RotationMovementExecutionObserver(drone, self.response_subject, degree_of_change)
        self.trick_observer = TrickMovementExecutionObserver(drone, self.response_subject)
        self.log_observer = LogObserver()
        # observe the different streams
        self.altitude_movement_subject.subscribe(self.altitude_observer)
        self.regular_movement_subject.subscribe(self.regular_observer)
        self.movement_subject_distance.subscribe(self.distance_observer)
        self.rotation_subject.subscribe(self.rotation_observer)
        self.trick_movement_subject.subscribe(self.trick_observer)
        self.response_subject.subscribe(self.log_observer)

    def adjust_rate_of_change(self, amount):
        if 0.02 < amount <= 5:
            self.regular_observer.rate_of_change = amount
        else:
            print("error: value for rate of change is out of bounds: {0}. "
                  "Should be between 0.02 and 5 meters".format(amount))

    def adjust_degree_of_change(self, amount):
        if 0 < amount <= 360:
            self.rotation_observer.degree_of_change = amount
        else:
            print("error: value for degree of change is out of bounds: {0}. "
                  "Should be between 0 and 360 degrees".format(amount))

    def add_custom_command(self, command, execution):
        commands_dict[command] = execution

    def __del__(self):
        self.movement_subject.dispose()
        self.response_subject.dispose()
