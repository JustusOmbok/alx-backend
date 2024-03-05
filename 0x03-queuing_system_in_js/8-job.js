import kue from 'kue';

function createPushNotificationsJobs(jobs, queue) {
    // Validate if jobs is an array
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    // Create a job for each job object in the jobs array
    jobs.forEach(jobData => {
        // Create a new job in the queue push_notification_code_3
        const job = queue.create('push_notification_code_3', jobData);

        // When the job is created, log the job ID
        job.on('enqueue', () => {
            console.log(`Notification job created: ${job.id}`);
        });

        // When the job is complete, log that the job completed
        job.on('complete', () => {
            console.log(`Notification job ${job.id} completed`);
        });

        // When the job fails, log the error
        job.on('failed', (err) => {
            console.log(`Notification job ${job.id} failed: ${err}`);
        });

        // When the job progresses, log the progress percentage
        job.on('progress', (progress) => {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });

        // Save the job to the queue
        job.save();
    });
}

export default createPushNotificationsJobs;
