#!/usr/bin/env python3

"""
OSC-audioPlayer - talks to PD patch OSC-audioPlayer.pd
Steve Symons 2018

Depends on:     pythonosc

The PD patch has 8 channels for streaming a wav or mp3 or aiff.
Channels numbered 0 to 7
"""

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

def oscaudio_send(addr, channel, cmd, data):
  msg = osc_message_builder.OscMessageBuilder(addr)
  msg.add_arg(channel)
  msg.add_arg(cmd)
  msg.add_arg(data)
  msg = msg.build()
  client.send(msg)

#opens and starts playing
def oscaudio_play(channel, data):
  oscaudio_send("/ch", channel, "play", data)

#sets pan 0 (left) 1 (right)
def oscaudio_pan(channel,data):
  oscaudio_send("/ch", channel, "pan", data)

#sets loop 1 on 0 off (default to off)
def oscaudio_loop(channel,data):
  oscaudio_send("/ch", channel, "loop", data)

#sets channel volume 0 to 1
def oscaudio_vol(channel,data):
  oscaudio_send("/ch", channel, "vol", data)
  
#opens but doesn't start
def oscaudio_open(channel,data):
  oscaudio_send("/ch", channel, "open", data)

#starts playing after an open
def oscaudio_start(channel):
  oscaudio_send("/ch", channel, "start", 1)
#stops playing NB must then 'open' or 'play' to start again - NO PAUSE
def oscaudio_stop(channel):
  oscaudio_send("/ch", channel, "stop", 1)

"""
Some short methods for ALL channels - though you can just send anything
oscaudio_send("/all", channel, command, data)

"""

#starts ALL playing after an open
def oscaudio_startAll(channel):
  oscaudio_send("/all", channel, "start", 1)
  
#stops ALL playing NB must then 'open' or 'play' to start again - NO PAUSE
def oscaudio_stopAll(channel):
  oscaudio_send("/all", channel, "stop", 1)

#sets ALL channels volume 0 to 1
def oscaudio_volAll(channel,data):
  oscaudio_send("/all", channel, "vol", data)
  


if __name__ == "__main__":
  #sets up the udp port stuff - best ignore tbh
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="192.168.120.65",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=9000,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.UDPClient(args.ip, args.port)
  time.sleep(1)



 #here you go
  oscaudio_play(0, "bell.aiff")
  time.sleep(0.5)
  oscaudio_play(0,"TouchStems_001.wav")
  oscaudio_pan(1,0.75)
  time.sleep(0.5)
  oscaudio_loop(1,0)
  for i in range(6):
    oscaudio_play(i,"TouchStems_00"+str(i)+".wav")
    time.sleep(0.5)
    
  time.sleep(10.5)
  oscaudio_pan(1,0)
  oscaudio_play(1, "bell.aiff")



  print("sent")
    
  
