import numpy.random as rand
class PowerUsage:
    def __init__(self):
        self.isTurenedOn = rand.randint(0,5)
    def getData(self):
        return self.isTurenedOn