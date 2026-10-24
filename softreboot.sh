#!/bin/bash
# Audiophonics
# Shutdown detection script
# Script to set GPIO 4 High for 1sec

PATH=/usr/bin:/usr/local/bin

# Script to set GPIO 4 High and Reboot
# Reboot blink will stop after Boot OK return
echo "setting pin GPIO 4 High"
pinctrl set 4 op dh

echo "Raspberry Pi Reboot"
sudo reboot
exit 0
