# 🚀 One-Click Internet Deployment

Deploy your Monopoly Deal Analyzer to the internet with one click!

## 🌐 Deploy Backend to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

**What this does:**
- Creates a PostgreSQL database
- Deploys your FastAPI backend
- Sets up automatic deployments from GitHub

**After deployment:**
1. Go to your Railway dashboard
2. Add environment variables (see below)
3. Copy your backend URL

## 🎨 Deploy Frontend to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/monopoly-deal-analyzer&project-name=monopoly-deal-analyzer&repository-name=monopoly-deal-analyzer)

**What this does:**
- Builds and deploys your React frontend
- Sets up automatic deployments from GitHub
- Provides a custom domain

**After deployment:**
1. Go to Vercel dashboard → Settings → Environment Variables
2. Add your backend URL and Stripe keys
3. Redeploy

## 🔧 Required Environment Variables

### Backend (Railway)
```env
SECRET_KEY=your-32-character-secret-key
ALLOWED_HOSTS=["https://your-vercel-app.vercel.app"]
STRIPE_SECRET_KEY=sk_live_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
```

### Frontend (Vercel)
```env
VITE_API_URL=https://your-railway-app.railway.app
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
```

## 🎉 That's It!

Your app will be live at:
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-project.railway.app`

## 🔒 Security Checklist

- [ ] Use production Stripe keys (not test keys)
- [ ] Set a secure SECRET_KEY (32+ characters)
- [ ] Update ALLOWED_HOSTS with your actual domain
- [ ] Enable HTTPS (automatic on Vercel/Railway)

## 📊 Monitoring

Both platforms provide:
- ✅ Automatic SSL certificates
- ✅ CDN and global distribution
- ✅ Automatic scaling
- ✅ Built-in monitoring and logs
- ✅ Custom domains (free on Vercel, paid on Railway)

## 💰 Costs

**Free Tier Limits:**
- **Vercel**: 100GB bandwidth, unlimited static sites
- **Railway**: $5/month credit (covers small apps)
- **Total**: ~$5/month for production app

**Scaling:**
- Both platforms scale automatically
- Pay only for what you use
- No server management required