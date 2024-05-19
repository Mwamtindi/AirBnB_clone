#!/usr/bin/python3
"""BaseModel class that defines all common attributes."""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """The BaseModel class of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args : (any)Not used.
            **kwargs : (dict)Key-value pairs rep the attributes.
        """
        tmformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for cu, dt in kwargs.items():
                if cu == "created_at" or cu == "updated_at":
                    self.__dict__[cu] = datetime.strptime(dt, tmformat)
                else:
                    self.__dict__[cu] = dt
        else:
            models.storage.new(self)

    def save(self):
        """Update public instance attr updated_at with the current datetime.
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns a dict containing all leys/values of __dict__ of instance
        Including a key __class__ with class name of the object
        """
        retdicty = self.__dict__.copy()
        retdicty["created_at"] = self.created_at.isoformat()
        retdicty["updated_at"] = self.updated_at.isoformat()
        retdicty["__class__"] = self.__class__.__name__
        return retdicty

    def __str__(self):
        """Returns the print rep of the BaseModel instance."""
        clsname = self.__class__.__name__
        return "[{}] ({}) {}".format(clsname, self.id, self.__dict__)
