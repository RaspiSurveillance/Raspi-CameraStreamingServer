#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2019-2021 Denis Meyer
#
# This file is part of raspi-camerastreamingserver
#

__prog__ = 'RaspiCameraStreamingServer'
__version__ = '1.0'

"""
Main

Usage: "python CameraStreamingServer.py <username>:<password> [--port 8080] [--reswidth 1280] [--resheight 720] [--framerate 24] [--rotation_degrees 0]"
"""

import logging

from tools.Helper import initialize_logger, get_ascii_art_banner
from tools.Settings import Settings
from tools.CameraStreamingServer import CameraStreamingServer

if __name__ == "__main__":
    settings = Settings()
    initialize_logger(settings)

    logging.info(get_ascii_art_banner())

    raspi_camerastreamingserver = CameraStreamingServer(__prog__, settings)
    raspi_camerastreamingserver.run()
