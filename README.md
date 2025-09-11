# 🤖 Prompt No-Code Website Assistant Builder

A powerful no-code platform for creating intelligent AI chatbots that can be embedded on any website. Simply upload your documents, train your AI assistant, and deploy it anywhere with a single embed script.

---

## ✨ Features

### 🚀 **No-Code AI Training**
- **Drag & drop document uploads** (PDF, TXT, DOCX, and more)
- **Website crawling** with advanced content extraction using Crawl4AI
- **Automatic knowledge base creation** using ChromaDB vector storage


### 🔐 **Secure API Management**
- **User API key storage system** with file-based persistence
- **Multiple AI provider support** (OpenAI, Google, Hugging Face)
- **Secure credential handling** with proper encryption
- **User session management** with persistent storage

### 🐳 **Production Ready**
- **Docker containerization** with health checks and resource limits
- **Development and production modes** with hot reload support
- **CORS configuration** for frontend-backend integration
- **Comprehensive error handling** and validation

---

## 🏗️ Architecture

### **Backend (FastAPI + Python 3.11)**
- **FastAPI** web framework with automatic API documentation
- **ChromaDB** vector database for knowledge storage
- **LangChain** for document processing and AI integration
- **Crawl4AI** for intelligent website content extraction
- **User API storage system** for secure credential management

### **Frontend (Next.js 15 + React 19)**
- **Modern React** with App Router and server components
- **Responsive design** with Tailwind CSS and mobile-first approach
- **Radix UI components** for accessibility and consistent design
- **Real-time preview** and configuration interface

### **Infrastructure**
- **Docker containers** with multi-stage builds and security hardening
- **Health monitoring** with automatic restart policies
- **Volume persistence** for data storage and API keys
- **Resource management** with CPU and memory limits

---

## 🛠️ Installation

### Prerequisites
- **Docker & Docker Compose** (recommended)
- **Python 3.11+** (for local development)
- **Node.js 18+** (for frontend development)
- **OpenAI API Key** or other supported AI provider

### Quick Start with Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/prompt-no-code-website-assistant-builder.git
   cd prompt-no-code-website-assistant-builder
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

3. **Start the backend:**
   ```bash
   # For development with hot reload
   .\start-local.ps1
   
   # Or manually with Docker Compose
   docker-compose up --build -d backend
   ```

4. **Access the application:**
   - **Backend API:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

### Frontend Development Setup

1. **Navigate to frontend directory:**
   ```bash
   cd prompt-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure backend URL:**
   ```bash
   # Create .env.local
   echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Access frontend:** http://localhost:3000

---

## 🎯 Usage Guide

### 1. **Train Your AI Assistant**
- Navigate to the **Train** tab
- Upload documents or provide website URLs for crawling
- Configure your AI model and API keys
- Save your configuration to create the knowledge base

### 2. **Customize Your Chatbot**
- Use the **Playground** tab for real-time customization
- Set chatbot name, display name, and welcome messages
- Upload custom profile images and configure styling
- Preview changes in the integrated chat interface

### 3. **Deploy Your Assistant**
- Go to the **Train** tab to get your embed script
- Copy the generated script code
- Paste it in your website
- Your AI assistant is now live and ready to help users

---
## 🔧 Development

### **Backend Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Development**
```bash
# Install dependencies
npm install

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### **Docker Development**
```bash
# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up --build

# Production mode
docker-compose up --build

# View logs
docker-compose logs -f backend

# Clean up
docker-compose down -v --remove-orphans
```

---

## 🚀 Deployment

### **Backend Deployment**
- **Docker**: Use provided Docker configuration for containerized deployment
- **Cloud**: Deploy on AWS, GCP, Azure with container services
- **Server**: Direct deployment with Python and systemd service

### **Frontend Deployment**
- **Vercel**: Optimized for Next.js applications (recommended)
- **Netlify**: Static site generation support
- **Docker**: Include frontend in containerized deployment

### **Environment Configuration**
```env
# Backend (.env)
OPENAI_API_KEY=your_openai_api_key
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# Frontend (.env.local)
NEXT_PUBLIC_BACKEND_URL=https://your-backend-api.com
NEXT_PUBLIC_FRONTEND_URL=https://your-frontend.vercel.app
```

---

## 🤝 Contributing

Contributions are eagerly welcomed!  Help us make **Prompt** even more amazing.  Pull requests, feature suggestions, bug reports – all are highly appreciated!  Let's build the future of no-code chatbots together!


1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Development Setup**
1. Follow the installation guide above
2. Make your changes with proper testing
3. Ensure code follows our style guidelines
4. Submit PR with detailed description

---


## 📞 Contact

**Team Chateaus** - Let's Chat! 💬