#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2019-2021 Denis Meyer
#
# This file is part of raspi-camerastreamingserver
#

"""Settings - The settings storage"""


import logging
import time
import json
import os


class Settings:

    _FILE_JSON_SETTINGS = 'settings.json'
    _FOLDER_LOG_OUT = 'logs'
    _FILE_LOG_OUT_TMPL = 'raspi-camerastreamingserver.application-{}.log'

    def __init__(self,
                    filename=_FILE_JSON_SETTINGS,
                    log_out_foldername=_FOLDER_LOG_OUT,
                    log_out_filename_tmpl=_FILE_LOG_OUT_TMPL):
        """Initializes the class
        
        :param filename: The settings file name
        :param log_out_foldername: The log output folder name
        :param log_out_filename_tmpl: The log output file name
        """
        logging.info('Initializing')

        self.filename = filename
        self.log_filename = os.path.join(
            os.getcwd(),
            log_out_foldername, log_out_filename_tmpl.format(time.strftime('%d-%m-%Y-%H-%M-%S')))

        self._settings_dict = {}

        ### Currently not in the settings file ###

        self.log_to_file = True
        self.log_level = logging.INFO
        self.log_format = '[%(asctime)s] [%(levelname)-7s] [%(module)-20s:%(lineno)-4s] %(message)s'
        self.log_dateformat = '%d-%m-%Y %H:%M:%S'

        ### Init ###

        self._read_settings()
        logging.debug(self._settings_dict)

    def _read_settings(self):
        """Reads the settings from file"""
        logging.debug('Reading settings from file')

        try:
            with open(self.filename, 'r') as jf:
                self._settings_dict = json.load(jf)
        except Exception as e:
            logging.error('Could not load from file "{}": "{}"'.format(self.filename, e))

    def get(self, key, default=''):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._settings_dict[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default

    def set(self, key, key2, value):
        """Sets a (new) value for a given key

        :param key: The key
        :param key: The second key
        :param value: The value
        """
        self._settings_dict[key][key2] = value
