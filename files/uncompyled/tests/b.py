# 2015.09.05 18:13:43 ora legale Europa occidentale
# Embedded file name: b.py
from functools import partial

class B(object):

    def __myprint(self, data, extra):
        print extra + data

    def __init__(self):
        main(partial(self.__myprint, 'd'))


def main(callback):
    callback('some')


B()
