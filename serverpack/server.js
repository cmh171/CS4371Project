const express = require('express');
const mongoose = require('mongoose');
const Door = require('./doorModel');

const app = express();

// Middleware to parse JSON requests
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb+srv://cmh171:KiviHbcMrE7Ywipl@application.dkdfsrp.mongodb.net/', {
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


app.get('/test/doors', async (req, res) => {
  try {
    const doors = await Door.find();
    res.json(doors);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});


app.get('/test/doors/:name', async(req, res) =>
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

app.post('/test/doors/update', async (req, res) => {
  const { name, status } = req.body;

  // Check if the status is valid (0 or 1)
  if (status !== 0 && status !== 1) {
    return res.status(400).json({ message: 'Invalid status. Status must be 0 or 1.' });
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
    res.status(500).json({ message: error.message });
  }
});






// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

