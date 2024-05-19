#!/usr/bin/python3
"""Script that defines User class that inherits from BaseModel."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represent a User class with following attr:
        email : (empty str)represent the email of the user.
        password : (empty str)represent the password of the user.
        first_name : (empty str)represent the first name of the user.
        last_name : (empty str)represent the last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
