Here is a concise plan to make an Airplay speaker the default sink persistently using pactl and ensuring services are configured in the user’s .config directory and run independently of user login:

# System assumption
This works on a Raspberry Pi running Bookworm, with pipewire and pipewire-pulse and pa-utils installed.

```
sudo apt install pipewire pipewire-pulse pulseaudio-utils
```

You don't need PulseAudio itself. But the utilities in pulseaudio-utils will work with Pipewire.

# Make sure the RAOP module is loaded in pipewire

Create a pipewire.conf for the user if you want
```
cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/
```

Make sure the raop module gets loaded. Add the following in this pipewire.conf:
```
context.properties = {
    default.clock.rate          = 48000
    default.clock.allowed-rates = [ 48000 ]
}

context.modules = [
    {   name = libpipewire-module-rtkit           args = {} }
    {   name = libpipewire-module-raop-discover  args = {} }
]
```
and restart pipewire
```
systemctl --user restart pipewire
```

# Get the list of available audio sinks and pick the one you want
```
pactl list sinks | grep -E 'Sink #|Name:|Description:|Volume:'
```

The Airplay speakers have this format: 
```
50	raop_sink.Sonos-F0F6C1D86672.local.192.168.111.166.7000	PipeWire	s16le 2ch 44100Hz	SUSPENDED
52	raop_sink.Sonos-347E5CF63B9A.local.192.168.111.125.7000	PipeWire	s16le 2ch 44100Hz	SUSPENDED
```

# Create a Script to Set the Default Sink

Create a shell script, e.g., set-default-sink.sh, in the user’s ```.config``` directory:
```
nano ~/.config/set-default-sink.sh
```

Add these two lines:
```
#!/bin/bash
pactl set-default-sink 'raop_sink.Sonos-38420B94B684.local.192.168.111.114.7000'
```

Make it executable:  
```
chmod +x ~/.config/set-default-sink.sh
```

# Create and configure a Systemd Service


```
mkdir .config/systemd
mkdir .config/systemd/user
```

Create a systemd service file in the folder 
```
sudo nano ~/.config/systemd/user/set-default-sink.service
```

Enter these lines:

```
[Unit]
Description=Set Default Audio Sink for Pipewire
After=pipewire.service

[Service]
ExecStart=/home/pi/.config/set-default-sink.sh
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

# Enable and Start the Service
Reload systemd for the user services, and enable the new service and start it 
```
systemctl --user daemon-reload
systemctl --user enable set-default-sink.service
systemctl --user start set-default-sink.service
```
# Allow the Service to Run Without User Login
Enable lingering for the user: 
```
sudo loginctl enable-linger $USER
```
# Test and Verify
Reboot the system or restart PipeWire: 
```
systemctl --user restart pipewire.service
```

Confirm the default sink: 
```
pactl get-default-sink
```
Play a test file:
```
paplay /usr/share/sounds/alsa/Noise.wav
```
This setup ensures the default sink is set on every boot and after any PipeWire restart, without requiring the user to log in.
