import threading

from rx import operators as ops
from rx.subject import Subject
from rx.core import Observer
import tkinter as tki
from PIL import Image
from PIL import ImageTk
import cv2
from library_Arnouts_Jarne.official_sdk_files.tello_pose import Tello_Pose


# observer classes
class BasicVideoObserver(Observer):

    def __init__(self, panel):
        self.panel = panel
        self.show = True

    def on_next(self, value):
        if self.show:
            # reformat the frame into a usable image
            image = Image.fromarray(value)
            image = ImageTk.PhotoImage(image)
            # update the panel
            self.panel.configure(image=image)
            self.panel.image = image

    def on_completed(self):
        print("video stream complete")

    def on_error(self, error):
        print("error with video stream: {0}".format(error))


class VideoAnalysisObserver(Observer):

    def __int__(self, panel, observable):
        self.observable = observable
        self.panel = panel
        self.analyse = False
        self.my_tello_pose = Tello_Pose()
        self.draw_skeleton = False
        # record the coordinates of the nodes in the pose recognition skeleton
        self.points = []
        # list of all the possible connections between skeleton nodes
        self.POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9], [9, 10],
                           [14, 11], [11, 12], [12, 13]]

    def on_next(self, value):
        if self.analyse:
            frame = cv2.bilateralFilter(value, 5, 50, 100)
            self.points.append(None)
            cmd, self.draw_skeleton, self.points = self.my_tello_pose.detect(frame)
            if cmd != '':
                self.observable.on_next(cmd)
            # Draw the detected skeleton points
            for i in range(15):
                if self.draw_skeleton:
                    cv2.circle(frame, self.points[i], 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                    cv2.putText(frame, "{}".format(i), self.points[i], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                                lineType=cv2.LINE_AA)
                # Draw Skeleton
            for pair in self.POSE_PAIRS:
                partA = pair[0]
                partB = pair[1]
                if self.points[partA] and self.points[partB]:
                    cv2.line(frame, self.points[partA], self.points[partB], (0, 255, 255), 2)
                    cv2.circle(frame, self.points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

            # reformat the frame into a usable image
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)
            # update the panel
            self.panel.configure(image=image)
            self.panel.image = image

    def on_completed(self):
        print("video analysis complete")

    def on_error(self, error):
        print("error with video analysis: {0}".format(error))


# class that houses an observables for moitoring all drone information
class VideoMonitor(object):

    def __init__(self, drone, panel, observable):
        # local variables
        self.drone = drone
        self.video_subject = Subject()
        self.basic_video_observer = BasicVideoObserver(panel)
        self.video_analysis_observer = VideoAnalysisObserver(panel, observable)
        # subscribe to the stream
        self.video_subject.subscribe(self.basic_video_observer)
        self.video_subject.subscribe(self.video_analysis_observer)
        # start a thread that collects the frames that will later be handled by the streams
        self.stop = threading.Event()
        self.driver_loop()
        self.thread = threading.Thread(target=self.driver_loop(), args=())
        self.thread.start()

    def change_analysis(self):
        self.video_analysis_observer.analyse = not self.video_analysis_observer.analyse
        self.basic_video_observer.show = not self.basic_video_observer.show

    def change_pose_commands(self, change):
        self.video_analysis_observer.my_tello_pose.change_pose_command(change)

    def driver_loop(self):
        while not self.stop.is_set():
            frame = self.drone.read
            if frame is None or frame.size == 0:
                continue
            self.video_subject.on_next(frame)

    def __del__(self):
        self.stop.set()
        self.video_subject.dispose()
