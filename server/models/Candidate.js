import mongoose from "mongoose";

const candidateSchema = new mongoose.Schema(
  {
    name: String,

    email: String,

    resumeFile: String,

    uploadedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
    },
  },
  {
    timestamps: true,
  }
);

const Candidate = mongoose.model(
  "Candidate",
  candidateSchema
);

export default Candidate;