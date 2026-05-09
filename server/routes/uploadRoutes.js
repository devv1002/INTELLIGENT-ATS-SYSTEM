import express from "express";

import protect from "../middleware/authMiddleware.js";

import upload from "../config/multer.js";

import {
  uploadResume,
} from "../controllers/uploadController.js";

const router = express.Router();


// RESUME UPLOAD
router.post(
  "/resume",
  protect,
  upload.single("resume"),
  uploadResume
);

export default router;