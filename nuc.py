import tkinter as tk
from tkinter import font as tkFont
import subprocess


# Find the light hardware ID and replace ut below
DEVICE_ID = "USB\VID_05AC&PID_024F&REV_0124"


class DeviceControl(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the root window
        self.title("Control a light bulb")
        self.geometry("400x300")

        # Light Status
        self.__light_status = "ON"

        # Label
        self.label = tk.Label(
            self, text="The light is " + self.__light_status, font=50, justify=tk.CENTER)
        self.label.grid(row=0, column=0, pady=(20, 40))

        # Button
        self.button = tk.Button(
            self, text="The light is " + self.__light_status, width=30)
        self.button["command"] = self.turn_light
        self.button["fg"] = "white"
        self.button["bg"] = "yellow"
        self.button["font"] = 50
        # self.button["style"] = tkFont.Font(size=50)
        self.button.grid(row=1, column=0, ipady=10, padx=10)

    def turn_light(self):
        if self.__light_status == "ON":
            returnObject = subprocess.run(
                ["./devcon.exe", "remove", DEVICE_ID])
            self.__light_status = "OFF"
        elif self.__light_status == "OFF":
            self.__light_status = "ON"
            returnObject = subprocess.run(["./devcon.exe", "rescan"])
        self.change_elements_text()

    def change_elements_text(self):
        text = "The light is " + self.__light_status
        self.label["text"] = text
        self.button["text"] = text
        if self.__light_status == "ON":
            self.button["bg"] = "yellow"
        else:
            self.button["bg"] = "black"


if __name__ == "__main__":
    app = DeviceControl()
    app.mainloop()
