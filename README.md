This is a project where I am creating a video player for a random video file.

It should work on a Raspberry Pi with an LCD HAT installed.

# Current system description
My current attempt is to make it work on a system with the following specs:
- Raspberry Pi Zero W V1.1
- Waveshare LCD 1.3" HAT
- OS Relase: Bookworm (ONLY **32-bit** is SUPPORTED by the fbcb DRIVER)
- Video player: VLC
- Audio server: pipewire (+ pipewire-pulse)
- Speaker: SONOS speaker capable of Airplay

# Older release
The Old-README-2020.md file includes the explorations I did in the first iteration of the projet. 

It ran on RPi Buster, with a Waveshare 1.3" LCD HAT, using omxplayer to play the videos, and using fbcp to copy the HDMI framebuffer to the small screen, with the audio going to a Bluetooth speaker. 

It ran for a few years, with some known issues documented in [the old README](Old-README-2020.md) file

# Major components:
- Bookworm (32-bit, because 64-bit is not supported by the fbcb driver I'm using)
- VLC (I tried mplayer, it didn't work)
- The fbcp driver to drive the LCD HAT display. See [Instructions for the LCD HAT](LCD%20%HAT%20%config.md)
- pipewire + pipewire-pulse (they both installed flawlessly on Bookworm, unlike Bullseye). The current version of pipewire finally works with Airplay.
- A script to set the desired default speaker on the system. See [default speaker.md](default%20%speaker.md) for details.
- Test with VLC:
```
cvlc --file-caching=5000 --network-caching=10000 --no-fb-tty --vout fb --fbdev=/dev/fb0 sample.mp4
```
--no-fb-tty is necessary when using a terminal (especially over ssh).

Adjust the fbdev value to match your framebuffer.

Does the audio work? Does the video work?
- A node-red flow that handles the hardware buttons and constitutes the bulk of the user experience.
- A set of video files from your favorite TV shows.
