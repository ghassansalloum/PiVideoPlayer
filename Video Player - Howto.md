# Two concepts:
1. Call VLC straight from NodeRed
2. Or, have a video playing service that takes commands from Node-Red. (ABANDONED idea)

# Call VLC from Node-Red

Call VLC from an `exec` node. The downside of this method is that Node-Red owns the video playing session, and if I restart it  VLC will be killed and the video will stop.

I learned that pre-pending the exec commands with ``` XDG_RUNTIME_DIR=/run/user/1000 ``` helps when there's a discrepancy
between the result on the console (in ssh) and what you get with the same command in node-red. 
DBUS_SESSION_BUS_ADDRESS was also recommended, I added it just to be on the safe side.

I ran ```env``` on the console, and then again in an `exec` in node-red. These two environment variables were among the ones that were different between the two results.

I also learned that the `--no-fb-tty` was necessary, without it the video was displaying on the console despite the --fbdev option.

Specifically, I verified that this works:
```
XDG_RUNTIME_DIR=/run/user/1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus /usr/bin/cvlc --file-caching=5000 --network-caching=10000 --no-fb-tty --vout fb --fbdev=/dev/fb0 --quiet sample.mp4"
```

This also works:
```
XDG_RUNTIME_DIR=/run/user/1000 /usr/bin/cvlc --file-caching=5000 --no-fb-tty --vout fb --fbdev=/dev/fb0 --quiet sample.mp4
```
Et voila. The trick that eluded me for 3-4 years is to narrow down the list of options I need to pass, and to set up the proper environment variables when invoking the cvlc command.

# Video-playing service (ABANDONED idea)

(__I did not end up using this method, but I'm keeping it here in case it helps in the future. It was a cool idea and led me to the environment variables investigation.__)

(__The upside of this method would be that if I am messing with Node-Red, this method would not interrupt a video that is playing__)

This is a more indirect way to play the video. I created it in the process of debuggging and understanding 
how interacting with the framebuffer truly works.

Create the script that plays the video.
```nano videoplayer.py```

and use this script [videplayer.py](videplayer.py)
  
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

You now have a TCP server listening on a TCP port, waiting for commands to start and stop video play.

Create a node-red flow that passes the command in the correct format in the TCP request.<img width="1206" alt="Screenshot 2025-01-19 at 9 35 54 PM" src="https://github.com/user-attachments/assets/f7ee7d64-b8df-422c-b0f0-85c67969beac" />

<img width="1263" alt="Screenshot 2025-01-19 at 9 37 53 PM" src="https://github.com/user-attachments/assets/b91e7cbe-fc9c-4376-96c6-5c9cf3830614" />
