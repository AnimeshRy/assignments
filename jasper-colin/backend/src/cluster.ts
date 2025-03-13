import cluster from 'cluster';
import os from 'os';
import process from 'process';
import { startServer } from './index';

const numCPUs = os.cpus().length;

export const setupCluster = () => {
  if (cluster.isPrimary) {
    console.log(`Primary ${process.pid} is running`);
    console.log(`Setting up ${numCPUs} workers...`);

    // Fork workers based on CPU cores
    for (let i = 0; i < numCPUs; i++) {
      cluster.fork();
    }

    cluster.on('exit', (worker, code, signal) => {
      console.log(`Worker ${worker.process.pid} died (${signal || code})`);
      console.log('Starting a new worker...');
      cluster.fork();
    });

    // Log when a worker connects
    cluster.on('online', (worker) => {
      console.log(`Worker ${worker.process.pid} is online`);
    });

  } else {
    // Workers can share any TCP connection
    startServer();
    console.log(`Worker ${process.pid} started`);
  }
};

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  process.exit(1);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.error('Unhandled Rejection:', err);
  process.exit(1);
});

if (require.main === module) {
  setupCluster();
}
