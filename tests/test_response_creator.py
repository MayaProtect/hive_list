import unittest

from uuid import uuid4
from datetime import timezone, datetime
from colorama import Fore
from app import ResponseCreator, Hive


class TestResponseCreator(unittest.TestCase):
    def test_instance(self):
        hives = []
        for i in range(0, 8):
            hives.append(self.generate_hive())
        hives_to_test = []
        for hive in hives:
            hives_to_test.append(hive[1])
        response_creator = ResponseCreator(hives_to_test, 50, 1, 25)
        self.assertTrue(type(response_creator) is ResponseCreator)

    def test_create_response(self):
        hives = []
        for i in range(0, 25):
            hives.append(self.generate_hive())

        hives_to_test = []
        for hive in hives:
            hives_to_test.append(hive[1])

        expected_hives = []
        for hive in hives:
            expected_hives.append(hive[0].__to_json__())

        expected = {
            "hives": expected_hives,
            "actual_page": 1,
            "elements_per_page": 25,
            "count_hives": 25
        }
        self.maxDiff = None
        response_creator = ResponseCreator(hives_to_test, 25, 1, 25)
        self.assertEqual(response_creator.create_response(), expected)

    def test_raise_exception_if_response_is_none(self):
        with self.assertRaises(ValueError):
            ResponseCreator(None, 50, 1, 25)

    def test_raise_exception_if_response_is_not_a_cursor_or_list(self):
        with self.assertRaises(TypeError):
            ResponseCreator(1, 50, 1, 25)

    def test_raise_exception_if_total_count_is_none(self):
        with self.assertRaises(ValueError):
            ResponseCreator([], None, 1, 25)

    def test_raise_exception_if_total_count_is_not_an_int(self):
        with self.assertRaises(TypeError):
            ResponseCreator([], "50", 1, 25)

    def test_raise_exception_if_page_is_none(self):
        with self.assertRaises(ValueError):
            ResponseCreator([], 50, None, 25)

    def test_raise_exception_if_page_is_not_an_int(self):
        with self.assertRaises(TypeError):
            ResponseCreator([], 50, "1", 25)

    def test_raise_exception_if_page_size_is_none(self):
        with self.assertRaises(ValueError):
            ResponseCreator([], 50, 1, None)

    def test_raise_exception_if_page_size_is_not_an_int(self):
        with self.assertRaises(TypeError):
            ResponseCreator([], 50, 1, "25")

    @staticmethod
    def generate_hive():
        uuid_hive = uuid4()
        uuid_station = uuid4()
        uuid_owner = uuid4()
        name_owner = "John Doe"
        data = {
            "uuid": uuid_hive.bytes,
            "station_uuid": uuid_station.bytes,
            "owner": {
                "uuid": uuid_owner.bytes,
                "name": name_owner
            },
            "temperature": 20.0,
            "sound_level": 67.3,
            "weight": 37.5,
            "events": []
        }
        hive = Hive(data)

        return hive, data, uuid_hive, uuid_station, uuid_owner, name_owner

    @classmethod
    def tearDownClass(cls):
        print(Fore.YELLOW + ">>>>>> End of ResponseCreator tests" + Fore.RESET)

    @classmethod
    def setUpClass(cls):
        print(Fore.GREEN + ">>>>>> Start of ResponseCreator tests" + Fore.RESET)
