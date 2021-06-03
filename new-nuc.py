import socketio
import subprocess


IP_ADDRESS = "192.168.1.2"
DEVICE_ID = "USB\VID_05AC&PID_024F&REV_0124"
COMMAND = "uhubctl -l 1-1 -p 2 -a "
# COMMAND = "uhubctl -l 1-1 -a "


def turnLightOn():
    print("Turning light ON")
    returnObject = subprocess.run(["./devcon.exe", "rescan"])


def turnLightOff():
    print("Turning light OFF")
    returnObject = subprocess.run(["./devcon.exe", "remove", DEVICE_ID])


sio = socketio.Client()
sio.connect(f"http://{IP_ADDRESS}:8080/nuc")


@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from server")


@sio.on("control signal")
def on_control_signal(data):
    print(data["signal"])
    if data["signal"] == "ON":
        turnLightOn()
    else:
        turnLightOff()
