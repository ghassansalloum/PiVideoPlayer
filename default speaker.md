Here is a concise plan to make an Airplay speaker the default sink persistently using pactl and ensuring services are configured in the user’s .config directory and run independently of user login:

# System assumption
This works on a Raspberry Pi running Bookworm, with pipewire and pipewire-pulse and pa-utils installed.

Plan

# Create a Script to Set the Default Sink

Create a shell script, e.g., set-default-sink.sh, in the user’s .config directory:


```
#!/bin/bash
pactl set-default-sink 'raop_sink.Sonos-38420B94B684.local.192.168.111.114.7000'
```

Make it executable:  ```chmod +x ~/.config/set-default-sink.sh```

# Create and configure a Systemd Service

Create a systemd service file in ~/.config/systemd/user/set-default-sink.service:

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
Reload systemd for the user services: ```systemctl --user daemon-reload```

Enable the service: ```systemctl --user enable set-default-sink.service```

Start the service: ```systemctl --user start set-default-sink.service```
# Allow the Service to Run Without User Login
Enable lingering for the user: ```sudo loginctl enable-linger $USER```
# Test and Verify
Reboot the system or restart PipeWire: ```systemctl restart pipewire.service```

Confirm the default sink: ```pactl get-default-sink```

This setup ensures the default sink is set on every boot and after any PipeWire restart, without requiring the user to log in.
