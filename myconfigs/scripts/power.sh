#!/bin/bash

chosen=$(printf "Lock\nLogout\nReboot\nPowerOff\n" | rofi -p "Power" -dmenu -i -theme-str)

case "$chosen" in
        "Lock")
                        yes_no=$(printf "no\nyes" | rofi -p "Would You Like to $chosen" -dmenu -i -theme-str)
                        case $yes_no in
                                [no]* ) exit;;
                                [yes]* ) mpv --no-video .config/sounds/game-bonus-144751.mp3 && xscreensaver-command -lock;;
                        esac;;
        "Logout")
                        yes_no=$(printf "no\nyes" | rofi -p "Would You Like to $chosen" -dmenu -i -theme-str)
                        case $yes_no in
                                [no]* ) exit;;
                                [yes]* ) mpv --no-video .config/sounds/cute-level-up-3-189853.mp3 && qtile cmd-obj -o cmd -f shutdown;;
                        esac;;
        "Reboot")
                        yes_no=$(printf "no\nyes" | rofi -p "Would You Like to $chosen" -dmenu -i -theme-str)
                        case $yes_no in
                                [no]* ) exit;;
                                [yes]* ) mpv --no-video .config/sounds/ambient-piano-logo-165357.mp3 && reboot;;
                        esac;;
        "PowerOff")
                        yes_no=$(printf "no\nyes" | rofi -p "Would You Like to $chosen" -dmenu -i -theme-str)
                        case $yes_no in
                                [no]* ) exit;;
                                [yes]* ) mpv --no-video .config/sounds/lovelyboot1-103697.mp3 && poweroff;;
                        esac;;
esac
