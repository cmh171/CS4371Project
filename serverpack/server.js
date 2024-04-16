const express = require('express');
const mongoose = require('mongoose');
const Door = require('./doorModel');
const cors = require('cors');

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

/**
 * Gets the status of a single Door
 */
app.get('/project/doors/:name', async (req, res) => {
  //console.log("Get door");


app.get('/project/doors/:name', async(req, res) =>
{
  try {
    const door = await Door.findOne({ name: req.params.name });
    if (door) {
      res.json({ status: door.status });
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
    Door.create({ name: req.body.name, status: req.body.status }).then(() => {
      res.sendStatus(201);
    });
  }
  catch (error) {
    res.sendStatus(500);
  }
});

/**
 * Update a single Door. Do this from the App
 */
app.post('/project/doors/update', async (req, res) => {
  console.log("UPDATE CALLED");
  const { name, status } = req.body;
  console.log(name);
  console.log(status);
  // Check if the status is valid (0 or 1)
  if (!status) {
    return res.status(400).json({ message: 'Invalid status.' });
  }

  try {
    const door = await Door.findOneAndUpdate(
      { name: name },
      { $set: { status: status } },
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

