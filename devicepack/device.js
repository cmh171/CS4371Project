let opened = "fa-door-open"
let closed = "fa-door-closed"

/*function pressed() {
    let door = document.getElementById("door");

    if (door.classList[1] === closed)
        door.classList.replace(closed, opened);
    else
        door.classList.replace(opened, closed);
}*/

/**
 * get door by name
 *  if 404, then attempt to register the device
 */

function fetchData() {
    console.log("Fetching");
    fetch('http://127.0.0.1:8000/test/doors/HOUSE_FRONT')
    .then((response) => {
        if(response.status === 404) {
            register();
        }
        else if (response.ok) {
            return response.json();
        }
    })
    .then((data) => {
        //console.log(data.status);
        let door = document.getElementById("door");
        if (data.status === "closed")
            door.classList.replace(opened, closed);
        else
            door.classList.replace(closed, opened);
    });
}

function register() {
    fetch('http://127.0.0.1:8000/test/doors/register', {
        method: 'POST',
        body: JSON.stringify({
            name: 'HOUSE_FRONT',
            status: 'closed'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

let interval = setInterval(fetchData, 5000);