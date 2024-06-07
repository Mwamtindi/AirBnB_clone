#!/usr/bin/python3
"""Defines unittests for state.py in models.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime_obj
from time import sleep_time
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests to test instantiation of state class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime_obj, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime_obj, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        state_obj = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state_obj))
        self.assertNotIn("name", state_obj.__dict__)

    def test_two_states_unique_ids(self):
        state_obj1 = State()
        state_obj2 = State()
        self.assertNotEqual(state_obj1.id, state_obj2.id)

    def test_two_states_different_created_at(self):
        state_obj1 = State()
        sleep_time(0.05)
        state_obj2 = State()
        self.assertLess(state_obj1.created_at, state_obj2.created_at)

    def test_two_states_different_updated_at(self):
        state_obj1 = State()
        sleep_time(0.05)
        state_obj2 = State()
        self.assertLess(state_obj1.updated_at, state_obj2.updated_at)

    def test_str_representation(self):
        datetime_today = datetime_obj.today()
        datetime_repr = repr(datetime_today)
        state_obj = State()
        state_obj.id = "123456"
        state_obj.created_at = state_obj.updated_at = datetime_today
        state_str = state_obj.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + datetime_repr, state_str)
        self.assertIn("'updated_at': " + datetime_repr, state_str)

    def test_args_unused(self):
        state_obj = State(None)
        self.assertNotIn(None, state_obj.__dict__.values())

    def test_instantiation_with_kwargs(self):
        datetime_today = datetime_obj.today()
        datetime_iso = datetime_today.isoformat()
        state_obj = State(id="345", created_at=datetime_iso, updated_at=datetime_iso)
        self.assertEqual(state_obj.id, "345")
        self.assertEqual(state_obj.created_at, datetime_today)
        self.assertEqual(state_obj.updated_at, datetime_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests to test save method of state class."""

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
        state_obj = State()
        sleep_time(0.05)
        first_updated_at = state_obj.updated_at
        state_obj.save()
        self.assertLess(first_updated_at, state_obj.updated_at)

    def test_two_saves(self):
        state_obj = State()
        sleep_time(0.05)
        first_updated_at = state_obj.updated_at
        state_obj.save()
        second_updated_at = state_obj.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep_time(0.05)
        state_obj.save()
        self.assertLess(second_updated_at, state_obj.updated_at)

    def test_save_with_arg(self):
        state_obj = State()
        with self.assertRaises(TypeError):
            state_obj.save(None)

    def test_save_updates_file(self):
        state_obj = State()
        state_obj.save()
        state_id = "State." + state_obj.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests to test to_dict method of state class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        state_obj = State()
        self.assertIn("id", state_obj.to_dict())
        self.assertIn("created_at", state_obj.to_dict())
        self.assertIn("updated_at", state_obj.to_dict())
        self.assertIn("__class__", state_obj.to_dict())

    def test_to_dict_contains_added_attributes(self):
        state_obj = State()
        state_obj.middle_name = "Holberton"
        state_obj.my_number = 98
        self.assertEqual("Holberton", state_obj.middle_name)
        self.assertIn("my_number", state_obj.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        state_obj = State()
        state_dict = state_obj.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        datetime_today = datetime_obj.today()
        state_obj = State()
        state_obj.id = "123456"
        state_obj.created_at = state_obj.updated_at = datetime_today
        state_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': datetime_today.isoformat(),
            'updated_at': datetime_today.isoformat(),
        }
        self.assertDictEqual(state_obj.to_dict(), state_dict)

    def test_contrast_to_dict_dunder_dict(self):
        state_obj = State()
        self.assertNotEqual(state_obj.to_dict(), state_obj.__dict__)

    def test_to_dict_with_arg(self):
        state_obj = State()
        with self.assertRaises(TypeError):
            state_obj.to_dict(None)


if __name__ == "__main__":
    unittest.main()
