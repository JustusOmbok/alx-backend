const express = require('express');
const kue = require('kue');
const { promisify } = require('util');
const redis = require('redis');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();

// Promisify Redis functions
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Function to reserve a seat
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Function to get the current available seats
const getCurrentAvailableSeats = async () => {
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats) || 0;
};

// Set the initial number of available seats to 50
reserveSeat(50);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Create a Kue queue
const queue = kue.createQueue();

// Event listener for completed jobs
queue.on('job complete', (id) => {
  kue.Job.get(id, (err, job) => {
    if (err){
	  console.error(`Error getting job ${id}: ${err.message}`);
	  return;
    }
    console.log(`Seat reservation job ${job.id} completed`);
  });
});

// Event listener for failed jobs
queue.on('job failed', (id, err) => {
  kue.Job.get(id, (error, job) => {
    if (error) return;
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });
});

// Route to process the queue and reserve seats
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  const currentAvailableSeats = await getCurrentAvailableSeats();
  if (currentAvailableSeats <= 0) {
    reservationEnabled = false;
    return;
  }

  const newAvailableSeats = currentAvailableSeats - 1;
  await reserveSeat(newAvailableSeats);

  if (newAvailableSeats <= 0) {
    reservationEnabled = false;
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
