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
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt=240 240 60 1 0 0 0
```
and comment out ```dtoverlay=vc4-kms-v3d``` ( I believe teh driver dev wants all ```dtoverlay``` lines commented out )
This will make the HDMI connection stop working.

# Enable the SPI interface

```sudo raspi-config```
Go to the Interface options.

# Do quick tests

```cat /dev/random > /dev/fb0```
You should see noise on the small screen

Fbi is a quick image viewer
```sudo apt install fbi```

Get an image from the web
```cd ~
wget https://i.pinimg.com/originals/51/26/d3/5126d3a1f2ef917b584d83c86fda95e6.jpg -O mj.jpg
sudo fbi -T 1 -d /dev/fb0 -noverbose --autozoom mj.jpg
```
If you see an image, the driver is working. The next step is installing the video player.


# Configure for reboots
