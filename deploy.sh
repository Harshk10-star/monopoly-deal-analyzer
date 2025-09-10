#!/bin/bash

# Monopoly Deal Analyzer - Deployment Script
# This script helps deploy the application in different environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_status "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    if [ ! -f .env ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your actual configuration values!"
        print_status "Key values to update:"
        echo "  - POSTGRES_PASSWORD"
        echo "  - SECRET_KEY"
        echo "  - STRIPE_SECRET_KEY (if using payments)"
        echo "  - STRIPE_PUBLISHABLE_KEY (if using payments)"
        echo ""
        read -p "Press Enter to continue after updating .env file..."
    else
        print_success ".env file already exists"
    fi
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker Compose..."
    
    # Build and start services
    print_status "Building and starting services..."
    docker-compose up --build -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check service health
    if docker-compose ps | grep -q "Up (healthy)"; then
        print_success "Services are running and healthy!"
    else
        print_warning "Some services may not be fully ready yet. Checking status..."
        docker-compose ps
    fi
    
    # Show service URLs
    echo ""
    print_success "Deployment completed!"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    print_status "To view logs: docker-compose logs -f"
    print_status "To stop services: docker-compose down"
}

# Function to deploy for development
deploy_development() {
    print_status "Setting up development environment..."
    
    # Check if Python and Node.js are installed
    if ! command_exists python3; then
        print_error "Python 3 is required for development setup"
        exit 1
    fi
    
    if ! command_exists node; then
        print_error "Node.js is required for development setup"
        exit 1
    fi
    
    # Setup backend
    print_status "Setting up backend..."
    cd backend
    
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    print_status "Activating virtual environment and installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Create SQLite database for development
    print_status "Initializing database..."
    python -c "
from app.core.database import engine, Base
from app.models.game import *
from app.models.configuration import *
Base.metadata.create_all(bind=engine)
print('Database initialized!')
"
    
    cd ..
    
    # Setup frontend
    print_status "Setting up frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi
    
    cd ..
    
    print_success "Development environment setup completed!"
    echo ""
    print_status "To start development servers:"
    echo "  Backend:  cd backend && source venv/bin/activate && python -m uvicorn main:app --reload"
    echo "  Frontend: cd frontend && npm run dev"
}

# Function to show usage
show_usage() {
    echo "Monopoly Deal Analyzer - Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker      Deploy using Docker Compose (recommended)"
    echo "  dev         Setup development environment"
    echo "  check       Check prerequisites only"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker   # Deploy with Docker"
    echo "  $0 dev      # Setup for development"
    echo "  $0 check    # Check if Docker is installed"
}

# Main deployment logic
main() {
    echo "🎯 Monopoly Deal Analyzer - Deployment Script"
    echo "=============================================="
    echo ""
    
    case "${1:-docker}" in
        "docker")
            check_prerequisites
            setup_environment
            deploy_docker
            ;;
        "dev"|"development")
            setup_environment
            deploy_development
            ;;
        "check")
            check_prerequisites
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            print_error "Unknown option: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"