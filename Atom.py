#functions to test if a given variable is an int/float
def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#class to represent a lisp atom
#can be either a number literal or a string
#if it is a string it will be interpreted as a symbol
class Atom():
    def __init__(self, data):
        self.is_num = False
        self.is_str = False
        if is_int(data):
            self.data = int(data)
            self.is_num = True
        elif is_float(data):
            self.data = int(float(data))
            self.is_num = True
        else:
            self.data = data
            self.is_str = True

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def __add__(self, other):
        if self.is_num and other.is_num:
            return self.data + other.data
        else:
            raise RuntimeError("Cant add 2 atoms that arent both numbers")

    def __sub__(self, other):
        if self.is_num and other.is_num:
            return self.data - other.data
        else:
            raise RuntimeError("Cant subtract 2 atoms that arent both numbers")

    def __mul__(self, other):
        if self.is_num and other.is_num:
            return self.data * other.data
        else:
            raise RuntimeError("Cant multiply 2 atoms that arent both numbers")

    def __floordiv__(self, other):
        if self.is_num and other.is_num:
            return int(self.data / other.data)
        else:
            raise RuntimeError("Cant divide 2 atoms that arent both numbers")

    def __eq__(self, other):
        if isinstance(other, Atom) and other.data == self.data:
            return True
        return False
