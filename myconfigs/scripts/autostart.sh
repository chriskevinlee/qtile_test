#!/bin/bash
xrandr -s 1920x1080 &
nitrogen --restore &
mpv --no-video /home/chris/Downloads/computer-startup-music-97699.mp3
xscreensaver -no-splash &
conky -c ~/.config/conky/conky.conf
