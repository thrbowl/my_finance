# -*- coding: utf-8 -*-
import os
from my_finance import db, gui

ROOT = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    dbfile = os.path.join(ROOT, 'my_finance.db')
    if not os.path.isfile(dbfile):
        db.init()
    gui.run()
