This is the software stack needed to make the LCD HAT from Waveshare (1.3 inches for me) work

# Install the fbcp driver
Unfortunately it only works on 32-bit OSes, and uses an API that is deprecated on the Pi5+ hardware. Luckily I'm still using an RPi Zero 2 W.

# Configure boot.config

# Enable the SPI interface

```sudo raspi-config```
Go to the Interface options.

# Install fbi for quick tests

# Configure for reboots
