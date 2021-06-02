import unittest
import time
from library_Arnouts_Jarne.original_code.video import VideoMonitor


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.video = VideoMonitor(None, None, None)
        self.analyser = self.video.video_analysis_observer
        self.pose = self.analyser.tello_pose_analysis
        self.basic = self.video.basic_video_observer

    def tearDown(self):
        self.video.__del__()

    def test_pose_command(self):
        new_command = "flipr"
        self.video.change_pose_commands(["V", new_command])
        time.sleep(1)
        updated_command = self.pose.pose_dict.get("V")
        self.assertEqual(new_command, updated_command)

    def test_analysis(self):
        self.assertEqual(self.basic.show, True)
        self.assertEqual(self.analyser.analysis, False)
        self.video.change_analysis()
        self.assertEqual(self.basic.show, False)
        self.assertEqual(self.analyser.analysis, True)


if __name__ == '__main__':
    unittest.main()
