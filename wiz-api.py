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

async def setColor(pb,color,lights):
          for light in lights:
               pb._set_rgb(color)
               await light.turn_on(pb)


def assignRGB(pb,bulbs,RGB):
     try:
          rgb = tuple([int(item) for item in RGB.replace("RGB","").replace(")","").replace("(","").split(",")])
     except:
          return (0,0,0)
     print(rgb)
     loop.run_until_complete(setColor(pb,rgb,bulbs))
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



loop = asyncio.get_event_loop()
bulbs = loop.run_until_complete(init_bulbs())
#lights = init_lights(bulbs)
#loop.run_until_complete(callPilot(bulbs))
pb = PilotBuilder()
#loop.run_until_complete(policeLights(pb,bulbs))
listener(pb,bulbs)
