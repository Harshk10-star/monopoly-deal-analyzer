#!/bin/bash
set -e

echo "Installing frontend dependencies..."
cd frontend
npm install

echo "Building frontend..."
npm run build

echo "Setting up backend..."
cd ../backend
mkdir -p static
cp -r ../frontend/dist/* static/

echo "Build complete!"