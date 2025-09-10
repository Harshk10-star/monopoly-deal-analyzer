#!/bin/bash

# Build frontend first
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Copy built frontend to backend static folder
echo "Copying frontend build..."
mkdir -p backend/static
cp -r frontend/dist/* backend/static/

# Start the backend server
echo "Starting server..."
cd backend
python main_combined.py