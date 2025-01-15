This is a project where I am creating a video player for a random video file.

It should work on a Raspberry Pi with an LCD HAT installed.

# System description
My current attempt is to make it work on a system with the following specs:
- Raspberry Pi Zero W V1.1
- Waveshare LCD 1.3" HAT
- OS Relase: Bookworm
- Video player: VLC
- Audio server: pipewire (+ pipewire-pulse)
- Speaker: SONOS speaker capable of Airplay

# Older release
The Old-README-2020.md file includes the explorations I did in the first iteration of the projet. 

It ran on RPi Buster, with a Waveshare 1.3" LCD HAT, using omxplayer to play the videos, and using fbcp to copy the HDMI framebuffer to the small screen. 

It ran for a few years, with some known issues documented in [the old README](Old-README-2020.md) file
