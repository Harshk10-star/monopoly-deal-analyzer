# 🌐 Deploy to Internet - Complete Guide

Get your Monopoly Deal Analyzer live on the internet in 15 minutes!

## 🎯 Recommended: Vercel + Railway (Free Tier Available)

This is the easiest and most cost-effective way to deploy your app.

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Step 1: Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit with configuration system"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/monopoly-deal-analyzer.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Railway

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Login with GitHub"
   - Authorize Railway to access your repositories

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `monopoly-deal-analyzer` repository
   - Select the `backend` folder as the root directory

3. **Add Database**
   - In your Railway project dashboard
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically create a database and provide connection details

4. **Configure Environment Variables**
   - Click on your backend service
   - Go to "Variables" tab
   - Add these variables:

   ```env
   SECRET_KEY=your-super-secure-32-character-secret-key-change-this
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALLOWED_HOSTS=["https://your-app-name.vercel.app"]
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   ```

   **Note**: Railway automatically provides `DATABASE_URL` from the PostgreSQL service.

5. **Deploy**
   - Railway will automatically build and deploy your backend
   - You'll get a URL like: `https://monopoly-deal-analyzer-production.up.railway.app`
   - Copy this URL for the frontend configuration

### Step 3: Deploy Frontend to Vercel

1. **Sign up for Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Continue with GitHub"
   - Authorize Vercel to access your repositories

2. **Import Project**
   - Click "New Project"
   - Import your `monopoly-deal-analyzer` repository
   - Set these build settings:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Configure Environment Variables**
   - In project settings, go to "Environment Variables"
   - Add these variables:

   ```env
   VITE_API_URL=https://your-railway-backend-url.up.railway.app
   VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   VITE_ENVIRONMENT=production
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - You'll get a URL like: `https://monopoly-deal-analyzer.vercel.app`

### Step 4: Update CORS Settings

1. **Update Backend CORS**
   - Go back to Railway dashboard
   - Update the `ALLOWED_HOSTS` variable with your Vercel URL:
   ```env
   ALLOWED_HOSTS=["https://monopoly-deal-analyzer.vercel.app"]
   ```

2. **Redeploy Backend**
   - Railway will automatically redeploy with the new settings

### Step 5: Test Your Deployment

1. **Visit Your App**
   - Go to your Vercel URL: `https://monopoly-deal-analyzer.vercel.app`
   - The app should load successfully

2. **Test Configuration System**
   - Navigate to Dashboard → Rules tab
   - Try different configuration presets
   - Test the validation system

3. **Test AI Analysis**
   - Set up a game state
   - Try the AI analysis with different configurations
   - Verify recommendations are working

---

## 🔧 Alternative: DigitalOcean App Platform

### One-Click Deploy Button

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/yourusername/monopoly-deal-analyzer/tree/main)

### Manual Setup

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Sign up (get $200 credit with GitHub Student Pack)

2. **Create App**
   - Go to Apps → Create App
   - Connect your GitHub repository
   - DigitalOcean will detect the `.do/app.yaml` configuration

3. **Configure Environment Variables**
   - Set the required environment variables in the DigitalOcean dashboard
   - Use the same variables as listed above

4. **Deploy**
   - DigitalOcean will build and deploy both frontend and backend
   - You'll get URLs for both services

---

## 💰 Cost Breakdown

### Free Tier (Recommended for Testing)
- **Vercel**: Free (100GB bandwidth/month)
- **Railway**: $5/month credit (covers small apps)
- **Total**: ~$5/month

### Production Scale
- **Vercel Pro**: $20/month (unlimited bandwidth)
- **Railway**: Pay per usage (~$10-50/month depending on traffic)
- **DigitalOcean**: $12/month (includes database)

---

## 🔒 Production Security Checklist

### Before Going Live

1. **Update Environment Variables**
   ```env
   # Use production Stripe keys
   STRIPE_SECRET_KEY=sk_live_your_production_key
   STRIPE_PUBLISHABLE_KEY=pk_live_your_production_key
   
   # Generate secure secret key (32+ characters)
   SECRET_KEY=your-super-secure-production-secret-key-32-chars-min
   
   # Set correct domain
   ALLOWED_HOSTS=["https://yourdomain.com","https://www.yourdomain.com"]
   ```

2. **Custom Domain (Optional)**
   - **Vercel**: Add custom domain in project settings (free SSL)
   - **Railway**: Add custom domain (requires paid plan)

3. **Database Backups**
   - Railway: Automatic backups included
   - DigitalOcean: Configure backup schedule

---

## 📊 Monitoring & Maintenance

### Built-in Monitoring
- **Vercel**: Analytics, performance metrics, error tracking
- **Railway**: Resource usage, logs, uptime monitoring
- **DigitalOcean**: App metrics, alerts, logs

### Additional Monitoring (Optional)
- **Sentry**: Error tracking and performance monitoring
- **LogRocket**: User session recording
- **Google Analytics**: User behavior tracking

---

## 🚀 Going Live Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Railway with database
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] SSL certificates active (automatic)
- [ ] Custom domain configured (optional)
- [ ] Stripe webhooks configured (if using payments)
- [ ] Error monitoring set up
- [ ] Database backups enabled

---

## 🆘 Troubleshooting

### Common Issues

**CORS Errors**
```bash
# Check ALLOWED_HOSTS includes your frontend domain
ALLOWED_HOSTS=["https://your-app.vercel.app"]
```

**Database Connection Issues**
```bash
# Verify DATABASE_URL is set automatically by Railway
# Check database service is running in Railway dashboard
```

**Build Failures**
```bash
# Check build logs in Vercel/Railway dashboard
# Verify all dependencies are in package.json/requirements.txt
```

**Environment Variables Not Working**
```bash
# Redeploy after adding environment variables
# Check variable names match exactly (case-sensitive)
```

### Getting Help

1. **Check Deployment Logs**
   - Vercel: Project → Functions → View logs
   - Railway: Service → Deployments → View logs

2. **Test API Endpoints**
   ```bash
   # Test backend health
   curl https://your-backend.railway.app/health
   
   # Test configuration endpoint
   curl https://your-backend.railway.app/api/v1/configuration/test
   ```

3. **Community Support**
   - Vercel Discord: [vercel.com/discord](https://vercel.com/discord)
   - Railway Discord: [discord.gg/railway](https://discord.gg/railway)

---

## 🎉 Success!

Once deployed, your Monopoly Deal Analyzer will be live on the internet with:

✅ **Full Configuration System**: 10 edge case rules with 4 presets
✅ **AI Analysis**: Rule-aware game recommendations  
✅ **Production Ready**: SSL, CDN, automatic scaling
✅ **Global Access**: Available worldwide with fast loading
✅ **Automatic Deployments**: Updates deploy automatically from GitHub

Your app is now ready for users around the world to configure their Monopoly Deal edge cases and get AI-powered game analysis! 🎲🌐