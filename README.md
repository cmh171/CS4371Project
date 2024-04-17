CS.4371.251 - Computer Systems Security   
Professor: Dr. Heena Rathore   
Texas State University   
04/17/2024

Authors (Group 15) consists of:   
Hunter Treadway, James Allen, Nathan Padgett, Chris Hanly, and Sam Nava.

-------------------------------------------

Overview:   
A. Preamble   
B. Dependencies   
C. Clone / Download Source Code   
D. Server Setup   
E. Application Setup   
F. Application & Endpoint Use   
G. Addendum   

-------------------------------------------

A. Preamble:

The common IOT schema includes three core components: An IOT device, a Server, and an Application.   
Namely, an application is used to send messages to an IOT server/hub.   
These messages are then read from the server/hub by the IOT device.    

As observed in Sensitive Information Tracking in Commodity IoT (https://arxiv.org/pdf/1802.08307v1.pdf), sensitive data flows were being emitted from the IOT device and IOT application.   
The team in this paper illustrated with a tool called SAINT (Static Taint Analysis Tool) that program source code
from over 200 Samsung SmartHub applications, that over 50% were trafficking potentially sensitive information.

Concerning these sensitive data flows, our project is a demonstation of this IOT architecture and
how encryption can be used to mask sensitive data traffic. Our demonstration uses a Hill cipher for
encryption that is hardcoded into the Application and IOT device. Furthermore the "IOT Device" in 
the context of this project is in fact a javascript application. This javascript application is being
used to imitate software that may actually be seen on an IOT device.   

--------------------------------------------

B. Dependencies   

The dependencies for running this project locally on your machine include:   

    1. Node JS (to run the REST server) https://nodejs.org/en/download   
    2. Pip (to install necessary python dependencies) https://pip.pypa.io/en/stable/installation/   
    3. Modern browser (to view device endpoint status) https://www.mozilla.org/en-US/firefox/new/   

Install dependences 1, 2, and (if necessary) 3.    

--------------------------------------------

C. Clone / Download Source Code   

The source code is on this github repository: https://github.com/cmh171/CS4371Project   

1. The simplest way to use this code is to download the .zip file:   
    a. On the github page, Press the green "<> Code" button   
    b. Select "Download as .zip"   
    c. In your Downloads folder, extract the contents of the .zip (usually by double-clicking)   
    d. Move the contents of the .zip to a desired working folder, hereby referred to as $folder.   

2. Alternatively, you can clone the github repo:
    a. If it is not already installed, install Git to your computer   
        i. https://git-scm.com/book/en/v2/Getting-Started-Installing-Git   
    b. Create a directory to work in   
    c. In Powershell or Terminal, navigate to the directory you just made   
    d. In Powershell or Terminal, run "git clone https://github.com/cmh171/CS4371Project.git"   
    e. The source code will now be in your working folder under a directory named
        "CS4371Project"   
    f. From here forward, the directory '$workingFolder/CS4371Project' will be referred to
        as $folder.   

--------------------------------------------

D. Server Setup   

A REST server needs to be running in order to mediate updates between the Application and the Device.
This REST server is connecting to a cloud instance of MongoDB.   

    1. Download the source code as seen in section C.
    2. Open terminal/ powershell on your device and change directory to $folder/serverpack     
    3. In the terminal, run "npm start"    
    4. On a successful server start, you will see console output including   
        "Server is running on port 3000"   
        "Connected to MongoDB database"   
    5. At this point, this REST server is running. Leave this terminal window open and open a new   
        terminal/powershell window.    

--------------------------------------------

E. Application Setup   
A simple python application will be used to send updates to the REST server through a simple GUI.   

    1. Change directory to $folder/pyapp   
    2. In the terminal, run "pip install pymongo requests numpy"   
    3. Once those install have completed, run "python3 testingapp.py"   
        If 'python3' is not setup in your PATH, you will need to either run the python code   
        through an IDE (like IDLE or VSCode), or configure your PATH (https://realpython.com/add-python-to-path/)   
    4. A GUI should launch in your desktop environment.   

--------------------------------------------

F. Application & Endpoint Use   
A javascript web application will be used to serve as a "device controller", otherwise known as a device endpoint.   
The javascript web application can register new devices with the REST server and application.   
Otherwise, it periodically reads from the REST server to acquire status updates.   

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

G. Addendum   

1. Material Learned from the Project

    Our team learned about the environment of code analysis tools and frameworks often found in certain 
    development communities. Namely, SAINT and IOTBench were tools developed for use by developers to make
    their code more secure.   

    Furthermore, we learned about the architecture of IOT environments. Namely, how devices interact with a 
    server/hub, and how that hub then communicates with the IOT Application.   

    Finally, we all got some useful experience in using Git in a team environment and applying the MERN stack
    and python in a useful way.  

2. Lessons Learned / What Went Wrong?

    Above all else, our team learned one large and glaring lesson: "Development environments change fast."   
    When selecting our topic and making a proposal, our team was very myopic and focused on how we can 
    apply the tools and techniques described in the paper we had studied.   

    Little did we know that the SAINT tool described in the paper had been completely abandoned for over five years.   
    The online version of the tool was defunct and the offline version of the tool was inaccessible.   

    Furthermore, the collection of Samsung SmartThings apps that was reportedly hosted on a community GitHub
    was no longer there. We found that the entire development framework used by Samsung had moved towards a
    lua-based "Edge Drivers" schema (https://community.smartthings.com/t/faq-i-have-no-idea-what-edge-is-is-that-a-new-developer-tool-2022/237775). Most importantly, we no longer had access to source code that was previously available. 

    Thus, our team could no longer follow our original project proposal. We could not apply the SAINT tool against a selection of apps and analyze those taint streams more closely. Instead, we had to pivot and demonstrate a simple solution to the "exposed potentially sensitive data" issue that was observed in the paper. In turn, we created software to model the common IOT architecture and applied encryption to mask potentially-sensitive data streams. 


3. Archaeology

    Sensitive Information Tracking in Commodity IoT (https://arxiv.org/pdf/1802.08307v1.pdf)   

    A Survey on IoT Platforms: Communication, security, and privacy perspectives (https://www.sciencedirect.com/science/article/abs/pii/S1389128621001444)   
