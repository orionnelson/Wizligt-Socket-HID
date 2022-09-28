# Wizligt-Socket-HID
Creates an API on Port 5352 that connects to the WizLight and Can Be issued commands RGB(R,G,B) to set RGB Lights

# This Library is a Wrapper to controll Multiple RGB Wizlights on a local network


## File Description
- ```wiz-api.py``` Sets up an Api Socket on port 5352 for accepting RGB information in the form ```RGB(0-255,0-255,0-255)```
- ```wiz-wireshark.py``` Accepts RGB information from a wireshark command and sets all wizlights on the local network.
- ```client-rgb-stream.py``` Testing script for the socket api on port 5352
