#!/usr/bin/python3
# Moode for Audiophonics SPC II power management board
# Initialisation of GPIO outputs 4 (SofhutDown) and 22 (BootOK) and 17 (Button shutdown)
# Script is lauched by /etc/rc.local
# Power LED stops slowly blinking and lights steadily after MoOde is ready
#
# All-in-One script 
# Start it without parameter to initialise
# "spc_moode.py reboot" to reboot
# "spc_moode.py shutdown" to shutdown
#
# GPIO access is done through pinctrl (Raspberry Pi OS Bookworm and later)
# pinctrl is part of the raspi-utils package, no extra dependency needed


import sys
import os
import time
import subprocess

GPIO_SOFTSHUTDOWN = 4
GPIO_BUTTON = 17
GPIO_BOOTOK = 22

def gpio_set(pin, direction, level):
    subprocess.run(["pinctrl", "set", str(pin), direction, level], check=True)

def gpio_get(pin):
    return "hi" in subprocess.run(["pinctrl", "get", str(pin)], check=True, capture_output=True, text=True).stdout

def boot():

    print ("Audiophonics initialisation script starting...")
    print ("Asserting pins : ")
    print ("SoftShutDown  : GPIO04=out, Low")
    print ("BootOK        : GPIO22=out, High")
    print ("Shutdown        : GPIO17=in")
 
    print ("Setting SoftShutDown output Low")
    gpio_set(GPIO_SOFTSHUTDOWN, "op", "dl")
    print ("Setting BootOK output Low")
    gpio_set(GPIO_BOOTOK, "op", "dl")

    
    # Testing Moode Ready :
    print ("Waiting for MoOde Availability")
    print ("Condition is checked out every 5 seconds")
    option= "-q"
    sqlSelect="select value from cfg_system where param='wrkready'"

    while True:
     result=subprocess.check_output(['/usr/local/bin/moodeutl',option,sqlSelect])
     if result == b'1\n':
       print ("Setting BootOK output High")
       gpio_set(GPIO_BOOTOK, "op", "dh")
       break
     time.sleep(2)

    # Button shutdown loop :
    while True :
        if gpio_get(GPIO_BUTTON):
            print ("ShutDown order received, RaspBerry pi will now shutdown...")
            os.system ('sudo /usr/sbin/shutdown -h -P now')
            break
        time.sleep(2)
    sys.exit()

def shutdown():
    print ("RaspberryPi shutdown")
    print ("Setting pin GPIO4 High")
    gpio_set(GPIO_SOFTSHUTDOWN, "op", "dh")
    time.sleep(1)
    print ("Setting pin GPIO4 Low")
    gpio_set(GPIO_SOFTSHUTDOWN, "op", "dl")
    time.sleep(1)
    os.system ('sudo shutdown -h -P now')
    sys.exit()

def reboot():
    print ("RaspberryPi Reboot")
    print ("Setting pin GPIO4 High")
    gpio_set(GPIO_SOFTSHUTDOWN, "op", "dh")
    time.sleep(1)
    os.system ('sudo reboot')
    sys.exit()

# Argument checking to know what to do :

if len(sys.argv) == 1 :
    boot()
elif sys.argv[1] == 'reboot':
    print ('Argument:', sys.argv[1])
    reboot()
elif sys.argv[1] == 'shutdown':
    print ('Argument:', sys.argv[1])
    shutdown()
else:
    print ("No valid argument, use nothing, reboot or shutdown")
    sys.exit()
