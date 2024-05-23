#!/bin/bash
xrandr -s 1920x1080 &
# nitrogen --restore &
feh --bg-scale .config/wallpapers/wallpaper_cave_nature/Sunset/32aGXc2-sunset-backgrounds.jpg
mpv --no-video /home/chris/Downloads/computer-startup-music-97699.mp3
xscreensaver -no-splash &
conky -c ~/.config/conky/conky.conf
