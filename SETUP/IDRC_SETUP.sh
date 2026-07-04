#!/bin/bash

echo "this script is meant for Pulse Audio on KDE, it might work elsewhere im not sure"

pactl load-module module-null-sink sink_name=tts_speaker sink_properties=device.description=TTS_Virtual_Speaker


echo "on KDE you can route the audio by playing a long clip, going to audio and moving the app to the TTS_Virtual_Speaker speaker"

echo "this is a really long string for you to set it up with this is a really long string for you to set it up with this is a really long string for you to set it up with this is a really long string for you to set it up with this is a really long string for you to set it up with this is a really long string for you to set it up with this is a really long string for you to set it up with this is a really long string for you to set it up with\nexit()" | python3 ../VRC_TTS.py

echo "warning this will reset after a reboot so if you want you should go to your config and set this up correctly https://wiki.archlinux.org/title/PulseAudio#Configuration_files"
