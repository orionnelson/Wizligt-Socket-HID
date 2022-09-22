import asyncio
import time
import netifaces
import ipaddress
import socket

from pywizlight import wizlight, PilotBuilder, discovery


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
async def findbulbs(broadcast):
     bulbs = await discovery.discover_lights(broadcast_space=broadcast)
     return bulbs

def printBulbs(bulbs):
     for bulb in bulbs:
          print(bulb.__dict__)

# Write a function that takes a string and a list and returns the list entry with the most matching characters to a string
def mostMatching(list_to_match, s_match):
        m_count = 0
        result = ""
        for item in list_to_match:
            count = m_match_helper(item,s_match)
            if count > m_count:
                m_count = count
                result = item
        return result 


#Write a function that takes two strings and returns the amount of matching characters
def m_match_helper(s1,s2):
    count = 0 
    max_length = max(len(s1),len(s2))
    for x in range(0,max_length):
        if s1[x] == s2[x]:
            count = count + 1
        else:
            return count
    return count

# Gets The Local BroadCast Address
async def init_bulbs():
     spaces = set()
     pinterfaces = netifaces.interfaces()
     for intf in pinterfaces:
          fce = netifaces.ifaddresses(intf)
          for key in fce.keys():
               if 'broadcast' in fce[key][-1].keys():
                    address = fce[key][-1]['broadcast'].split('%')[0]
                    try:
                         if ipaddress.IPv4Address(address):
                              spaces.add(address)
                    except:
                         pass
     space = mostMatching(spaces,local_ip)
     bulbs = await findbulbs(space)
     #printBulbs(bulbs)
     return bulbs
# Returns array of wizlight

def convert2saturated(color):
     import colorsys as cs
     hsv = cs.rgb_to_hsv(color[0]/255,color[1]/255,color[-1]/255)
     #print(hsv)
     #print(cs.hsv_to_rgb(hsv[0],hsv[1],hsv[-1]))
     rgb = cs.hsv_to_rgb(hsv[0],255,1)
     rgb = (int(abs(rgb[0])),int(abs(rgb[1])),int(abs(rgb[-1])))
     #print(rgb)
     return rgb

async def setColor(pb,color,lights):
          #color = convert2saturated(color)
          #print(color)
          for light in lights:
               pb._set_rgb(color)
               pb._set_warm_white(0)
               pb._set_cold_white(0)
               #pb._set_brightness(max(color))
               await light.turn_on(pb)



import subprocess
import sys
import string

def hex2int(hexd):
     return int(hexd, 16)
def assignRGB(pb,bulbs):
     rgb=(0,0,0)
     cmd = 'tshark -i USBPcap1 -Y "frame.len==91" -T fields -e usbhid.data -l'
     process = subprocess.Popen(cmd, shell = True,bufsize = 1, stdout=subprocess.PIPE, stderr = subprocess.STDOUT,encoding='utf-8', errors = 'replace' ) 
     while True:
         realtime_output = process.stdout.readline()
         if realtime_output == '' and process.poll() is not None:
             break
         if realtime_output:
             #print(realtime_output)
             realtime_output = realtime_output.strip()[8:14]
             #print(realtime_output)
             if len(realtime_output)==6 and all(c in string.hexdigits for c in realtime_output):
                  rgb = (hex2int(realtime_output[0:2]),hex2int(realtime_output[2:4]),hex2int(realtime_output[4:6]))
                  #print(realtime_output.strip()!='000000')
                  if realtime_output.strip()!='000000':
                       print(realtime_output.strip(), flush=False)
                  loop.run_until_complete(setColor(pb,rgb,bulbs))
                  sys.stdout.flush()
     return rgb




def listener(pb,bulbs):
    HOST = "127.0.0.1"
    PORT = 5352
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
         s.bind((HOST, PORT))
         s.listen()
         conn, addr = s.accept()
         with conn:
             print(f"Connected by {addr}")
             while True:
                 data = conn.recv(1024)
                 if not data:
                     break
                 data = data.decode()
                 if data[:3] == "RGB":
                     assignRGB(pb,bulbs,data)
                 else:
                      print("Failed to Connect")
                 conn.sendall(data.encode())


while True:
     try:     
          loop = asyncio.get_event_loop()
          bulbs = loop.run_until_complete(init_bulbs())
          #lights = init_lights(bulbs)
          #loop.run_until_complete(callPilot(bulbs))
          pb = PilotBuilder()
          #loop.run_until_complete(policeLights(pb,bulbs))
          #listener(pb,bulbs)
          assignRGB(pb,bulbs)
     except:
          pass
