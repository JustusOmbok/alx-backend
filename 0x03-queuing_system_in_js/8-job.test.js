import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
    let queue;

    beforeEach(() => {
        // Create a queue with Kue
        queue = kue.createQueue();
        // Enter test mode
        queue.testMode.enter();
    });

    afterEach(() => {
        // Clear the queue
        queue.testMode.clear();
        // Exit test mode
        queue.testMode.exit();
    });

    it('should display an error message if jobs is not an array', () => {
        expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
    });

    it('should create two new jobs to the queue', () => {
        const jobs = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account'
            },
            {
                phoneNumber: '4153518781',
                message: 'This is the code 5678 to verify your account'
            }
        ];

        createPushNotificationsJobs(jobs, queue);

        // Get all jobs in the queue
        const queuedJobs = queue.testMode.jobs;
        
        // Expect two jobs to be created
        expect(queuedJobs).to.have.lengthOf(2);

        // Check job properties
        expect(queuedJobs[0].type).to.equal('push_notification_code_3');
        expect(queuedJobs[0].data).to.deep.equal(jobs[0]);

        expect(queuedJobs[1].type).to.equal('push_notification_code_3');
        expect(queuedJobs[1].data).to.deep.equal(jobs[1]);
    });
});
