#!/bin/bash
# Audiophonics
# Shutdown detection script
# Script to set GPIO 4 High for 1sec

PATH=/usr/bin:/usr/local/bin

echo "Setting pin GPIO4 High"
pinctrl set 4 op dh

/bin/sleep 1
echo "Setting pin GPIO4 Low"
pinctrl set 4 dl

echo "RaspberryPi shutdown"
sudo shutdown -h -P now
exit 0
