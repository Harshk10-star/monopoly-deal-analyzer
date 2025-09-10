# Monopoly Deal Analyzer - Deployment Guide

This guide covers multiple deployment options for the Monopoly Deal Analyzer application.

## 🚀 Quick Deployment Options

### Option 1: Local Development (Recommended for Testing)
### Option 2: Docker Deployment (Recommended for Production)
### Option 3: Cloud Deployment (Vercel + Railway)
### Option 4: VPS Deployment (DigitalOcean/AWS)

---

## 🏠 Option 1: Local Development Deployment

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (or SQLite for development)

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

2. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env
```

Edit `.env`:
```env
# Database (SQLite for development)
DATABASE_URL=sqlite:///./monopoly_deal.db

# Security
SECRET_KEY=your-development-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_HOSTS=["http://localhost:3000","http://localhost:5173"]

# Optional: Stripe (for payment testing)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
```

3. **Initialize Database**
```bash
# Create tables and add sample data
python -c "
from app.core.database import engine, Base
from app.models.game import *
from app.models.configuration import *
Base.metadata.create_all(bind=engine)
print('Database initialized!')
"
```

4. **Start Backend**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment**
Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
```

3. **Start Frontend**
```bash
npm run dev
```

**Access**: Frontend at `http://localhost:3000`, Backend at `http://localhost:8000`

---

## 🐳 Option 2: Docker Deployment (Recommended)

### Create Docker Files

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: monopoly_deal
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/monopoly_deal
      SECRET_KEY: your-production-secret-key
      ALLOWED_HOSTS: '["http://localhost:3000","https://yourdomain.com"]'
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

**Deploy with Docker**:
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## ☁️ Option 3: Cloud Deployment (Vercel + Railway)

### Backend on Railway

1. **Create Railway Account** at [railway.app](https://railway.app)

2. **Deploy Backend**:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add postgresql
railway deploy
```

3. **Configure Environment Variables** in Railway dashboard:
```env
DATABASE_URL=postgresql://user:pass@host:port/db  # Auto-provided by Railway
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=["https://your-frontend-domain.vercel.app"]
STRIPE_SECRET_KEY=sk_live_your_stripe_key
```

### Frontend on Vercel

1. **Create Vercel Account** at [vercel.com](https://vercel.com)

2. **Deploy Frontend**:
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Set environment variables
vercel env add VITE_API_URL
# Enter your Railway backend URL: https://your-app.railway.app
```

3. **Configure Build Settings** in Vercel dashboard:
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

---

## 🖥️ Option 4: VPS Deployment (DigitalOcean/AWS)

### Server Setup

1. **Create VPS** (Ubuntu 22.04 recommended)

2. **Initial Server Setup**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx postgresql postgresql-contrib

# Install PM2 for process management
sudo npm install -g pm2

# Create application user
sudo adduser monopoly
sudo usermod -aG sudo monopoly
```

### Backend Deployment

1. **Setup Application**:
```bash
# Switch to app user
sudo su - monopoly

# Clone repository
git clone https://github.com/yourusername/monopoly-deal-analyzer.git
cd monopoly-deal-analyzer/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Database**:
```bash
# Setup PostgreSQL
sudo -u postgres createuser --interactive monopoly
sudo -u postgres createdb monopoly_deal -O monopoly

# Set password
sudo -u postgres psql -c "ALTER USER monopoly PASSWORD 'your_password';"
```

3. **Configure Environment**:
```bash
# Create production environment file
cat > .env << EOF
DATABASE_URL=postgresql://monopoly:your_password@localhost/monopoly_deal
SECRET_KEY=your-super-secure-production-key
ALLOWED_HOSTS=["https://yourdomain.com"]
STRIPE_SECRET_KEY=sk_live_your_stripe_key
EOF
```

4. **Start Backend with PM2**:
```bash
# Create PM2 ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'monopoly-backend',
    script: 'venv/bin/uvicorn',
    args: 'main:app --host 0.0.0.0 --port 8000',
    cwd: '/home/monopoly/monopoly-deal-analyzer/backend',
    env: {
      NODE_ENV: 'production'
    }
  }]
}
EOF

# Start application
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Frontend Deployment

1. **Build Frontend**:
```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
VITE_API_URL=https://yourdomain.com/api npm run build
```

2. **Configure Nginx**:
```bash
sudo nano /etc/nginx/sites-available/monopoly-deal
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /home/monopoly/monopoly-deal-analyzer/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        root /home/monopoly/monopoly-deal-analyzer/backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

3. **Enable Site and SSL**:
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/monopoly-deal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🔧 Production Configuration

### Environment Variables

**Backend (.env)**:
```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Security
SECRET_KEY=your-super-secure-production-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_HOSTS=["https://yourdomain.com","https://www.yourdomain.com"]

# Stripe
STRIPE_SECRET_KEY=sk_live_your_actual_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_actual_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Optional: Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
```

**Frontend (.env.production)**:
```env
VITE_API_URL=https://yourdomain.com/api
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_your_actual_stripe_key
VITE_ENVIRONMENT=production
```

### Security Checklist

- [ ] Use HTTPS in production
- [ ] Set secure SECRET_KEY (32+ characters)
- [ ] Configure CORS properly
- [ ] Use production Stripe keys
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Use environment variables for secrets
- [ ] Enable firewall on VPS
- [ ] Regular security updates

---

## 📊 Monitoring & Maintenance

### Health Checks

**Backend Health Check**:
```bash
curl https://yourdomain.com/api/health
```

**Frontend Health Check**:
```bash
curl https://yourdomain.com/
```

### Logs

**Docker Logs**:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**PM2 Logs**:
```bash
pm2 logs monopoly-backend
```

### Database Backup

```bash
# Backup
pg_dump monopoly_deal > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql monopoly_deal < backup_file.sql
```

---

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check ALLOWED_HOSTS in backend .env
   - Verify frontend API URL

2. **Database Connection**
   - Check DATABASE_URL format
   - Verify database is running
   - Check firewall settings

3. **Build Failures**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify environment variables

4. **SSL Certificate Issues**
   - Renew with `sudo certbot renew`
   - Check domain DNS settings

### Getting Help

- Check application logs
- Verify environment variables
- Test API endpoints individually
- Check network connectivity
- Review security group settings (cloud)

---

## 📈 Scaling Considerations

### Performance Optimization

1. **Database**
   - Add database indexes
   - Use connection pooling
   - Consider read replicas

2. **Backend**
   - Use Redis for caching
   - Implement rate limiting
   - Add load balancer

3. **Frontend**
   - Enable CDN
   - Optimize bundle size
   - Use service workers

### Monitoring

- Set up application monitoring (Sentry)
- Database performance monitoring
- Server resource monitoring
- User analytics

This deployment guide should get you up and running in any environment. Choose the option that best fits your needs and technical expertise!