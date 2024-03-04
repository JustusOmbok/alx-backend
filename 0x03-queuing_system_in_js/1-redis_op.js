import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

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
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, redis.print);
}

// Function to display the value of a school in Redis
function displaySchoolValue(schoolName) {
    client.get(schoolName, (err, reply) => {
        if (err) {
            console.error(`Error retrieving value for ${schoolName}: ${err}`);
            return;
        }
        console.log(reply);
    });
}

// Call functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
