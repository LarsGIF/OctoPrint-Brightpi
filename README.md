# OctoPrint-Brightpi

This is a plugin to OctoPrint controlling a Bright-Pi camera light assembly from PiSupply.
https://github.com/PiSupply/Bright-Pi

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
using this URL:
https://github.com/LarsGIF/OctoPrint-Brightpi/archive/1.0.2.zip

## Configuration

The smbus (I2C) need to be enabled. 
sudo raspi-config nonint do_i2c 0
Reboot is required

See also https://github.com/PiSupply/Bright-Pi
