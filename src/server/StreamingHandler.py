#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2019-2021 Denis Meyer
#
# This file is part of raspi-camerastreamingserver
#

"""Streaming handler"""

import logging
from http import server

class StreamingHandler(server.BaseHTTPRequestHandler):
    USERNAME_PASSWORD_BASE64 = ''
    settings = {}
    output = {}
    STREAM_NAME = 'stream.mjpg'
    INDEX_HTML_TMPL = ''

    def do_authhead(self):
        '''Does the authentication'''
        logging.debug('Send authentication header')

        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm=\"Please enter your username and password\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        '''HEAD method'''
        logging.debug('Handling HEAD')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        '''GET method'''
        logging.debug('Handling GET')

        header_auth = self.headers.get('Authorization')
        if header_auth is None:
            logging.debug('Not authorized - no auth header set')
            self.do_authhead()
            self.wfile.write(b'no auth header received')
        elif header_auth == 'Basic ' + self.USERNAME_PASSWORD_BASE64.decode('UTF-8'):
            logging.debug('Authorized')
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = self.get_index_html().encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/{}'.format(self.STREAM_NAME):
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with self.output.condition:
                            self.output.condition.wait()
                            frame = self.output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception:
                    logging.info('Removed streaming client %s', self.client_address)
            else:
                self.send_error(404)
                self.end_headers()
        else:
            logging.debug('Not authorized - wrong auth header set')
            self.do_authhead()
            self.wfile.write(header_auth.encode('UTF-8'))
            self.wfile.write('not authenticated'.encode('UTF-8'))

    def get_index_html(self):
        '''Returns the index.html'''
        if self.settings.get('on_device'):
            stream_html = '<img src="{}" width="{}" height="{}">'.format(
                self.STREAM_NAME,
                self.settings.get('camera')['resolution_width'],
                self.settings.get('camera')['resolution_height'])
        else:
            stream_html = 'Stream will be displayed here. Resolution width x height: {} x {}, framerate: {}'.format(
                self.settings.get('camera')['resolution_width'],
                self.settings.get('camera')['resolution_height'],
                self.settings.get('camera')['framerate'])

        return self.INDEX_HTML_TMPL.format(stream_html)
