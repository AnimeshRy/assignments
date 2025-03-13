import helmet from 'helmet';
import mongoSanitize from 'express-mongo-sanitize';
import hpp from 'hpp';
import { Express } from 'express';
import compression from 'compression';
import cookieParser from 'cookie-parser';

export const configureSecurityMiddleware = (app: Express): void => {
  // Set security HTTP headers
  app.use(helmet());

  // Additional security headers
  app.use(
    helmet.contentSecurityPolicy({
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    })
  );

  // Sanitize data against NoSQL query injection
  app.use(mongoSanitize());

  // Prevent parameter pollution
  app.use(hpp());

  // Enable gzip compression
  app.use(compression());

  // Parse cookies
  app.use(cookieParser());

  // Trust proxy if behind a reverse proxy (like nginx)
  app.set('trust proxy', 1);
};
