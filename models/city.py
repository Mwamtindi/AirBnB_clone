#!/usr/bin/python3
"""Script that defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """attributes:
        state_id : (empty str)represent the state id.
        name : (empty str)represent the name of the city.
    """

    state_id = ""
    name = ""
