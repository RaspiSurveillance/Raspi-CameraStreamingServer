# Raspi-CameraStreamingServer

Raspberry Pi Camera Streaming Server with basic username:password authentication.

## Copyright

Copyright (C) 2019-2021 Denis Meyer

## Prerequisites

### Hardware

* Camera

### Software

* A set up Raspberry Pi
* Python 3 (as "python3")
* Windows
  * Add Python to PATH variable in environment
* Configure settings.json

## Usage

* Configure src/settings.json

* Start shell
* [Install the required libraries (picamera) if not already installed]
* Run the app via script
  * Edit the start script (at least change the username/password)
  * `./scripts/start.sh`
  * Stop the app via script
    * `./scripts/stop.sh`
* Run the app
  * `cd src`
  * `python raspi-camerastreamingserver.py <username>:<password> [--port 8000] [--reswidth 1280] [--resheight 900] [--framerate 8] [--rotation_degrees 0] [--awb auto] [-filter none]`
    * awb
      * https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.awb_mode
      * Posible values: off, auto, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon
    * filter
      * https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.image_effect
      * Posible values: none, negative, solarize, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolor, film, blur, saturation, colorswap, washedout, posterise, colorpoint, colorbalance, cartoon, deinterlace1, deinterlace2
  * Stop the app
    * Ctrl-C
