/**
 * IoT Device Simulator
 * The device polls its state from the server, then matches the polled state.
 *      This is inefficient, but works.
 * 
 * The html file needs to be opened in a Browser, not with npm.
 */

// variables for easy calling.
let opened = "fa-door-open"
let closed = "fa-door-closed"
let devices = [] // list to contain all the devices once they are fetched
let intervals = []; // contains "intervals", a periodic timer that will make HTTP requests

function fetchRegisteredDevices() {
    console.log('Fetching all devices...');
    fetch(`http://127.0.0.1:3000/test/doors`)
        .then((response) => {
            if (response.ok) return response.json();
        })
        .then((data) => {
            data.forEach(element => {
                devices.push(element); // add all fetched devices to device[]
            });
            displayDevices();

            devices.forEach(device => {
                intervals[device.name] = setInterval(() => fetchDeviceStatus(device), 3000); // create a timer for each device
            });
        });
}

/**
 * Poll device status from the hub/server, then change the device status to match polled status.
 */
function fetchDeviceStatus(device) {
    //console.log(`Fetching: ${device.name}`);
    fetch(`http://127.0.0.1:3000/test/doors/${device.name}`)
        .then(response => {
            if (response.status === 404) {
                // register device?
            }
            else if (response.ok) return response.json();
        })
        .then(data => {
            //console.log(data);
            let dev = document.getElementById(`${device._id}`); // this gets the DOM element
            if (data.status === "closed") dev.classList.replace(opened, closed);
            else dev.classList.replace(closed, opened);
        });
}

/**
 * If the device isn't registered, register the device with the hub/server.
 */
function register(deviceName) {
    fetch('http://127.0.0.1:3000/test/doors/register', {
        method: 'POST',
        body: JSON.stringify({
            name: deviceName,
            status: 'closed'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log('Registered got a response');
        if (response.ok) {
            console.log("Device Registered");
            devices = []; // clear the devices
            let childElements = document.body.querySelectorAll(".device-box");
            //document.body.innerHTML = "";
            childElements.forEach(element => {
                element.remove();
            });
            intervals.forEach(interval => {
                clearInterval(interval);
            });
            fetchRegisteredDevices();
        }
    });
}

function displayDevices() {
    devices.forEach(device => {
        document.body.appendChild(deviceDisplay(device));
    });
}

function deviceDisplay(device) {
    // create i element and attach correct attributes
    let i = document.createElement("i");
    i.classList.add("fa-solid");
    if (device.status === "closed") i.classList.add(closed);
    else i.classList.add(opened);
    i.id = device._id;

    let header = document.createElement("h2");
    header.innerText = device.name;

    let deviceBox = document.createElement("div");
    deviceBox.classList.add("device-box");

    deviceBox.appendChild(header);
    deviceBox.appendChild(i);

    return deviceBox;
}

let start = document.getElementById("start");
let addDev = document.getElementById("add");
start.addEventListener('click', () => {
    fetchRegisteredDevices();
});
addDev.addEventListener('click', () => {
    console.log("Clicked");
    let addInput = document.getElementById("device-input");
    console.log(addInput.value);
    register(addInput.value);
    addInput.value = "";
});

