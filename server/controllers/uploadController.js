import Candidate from "../models/Candidate.js";


// UPLOAD RESUME
export const uploadResume = async (req, res) => {

  try {

    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No file uploaded",
      });
    }

    const candidate = await Candidate.create({
      resumeFile: req.file.path,
      uploadedBy: req.user.id,
    });

    res.status(201).json({
      success: true,
      message: "Resume uploaded successfully",
      candidate,
    });

  } catch (error) {

    console.log(error);

    res.status(500).json({
      success: false,
      message: "Server Error",
    });
  }
};