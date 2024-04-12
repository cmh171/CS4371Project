import tkinter as tk
from pymongo import MongoClient
import requests

class toggleLights:
    def __init__(self):
        self.is_on = False

    def __init__(button, root):

        #Setting up button
        button.root = root
        button.toggle_value = 0
        button.toggle_button = tk.Button(root, text="Closed", command=button.toggle)
        button.toggle_button.pack()
        button.count = 0
        button.state = 0

        #Connecting to Mongodb
        button.client = MongoClient()
        button.db = button.client['project'] 
        button.collection = button.db['lights']
        print("handleLights initialized successfully.")

    def on(self):
        self.is_on = True
        print("The lights are on")

    def off(self):
        self.is_on = False
        print("The lights are off")

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

if __name__ == "__main__":
    lights = toggleLights()

    #Checking if app is connected to the server
    url = 'http://localhost:3000/'
    response = requests.get(url)
    if response.status_code == 200:
        print("Connected")
    else:
        print("Not Connected")

    # Simulating IoT commands
    print("Turning on the lights...")
    lights.on()

    print("Toggling the lights...")
    lights.toggle()

    print("Turning off the lights...")
    lights.off()
