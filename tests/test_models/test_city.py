#!/usr/bin/python3
"""Defines unittests for city.py in models.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City

class TestCity_instantiation(unittest.TestCase):
    """Unittests to test instantiation of city class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city_instance = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city_instance))
        self.assertNotIn("state_id", city_instance.__dict__)

    def test_name_is_public_class_attribute(self):
        city_instance = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city_instance))
        self.assertNotIn("name", city_instance.__dict__)

    def test_two_cities_unique_ids(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_two_cities_different_created_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_two_cities_different_updated_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_str_representation(self):
        current_datetime = datetime.today()
        current_datetime_repr = repr(current_datetime)
        city_instance = City()
        city_instance.id = "123456"
        city_instance.created_at = city_instance.updated_at = current_datetime
        city_str = city_instance.__str__()
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + current_datetime_repr, city_str)
        self.assertIn("'updated_at': " + current_datetime_repr, city_str)

    def test_args_unused(self):
        city_instance = City(None)
        self.assertNotIn(None, city_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        current_datetime = datetime.today()
        current_datetime_iso = current_datetime.isoformat()
        city_instance = City(id="345", created_at=current_datetime_iso, updated_at=current_datetime_iso)
        self.assertEqual(city_instance.id, "345")
        self.assertEqual(city_instance.created_at, current_datetime)
        self.assertEqual(city_instance.updated_at, current_datetime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests to test save method of city class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        self.assertLess(first_updated_at, city_instance.updated_at)

    def test_two_saves(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        second_updated_at = city_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city_instance.save()
        self.assertLess(second_updated_at, city_instance.updated_at)

    def test_save_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.save(None)

    def test_save_updates_file(self):
        city_instance = City()
        city_instance.save()
        city_id = "City." + city_instance.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests to test to_dict method of City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        city_instance = City()
        self.assertIn("id", city_instance.to_dict())
        self.assertIn("created_at", city_instance.to_dict())
        self.assertIn("updated_at", city_instance.to_dict())
        self.assertIn("__class__", city_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city_instance = City()
        city_instance.middle_name = "Holberton"
        city_instance.my_number = 98
        self.assertEqual("Holberton", city_instance.middle_name)
        self.assertIn("my_number", city_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city_instance = City()
        city_dict = city_instance.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        current_datetime = datetime.today()
        city_instance = City()
        city_instance.id = "123456"
        city_instance.created_at = city_instance.updated_at = current_datetime
        expected_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': current_datetime.isoformat(),
            'updated_at': current_datetime.isoformat(),
        }
        self.assertDictEqual(city_instance.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        city_instance = City()
        self.assertNotEqual(city_instance.to_dict(), city_instance.__dict__)

    def test_to_dict_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.to_dict(None)

if __name__ == "__main__":
    unittest.main()
