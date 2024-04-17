import tkinter as tk
from pymongo import MongoClient
import requests
import sys
import numpy as np

#----------------------------------------------------------
#Defining data layout and key globally
#----------------------------------------------------------

data = {
            #'id' : button.count,
            'name' : '',
            'status' : ''
        }
key = 'door'

#----------------------------------------------------------
#hill encryption 
#----------------------------------------------------------

def cipher_encryption(plain, key):
    # removing spaces, setting to upper
        plain = plain.upper().replace(" ","")
        key = key.upper().replace(" ", "")

        # initializing necessary arrays
        plain_matrices = []
        encrypted_matricies = []
        key_matrix = []

        # offset for uppercase to alphabet mod26 is 65
        offset = 65
        # flag for if we're appending a character
        padding_char_flag = 0

        # handle if plain is odd
        if len(plain) % 2 != 0: 
            #ascii value of ~ is 126
            plain += '~'
            padding_char_flag = 1

        
        # convert message to matrices
        for i in range(0, len(plain), 2):
            char1 = ord(plain[i]) - offset
            char2 = ord(plain[i + 1]) - offset
            matrix = [[char1], [char2]]
            plain_matrices.append(matrix)
        
        #convert plain_matrices into a numpy matrix
        plain_matrices = np.array(plain_matrices)

        # convert key to 2x2 matrix
        for i in range (0, len(key), 2):
            char1 = ord(key[i]) - offset
            char2 = ord(key[i+1]) - offset
            key_matrix.append([char1, char2])

        # check that the key matrix is in fact a 2x2
        if len(key_matrix) != 2 or len(key_matrix[0]) != 2:
            raise ValueError("Key must be a 2x2 matrix")

        # converting to numpy matrix
        key_matrix = np.array(key_matrix)

        # checking validity of the key
        # finding determinant
        determinant = int(np.round(np.linalg.det(key_matrix)))

        # check if det == 0, if so error
        if determinant == 0:
            raise ValueError("Key must have a determinant != 0")

        # start loading encrypted_matrix with shifted text values
        for matrix in plain_matrices:
            encrypted_matrix = np.dot(key_matrix, matrix) % 26
            encrypted_matricies.append(encrypted_matrix)

        encrypted_text = ""

        # start loading shifted characters into a string
        for matrix in encrypted_matricies:
            char1 = chr(matrix[0][0] + offset)
            char2 = chr(matrix[1][0] + offset)
            encrypted_text += char1 + char2
        
        # strip padding char if it was appended
        if padding_char_flag == 1:
            encrypted_text = encrypted_text[:-1]
        return encrypted_text

#----------------------------------------------------------
#hill decryption
#----------------------------------------------------------

def cipher_decryption(cipher, key):
    # removing spaces, setting to upper
    cipher = cipher.upper().replace(" ","")
    key = key.upper().replace(" ", "")

    # initializing necessary arrays
    plain_matrices = []
    encrypted_matricies = []
    key_matrix = []

    # offset for uppercase to alphabet mod26 is 65
    offset = 65
    # flag for if we're appending a character
    padding_char_flag = 0

    # handle if plain is odd
    if len(cipher) % 2 != 0: 
        #ascii value of ~ is 126
        cipher += '~'
        padding_char_flag = 1
    
    # convert cipher to matrices
    for i in range(0, len(cipher), 2):
        char1 = ord(cipher[i]) - offset
        char2 = ord(cipher[i + 1]) - offset
        matrix = [[char1], [char2]]
        encrypted_matricies.append(matrix)
    
    #convert encrypted_matrices into a numpy matrix
    encrypted_matricies = np.array(encrypted_matricies)

    # convert key to 2x2 matrix
    for i in range (0, len(key), 2):
        char1 = ord(key[i]) - offset
        char2 = ord(key[i+1]) - offset
        key_matrix.append([char1, char2])

    # check that the key matrix is in fact a 2x2
    if len(key_matrix) != 2 or len(key_matrix[0]) != 2:
        raise ValueError("Key must be a 2x2 matrix")

    # converting to numpy matrix
    key_matrix = np.array(key_matrix)

    # checking validity of the key
    # finding determinant
    determinant = int(np.round(np.linalg.det(key_matrix)))

    # check if det == 0, if so error
    if determinant == 0:
        raise ValueError("Key must have a determinant != 0")

    # define multiplicative inverse
    mult_inverse = pow(determinant, -1, 26)

    # define the adjugate of the key_matrix
    # this is not extensible, but we already know we have a 2x2 so this is what
    # we're doing. 
    adjugate_matrix = np.array([[key_matrix[1, 1], -key_matrix[0, 1]],
                            [-key_matrix[1, 0], key_matrix[0, 0]]])
    

    #k^-1 = mult_inverse(det % 26) * adjugate(k)
    inverted_key_matrix = mult_inverse * adjugate_matrix % 26

    # start loading plaintext matrix with shifted text values
    for matrix in encrypted_matricies:
        plain_matrix = np.round(np.dot(inverted_key_matrix, matrix) % 26).astype(int)
        plain_matrices.append(plain_matrix)

    plain_matrices = np.array(plain_matrices)

    decrypted_text = ""

    # start loading shifted characters into a string
    for matrix in plain_matrices:
        char1 = chr(matrix[0][0] + offset)
        char2 = chr(matrix[1][0] + offset)
        decrypted_text += char1 + char2
    
    # strip padding char if it was appended
    if padding_char_flag == 1:
        decrypted_text = decrypted_text[:-1]
    
    return decrypted_text

#----------------------------------------------------------
#Updating the textbox status
#----------------------------------------------------------

def update_textbox(button, text):
        
        #Deletes any old lines once the max of 10 lines of text has been reached
        current = button.textbox.get("1.0", tk.END)
        lines = current.split("\n")
        if len(lines) > 11:
            button.textbox.delete("1.0", tk.END)

        # Update the textbox with new text
        button.textbox.insert(tk.END, text + "\n")  

#----------------------------------------------------------
#Creating the button class and setting up the button
#----------------------------------------------------------

class ToggleButtonApp:
    def __init__(button, root):
        #grabbing current door status in db
        button.state = 0
        url = 'http://localhost:3000/project/doors/HOUSE_FRONT'
        response = requests.get(url, json=data)
        if response.status_code == 200:
            door_status = response.json().get('status')
        #Setting up button 1
        button.door_status_decrypt = cipher_decryption(door_status,key)
        button.root = root
        button.toggle_value = 0
        button.toggle_button = tk.Button(root, text='Toggle Status', command=button.toggle)
        button.toggle_button.place(x=100, y=50)
        label = tk.Label(root,text="HOUSE_FRONT")
        label.place(x=100, y=25)
        button.textbox = tk.Text(root, height=10, width=50)
        button.textbox.place(x=100,y=150)
        button.state = 0
        button.position = "closed"
        button.closed = "closed"
        button.opened = "opened"
        button.encrypt = ''
        button.decrypt = ''

        #grabbing current door status in db
        url2 = 'http://localhost:3000/project/doors/HOUSE_BACK'
        response = requests.get(url2, json=data)
        if response.status_code == 200:
            door_status2 = response.json().get('status')
        #Setting up button 2
        button.door_status_decrypt2 = cipher_decryption(door_status2,key)
        button.toggle_value2 = 0
        button.toggle_button2 = tk.Button(root, text='Toggle Status', command=button.toggle2)
        button.toggle_button2.place(x=225, y=50)
        label2 = tk.Label(root,text="HOUSE_BACK")
        label2.place(x=225, y=25)
        button.state2 = 0
        button.position2 = "closed"
        button.closed2 = "closed"
        button.opened2 = "opened"
        button.encrypt2 = ''
        button.decrypt2 = ''

        #grabbing current door status in db
        url3 = 'http://localhost:3000/project/doors/GARAGE'
        response = requests.get(url3, json=data)
        if response.status_code == 200:
            door_status3 = response.json().get('status')
        #Setting up button 3
        button.door_status_decrypt3 = cipher_decryption(door_status3,key)
        button.toggle_value3 = 0
        button.toggle_button3 = tk.Button(root, text='Toggle Status', command=button.toggle3)
        button.toggle_button3.place(x=350, y=50)
        label3 = tk.Label(root,text="GARAGE")
        label3.place(x=350, y=25)
        button.state3 = 0
        button.position3 = "closed"
        button.closed3 = "closed"
        button.opened3 = "opened"
        button.encrypt3 = ''
        button.decrypt3 = ''


        #Connecting to Mongodb
        button.client = MongoClient()
        button.db = button.client['project'] 
        button.collection = button.db['doors']
        print("ToggleButtonApp initialized successfully.")

#----------------------------------------------------------
#Toggle setup for the button 1
#----------------------------------------------------------

    def toggle (button):

        #Connects to the update path
        url = 'http://localhost:3000/project/doors/update'

        #Setting up toggling for button 1
        print("Toggling button state...")
        button.toggle_value = not button.toggle_value
        #button.toggle_button.config(text=str(button.door_status_decrypt))

        #If/Else to toggle whether button 1 "closed" or "open"
        if button.toggle_value == 0:
            print ("Now Closed")
            button.state = 0
            button.position = "closed"
            update_textbox(button, "HOUSE_FRONT is: ")
            update_textbox(button, button.position)
            
              
        else:
            #button.toggle_button.config(text=str('Open'))
            print ("Now Open")
            button.state = 1
            button.position = "open"
            update_textbox(button, "HOUSE_FRONT is: ")
            update_textbox(button, button.position)

        #Encrypts position from button 1
        button.encrypt = cipher_encryption(button.position, 'door')
        print ("Encryption: ", button.encrypt)
        print("Sending off the data once it works")

        #Sends encrypted position of button 1 off to the database
        data = {
            #'id' : button.count,
            'name' : 'HOUSE_FRONT',
            'status' : button.encrypt if button.state == 0 else button.encrypt
        }

        #Confirms position of button 1 was saved
        response = requests.post(url,json=data)
        if response.status_code == 200:
            print("Door status saved")
            print(button.position)
        else:
            print("Error occured", response.status_code)
        print("Data sent, current door position is: ", button.position)
        
        #Grabs status of "HOUSE_FRONT" to decrypt
        url = 'http://localhost:3000/project/doors/HOUSE_FRONT'
        response = requests.get(url, json=data)
        if response.status_code == 200:
            door_status = response.json().get('status')
        
        #Decrypts status of "HOUSE_FRONT"
        button.decrypt = cipher_decryption(door_status, 'door')

        print('Decryption: ', button.decrypt)
        print("House front is: ", button.decrypt)

#----------------------------------------------------------
#Toggle setup for the button 2
#----------------------------------------------------------

    def toggle2 (button):

        #Connects to the update path
        url = 'http://localhost:3000/project/doors/update'

        #Setting up toggling for button 2
        print("Toggling button state...")
        button.toggle_value2 = not button.toggle_value2

        #If/Else to toggle whether button 2 "closed" or "open"
        if button.toggle_value2 == 0:
            print ("Now Closed")
            button.state2 = 0
            button.position2 = "closed"
            update_textbox(button, "HOUSE_REAR is: ")
            update_textbox(button, button.position2)
              
        else:
            print ("Now Open")
            button.state2 = 1
            button.position2 = "open"
            update_textbox(button, "HOUSE_REAR is: ")
            update_textbox(button, button.position2)

        #Encrypts position from button 2
        button.encrypt2 = cipher_encryption(button.position2, 'door')
        print ("Encryption: ", button.encrypt2)
        print("Sending off the data once it works")

        #Sends encrypted position of button 2 off to the database
        data = {
            #'id' : button.count,
            'name' : 'HOUSE_BACK',
            'status' : button.encrypt2 if button.state2 == 0 else button.encrypt2
        }

        #Confirms position of button 2 was saved
        response = requests.post(url,json=data)
        if response.status_code == 200:
            print("Door status saved")
            print(button.position2)
        else:
            print("Error occured", response.status_code)
        print("Data sent, current door position is: ", button.position2)
        
        #Grabs status of "HOUSE_REAR" to decrypt
        url = 'http://localhost:3000/project/doors/HOUSE_BACK'
        response = requests.get(url, json=data)
        if response.status_code == 200:
            door_status = response.json().get('status')

        #Decrypts status of "HOUSE_REAR"
        button.decrypt2 = cipher_decryption(door_status, 'door')

        print('Decryption: ', button.decrypt2)
        print("House back is: ", button.decrypt2)

#----------------------------------------------------------
#Toggle setup for the button 3
#----------------------------------------------------------

    def toggle3 (button):

        #Connects to the update path
        url = 'http://localhost:3000/project/doors/update'

        #Setting up toggling for button 3
        print("Toggling button state...")
        button.toggle_value3 = not button.toggle_value3

        #If/Else to toggle whether button 3 "closed" or "open"
        if button.toggle_value3 == 0:
            print ("Now Closed")
            button.state3 = 0
            button.position3 = "closed"
            update_textbox(button, "GARAGE is: ")
            update_textbox(button, button.position3)
              
        else:
            print ("Now Open")
            button.state3 = 1
            button.position3 = "open"
            update_textbox(button, "GARAGE is: ")
            update_textbox(button, button.position3)

        #Encrypts position from button 3
        button.encrypt3 = cipher_encryption(button.position3, 'door')
        print ("Encryption: ", button.encrypt3)
        print("Sending off the data once it works")

        #Sends encrypted position of button 3 off to the database
        data = {
            #'id' : button.count,
            'name' : 'GARAGE',
            'status' : button.encrypt3 if button.state3 == 0 else button.encrypt3
        }

        #Confirms position of button 3 was saved
        response = requests.post(url,json=data)
        if response.status_code == 200:
            print("Door status saved")
            print(button.position3)
        else:
            print("Error occured", response.status_code)
        print("Data sent, current door position is: ", button.position3)
        
        #Grabs status of "GARAGE" to decrypt
        url = 'http://localhost:3000/project/doors/GARAGE'
        response = requests.get(url, json=data)
        if response.status_code == 200:
            door_status = response.json().get('status')

        #Decrypts status of "GARAGE"
        button.decrypt3 = cipher_decryption(door_status, 'door')

        print('Decryption: ', button.decrypt3)
        print("Garage is: ", button.decrypt3)

#----------------------------------------------------------
#Main sets up the window
#----------------------------------------------------------

def main():

    print("Starting ToggleButtonApp...")

    #Checking if app is connected to the server
    url = 'http://localhost:3000/'
    response = requests.get(url)
    if response.status_code == 200:
        print("Connected")
    else:
        print("Not Connected")
    print (response.text)

    #For bug fixing purposes, gives the current table in the database
    #url = 'http://localhost:3000/project/doors/'
    #response = requests.get(url)

    #Setting up app window
    root = tk.Tk()
    root.geometry("650x450")
    app = ToggleButtonApp(root)
    root.mainloop()
    
    print("ToggleButtonApp finished.")

if __name__ == "__main__":
    main()