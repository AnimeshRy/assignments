import express, { Express } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import connectDB from './config/database';
import productRoutes from './routes/productRoutes';
import authRoutes from './routes/auth.routes';
import { errorHandler, notFound } from './middleware/errorMiddleware';
import { apiLimiter } from './middleware/rateLimitMiddleware';
import { configureSecurityMiddleware } from './middleware/securityMiddleware';

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Security Middleware
configureSecurityMiddleware(app);

// CORS configuration with more secure options
app.use(
  cors({
    origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400, // 24 hours
  })
);

// Body parsing middleware with size limits
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// Apply rate limiting to all routes
app.use('/api', apiLimiter);

// Routes
app.use('/api/products', productRoutes);
app.use('/api/auth', authRoutes);

// Error Handling Middlewares
app.use(notFound);
app.use(errorHandler);

// Export the startServer function for use with clustering
export const startServer = async (): Promise<void> => {
  try {
    await connectDB();
    const server = app.listen(port, () => {
      console.log(`Server is running on port ${port}`);
    });

    // Implement graceful shutdown
    const gracefulShutdown = () => {
      console.log('Received kill signal, shutting down gracefully');
      server.close(() => {
        console.log('Closed out remaining connections');
        process.exit(0);
      });

      // If after
      setTimeout(() => {
        console.error('Could not close connections in time, forcefully shutting down');
        process.exit(1);
      }, 10000);
    };

    // Listen for shutdown signals
    process.on('SIGTERM', gracefulShutdown);
    process.on('SIGINT', gracefulShutdown);

  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
};

// Start the server if this file is run directly
if (require.main === module) {
  startServer();
}
