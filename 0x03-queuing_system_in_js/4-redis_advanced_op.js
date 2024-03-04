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

// Function to create a hash in Redis
function createHash() {
    client.hset('HolbertonSchools', 'Portland', '50', redis.print);
    client.hset('HolbertonSchools', 'Seattle', '80', redis.print);
    client.hset('HolbertonSchools', 'New York', '20', redis.print);
    client.hset('HolbertonSchools', 'Bogota', '20', redis.print);
    client.hset('HolbertonSchools', 'Cali', '40', redis.print);
    client.hset('HolbertonSchools', 'Paris', '2', redis.print);
}

// Function to display the hash stored in Redis
function displayHash() {
    client.hgetall('HolbertonSchools', (err, reply) => {
        if (err) {
            console.error(`Error retrieving hash from Redis: ${err}`);
            return;
        }
        console.log(reply);
    });
}

// Call functions
createHash();
setTimeout(displayHash, 500); // Delay the displayHash function to ensure all hset operations are completed
