#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import random
import os.path
import random
from datetime import datetime


from multiprocessing import Queue
from multiprocessing import Process
from subprocess import call

baseDirectory = "/home/pi/vids/"

# define the names of the folders containing the video files.
series = ["Series1", "TBD", "Series2"]

GPIO.setmode(GPIO.BCM)

def playEpisode(choice):
    directory = os.path.join(baseDirectory, series[choice])
    random.seed(datetime.now())
    episode = random.choice(os.listdir(directory))
    path = os.path.join(directory, episode)

    os.system('killall omxplayer.bin')
    print(path)
    cmd = r'nohup omxplayer -b --orientation 180 -o alsa:bluealsa "'+path+ '" &'
    os.system(cmd)
    os.system('cls')

# Shutdown button
def shutdown_now():
 os.system('sudo shutdown now')

# Frasier button
def processButton1(btnPin):
 try:
   import RPi.GPIO as GPIO
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   while(1):
      GPIO.wait_for_edge(btnPin, GPIO.FALLING)
      playEpisode(0)
      time.sleep(1.5)
 except ValueError, Argument:
  print "Error", Argument

# Stop all button
def processButton2(btnPin):
 try:
   import RPi.GPIO as GPIO
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   while(1):
      GPIO.wait_for_edge(btnPin, GPIO.FALLING)
      os.system('killall omxplayer.bin')
      os.system('cls')
      time.sleep(1.5)
 except:
  print("Failed")


# Seinfeld button
def processButton3(btnPin):
 import RPi.GPIO as GPIO
 GPIO.setmode(GPIO.BCM)
 #buttonPin3 = 16
 GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

 while(1):
    GPIO.wait_for_edge(btnPin, GPIO.FALLING)
    playEpisode(2)
    time.sleep(1.5)



# Shutdown button
def processJoystickPress(btnPin):
 import RPi.GPIO as GPIO
 GPIO.setmode(GPIO.BCM)
 # Joystick Press = 13
 GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

 while(1):
     GPIO.wait_for_edge(btnPin, GPIO.FALLING)
     shutdown_now()
     time.sleep(1.5)


def main():
    print "Starting video player 'daemon' from /home/pi/piplayer"
    Process(target=processButton1, args=[21]).start()
    Process(target=processButton2, args=[20]).start()
    Process(target=processButton3, args=[16]).start()
    Process(target=processJoystickPress, args=[13]).start()

    os.system('cls')


try:
  if __name__ == "__main__":
      main()
except KeyboardInterrupt:
  print("Exiting!")
  GPIO.cleanup()
