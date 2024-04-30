#!/bin/bash

volume_increase="+10%"
volume_decrease="-10%"
volume_mute="toggle"

if [ "$1" = "up" ]; then
    pactl set-sink-volume @DEFAULT_SINK@ "$volume_increase"
elif [ "$1" = "down" ]; then
    pactl set-sink-volume @DEFAULT_SINK@ "$volume_decrease"
elif [ "$1" = "mute" ]; then
    pactl set-sink-mute @DEFAULT_SINK@ "$volume_mute"
fi

is_muted=$(pactl list sinks | awk '/^\s*Mute:/ {print $2}')
if [ "$is_muted" = "yes" ]; then
    echo "Volume is muted"
else
    current_volume=$(pactl list sinks | awk '/^\s*Volume:/ {print $5}')
    echo "Current volume level: $current_volume"
fi
