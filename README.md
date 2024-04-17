Group 15 consists of:   
Hunter Treadway, James Allen, Nathan Padgett, Chris Hanly, and Sam Nava.

Preamble:

The common IOT schema includes three core components: An IOT device, a Server, and an Application.   
Namely, an application is used to send messages to an IOT server/hub.   
These messages are then read from the server/hub by the IOT device.    

As observed in Sensitive Information Tracking in Commodity IoT (https://arxiv.org/pdf/1802.08307v1.pdf), sensitive data flows were being emitted from the IOT device and IOT application.   

Concerning these sensitive data flows, our project is a demonstation of this IOT architecture and
how encryption can be used to mask sensitive data traffic. Our demonstration uses a Hill cipher for
encryption that is hardcoded into the Application and IOT device. Furthermore the "IOT Device" in 
the context of this project is in fact a javascript application. This javascript application is being
used to imitate software that may actually be seen on an IOT device.   

-------------------------------------------

Overview:   
A. Dependencies   
B. Server Setup   
C. Application Setup   
D. Application & Endpoint Use   
E. Addendum   

--------------------------------------------

A. Dependencies   

The dependencies for running this project locally on your machine include:   
    1. Node JS (to run the REST server) https://nodejs.org/en/download   
    2. Pip (to install necessary python dependencies) https://pip.pypa.io/en/stable/installation/   
    3. Modern browser (to view device endpoint status) https://www.mozilla.org/en-US/firefox/new/   
    4. Source code (https://github.com/cmh171/CS4371Project)   

Install dependences 1, 2, and (if necessary) 3.   
Download the source code.   

--------------------------------------------

B. Server Setup   

    1. Once the source code is downloaded, unzip the compressed file to a desired location   
        hereby known as $folder.   
    2. Open terminal/ powershell on your device and change directory to $folder/serverpack     
    3. In the terminal, run "npm start"    
    4. On a successful server start, you will see console output including   
        "Server is running on port 3000"   
        "Connected to MongoDB database"   
    5. At this point, this REST server is running. Leave this terminal window open and open a new   
        terminal/powershell window.    

--------------------------------------------

C. Application Setup   

    1. Change directory to $folder/pyapp   
    2. In the terminal, run "pip install pymongo requests numpy"   
    3. Once those install have completed, run "python3 testingapp.py"   
        If 'python3' is not setup in your PATH, you will need to either run the python code   
        through an IDE (like IDLE or VSCode), or configure your PATH (https://realpython.com/add-python-to-path/)   
    4. A GUI should launch in your desktop environment.   

--------------------------------------------

D. Application & Endpoint Use   

    1. Under $folder/devicepack exists a file exists "device.html"   
    2. Run "device.html" in a modern browser (eg Firefox)   
        This can be most easily performed by using the "explorer" GUI to navigate to the   
        $folder/devicepack directory and opening the file with your browser.   
    3. On the webpage, press the "Start Sim" button. Doors and their current status will display.   
    4. Now that the REST Server, the PyApp application, and the endpoint are all showing,   
        we can use the application to control the status of the device.    
    5. On the running GUI of testingapp.py, click on the status buttons of the different doors.   
    6. The status between "opened" and "closed" will change on the device endpoint (as viewed in your browser)   

This is a demonstration of the three-component setup of the standard IOT device, using encryption to relay status updated.   

--------------------------------------------

E. Addendum   

Scholarly Papers:   

    Sensitive Information Tracking in Commodity IoT (https://arxiv.org/pdf/1802.08307v1.pdf)   

    A Survey on IoT Platforms: Communication, security, and privacy perspectives (https://www.sciencedirect.com/science/article/abs/pii/S1389128621001444)   
