#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2019-2021 Denis Meyer
#
# This file is part of raspi-camerastreamingserver
#

"""Raspberry Pi"""

import logging
import base64
import sys
import ssl

from server.StreamingHandler import StreamingHandler
from server.StreamingOutput import StreamingOutput
from server.StreamingServer import StreamingServer
from tools.Helper import parse_args, read_txt

class CameraStreamingServer:

    def __init__(self, __prog__, settings):
        """Initialization

        :param settings: The settings
        """
        logging.info('Initializing')

        self.settings = settings

        if self.settings.get('on_device'):
            _picamera = __import__('picamera', globals(), locals(), ['PiCamera'], 0)
            self.PiCamera = _picamera.PiCamera

        # Parse command line arguments
        self.args = parse_args(__prog__, self.settings)
        self.running = False
        self.url = ''
        self.port = 0

        # Initialize internally
        self._init()

    def _init(self):
        """Internal initialization"""
        logging.debug('Initializing')

        if ':' not in self.args.username_password:
            logging.error('Wrong format. Use "{}"'.format('username:password'))
            sys.exit()

        # Save given parameters
        self.settings.set('server', 'port', self.args.port)
        self.settings.set('camera', 'resolution_width', self.args.reswidth)
        self.settings.set('camera', 'resolution_height', self.args.resheight)
        self.settings.set('camera', 'framerate', self.args.framerate)
        self.settings.set('camera', 'rotation_degrees', self.args.rotation_degrees)
        self.settings.set('camera', 'awb', self.args.awb)
        self.settings.set('camera', 'filter', self.args.filter)

        # Extract URL and port
        self.url = self.settings.get('server')['url']
        self.port = self.settings.get('server')['port']

        # Prepare the StreamingHandler
        StreamingHandler.USERNAME_PASSWORD_BASE64 = base64.b64encode(
            self.args.username_password.encode('utf-8'))
        StreamingHandler.settings = self.settings
        StreamingHandler.INDEX_HTML_TMPL = read_txt(self.settings.get('html')['index'])

    def _cleanup(self):
        """Cleans up all initialized resources"""
        logging.info('Cleaning up')
        self.running = False
        logging.info('Done cleaning up')

    def run(self):
        """Starts the main loop"""
        if self.running:
            logging.info('Already started')
            return

        if not self.running:
            self.running = True

        logging.info('Starting main loop')

        # If run on the Raspberry Pi
        try:
            if self.settings.get('on_device'):
                resolution = self.settings.get('camera')['resolution_str'].format(
                    self.settings.get('camera')['resolution_width'], self.settings.get('camera')['resolution_height'])
                framerate = self.settings.get('camera')['framerate']
                logging.info('Streaming with resolution: {}, framerate: {}'.format(
                    resolution, framerate))
                with self.PiCamera(resolution=resolution, framerate=framerate) as camera:
                    StreamingHandler.output = StreamingOutput()
                    camera.rotation = self.settings.get('camera')['rotation_degrees']
                    camera.awb_mode = self.settings.get('camera')['awb']
                    camera.image_effect = self.settings.get('camera')['filter']
                    camera.start_recording(StreamingHandler.output, format='mjpeg')
                    try:
                        logging.info('Starting server at "{}:{}"'.format(self.url, self.port))
                        address = (self.url, self.port)
                        self.server = StreamingServer(address, StreamingHandler)
                        self.server.serve_forever()
                    except:
                        logging.info('Stopping main loop')
                    finally:
                        camera.stop_recording()
            # If not run on the Raspberry Pi
            else:
                try:
                    logging.info('Starting server at "{}:{}"'.format(self.url, self.port))
                    address = (self.url, self.port)
                    self.server = StreamingServer(address, StreamingHandler)
                    if self.settings.get('server')['certfile'] and self.settings.get('server')['keyfile']:
                        self.server.socket = ssl.wrap_socket(
                            self.server.socket,
                            certfile=self.settings.get('server')['certfile'],
                            keyfile=self.settings.get('server')['keyfile'],
                            server_side=True,
                            ssl_version=ssl.PROTOCOL_TLS)
                    self.server.serve_forever()
                except:
                    logging.info('Stopping main loop')
        finally:
            self._cleanup()
            logging.info('Stopping')
