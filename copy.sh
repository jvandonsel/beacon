#!/bin/bash
# Copy all python files to the ESP32 over webrepl

if [ "$1" == "" ]; then
    echo "Missing password argument"
    exit 1
fi
password=$1

BOARD_IP=192.168.1.22
WEBREPL=~/code/webrepl/webrepl/webrepl_cli.py
# PYBOARD=~/code/micropython/tools/pyboard.py

DEVICE=/dev/tty.usbserial-10

copy_file() {
    ${WEBREPL} -p ${password} ${1}  ${BOARD_IP}:${2}
    # ${PYBOARD} --device ${DEVICE} -f cp ${1} :

}

copy_file boot.py
copy_file utils.py
copy_file weather.py
copy_file wifi.py
copy_file leds.py
