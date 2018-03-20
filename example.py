import matplotlib.pyplot as plt
import matplotlib


class Example(object):
    def __init__(self):
        self.example1 = 'how could they?'


class SubEx(Example):
    def __init__(self):
        self.ruined = 'this is awful.'


class Attr(matplotlib.Figure):
    def __repr__(self):
        return 'nonesense'


sub_ex = SubEx()

sub_ex.ruined


def function(param):
    return param


function(sub_ex)
