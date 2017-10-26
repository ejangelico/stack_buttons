from bs4 import BeautifulSoup
import urllib
import sys


class Inventory:
    def __init__(self, ref="http://glass.uchicago.edu"):
        # an inventory dictionary
        # structure is invent['type'] = [[thickness, frequency], ...]
        self.invent = {'thick': [], 'thin': [], 'rthick': [], 'rthin': [], 'shims':[]}
        self.webref = ref
        self.btypes = ['thick', 'thin', 'rthick', 'rthin', 'shims']

        # load in the inventory
        # using a web source parsing function
        self.load_inventory()

    def load_inventory(self):
        page = urllib.urlopen(self.webref).read()
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find_all("table", {"id": "buttons"})

        # assumes there is only one table with the id buttons
        headers = table[0].find_all("tr")

        currenttype = None

        for line in headers:
            # onto a new type of button
            if (len(line.contents[0]) == 1):
                btyperaw = line.contents[0].string
                if (len(btyperaw.split('-')) == 2):
                    # then it is non resistive
                    isresist = ''
                else:
                    isresist = 'r'

                thickstr = btyperaw.split(' ')[0].lower()

                currenttype = isresist + thickstr

            elif (len(line.contents[0]) == 4):
                # these are 60Mohm resistives
                continue

            else:
                thickraw = (line.contents[2].string).split(' ')
                if (len(thickraw) > 3):
                    # this is a large range bin, ignore it
                    continue

                thickness = float(thickraw[0])
                multiplicity = int(line.contents[1].string)

                self.invent[currenttype].append([thickness, multiplicity])



    def get_invent(self):
        return self.invent

    # decrements the frequency of the
    # button with type "ltype" thickness
    def decrement(self, ltype, thickness):
        exists = False  # if the thickness input even exists in the inventory
        for i, button in enumerate(self.invent[ltype]):
            if (button[0] == thickness):
                exists = True

                # if this is the last of those buttons
                # remove it from the inventory
                if (button[1] == 1):
                    self.invent[ltype].remove(self.invent[ltype][i])
                else:
                    # decrement the frequency element
                    self.invent[ltype][i][1] -= 1

        if (exists):
            return 0
        else:
            return 1  # button not found

    # increments the frequency of the
    # button with type "ltype" thickness
    def increment(self, ltype, thickness):
        exists = False  # if the thickness input even exists in the inventory
        for i, button in enumerate(self.invent[ltype]):
            if (button[0] == thickness):
                exists = True
                # decrement the frequency element
                self.invent[ltype][i][1] += 1


        if (exists):
            return 0
        else:
            #if the button is not found, add it to the inventory
            self.invent[ltype].append([thickness, 1])
            return 1


    # return the most frequent thicknesses
    # in each type of button
    def most_frequent_alltypes(self):
        winners = {'thick': None, 'thin': None, 'rthick': None, 'rthin': None, 'shims' : None}
        for btype in self.btypes:

            # here is a catch if one type of button
            # is completely empty
            if (len(self.invent[btype]) == 0):
                winners[btype] = None
                continue

            winners[btype] = sorted(self.invent[btype], key=lambda x: x[1])[-1]

        return winners

    # finds the button with value closest to val
    # in the inventory
    def find_closest_button(self, ltype, val):
        return (min(self.invent[ltype], key=lambda x: abs(x[0] - val)))[0]

    #checks if the thickness exists in the invent
    def exists(self, ltype, th):
        for t in self.invent[ltype]:
            if(t == float(th)):
                return True

        return False