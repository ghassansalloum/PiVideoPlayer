This is the software stack needed to make the LCD HAT from Waveshare (1.3 inches for me) work


# Install the fbcp driver
Unfortunately it only works on 32-bit OSes, and uses an API that is deprecated on the Pi5+ hardware. Luckily I'm still using an RPi Zero 2 W.

```cd ~
sudo apt install libraspberrypi-dev
sudo apt install cmake
sudo apt install git
git clone https://github.com/juj/fbcp-ili9341.git
cd fbcp-ili9341
mkdir build
cd build
cmake -DDMA_RX_CHANNEL=5 -DUSE_DMA_TRANSFERS=ON -DSPI_BUS_CLOCK_DIVISOR=6 -DWAVESHARE_ST7789VW_HAT=ON -DSTATISTICS=0 -DDISPLAY_ROTATE_180_DEGREES=ON ..
make -j
sudo ./fbcp-ili9341
```

# Configure boot.config

Go to ```sudo nano /boot/firmware/config.txt```
and add this:
```
```
and comment out ```dtoverlay=vc4-kms-v3d``` ( I believe teh driver dev wants all ```dtoverlay``` lines commented out )

# Enable the SPI interface

```sudo raspi-config```
Go to the Interface options.

# Install fbi for quick tests

# Configure for reboots
