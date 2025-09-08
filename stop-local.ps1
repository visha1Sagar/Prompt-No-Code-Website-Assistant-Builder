# Quick Backend Stop Commands

# Stop backend container
Write-Host "🛑 Stopping backend container..." -ForegroundColor Yellow
docker-compose down

# Remove containers and volumes (clean slate)
Write-Host "🧹 Cleaning up containers and volumes..." -ForegroundColor Yellow
docker-compose down -v --remove-orphans

# Remove images (if you want to rebuild from scratch)
$removeImages = Read-Host "Do you want to remove Docker images as well? (y/N)"
if ($removeImages -eq "y" -or $removeImages -eq "Y") {
    Write-Host "🗑️ Removing Docker images..." -ForegroundColor Yellow
    docker rmi $(docker images "prompt*" -q) 2>$null
}

Write-Host "✅ Backend cleanup complete!" -ForegroundColor Green
Write-Host "📝 Note: Your Vercel frontend deployment is unaffected" -ForegroundColor Blue
