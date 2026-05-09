import Candidate from "../models/Candidate.js";


// UPLOAD RESUME
export const uploadResume = async (req, res) => {

  try {

    if (!req.files || req.files.length === 0) {
      return res.status(400).json({
        success: false,
        message: "No file uploaded",
      });
    }

    const uploadedCandidates = await Promise.all(

        req.files.map(async (file) => {
      
          return await Candidate.create({
      
            resumeFile: file.path,
      
            uploadedBy: req.user.id,
      
          });
      
        })
      );

    res.status(201).json({
      success: true,
      message: "Resume uploaded successfully",
      files: req.files,
      candidates: uploadedCandidates
    });

  } catch (error) {

    console.log(error);

    res.status(500).json({
      success: false,
      message: "Server Error",
    });
  }
};