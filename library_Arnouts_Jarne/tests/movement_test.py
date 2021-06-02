import unittest
import time
from library_Arnouts_Jarne.original_code.movement import MovementExecutor, commands_dict
from library_Arnouts_Jarne.official_sdk_files.tello import Tello


class MyTestCase(unittest.TestCase):

    # setup a drone before the test
    def setUp(self):
        self.drone = Tello('81.83.75.219', 3000)
        self.rate_of_change = 0.05
        self.degree_of_change = 45
        self.movement_executor = MovementExecutor(self.drone, self.rate_of_change, self.degree_of_change)
        self.movement_subject = self.movement_executor.movement_subject()

    # dispose of the classes after the test
    def tearDown(self):
        self.drone.__del__()
        self.movement_executor.__del__()

    # test if variables are correct upon creation and can be changed
    def test_variables(self):
        saved_roc = self.movement_executor.regular_observer.rate_of_change
        self.assertEqual(saved_roc, self.rate_of_change)
        saved_doc = self.movement_executor.rotation_observer.degree_of_change
        self.assertEqual(saved_doc, self.degree_of_change)

        self.movement_executor.adjust_rate_of_change(0.10)
        new_roc = self.movement_executor.regular_observer.rate_of_change
        self.assertEqual(new_roc, 0.10)
        self.movement_executor.adjust_degree_of_change(25)
        new_doc = self.movement_executor.rotation_observer.degree_of_change
        self.assertEqual(new_doc, 25)

    # test if custom commands can be added
    def test_commands(self):
        new_command = [["regular", "left"], ["regular", "right"], ["regular", "up"], ["regular", "down"]]
        self.movement_executor.add_custom_command("all_directions", new_command)
        self.assertEqual(commands_dict.get("all_direction"), new_command)

    # test takeoff and landing
    def test_takeoff_and_land(self):
        self.movement_subject.on_next(["regular", "takeoff"])
        time.sleep(5)
        new_height = self.drone.get_height()
        self.assertNotEqual(new_height, 0)

        self.movement_subject.on_next(["regular", "land"])
        time.sleep(5)
        new_height = self.drone.get_height()
        self.assertEqual(new_height, 0)

    # test basic movement
    def test_basic_movement(self):
        self.movement_subject.on_next(["regular", "takeoff"])
        time.sleep(5)
        new_height = self.drone.get_height()
        self.assertNotEqual(new_height, 0)

        self.movement_subject.on_next(["regular", "up"])
        time.sleep(2)
        height_after_up = self.drone.get_height()
        self.assertNotEqual(new_height, height_after_up)

        self.movement_subject.on_next(["regular", "down"])
        time.sleep(2)
        height_after_down = self.drone.get_height()
        self.assertGreater(height_after_up, height_after_down)

        self.movement_subject.on_next(["regular", "land"])
        time.sleep(5)
        new_height = self.drone.get_height()
        self.assertEqual(new_height, 0)

    # test movement with distance
    def test_basic_movement_distance(self):
        self.movement_subject.on_next(["regular", "takeoff"])
        time.sleep(5)
        new_height = self.drone.get_height()
        self.assertNotEqual(new_height, 0)

        self.movement_subject.on_next(["distance", ["up", 0.15]])
        time.sleep(2)
        height_after_up = self.drone.get_height()
        self.assertNotEqual(new_height, height_after_up)

        self.movement_subject.on_next(["distance", ["down", 0.20]])
        time.sleep(2)
        height_after_down = self.drone.get_height()
        self.assertGreater(height_after_up, height_after_down)

        self.movement_subject.on_next(["regular", "land"])
        time.sleep(5)
        new_height = self.drone.get_height()
        self.assertEqual(new_height, 0)


if __name__ == '__main__':
    unittest.main()
