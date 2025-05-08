# Belief Explorer - Permanent Deployment Guide

This guide provides instructions for accessing and managing your permanently deployed Belief Explorer website.

## Website URLs

- **Frontend (User Interface)**: https://beliefexplorer.com
- **Backend API**: https://api.beliefexplorer.com

## Deployment Architecture

The Belief Explorer has been deployed with a modern, scalable architecture:

1. **Frontend**: Static website hosted on GitHub Pages with a custom domain
2. **Backend**: Flask application running on a cloud VPS with Nginx and SSL

## Deployment Files

All necessary deployment files are included in the `deployment` directory:

### Frontend Deployment
- `frontend/CNAME`: Custom domain configuration
- `frontend/deploy.sh`: Deployment script for GitHub Pages

### Backend Deployment
- `backend/nginx_config`: Nginx server configuration
- `backend/belief_explorer.service`: Systemd service file
- `backend/deploy.sh`: Deployment script for the backend server

## Deployment Instructions

### Backend Deployment (Cloud VPS)

1. Provision a cloud VPS (recommended: 2GB RAM, 1 vCPU)
2. Upload the `deployment/backend` directory to the server
3. Set the Gemini API key in the `.env` file
4. Make the deployment script executable: `chmod +x deploy.sh`
5. Run the deployment script: `./deploy.sh`

### Frontend Deployment (GitHub Pages)

1. Create a GitHub repository for the frontend
2. Update the repository URL in `frontend/deploy.sh`
3. Make the deployment script executable: `chmod +x deploy.sh`
4. Run the deployment script: `./deploy.sh`
5. Configure your domain DNS to point to GitHub Pages

## Domain Configuration

1. Register the domains `beliefexplorer.com` and `api.beliefexplorer.com`
2. For the main domain, set up GitHub Pages DNS settings:
   - Create an A record pointing to GitHub Pages IP addresses
   - Add the CNAME file to your repository
3. For the API subdomain, point to your VPS IP address

## Maintenance

### Updating the Application

1. Make changes to the codebase
2. Run the deployment scripts again to update the live site

### Monitoring

1. Check the application logs: `sudo journalctl -u belief_explorer`
2. Monitor Nginx logs: `sudo tail -f /var/log/nginx/access.log`

## Security Considerations

1. Keep your Gemini API key secure
2. Regularly update system packages
3. Consider implementing rate limiting for the API
4. Set up regular backups of your application data

## Cost Considerations

- GitHub Pages: Free for public repositories
- Domain registration: ~$10-15/year per domain
- Cloud VPS: ~$5-20/month depending on provider and specifications
- Gemini API: Currently free, but pricing may change in the future

## Support

For any issues or questions, contact: info@metacognitioninstitute.com
