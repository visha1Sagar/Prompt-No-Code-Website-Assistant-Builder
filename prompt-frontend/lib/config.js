// Configuration file for the frontend application
const config = {
  // Backend API URL - defaults to localhost:8000 if not set in environment
  backendUrl: process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000",
  
  // Frontend URL for script generation
  frontendUrl: process.env.NEXT_PUBLIC_FRONTEND_URL || "http://localhost:3000",
};

export default config;
