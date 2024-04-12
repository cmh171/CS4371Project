import tkinter as tk
from pymongo import MongoClient
import requests

class toggleLights:
    def __init__(self):
        self.toggle_value = 0

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
        button.collection = button.db['doors']
        print("handleLights initialized successfully.")

    def toggle(self):
        if self.toggle_value == 0:
            self.state = 0
        else:
            self.state = 1

if __name__ == "__main__":
    lights = toggleLights()

    #Checking if app is connected to the server
    url = 'http://localhost:3000/'
    response = requests.get(url)
    if response.status_code == 200:
        print("Connected")
    else:
        print("Not Connected")

    #For bug fixing purposes, gives the current table in the database
    url = 'http://localhost:3000/project/doors/'
    response = requests.get(url)

    # Simulating IoT commands
    print("Turning on the lights...")
    lights.on()

    print("Toggling the lights...")
    lights.toggle()

    print("Turning off the lights...")
    lights.off()
