# Two concepts:
1. Call VLC straight from NodeRed
2. Or, have a video playing service that takes commands from Node-Red.

# Call VLC from Node-Red

# Video-playing service
This is a more indirect way to play the video. I created it in the process of debuggging and understanding 
how interacting with the framebuffer truly works.

Create the script that plays the video.
(script goes here)
  
Create a service to manage the script and load it after a reboot. This will create it for all users:
```
sudo nano /etc/systemd/system/videoplayer.service
```
(You can also write it to a user directory if you just want to create it for the ```pi``` user, and dont want to sudo to start it. 
In my case the device's only job is to play video and there are no other users.

Write this content:
```
[Unit]
Description=Video Player Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/videoplayer.py
WorkingDirectory=/home/pi/
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Start and Enable the Service
Reload the systemd manager:
```
sudo systemctl daemon-reload
```
Start the service:
```
sudo systemctl start videoplayer.service
```
Enable the service to run on boot:
```
sudo systemctl enable videoplayer.service
```
Check the service status:
```
sudo systemctl status videoplayer.service
```
Ensure there are no errors in the output.

If you later forget where the file defining the service is, run this.
```
systemctl show -p FragmentPath videoplayer.service
```
