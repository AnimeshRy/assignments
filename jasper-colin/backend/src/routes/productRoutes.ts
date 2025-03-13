import express from 'express';
import {
  createProduct,
  getAllProducts,
  getProduct,
  updateProduct,
  deleteProduct,
} from '../controllers/productController';
import { validateProductId, validateProductInput } from '../middleware/validationMiddleware';
import { protect } from '../middleware/auth';

const router = express.Router();

router.route('/')
  .post(protect, validateProductInput, createProduct)
  .get(getAllProducts);

router.route('/:id')
  .get(validateProductId, getProduct)
  .put(protect, validateProductId, validateProductInput, updateProduct)
  .delete(protect, validateProductId, deleteProduct);

export default router;
