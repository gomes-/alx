#!/usr/bin/env python

__author__ = 'Alex Gomes'

import alx.data.io, logging, os, sys


class Save:
    """

    """
    io = None

    def __init__(self):
        Save.io = alx.data.io.IO()
        path = Save.io.data_check()
        sys.path.append(path)
        logging.debug("path: {0}".format(path))

    def save_cmd(self, name, cmd):
        logging.debug("{0}->save_cmd(name:{1}, cmd:{2})".format(os.path.abspath(__file__), name, cmd))

        import my_data

        my_data.alx_save[name] = cmd

        Save.io.export_data(my_data.alx_save)


    def flush_cmd(self, name):

        import my_data

        try:
            my_data.alx_save.pop(name, None)
        except:
            raise ()

        Save.io.export_data(my_data.alx_save)

    def flush_all(self):

        Save.io.export_data({})