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
  
    upload.array("resumes", 10),
  
    (req, res, next) => {
  
      const allowedTypes = [
  
        "application/pdf",
  
        "application/msword",
  
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ];
  
      for (const file of req.files) {
  
        if (
  
          !allowedTypes.includes(
            file.mimetype
          )
  
        ) {
  
          return res.status(400).json({
  
            success: false,
  
            message: "Invalid file type. Only PDF/DOC/DOCX allowed."
          });
        }
      }
  
      next();
    },
  
    uploadResume
  );

export default router;