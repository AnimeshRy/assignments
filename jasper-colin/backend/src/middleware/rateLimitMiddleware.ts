import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';

dotenv.config();

// Create a limiter for general API endpoints
export const apiLimiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000', 10), // default 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX || '100', 10), // default 100 requests per windowMs
  message: {
    status: 'error',
    message: 'Too many requests from this IP, please try again after 15 minutes'
  },
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});

// Create a stricter limiter for authentication endpoints (if needed in the future)
export const authLimiter = rateLimit({
  windowMs: parseInt(process.env.AUTH_RATE_LIMIT_WINDOW_MS || '3600000', 10), // default 1 hour
  max: parseInt(process.env.AUTH_RATE_LIMIT_MAX || '5', 10), // default 5 requests per windowMs
  message: {
    status: 'error',
    message: 'Too many login attempts from this IP, please try again after an hour'
  },
  standardHeaders: true,
  legacyHeaders: false,
});
