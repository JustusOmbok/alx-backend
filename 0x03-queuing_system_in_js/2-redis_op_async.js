import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client
const client = redis.createClient();

// Promisify Redis functions
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Handle connection event
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Handle error event
client.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err}`);
});

// Handle connection close event
client.on('end', () => {
    console.log('Connection to Redis server closed');
});

// Function to set a new school value in Redis
async function setNewSchool(schoolName, value) {
    await setAsync(schoolName, value);
    console.log('Reply: OK');
}

// Function to display the value of a school in Redis using async/await
async function displaySchoolValue(schoolName) {
    try {
        const reply = await getAsync(schoolName);
        console.log(reply);
    } catch (err) {
        console.error(`Error retrieving value for ${schoolName}: ${err}`);
    }
}

// Call functions
(async () => {
    await displaySchoolValue('Holberton');
    await setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');
})();
