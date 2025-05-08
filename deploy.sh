#!/bin/bash

# Deployment script for Belief Explorer backend
# This script sets up the backend on a cloud VPS

# Exit on error
set -e

echo "Starting Belief Explorer backend deployment..."

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
echo "Installing dependencies..."
sudo apt-get install -y python3-pip python3-dev nginx

# Install Python packages
echo "Installing Python packages..."
pip3 install -r requirements.txt
pip3 install gunicorn

# Set up Nginx
echo "Setting up Nginx..."
sudo cp nginx_config /etc/nginx/sites-available/belief_explorer
sudo ln -sf /etc/nginx/sites-available/belief_explorer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up systemd service
echo "Setting up systemd service..."
sudo cp belief_explorer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable belief_explorer
sudo systemctl start belief_explorer

# Set up SSL with Let's Encrypt
echo "Setting up SSL with Let's Encrypt..."
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.beliefexplorer.com --non-interactive --agree-tos --email info@metacognitioninstitute.com

echo "Deployment completed successfully!"
echo "The Belief Explorer backend is now running at https://api.beliefexplorer.com"
