#!/bin/bash
# Copy all python files to the ESP32 over webrepl

WEBREPL=~/code/webrepl/webrepl/webrepl_cli.py
DEST=192.168.1.24

${WEBREPL} ./boot.py  ${DEST}:/boot.py
${WEBREPL} ./utils.py  ${DEST}:/utils.py
${WEBREPL} ./weather.py  ${DEST}:/weather.py