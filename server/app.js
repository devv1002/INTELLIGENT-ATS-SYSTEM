import express from "express";
import cors from "cors";
import morgan from "morgan";
import uploadRoutes from "./routes/uploadRoutes.js";
import authRoutes from "./routes/authRoutes.js";
import testRoutes from "./routes/testRoutes.js";

const app = express();

app.use(express.json());

app.use(cors());

app.use(morgan("dev"));

// STATIC UPLOADS
app.use("/uploads", express.static("uploads"));


app.get("/", (req, res) => {
  res.json({
    message: "TalentLens AI Backend Running",
  });
});


// ROUTES
app.use("/api/auth", authRoutes);

app.use("/api/test", testRoutes);

app.use("/api/upload", uploadRoutes);

export default app;