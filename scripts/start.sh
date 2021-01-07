#!/bin/bash

cd src
if [[ ! -e /tmp/raspi-camerastreamingserver.py.pid ]]; then
    echo "Starting Raspi-CameraStreamingServer..."
    python3 raspi-camerastreamingserver.py <username>:<password> --reswidth 1280 --resheight 900 --framerate 8 --rotation_degrees 0 --awb auto --filter none &
    echo $! > /tmp/raspi-camerastreamingserver.py.pid
    echo "Raspi-CameraStreamingServer has been started with pid "
    cat /tmp/raspi-camerastreamingserver.py.pid
else
    echo -n "ERROR: Raspi-CameraStreamingServer seems to be running with pid "
    cat /tmp/raspi-camerastreamingserver.py.pid
    echo
fi
