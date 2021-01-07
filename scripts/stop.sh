#!/bin/bash

if [[ -e /tmp/raspi-camerastreamingserver.py.pid ]]; then
    echo "Raspi-CameraStreamingServer is running, stopping..."
    kill `cat /tmp/raspi-camerastreamingserver.py.pid`
    rm /tmp/raspi-camerastreamingserver.py.pid
    echo "Raspi-CameraStreamingServer has been stopped"
else
    echo "Raspi-CameraStreamingServer is not running"
fi
