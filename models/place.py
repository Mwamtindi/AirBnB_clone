#!/usr/bin/python3
"""Script that defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """attributes:
        city_id : string that rep City id.
        user_id : string that rep User id.
        name : string that rep name of the place.
        description : string that rep description of the place.
        number_rooms : integer that rep number of rooms of the place.
        number_bathrooms : integer that rep number of bathrooms of the place.
        max_guest : integer that rep maximum number of guests of the place.
        price_by_night : integer that rep price by night of the place.
        latitude : float that rep latitude of the place.
        longitude : float that rep longitude of the place.
        amenity_ids : list that rep a list of Amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
