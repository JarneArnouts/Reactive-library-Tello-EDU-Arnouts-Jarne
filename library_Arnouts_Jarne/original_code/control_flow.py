from rx import operators as ops
from rx.subject import Subject
from rx.core import Observer


class IFObserver(Observer):
    def __int__(self, executor):
        self.movement_executor = executor

    def on_next(self, value):
        if eval(value[1]):
            self.movement_executor.on_next(value[2])
        else:
            self.movement_executor.on_next(value[3])

    def on_completed(self):
        print("FOR observer process finished")

    def on_error(self, error):
        print("error in if observer: {0}".format(error))


class FORObserver(Observer):
    def __int__(self, executor):
        self.movement_executor = executor

    def on_next(self, value):
        for i in range(value[1]):
            self.movement_executor.on_next(value[2])

    def on_completed(self):
        print("FOR observer process finished")

    def on_error(self, error):
        print("error in for observer: {0}".format(error))


class ControlFLowController(object):
    def __init__(self, movement_executor):
        self.movement_executor = movement_executor
        self.control_flow_subject = Subject()
        self.if_subject = self.control_flow_subject.pipe(ops.filter(lambda structure:
                                                                    "if" in structure[0]))
        self.for_subject = self.control_flow_subject.pipe(ops.filter(lambda structure:
                                                                     "for" in structure[0]))
        self.if_observable = IFObserver(self.movement_executor)
        self.for_observable = FORObserver(self.movement_executor)
        self.if_subject.subscribe(self.if_observable)
        self.for_subject.subscribe(self.if_observable)
