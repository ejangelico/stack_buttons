import numpy as np
import matplotlib.pyplot as plt
import Layer
import sys
import copy
import itertools


class Stack:
    def __init__(self, inputfile):

        # a layer that represents the
        # final desired height of the entire stack
        self.final = Layer.Layer("final", "aux")

        #a layer that represents the measurements of depth
        #  from the hole block. This is use mostly for plotting
        # purposes
        self.holeblock = Layer.Layer("holeblock", "aux")

        # an input file that specifies total stack
        # heights desired for each point in the stackup
        self.finput = inputfile
        self.load_input_graphic_csv()
        self.load_holeblock()

        # a list of layers that are the output of
        # the program to calculate a set of buttons
        # to use. This is initialized when the
        # function "calculateForSequence" is called
        self.layers = []

    # this is an input loading function that
    # takes specifically from evan angelico's
    # graphically generated excel files. very specific
    # please write your own load_input function for
    # any other specific input file type
    def load_input_graphic_csv(self):
        finraw = open(self.finput, 'r')
        filelines = finraw.readlines()
        filelines = filelines[0].split('\r')

        stacklines = [_.split(',') for _ in filelines[17:24]]
        stackrows = [filter(lambda x: x != '', _) for _ in stacklines]

        # at this point, the black magic above has
        # trimmed away all of the commas in the csv
        # and all of the irrelevent data to leave behind
        # a list of lists of rows of buttons.I.e. four rows
        # of four buttons and a single button for the rows that
        # have one resistive button
        for i, val in enumerate(stackrows[0]):
            self.final.set_val(i + 1, float(val))

        for i, val in enumerate(stackrows[2]):
            self.final.set_val(i + 5, float(val))

        for i, val in enumerate(stackrows[4]):
            self.final.set_val(i + 9, float(val))

        for i, val in enumerate(stackrows[6]):
            self.final.set_val(i + 13, float(val))

        # now for resistives
        self.final.set_val(17, float(stackrows[1][0]))
        self.final.set_val(18, float(stackrows[3][0]))
        self.final.set_val(19, float(stackrows[3][1]))
        self.final.set_val(20, float(stackrows[5][0]))

    def load_holeblock(self):
        finraw = open(self.finput, 'r')
        filelines = finraw.readlines()
        filelines = filelines[0].split('\r')

        stacklines = [_.split(',') for _ in filelines[2:11]]
        stackrows = [filter(lambda x: x != '', _) for _ in stacklines]
        stackrows = [filter(bool, _) for _ in stackrows]

        # at this point, the black magbuttonlayeras
        # trimmed away all of the commas in the csv
        # and all of the irrelevent data to leave behind
        # a list of lists of rows of buttons.I.e. four rows
        # of four buttons and a single button for the rows that
        # have one resistive button
        for i, val in enumerate(stackrows[0][5:]):
            self.holeblock.set_val(i + 1, float(val))

        self.holeblock.set_val(6, float(stackrows[1][-1]))

        for i, val in enumerate(stackrows[2][5:]):
            self.holeblock.set_val(i + 7, float(val))

        self.holeblock.set_val(12, float(stackrows[3][-1]))

        for i, val in enumerate(stackrows[4][11:]):
            self.holeblock.set_val(i + 13, float(val))

        self.holeblock.set_val(22, float(stackrows[5][-1]))

        for i, val in enumerate(stackrows[6][5:]):
            self.holeblock.set_val(i + 23, float(val))

        self.holeblock.set_val(28, float(stackrows[7][-1]))

        for i, val in enumerate(stackrows[8][5:]):
            self.holeblock.set_val(i + 29, float(val))

        return

    #function that makes a colorplot of
    #the holeblock layer
    def plot_holeblock(self):

        #build an array of (x, y) coordinates
        #based on an inner dish of 20x20cm split into
        #divisions of 5's
        curx = 0
        cury = 0
        x = []
        y = []
        depths = []
        for i in range(1, len(self.holeblock) + 1):
            if (curx > 20):
                # do the small button in the middle
                x.append(10)
                y.append(cury + 2.5)
                depths.append(self.holeblock.get_val(i))
                cury += 5
                curx = 0
                continue



            x.append(curx)
            y.append(cury)
            depths.append(self.holeblock.get_val(i))

            if(cury == 10):
                curx += 2.5
            else:
                curx += 5


        #plot it using tricontourf
        fig, ax = plt.subplots()
        ax.plot(x, y, 'ko')
        v = np.linspace(self.holeblock.get_minimum_value(), self.holeblock.get_maximum_value(), 20)
        mycs = plt.tricontourf(x, y, depths, v, cmap=plt.get_cmap('jet'))
        cb = plt.colorbar(ticks=v)
        cb.set_label("Depth (mils)")
        ax.set_aspect('equal')
        ax.set_ylim([-2, 22])
        ax.set_xlim([-2, 22])
        plt.show()










    # get the sum of all layer values
    # at position n
    def get_sum_layers(self, n):
        s = 0
        for lay in self.layers:
            if (lay.get_val(n) is None):
                continue
            else:
                s += lay.get_val(n)

        return s
