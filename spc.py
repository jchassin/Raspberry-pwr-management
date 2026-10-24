#!/usr/bin/python3
#AUDIOPHONICS SPC POWER CONTROLLER
#Python script using pinctrl (Raspberry Pi OS Bookworm and later)
#In case WiringPi do not work
#pinctrl is part of the raspi-utils package, no extra dependency needed
#Must be run as root to be able to send shutdown order

import time
import os
import subprocess

#Set GPIO used here :
bootok = 22
shutdown = 17

def gpio_set(pin, direction, level):
    subprocess.run(["pinctrl", "set", str(pin), direction, level], check=True)

def gpio_get(pin):
    return "hi" in subprocess.run(["pinctrl", "get", str(pin)], check=True, capture_output=True, text=True).stdout

print("Audiophonics Shutdown script starting...")
print("Asserting pins : ")
print("BootOK   : GPIO" + str(bootok) + "=out, High")
print("ShutDown : GPIO" + str(shutdown) + "=in, Low")

#When script Launched, send BOOT OK signal
gpio_set(bootok, "op", "dh")

# Initialise GPIO 17 for shutdown order
gpio_set(shutdown, "ip", "pn")

while True:
    sdstate = gpio_get(shutdown)
    time.sleep(0.5)
    if sdstate:
        print("ShutDown order received, RaspBerry pi will now shutdown...")
        time.sleep(0.5)
        os.system("shutdown -h -P now")
        break
