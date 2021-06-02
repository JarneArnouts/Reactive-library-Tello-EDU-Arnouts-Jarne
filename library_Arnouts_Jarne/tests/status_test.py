import unittest
import time
from library_Arnouts_Jarne.original_code.status import ResponseMonitor


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.response_monitor = ResponseMonitor(drone=None, max_height=20, min_height=10, command_observable=None)
        self.array = self.response_monitor.response_array
        self.response_subject = self.response_monitor.response_subject

    def tearDown(self):
        self.response_monitor.__del__()

    # check if all the correct warnings are given for certain values
    def test_warnings(self):
        self.array[0] = 1
        self.array[1] = 1
        self.array[2] = 620
        self.array[3] = 35
        self.array[4] = 5
        self.response_subject.on_next(self.array)
        time.sleep(2)
        flight_warning = self.response_monitor.flight_warning
        battery_warning = self.response_monitor.battery_warning
        height_warning = self.response_monitor.height_warning
        self.assertNotEqual(flight_warning, None)
        self.assertNotEqual(battery_warning, None)
        self.assertEqual(height_warning, "Drone is flying too high")

        self.array[2] = 400
        self.array[3] = 5
        self.array[4] = 25
        self.response_subject.on_next(self.array)
        time.sleep(2)
        height_warning = self.response_monitor.height_warning
        battery_warning = self.response_monitor.battery_warning
        flight_warning = self.response_monitor.flight_warning
        self.assertEqual(height_warning, "Drone is flying too low")
        self.assertEqual(battery_warning, None)
        self.assertEqual(flight_warning, None)


if __name__ == '__main__':
    unittest.main()
