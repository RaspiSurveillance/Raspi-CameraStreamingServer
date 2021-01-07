#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2019-2021 Denis Meyer
#
# This file is part of raspi-camerastreamingserver
#

"""Helper"""

import os
import sys
import logging
import argparse


def initialize_logger(settings):
    """Initializes the logger

    :param settings: The settings
    """
    if settings.log_to_file:
        basedir = os.path.dirname(settings.log_filename)

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    logger.propagate = False

    logger.handlers = []

    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setLevel(settings.log_level)
    handler_console.setFormatter(logging.Formatter(
        fmt=settings.log_format, datefmt=settings.log_dateformat))
    logger.addHandler(handler_console)

    if settings.log_to_file:
        handler_file = logging.FileHandler(
            settings.log_filename, mode='w', encoding=None, delay=False)
        handler_file.setLevel(settings.log_level)
        handler_file.setFormatter(logging.Formatter(
            fmt=settings.log_format, datefmt=settings.log_dateformat))
        logger.addHandler(handler_file)

def get_ascii_art_banner():
    """Returns the ASCII-art banner
    
    :return: ASCII-art banner
    """
    return r"""
  _____                 _         _____        ______          ______
 |  __ \               (_)       / ____|      / ____/         /  ____|
 | |__) |__ _ ___ _ __  _ ______| |          | (___          |  (___  
 |  _  // _` / __| '_ \| |______| |           \___ \         \___   \ 
 | | \ \ (_| \__ \ |_) | |      | |____       ____) |         ___)  |
 |_|  \_\__,_|___/ .__/|_|       \_____|amera|_____/ treaming|______/erver
                 | |
                 |_| (C) 2019-2021 Denis Meyer
"""

def parse_args(__prog__, settings):
    """Parses the command line arguments
    
    :param __prog__: Program name
    :param settings: The settings
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(prog=__prog__)
    parser.add_argument('username_password', help='username:password')
    parser.add_argument('--port', required=False, type=int,
                        help='port number', default=settings.get('server')['port'])
    parser.add_argument('--reswidth', required=False, type=int,
                        help='resolution width', default=settings.get('camera')['resolution_width'])
    parser.add_argument('--resheight', required=False, type=int,
                        help='resolution height', default=settings.get('camera')['resolution_height'])
    parser.add_argument('--framerate', required=False, type=int,
                        help='frame rate', default=settings.get('camera')['framerate'])
    parser.add_argument('--rotation_degrees', required=False, type=int,
                        help='rotation_degrees', default=settings.get('camera')['rotation_degrees'])
    parser.add_argument('--awb', required=False,
                        help='auto-white-balance', default=settings.get('camera')['awb'])
    parser.add_argument('--filter', required=False,
                        help='filter, image effect', default=settings.get('camera')['filter'])
    args = parser.parse_args()

    if not args.awb in ['off', 'auto', 'sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent', 'incandescent',
                        'flash', 'horizon']:
        logging.info('Setting awb parameter to "auto"')
        args.awb = 'auto'

    if not args.filter in ['none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
                           'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise',
                           'colorpoint', 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2']:
        logging.info('Setting filter parameter to "none"')
        args.filter = 'none'

    return args

def read_txt(filename):
    """Reads in a text file

    :param settings: The settings
    """

    outstr = ''

    try:
        with open(filename, 'r') as jf:
            outstr = jf.read()
    except Exception as e:
        logging.error('Could not load from file "{}": "{}"'.format(filename, e))

    return outstr
