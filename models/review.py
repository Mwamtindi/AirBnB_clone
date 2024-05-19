#!/usr/bin/python3
"""Script that defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """attributes:
        place_id : (empty str)represent the Place id.
        user_id : (empty str)represent the User id.
        text : (empty str)represent the text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
