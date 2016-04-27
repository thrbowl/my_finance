# -*- coding: utf-8 -*-
import os
from my_finance import db, gui, settings


if __name__ == '__main__':
    if not os.path.isfile(settings.DB_FILE):
        db.init()
    gui.run()
