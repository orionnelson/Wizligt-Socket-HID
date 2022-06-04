import socket
import time
import random as r
HOST = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, 5352))

def sendAll():
    s.sendall(b"RGB(255,0,0)")
    time.sleep(0.35)
    s.sendall(b"RGB(0,0,255)")
    time.sleep(0.35)
    s.sendall(b"RGB(0,255,0)")
    time.sleep(0.35)

for x in range(0,255):
    sendAll()
    data = s.recv(1024)
    print(f"Received {data!r}")
