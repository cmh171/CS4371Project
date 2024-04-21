/* Server.js

Simple REST Server used to facilitate updates between an IOT application and 
IOT Device controller.

Setup based on the MERN framework.
Uses Express, Mongoose, and MongoDB.
Connecting to a MongoDB Atlas cloud database.

Primary Contributors: Christopher Hanly and Hunter Treadway
*/

// require mongoose, express, and cors
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

// use mongoose door model
const Door = require('./doorModel');

const app = express();

// Middleware to parse JSON requests
app.use(express.json());

/**
 * Needed CORS for the device to connect to the server. 
 */
const corsOptions = {
  origin: '*'
};

// Middleware to use CORS
app.use(cors(corsOptions));

// Connect to MongoDB
mongoose.connect('mongodb+srv://mongoAccess:systemsecurity@application.dkdfsrp.mongodb.net/project', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Connection successful
mongoose.connection.once('open', () => {
  console.log('Connected to MongoDB database');
});

// Connection error
mongoose.connection.on('error', (err) => {
  console.error('MongoDB connection error:', err);
});


// ROUTES
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

/**
 * Gets all Doors
 */
app.get('/project/doors', async (req, res) => {
  try {
    const doors = await Door.find();
    res.json(doors);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

/*
 * Gets the status of a single Door
 */
app.get('/project/doors/:name', async (req, res) => {
  //console.log("Get door");

  try {
    const door = await Door.findOne({ name: req.params.name });
    if (door) {
      res.json({ 
                name: door.name,
                status: door.status,
                cipher: door.cipher 
                },);
    } else {
      res.status(404).json({ message: 'Door not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

/**
 * Register a new Door device.
 */
app.post('/project/doors/register', async (req, res) => {
  console.log(req.body);
  try {
    Door.create({ name: req.body.name, status: req.body.status, cipher: req.body.cipher }).then(() => {
      res.sendStatus(201);
    });
  }
  catch (error) {
    res.status(500).send({ message: error.message });
  }
});

/*
 * Update a single Door. Do this from the App
 */
app.post('/project/doors/update', async (req, res) => {
  console.log("UPDATE CALLED");
  const { name, status, cipher } = req.body;
  console.log(name);
  console.log(status);
  console.log(cipher);
  // Check if the status is valid (0 or 1)
  if (!status) {
    return res.status(400).json({ message: 'Invalid status.' });
  }

  try {
    const door = await Door.findOneAndUpdate(
      { name: name },
      { $set: { status: status,
                cipher: cipher } },
      { new: true } // Return the updated document
    );

    if (door) {
      res.json({ message: 'Door status updated', door: door });
    } else {
      res.status(404).json({ message: 'Door not found' });
    }
  } catch (error) { 
    console.log("There was an error updating the device.");
    res.status(500).json({ message: error.message });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
