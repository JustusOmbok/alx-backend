import redis from 'redis';

// Create a Redis client for subscribing
const subscriberClient = redis.createClient();

// Handle connection event
subscriberClient.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Handle error event
subscriberClient.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err}`);
});

// Subscribe to the "holberton school channel"
subscriberClient.subscribe('holberton school channel');

// Handle message event
subscriberClient.on('message', (channel, message) => {
    console.log(message);
    if (message === 'KILL_SERVER') {
        subscriberClient.unsubscribe();
        subscriberClient.quit();
    }
});
