#!/usr/bin/python3
"""Script that defines FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent the  storage engine.
    attributes:
        __file_path (string): path to the JSON file.
        __objects (dicty): empty but will store all objects by class name id.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj_class_name>.id"""
        otsname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(otsname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file(path: __file__path."""
        jecdict = FileStorage.__objects
        jectdict = {obj: jecdict[obj].to_dict() for obj in jecdict.keys()}
        with open(FileStorage.__file_path, "w") as file_obj:
            json.dump(jectdict, file_obj)

    def reload(self):
        """Deserialize the JSON file to __objects if it JSON file exists;
        otherwise, do nothing.
        """
        try:
            with open(FileStorage.__file_path) as file_handl:
                jectdict = json.load(file_handl)
                for s in jectdict.values():
                    c_name = s["__class__"]
                    del s["__class__"]
                    self.new(eval(c_name)(**s))
        except FileNotFoundError:
            return
