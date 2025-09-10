# 🚀 Quick Start Guide - Monopoly Deal Analyzer

Get up and running in 5 minutes with Docker, or 10 minutes with manual setup!

## 🐳 Option 1: Docker Deployment (Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed

### Steps

1. **Clone and Setup**
```bash
git clone <your-repo-url>
cd monopoly-deal-analyzer
```

2. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (optional for testing)
# At minimum, set a secure POSTGRES_PASSWORD and SECRET_KEY
```

3. **Deploy with Docker**

**On Windows:**
```powershell
.\deploy.ps1 docker
```

**On macOS/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh docker
```

4. **Access the Application**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000  
- 📚 **API Docs**: http://localhost:8000/docs

### Docker Management Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up --build -d
```

---

## 💻 Option 2: Manual Development Setup

### Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed
- PostgreSQL (optional - SQLite used by default)

### Backend Setup

1. **Setup Python Environment**
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
# Copy and edit environment file
cp .env.example .env
# Edit DATABASE_URL to use SQLite: sqlite:///./monopoly_deal.db
```

3. **Initialize Database**
```bash
python -c "
from app.core.database import engine, Base
from app.models.game import *
from app.models.configuration import *
Base.metadata.create_all(bind=engine)
print('Database initialized!')
"
```

4. **Start Backend Server**
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
```bash
# Create frontend environment file
echo "VITE_API_URL=http://localhost:8000" > .env
```

3. **Start Frontend Server**
```bash
npm run dev
```

### Access the Application
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000

---

## 🧪 Testing the Application

### 1. Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Test configuration system
curl http://localhost:8000/api/v1/configuration/test

# View API documentation
open http://localhost:8000/docs
```

### 2. Test Frontend
1. Open http://localhost:3000
2. Navigate to the Dashboard
3. Go to the "Rules" tab to see the configuration system
4. Try different rule presets
5. Test the AI analysis with different configurations

### 3. Test Configuration System
```bash
cd backend
python test_configuration_system.py
python test_full_configuration_demo.py
```

---

## 🎯 Key Features to Test

### Configuration System
- ✅ **Rule Presets**: Try "Strict Official" vs "Flexible House Rules"
- ✅ **Edge Cases**: Configure how house/hotel payments work
- ✅ **Validation**: See warnings for conflicting rules
- ✅ **Import/Export**: Save and share configurations

### AI Analysis  
- ✅ **Game Analysis**: Set up a game state and get AI recommendations
- ✅ **Different Strategies**: Try Aggressive, Defensive, Normal AI
- ✅ **Win Probabilities**: See calculated win chances
- ✅ **Rule-Aware**: AI respects your edge case configurations

### Game Interface
- ✅ **Card Management**: Add cards to hand, properties, money
- ✅ **Opponent Setup**: Configure opponent hands and properties  
- ✅ **Deck Management**: Draw cards from the complete deck
- ✅ **Real-time Updates**: See changes reflected immediately

---

## 🔧 Troubleshooting

### Common Issues

**Docker Issues:**
```bash
# If ports are in use
docker-compose down
docker system prune -f

# If build fails
docker-compose build --no-cache
```

**Backend Issues:**
```bash
# Database connection error
# Check DATABASE_URL in .env file

# Module import error  
# Ensure virtual environment is activated
# pip install -r requirements.txt
```

**Frontend Issues:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check API connection
# Verify VITE_API_URL in .env matches backend URL
```

### Getting Help

1. **Check Logs**
   - Docker: `docker-compose logs -f`
   - Backend: Check terminal output
   - Frontend: Check browser console

2. **Verify Configuration**
   - Check .env files exist and have correct values
   - Ensure ports aren't conflicting

3. **Test Components Individually**
   - Backend health: `curl http://localhost:8000/health`
   - Frontend: Check if page loads at `http://localhost:3000`

---

## 🎉 What's Next?

Once you have the application running:

1. **Explore Configuration Options**
   - Try different rule presets
   - Create custom configurations
   - Test edge case scenarios

2. **Test AI Analysis**
   - Set up different game scenarios
   - Compare AI recommendations with different rules
   - Analyze win probabilities

3. **Customize for Your Needs**
   - Add new rule options
   - Modify AI strategies
   - Extend the game interface

4. **Deploy to Production**
   - See `DEPLOYMENT_GUIDE.md` for cloud deployment options
   - Configure SSL and domain
   - Set up monitoring

---

## 📚 Additional Resources

- **Full Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **Configuration Guide**: `CONFIGURATION_GUIDE.md`
- **API Documentation**: http://localhost:8000/docs (when running)
- **Project Setup**: `SETUP.md`

Happy gaming! 🎲