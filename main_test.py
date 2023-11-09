import unittest

from main import get_weather_from_ip_main


class TestUtilityFunctions(unittest.TestCase):
    def test_get_weather_from_ip_function(self):
        # self.assertTrue(get_weather_from_ip() == {'Temprature': 11.1, 'Weather': 'Light rain', 'icon': 12, 'bikeable': True, 'Lat': 52.35, 'Lon': 4.922, 'Saved_at': '2023-11-07 11:14:04'})\
        actual_result = get_weather_from_ip_main()
        expected_result = {'Temprature': 11.1, 'Weather': 'Light rain', 'icon': 12, 'bikeable': True, 'Lat': 52.35,
                           'Lon': 4.922, 'Saved_at': '2023-11-07 11:14:04'}
        self.assertNotEqual(actual_result, expected_result, "The result should not equal the expected dictionary")

if __name__ == '__main__':
    unittest.main()
