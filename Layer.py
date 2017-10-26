import sys


class Layer:
    def __init__(self, name, ltype, values=None):
        self.name = name

        # the type of layer, either
        # shithestr +=ick, thin, or auxhillary (for other use)
        self.ltype = ltype

        # dictionary of thickness values for this layer
        # Integer indices provide a unique id for the location
        # in the stack based on:
        # Tubes pointing left, counting from left to right, starting from
        # top to bottom, with the four resistive buttons being numbers
        # 17, 18, 19, 20
        if (values is None):
            self.values = {}
        else:
            self.values = values


    def __str__(self):
        s = ''
        for v in self.values:
            s += str(v) + ", " + str(self.values[v]) + "\n"

        return s

    def __len__(self):
        return len(self.values)

    # get the value with location
    # index "n"
    def get_val(self, n):
        return self.values[n]

    def set_val(self, n, val):
        self.values[n] = val

    def set_name(self, nm):
        self.name = nm
        return

    def get_type(self):
        return self.ltype

    def get_minimum_value(self):
        min = self.values[1]
        for v in self.values:
            if(self.values[v] < min):
                min = self.values[v]

        return min

    def get_maximum_value(self):
        max = self.values[1]
        for v in self.values:
            if (self.values[v] > max):
                max = self.values[v]

        return max



    # subtract the value "c" from all
    # positions in the layer
    def subtract_from_all(self, c):
        for i in self.values:
            self.values[i] -= c
