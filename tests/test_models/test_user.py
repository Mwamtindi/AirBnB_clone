#!/usr/bin/python3
"""Defines unittests for user.py in models.
Unittest classes:
TestUserObject_instantiation
TestUserObject_save
TestUserObject_to_dict
"""
import os
import models
import unittest
from datetime import date_time_obj
from time import sleep
from models.user import User

class TestUserObject_instantiation(unittest.TestCase):
"""Unittests to test instantiation of User class."""

def test_no_args_instantiates(self):
    self.assertEqual(User, type(User()))

def test_new_instance_stored_in_objects(self):
    self.assertIn(User(), models.storage.all().values())

def test_id_is_public_str(self):
    self.assertEqual(str, type(User().id))

def test_created_at_is_public_datetime(self):
    self.assertEqual(date_time_obj, type(User().created_at))

def test_updated_at_is_public_datetime(self):
    self.assertEqual(date_time_obj, type(User().updated_at))

def test_email_is_public_str(self):
    self.assertEqual(str, type(User.email))

def test_password_is_public_str(self):
    self.assertEqual(str, type(User.password))

def test_first_name_is_public_str(self):
    self.assertEqual(str, type(User.first_name))

def test_last_name_is_public_str(self):
    self.assertEqual(str, type(User.last_name))

def test_two_users_unique_ids(self):
    user_obj1 = User()
    user_obj2 = User()
    self.assertNotEqual(user_obj1.id, user_obj2.id)

def test_two_users_different_created_at(self):
    user_obj1 = User()
    sleep(0.05)
    user_obj2 = User()
    self.assertLess(user_obj1.created_at, user_obj2.created_at)

def test_two_users_different_updated_at(self):
    user_obj1 = User()
    sleep(0.05)
    user_obj2 = User()
    self.assertLess(user_obj1.updated_at, user_obj2.updated_at)

def test_str_representation(self):
    date_time = date_time_obj.today()
    date_time_repr = repr(date_time)
    user_obj = User()
    user_obj.id = "123456"
    user_obj.created_at = user_obj.updated_at = date_time
    user_str = user_obj.__str__()
    self.assertIn("[User] (123456)", user_str)
    self.assertIn("'id': '123456'", user_str)
    self.assertIn("'created_at': " + date_time_repr, user_str)
    self.assertIn("'updated_at': " + date_time_repr, user_str)

def test_args_unused(self):
    user_obj = User(None)
    self.assertNotIn(None, user_obj.__dict__.values())

def test_instantiation_with_kwargs(self):
    date_time = date_time_obj.today()
    date_time_iso = date_time.isoformat()
    user_obj = User(id="345", created_at=date_time_iso, updated_at=date_time_iso)
    self.assertEqual(user_obj.id, "345")
    self.assertEqual(user_obj.created_at, date_time)
    self.assertEqual(user_obj.updated_at, date_time)

def test_instantiation_with_None_kwargs(self):
    with self.assertRaises(TypeError):
        User(id=None, created_at=None, updated_at=None)

class TestUserObject_save(unittest.TestCase):
"""Unittests to test save method of the User class."""

@classmethod
def setUp(self):
    try:
        os.rename("file.json", "temp_file")
    except IOError:
        pass

def tearDown(self):
    try:
        os.remove("file.json")
    except IOError:
        pass
    try:
        os.rename("temp_file", "file.json")
    except IOError:
        pass

def test_one_save(self):
    user_obj = User()
    sleep(0.05)
    first_updated_at = user_obj.updated_at
    user_obj.save()
    self.assertLess(first_updated_at, user_obj.updated_at)

def test_two_saves(self):
    user_obj = User()
    sleep(0.05)
    first_updated_at = user_obj.updated_at
    user_obj.save()
    second_updated_at = user_obj.updated_at
    self.assertLess(first_updated_at, second_updated_at)
    sleep(0.05)
    user_obj.save()
    self.assertLess(second_updated_at, user_obj.updated_at)

def test_save_with_arg(self):
    user_obj = User()
    with self.assertRaises(TypeError):
        user_obj.save(None)

def test_save_updates_file(self):
    user_obj = User()
    user_obj.save()
    user_id = "User." + user_obj.id
    with open("file.json", "r") as f:
        self.assertIn(user_id, f.read())

class TestUserObject_to_dict(unittest.TestCase):
"""Unittests to  test to_dict method of the User class."""

def test_to_dict_type(self):
    self.assertTrue(dict, type(User().to_dict()))

def test_to_dict_contains_correct_keys(self):
    user_obj = User()
    self.assertIn("id", user_obj.to_dict())
    self.assertIn("created_at", user_obj.to_dict())
    self.assertIn("updated_at", user_obj.to_dict())
    self.assertIn("__class__", user_obj.to_dict())

def test_to_dict_contains_added_attributes(self):
    user_obj = User()
    user_obj.middle_name = "Holberton"
    user_obj.my_number = 98
    self.assertEqual("Holberton", user_obj.middle_name)
    self.assertIn("my_number", user_obj.to_dict())

def test_to_dict_datetime_attributes_are_strs(self):
    user_obj = User()
    user_dict = user_obj.to_dict()
    self.assertEqual(str, type(user_dict["id"]))
    self.assertEqual(str, type(user_dict["created_at"]))
    self.assertEqual(str, type(user_dict["updated_at"]))

def test_to_dict_output(self):
    date_time = date_time_obj.today()
    user_obj = User()
    user_obj.id = "123456"
    user_obj.created_at = user_obj.updated_at = date_time
    to_dict = {
        'id': '123456',
        '__class__': 'User',
        'created_at': date_time.isoformat(),
        'updated_at': date_time.isoformat(),
    }
    self.assertDictEqual(user_obj.to_dict(), to_dict)

def test_contrast_to_dict_dunder_dict(self):
    user_obj = User()
    self.assertNotEqual(user_obj.to_dict(), user_obj.__dict__)

def test_to_dict_with_arg(self):
    user_obj = User()
    with self.assertRaises(TypeError):
        user_obj.to_dict(None)

if __name__ == "__main__":
    unittest.main()
