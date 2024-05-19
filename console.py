#!/usr/bin/python3
"""Script that defines HBnB console related to the HolbertonBnB project"""
import cmd
import re
from models import storage
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def parse(arg):
    cur_braces = re.search(r"\{(.*?)\}", arg)
    kets = re.search(r"\[(.*?)\]", arg)
    if cur_braces is None:
        if kets is None:
            return [e.strip(",") for e in split(arg)]
        else:
            ex = split(arg[:kets.span()[0]])
            tl = [e.strip(",") for e in ex]
            tl.append(kets.group())
            return tl
    else:
        ex = split(arg[:cur_braces.span()[0]])
        tl = [e.strip(",") for e in ex]
        tl.append(cur_braces.group())
        return tl


class HBNBCommand(cmd.Cmd):
    """attributes:
        prompt: (string) represent the command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Shouldn't execute anything."""
        pass

    def default(self, arg):
        """A default state  for the cmd module when input is not valid"""
        argdicty = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            gl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", gl[1])
            if match is not None:
                command = [gl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdicty.keys():
                    ll = "{} {}".format(gl[0], command[1])
                    return argdicty[command[0]](ll)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit implemented by command interpreter to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF implemented by command interpreter to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """
        Create a new class instance of BaseModel.
        """
        gl = parse(arg)
        if len(gl) == 0:
            print("** class name missing **")
        elif gl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(gl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Prints the string rep of an instance based on the class name and id.
        """
        gl = parse(arg)
        obj_dict = storage.all()
        if len(gl) == 0:
            print("** class name missing **")
        elif gl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(gl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], gl[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(gl[0], gl[1])])

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        """
        gl = parse(arg)
        obj_dict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif gl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(gl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(gl[0], gl[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(gl[0], gl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Prints all string representations of all instances based or
        +not on the class name.
        """
        gl = parse(arg)
        if len(gl) > 0 and gl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj = []
            for ob in storage.all().values():
                if len(gl) > 0 and gl[0] == ob.__class__.__name__:
                    obj.append(ob.__str__())
                elif len(gl) == 0:
                    obj.append(ob.__str__())
            print(obj)

    def do_count(self, arg):
        """
        Give out the number of instances of the class given."""
        gl = parse(arg)
        cnt = 0
        for ob in storage.all().values():
            if gl[0] == ob.__class__.__name__:
                cnt += 1
        print(cnt)

    def do_update(self, arg):
        """
        Update an instance based on the class name and id by adding or
        updating attribute."""
        gl = parse(arg)
        obj_dict = storage.all()

        if len(gl) == 0:
            print("** class name missing **")
            return False
        if gl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(gl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(gl[0], gl[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(gl) == 2:
            print("** attribute name missing **")
            return False
        if len(gl) == 3:
            try:
                type(eval(gl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(gl) == 4:
            ob = obj_dict["{}.{}".format(gl[0], gl[1])]
            if gl[2] in ob.__class__.__dict__.keys():
                vl_type = type(ob.__class__.__dict__[gl[2]])
                ob.__dict__[gl[2]] = vl_type(gl[3])
            else:
                ob.__dict__[gl[2]] = gl[3]
        elif type(eval(gl[2])) == dict:
            ob = obj_dict["{}.{}".format(gl[0], gl[1])]
            for p, q in eval(gl[2]).items():
                if (p in ob.__class__.__dict__.keys() and
                        type(ob.__class__.__dict__[p]) in {str, int, float}):
                    vl_type = type(ob.__class__.__dict__[p])
                    ob.__dict__[p] = vl_type(q)
                else:
                    ob.__dict__[p] = q
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
