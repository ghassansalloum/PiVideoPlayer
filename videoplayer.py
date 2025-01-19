import socket
import subprocess
import json
from datetime import datetime

def log_message(message):
    """Formats a log message with a timestamp."""
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"

def play_video(video_path):
    try:
        # Launch the video using cvlc with additional arguments
        subprocess.Popen(['cvlc', '--file-caching=5000 --network-caching=10000 --no-fb-tty --vout fb --fbdev=/dev/fb0 ', video_path, '--play-and-exit'])
        log = log_message(f"Playing video: {video_path}")
        return log
    except Exception as e:
        log = log_message(f"Error playing video: {str(e)}")
        return log

def stop_video():
    try:
        # Kill all VLC processes
        subprocess.run(['sudo', 'killall', 'vlc'], check=True)
        log = log_message("All VLC processes stopped.")
        return log
    except subprocess.CalledProcessError as e:
        log = log_message(f"Error stopping VLC: {str(e)}")
        return log

def handle_client_connection(client_socket):
    logs = []
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8').strip()
        logs.append(log_message(f"Received data: {data}"))
        
        # Try parsing the JSON data
        try:
            command = json.loads(data)
        except json.JSONDecodeError as e:
            logs.append(log_message(f"JSON Decode Error: {str(e)}"))
            response = log_message("Error: Invalid JSON format.")
            logs.append(response)
            client_socket.send("\n".join(logs).encode('utf-8'))
            return
        
        # Process the command
        action = command.get('action')
        logs.append(log_message(f"Parsed action: {action}"))

        if action == 'play':
            video_path = command.get('video')
            if video_path:
                logs.append(log_message(f"Video path provided: {video_path}"))
                response = play_video(video_path)
            else:
                response = log_message("Error: No video path provided.")
        elif action == 'stop':
            logs.append(log_message("Stop action triggered."))
            response = stop_video()
        else:
            response = log_message("Error: Unsupported action.")
    except Exception as e:
        response = log_message(f"Error processing request: {str(e)}")
    finally:
        logs.append(response)
        full_log = "\n".join(logs)
        client_socket.send(full_log.encode('utf-8'))
        client_socket.close()

def main():
    # Set up a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5000))  # Bind to localhost and port 5000
    server_socket.listen(5)
    print(log_message("Video player service is running and waiting for commands..."))

    while True:
        client_socket, addr = server_socket.accept()
        print(log_message(f"Accepted connection from {addr}"))
        handle_client_connection(client_socket)

if __name__ == "__main__":
    main()
