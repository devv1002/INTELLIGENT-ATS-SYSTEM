import jwt from "jsonwebtoken";

const protect = async (req, res, next) => {

  try {

    const token = req.headers.authorization;

    if (!token) {
      return res.status(401).json({
        success: false,
        message: "No token provided",
      });
    }

    console.log("AUTH HEADER:", token);
    console.log("JWT SECRET:", process.env.JWT_SECRET);

    const decoded = jwt.verify(
      token.split(" ")[1],
      process.env.JWT_SECRET
    );

    req.user = decoded;

    next();

  } catch (error) {

    console.log("JWT ERROR:", error);
  
    return res.status(401).json({
      success: false,
      message: "Invalid token",
    });
  }
};

export default protect;