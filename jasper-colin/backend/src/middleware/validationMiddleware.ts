import { Request, Response, NextFunction } from 'express';
import mongoose from 'mongoose';

export const validateProductId = (req: Request, res: Response, next: NextFunction) => {
  if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
    res.status(400);
    throw new Error('Invalid product ID');
  }
  next();
};

export const validateProductInput = (req: Request, res: Response, next: NextFunction) => {
  const { name, description, price, category } = req.body;

  if (!name || !description || !price || !category) {
    res.status(400);
    throw new Error('Please provide all required fields');
  }

  if (typeof price !== 'number' || price < 0) {
    res.status(400);
    throw new Error('Price must be a positive number');
  }

  next();
};
