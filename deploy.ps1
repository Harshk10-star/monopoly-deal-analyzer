# Monopoly Deal Analyzer - Windows PowerShell Deployment Script

param(
    [Parameter(Position=0)]
    [ValidateSet("docker", "dev", "development", "check", "help")]
    [string]$Action = "docker"
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green" 
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Colors.Red
}

function Test-CommandExists {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    $missingDeps = @()
    
    if (-not (Test-CommandExists "docker")) {
        $missingDeps += "docker"
    }
    
    if (-not (Test-CommandExists "docker-compose")) {
        $missingDeps += "docker-compose"
    }
    
    if ($missingDeps.Count -gt 0) {
        Write-Error "Missing dependencies: $($missingDeps -join ', ')"
        Write-Status "Please install the missing dependencies and try again."
        Write-Status "Docker Desktop for Windows includes both docker and docker-compose."
        Write-Status "Download from: https://www.docker.com/products/docker-desktop"
        exit 1
    }
    
    Write-Success "All prerequisites are installed!"
}

function Initialize-Environment {
    Write-Status "Setting up environment..."
    
    if (-not (Test-Path ".env")) {
        Write-Status "Creating .env file from template..."
        Copy-Item ".env.example" ".env"
        Write-Warning "Please edit .env file with your actual configuration values!"
        Write-Status "Key values to update:"
        Write-Host "  - POSTGRES_PASSWORD" -ForegroundColor $Colors.White
        Write-Host "  - SECRET_KEY" -ForegroundColor $Colors.White
        Write-Host "  - STRIPE_SECRET_KEY (if using payments)" -ForegroundColor $Colors.White
        Write-Host "  - STRIPE_PUBLISHABLE_KEY (if using payments)" -ForegroundColor $Colors.White
        Write-Host ""
        Read-Host "Press Enter to continue after updating .env file"
    } else {
        Write-Success ".env file already exists"
    }
}

function Deploy-Docker {
    Write-Status "Deploying with Docker Compose..."
    
    # Build and start services
    Write-Status "Building and starting services..."
    docker-compose up --build -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker deployment failed!"
        exit 1
    }
    
    # Wait for services to be ready
    Write-Status "Waiting for services to be ready..."
    Start-Sleep -Seconds 10
    
    # Check service health
    $services = docker-compose ps
    if ($services -match "Up.*healthy") {
        Write-Success "Services are running and healthy!"
    } else {
        Write-Warning "Some services may not be fully ready yet. Checking status..."
        docker-compose ps
    }
    
    # Show service URLs
    Write-Host ""
    Write-Success "Deployment completed!"
    Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor $Colors.Green
    Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor $Colors.Green
    Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor $Colors.Green
    Write-Host ""
    Write-Status "To view logs: docker-compose logs -f"
    Write-Status "To stop services: docker-compose down"
}

function Deploy-Development {
    Write-Status "Setting up development environment..."
    
    # Check if Python and Node.js are installed
    if (-not (Test-CommandExists "python")) {
        Write-Error "Python 3 is required for development setup"
        Write-Status "Download from: https://www.python.org/downloads/"
        exit 1
    }
    
    if (-not (Test-CommandExists "node")) {
        Write-Error "Node.js is required for development setup"
        Write-Status "Download from: https://nodejs.org/"
        exit 1
    }
    
    # Setup backend
    Write-Status "Setting up backend..."
    Set-Location "backend"
    
    if (-not (Test-Path "venv")) {
        Write-Status "Creating Python virtual environment..."
        python -m venv venv
    }
    
    Write-Status "Activating virtual environment and installing dependencies..."
    & "venv\Scripts\Activate.ps1"
    pip install -r requirements.txt
    
    # Create SQLite database for development
    Write-Status "Initializing database..."
    python -c @"
from app.core.database import engine, Base
from app.models.game import *
from app.models.configuration import *
Base.metadata.create_all(bind=engine)
print('Database initialized!')
"@
    
    Set-Location ".."
    
    # Setup frontend
    Write-Status "Setting up frontend..."
    Set-Location "frontend"
    
    if (-not (Test-Path "node_modules")) {
        Write-Status "Installing Node.js dependencies..."
        npm install
    }
    
    Set-Location ".."
    
    Write-Success "Development environment setup completed!"
    Write-Host ""
    Write-Status "To start development servers:"
    Write-Host "  Backend:  cd backend && venv\Scripts\Activate.ps1 && python -m uvicorn main:app --reload" -ForegroundColor $Colors.White
    Write-Host "  Frontend: cd frontend && npm run dev" -ForegroundColor $Colors.White
}

function Show-Usage {
    Write-Host "Monopoly Deal Analyzer - Windows PowerShell Deployment Script" -ForegroundColor $Colors.Blue
    Write-Host ""
    Write-Host "Usage: .\deploy.ps1 [OPTION]" -ForegroundColor $Colors.White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor $Colors.White
    Write-Host "  docker      Deploy using Docker Compose (recommended)" -ForegroundColor $Colors.White
    Write-Host "  dev         Setup development environment" -ForegroundColor $Colors.White
    Write-Host "  check       Check prerequisites only" -ForegroundColor $Colors.White
    Write-Host "  help        Show this help message" -ForegroundColor $Colors.White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor $Colors.White
    Write-Host "  .\deploy.ps1 docker   # Deploy with Docker" -ForegroundColor $Colors.White
    Write-Host "  .\deploy.ps1 dev      # Setup for development" -ForegroundColor $Colors.White
    Write-Host "  .\deploy.ps1 check    # Check if Docker is installed" -ForegroundColor $Colors.White
}

# Main deployment logic
function Main {
    Write-Host "🎯 Monopoly Deal Analyzer - Windows Deployment Script" -ForegroundColor $Colors.Blue
    Write-Host "======================================================" -ForegroundColor $Colors.Blue
    Write-Host ""
    
    switch ($Action) {
        "docker" {
            Test-Prerequisites
            Initialize-Environment
            Deploy-Docker
        }
        { $_ -in @("dev", "development") } {
            Initialize-Environment
            Deploy-Development
        }
        "check" {
            Test-Prerequisites
        }
        "help" {
            Show-Usage
        }
        default {
            Write-Error "Unknown option: $Action"
            Write-Host ""
            Show-Usage
            exit 1
        }
    }
}

# Run main function
Main