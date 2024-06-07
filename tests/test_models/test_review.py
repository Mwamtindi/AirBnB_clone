#!/usr/bin/python3
"""Defines unittests for review.py in models.
Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime_obj
from time import sleep_time
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests to test instantiation of review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime_obj, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime_obj, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        review_obj = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review_obj))
        self.assertNotIn("place_id", review_obj.__dict__)

    def test_user_id_is_public_class_attribute(self):
        review_obj = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review_obj))
        self.assertNotIn("user_id", review_obj.__dict__)

    def test_text_is_public_class_attribute(self):
        review_obj = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review_obj))
        self.assertNotIn("text", review_obj.__dict__)

    def test_two_reviews_unique_ids(self):
        review_obj1 = Review()
        review_obj2 = Review()
        self.assertNotEqual(review_obj1.id, review_obj2.id)

    def test_two_reviews_different_created_at(self):
        review_obj1 = Review()
        sleep_time(0.05)
        review_obj2 = Review()
        self.assertLess(review_obj1.created_at, review_obj2.created_at)

    def test_two_reviews_different_updated_at(self):
        review_obj1 = Review()
        sleep_time(0.05)
        review_obj2 = Review()
        self.assertLess(review_obj1.updated_at, review_obj2.updated_at)

    def test_str_representation(self):
        datetime_today = datetime_obj.today()
        datetime_repr = repr(datetime_today)
        review_obj = Review()
        review_obj.id = "123456"
        review_obj.created_at = review_obj.updated_at = datetime_today
        review_str = review_obj.__str__()
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + datetime_repr, review_str)
        self.assertIn("'updated_at': " + datetime_repr, review_str)

    def test_args_unused(self):
        review_obj = Review(None)
        self.assertNotIn(None, review_obj.__dict__.values())

    def test_instantiation_with_kwargs(self):
        datetime_today = datetime_obj.today()
        datetime_iso = datetime_today.isoformat()
        review_obj = Review(id="345", created_at=datetime_iso, updated_at=datetime_iso)
        self.assertEqual(review_obj.id, "345")
        self.assertEqual(review_obj.created_at, datetime_today)
        self.assertEqual(review_obj.updated_at, datetime_today)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests to test save method of review class."""

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
        review_obj = Review()
        sleep_time(0.05)
        first_updated_at = review_obj.updated_at
        review_obj.save()
        self.assertLess(first_updated_at, review_obj.updated_at)

    def test_two_saves(self):
        review_obj = Review()
        sleep_time(0.05)
        first_updated_at = review_obj.updated_at
        review_obj.save()
        second_updated_at = review_obj.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep_time(0.05)
        review_obj.save()
        self.assertLess(second_updated_at, review_obj.updated_at)

    def test_save_with_arg(self):
        review_obj = Review()
        with self.assertRaises(TypeError):
            review_obj.save(None)

    def test_save_updates_file(self):
        review_obj = Review()
        review_obj.save()
        review_id = "Review." + review_obj.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests to test to_dict method of review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        review_obj = Review()
        self.assertIn("id", review_obj.to_dict())
        self.assertIn("created_at", review_obj.to_dict())
        self.assertIn("updated_at", review_obj.to_dict())
        self.assertIn("__class__", review_obj.to_dict())

    def test_to_dict_contains_added_attributes(self):
        review_obj = Review()
        review_obj.middle_name = "Holberton"
        review_obj.my_number = 98
        self.assertEqual("Holberton", review_obj.middle_name)
        self.assertIn("my_number", review_obj.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        review_obj = Review()
        review_dict = review_obj.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        datetime_today = datetime_obj.today()
        review_obj = Review()
        review_obj.id = "123456"
        review_obj.created_at = review_obj.updated_at = datetime_today
        review_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': datetime_today.isoformat(),
            'updated_at': datetime_today.isoformat(),
        }
        self.assertDictEqual(review_obj.to_dict(), review_dict)

    def test_contrast_to_dict_dunder_dict(self):
        review_obj = Review()
        with self.assertRaises(TypeError):
            review_obj.to_dict(None)

    if __name__ == "__main__":
        unittest.main()
