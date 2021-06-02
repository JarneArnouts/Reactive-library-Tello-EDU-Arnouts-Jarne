import unittest
from library_Arnouts_Jarne.official_sdk_files.tello_pose import Tello_Pose


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.pose = Tello_Pose()

    # test if commands can be changed for certain poses
    def test_pose_command_change(self):
        pose_dict = self.pose.pose_dict
        original_dict = {'Flat': "takeoff",
                         'Down': "down",
                         'V': "flipl",
                         'Up': "up",
                         'UpStraight': "rotate_cw ",
                         'DownStraight': "land"}
        self.assertEqual(pose_dict, original_dict)
        self.pose.change_pose_command(["V", "right"])
        pose_dict = self.pose.pose_dict
        new_dict = {'Flat': "takeoff",
                    'Down': "down",
                    'V': "right",
                    'Up': "up",
                    'UpStraight': "rotate_cw ",
                    'DownStraight': "land"}
        self.assertEqual(pose_dict, new_dict)


if __name__ == '__main__':
    unittest.main()
