import tkinter as tk
from pymongo import MongoClient
import requests


class ToggleButtonApp:
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
        print("ToggleButtonApp initialized successfully.")

    def toggle (button):

        #Connects to the update path
        url = 'http://localhost:3000/project/doors/update'

        print("Toggling button state...")
        button.toggle_value = not button.toggle_value
        button.toggle_button.config(text=str('Closed'))

        if button.toggle_value == 0:
            print ("Now Closed")
            button.state = 0
              
        else:
            button.toggle_button.config(text=str('Open'))
            print ("Now Open")
            button.state = 1

        button.count+=1
        data = {
            #'id' : button.count,
            'name' : 'HOUSE_FRONT',
            'status' : 'closed' if button.state == 0 else 'opened'
        }

        response = requests.post(url,json=data)
        if response.status_code == 200:
            print("Door status saved")
        else:
            print("Error occured", response.status_code)

def main():

    print("Starting ToggleButtonApp...")

    #Checking if app is connected to the server
    url = 'http://localhost:3000/'
    response = requests.get(url)
    if response.status_code == 200:
        print("Connected")
    else:
        print("Not Connected")

    #For bug fixing purposes, gives the current table in the database
    #url = 'http://localhost:3000/project/doors/'
    #response = requests.get(url)

    print (response.text)
    root = tk.Tk()
    root.geometry("650x450")
    app = ToggleButtonApp(root)
    root.mainloop()
    print("ToggleButtonApp finished.")

if __name__ == "__main__":
    main()