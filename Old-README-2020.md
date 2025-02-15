# PiVideoPlayer
Raspberry Pi Zero W + LCD HAT video player + Bluetooth audio

* The Raspberry Pi Zero W is [this one](https://www.raspberrypi.org/pi-zero-w). I chose this one because I wanted the small form factor, for portability.
* The LCD IPS 1.3" HAT is this one from [Waveshare](https://www.waveshare.com/1.3inch-lcd-hat.htm). Buy it on [Amazon](https://www.amazon.com/interface-Embedded-Controller-Compatible-Raspberry/dp/B07FDQVYFM).

The high level structure of this project is:
0. Install the latest Raspbian image on the SD card for the Raspberry Pi 
1. Configure the LCD screen
2. Set up the bluetooth connection (it turns out to be tricky on Linux!)
3. Set up the video controller and player code that takes advantage of it all, and load the video files on the device.

Let's begin.

## LCD IPS 1.3" HAT

How to compile the 1.3" TFT LCD driver IPS HAT (with a joystick and 2 buttons)
from GitHub - [juj/fbcp-ili9341](https://github.com/juj/fbcp-ili9341): A blazing fast display driver for SPI-based LCD displays for Raspberry Pi

~~~python
cd ~
sudo apt-get install cmake
git clone https://github.com/juj/fbcp-ili9341.git
cd fbcp-ili9341
mkdir build
cd build
cmake -DDMA_RX_CHANNEL=5 -DUSE_DMA_TRANSFERS=ON -DSPI_BUS_CLOCK_DIVISOR=6 -DWAVESHARE_ST7789VW_HAT=ON -DSTATISTICS=0 -DDISPLAY_ROTATE_180_DEGREES=ON ..
make -j
sudo ./fbcp-ili9341
~~~	
From <https://github.com/juj/fbcp-ili9341> 

I tried DMA channel 10, it complained that it cant use a "lite" channel, and recommended that I use something <7, so I went with 5 and that seems to have made it work!



Then add a line in ---/etc/rc.local--- to load the driver at boot time:
> sudo /home/pi/fbcp-ili9341/build/fbcp-ili9341 &

## Bluetooth
### May 12
Now for the bluetooth audio.
~~~
sudo bluetoothctl
Agent on
Scan on
Pair XX:XX:XX
Trust XX:XX:XX
Connect XX:XX:XX:X
~~~
Replace the XX:XX:XX with the value for your bluetooth speaker or headphones. You can see them in the output of the 'scan' command above.
It paired, and got trusted (trusted means that it will automatically connect to it when it's detected)
Some issues connecting. 
I found a page that recommentded running pactl… That didn't work. (i turns out I don't need PulseAudio on the most recent version of Raspbian)
It's not clear whether the Pi Zero W that I have already has the libraries or I have to apt-get new ones.
	
	
### May 14
OK here's another attempt. I tried a different pair of headphones, thinking it's a hardware issue. That didn't work.

I then followed the instructions here, and I am one step further. The headphones connect successfully, and stay connected!
[https://peppe8o.com/fixed-connect-bluetooth-headphones-with-your-raspberry-pi/](https://peppe8o.com/fixed-connect-bluetooth-headphones-with-your-raspberry-pi/)
		
But no audio coming out of the omxplayer into the headphones.
Note that I haven't checked if an HDMI connected Pi will play audio.
	
<at this point I rebuilt the whole set up from scratch on the 128GB micro SD card that I received in the mail>
<I restarted effectively all the steps, which was a good thing because I had tried so many things to make Bluetooth work, I lost track of the state of the system>
***	
Add pi to the bluetooth group.
~~~
pi@raspberrypi:~ $ sudo adduser pi bluetooth
Adding user `pi' to group `bluetooth' ...
Adding user pi to group bluetooth
Done.
~~~			
And logout/login again
Now install the BlueAlsa proxy (I don’t know what 'proxy' refers to - yet)

> sudo apt-get install bluealsa
	
Did this 
bluetoothd with a2dp plugin
There is a a2dp plugin for our bluetooth agent. So we'll change the services' ExecStart parameter like so:

~~~	
sudo nano /etc/systemd/system/bluetooth.target.wants/bluetooth.service
	
#And while we're here we'll disable sap since this may cause some errors:
	
ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap --plugin=a2dp
~~~	

Not sure if this was necessary by the way. I'd like to remove this a2dp configuration and see if it still works.
	
1:20 AM - MADE IT WORRRRKKKKKKKKKKKKKKKKKKKKKKK
	
OK so I was messing all evening with Bluetooth settings trying to figure out what the f.. SCO is , and what A2DP is.
I learned SCO is the 'profile' for VOIP audio.
And that A2DP is the 'profile' for high quality audio.
	
I was having TWO issues in the last two hours:
 1- Anytime I tried to play audio via the 'aplay' command (the .. alsa .. player),  I'd get noise whether it was an mp3 or a movie. I eventally figured that the tool expects raw audio, and I was passing it encoded data (mp3!) Of COURSE I'd only get noise! DAMN. When it clicked in my head that THAT may be the issue, I quickly looked for and downloaded a .wav file and it played beautifully well!
	
 2- When I tried to play videos or audio in omxplayer, no sound would come out! I tried the "-o alsa" option in vain (as well as the "-o both" option), UNTIL, I realized I have to include some additional info, namely the MAC address of the bluetooth device I paired with the Rpi.
	omxplayer -o alsa:bluealsa <path to file>
And I had a corresponding profile in the .asoundrc file in my home directory
~~~
pi@raspberrypi:~ $ cat .asoundrc
				
#defaults.bluealsa.service "org.bluealsa"
#defaults.bluealsa.profile "a2dp"
#defaults.bluealsa.delay 10000
				
# Bluetooth headset
defaults.bluealsa {
     interface "hci0"            # host Bluetooth adapter
     #device "10:4F:A8:00:11:22"  # Bluetooth headset MAC address
     # device "AA:00:A7:00:B8:D4" Vidonn
     device "D0:8A:55:08:FC:BE" # <-- the headset that supports A2DP!
     profile "a2dp"
~~~
WEEEEEEEEEEEEEEEEEEEEEEEEEE!
	
## The video playing part

### Get a command line video player application.

I am using omxplayer
> sudo apt-get install omxplayer

Others that I know of but I haven't tried: vlc (may need X server), mplayer

### Copy the the media files
I have them on an external hard drive.
* Mount the external hard drive mount /dev/sda1 /mnt
* Copy the media files : I learned to use "rsync" to copy folders. For example:
> cp -rvn /mnt/Videos/GoneWithTheWindSeries/ ./vids/GoneWithTheWindSeries/
* I used scp (file copy over SSH) from a Windows machine, but using rsync is more convenient.

### Cron job monitoring the physical buttons of the LCD HAT.
See player.py script file for the code that makes the application work.

Run
>sudo nano /etc/rc.local

and include this:
~~~
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo /home/pi/fbcp-ili9341/build/fbcp-ili9341 &
/home/pi/player.py

exit 0

~~~

## The version of Raspbian I'm running on the Pi Zero W
~~~
pi@raspberrypizero:~ $ cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
~~~


## the MAC addresses of my Bluetooth speakers and headsets
found in /etc/asound.conf

~~~
pcm.!default {
	type plug
	slave {
		pcm {
			type bluealsa
			device "30:21:31:55:D8:B8" # Boxanne
			profile "a2dp"
		}
	}
	hint {
		show on
		description "Boxanne Red Speaker"
	}
	
}

~~~


## Pending work overall

A couple of days of break from the project and re-assess the next steps. This is the list of items that are still needed:
* A box
* A portable power supply solution
* A way for the system to shutdown gracefully if the power is about to get lost
* A way for omxplayer to play audio to both the HDMI device and the bluetooth device (two -o parameters?)
* A way to play to the bluetooth device that's connected, and support (play with the .asoundrc or /etc/asound.conf configs?) more than one? or explore passing a -o parameter to each paired bluetooth device?
* Address the too-fast playback glitch that happens occasionally on the Fra vids, and almost constantly on Sei vids.
* Clear the display on the terminal view that shows in the tiny screen. Maybe even turn off the LCD between video plays.
* General stability:
  * Now let's figure out why omxplayer STOPs the audio if I fast forward through the video
  * How can I make omxplayer resilient to turning off the headphones (it seems to crash/hang when I do so)
