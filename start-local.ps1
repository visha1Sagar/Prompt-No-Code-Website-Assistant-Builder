# Docker Backend-Only Setup and Run Script
# Frontend is deployed on Vercel separately

Write-Host "🚀 Starting Prompt AI Chatbot Backend with Docker..." -ForegroundColor Green
Write-Host "📝 Note: Frontend is deployed on Vercel separately" -ForegroundColor Blue

# Check if Docker is running
Write-Host "📋 Checking Docker installation..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not running. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created. Please add your OpenAI API key to the .env file." -ForegroundColor Green
    Write-Host "💡 You can also let users enter API keys via the frontend." -ForegroundColor Blue
}

# Ask user for development or production mode
$mode = Read-Host "Run backend in development mode with hot reload? (y/N)"
if ($mode -eq "y" -or $mode -eq "Y") {
    Write-Host "🔨 Building and starting backend container in development mode..." -ForegroundColor Yellow
    docker-compose -f docker-compose.dev.yml up --build -d backend
    $composeFile = "docker-compose.dev.yml"
    $apiUrl = "http://localhost:8000"
} else {
    Write-Host "🔨 Building and starting backend container in production mode..." -ForegroundColor Yellow
    docker-compose up --build -d backend
    $composeFile = "docker-compose.yml"
    $apiUrl = "http://localhost:8000"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 Backend started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Backend API: $apiUrl" -ForegroundColor Cyan
    Write-Host "🏥 Health Check: $apiUrl/health" -ForegroundColor Cyan
    Write-Host "📚 API Docs: $apiUrl/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 Configure your Vercel frontend to use: $apiUrl" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔍 To check container status: docker ps" -ForegroundColor Gray
    Write-Host "📊 To view logs: docker-compose -f $composeFile logs -f backend" -ForegroundColor Gray
    Write-Host "📱 Frontend (Next.js): http://localhost:3000" -ForegroundColor Cyan
    Write-Host "🔗 Backend API (FastAPI): http://localhost:8000" -ForegroundColor Cyan
    Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔍 To view logs: docker-compose logs -f" -ForegroundColor Yellow
    Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🚀 Your AI Chatbot Platform is ready to use!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to start containers. Check the logs with: docker-compose logs" -ForegroundColor Red
}
