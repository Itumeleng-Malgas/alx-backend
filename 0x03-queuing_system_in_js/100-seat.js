import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;
const queue = kue.createQueue();
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected');
});

client.on('error', (err) => {
  console.error('Redis error:', err);
});

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

let reservationEnabled = true;
const INITIAL_AVAILABLE_SEATS = 50;

const reserveSeat = async (number) => {
  try {
    await setAsync('available_seats', number);
  } catch (error) {
    throw new Error(`Failed to reserve seat: ${error.message}`);
  }
};

const getCurrentAvailableSeats = async () => {
  try {
    const seats = await getAsync('available_seats');
    return parseInt(seats) || 0;
  } catch (error) {
    throw new Error(`Failed to get available seats: ${error.message}`);
  }
};

// Set initial available seats in Redis on application launch
reserveSeat(INITIAL_AVAILABLE_SEATS)
  .then(() => console.log(`Initial available seats set to ${INITIAL_AVAILABLE_SEATS}`))
  .catch((err) => console.error('Failed to set initial available seats:', err.message));

// Routes
app.get('/available_seats', async (req, res) => {
  try {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      console.error('Failed to create job:', err.message);
      return res.json({ status: 'Reservation failed' });
    }
    console.log('Job created with ID:', job.id);
    res.json({ status: 'Reservation in process' });
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      let availableSeats = await getCurrentAvailableSeats();
      if (availableSeats === 0) {
        reservationEnabled = false;
        console.log(`Reservation disabled, no seats available`);
        done(new Error('Not enough seats available'));
      } else {
        availableSeats--;
        await reserveSeat(availableSeats);
        console.log(`Seat reservation job ${job.id} completed`);
        done();
      }
    } catch (error) {
      console.error(`Seat reservation job ${job.id} failed: ${error.message}`);
      done(error);
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
