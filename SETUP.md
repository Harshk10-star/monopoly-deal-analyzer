# Monopoly Deal Analyzer - Setup Guide

This guide will help you set up and run the full-stack Monopoly Deal Analyzer application.

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ and npm installed
- PostgreSQL database running
- Stripe account (for payments)

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the environment template and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your actual values:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/monopoly_deal

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_HOSTS=["http://localhost:3000","http://localhost:5173"]

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_actual_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb monopoly_deal

# Run database setup script
python setup_db.py
```

### 4. Test the Backend

```bash
# Test the game engine
python test_game_engine.py

# Start the server
python start.py
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Node.js Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Testing the Application

### 1. Backend API Testing

Visit `http://localhost:8000/docs` to see the interactive API documentation.

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

### 2. Frontend Testing

1. Open `http://localhost:3000` in your browser
2. Register a new account
3. Try the free analysis
4. Test the game analysis features

## Project Structure

```
monopoly-deal-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API endpoints
│   │   ├── core/                 # Core functionality
│   │   └── models/               # Data models
│   ├── main.py                   # FastAPI app entry point
│   ├── requirements.txt          # Python dependencies
│   └── start.py                  # Development server script
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── contexts/             # React contexts
│   │   ├── pages/                # Page components
│   │   └── services/             # API services
│   ├── package.json              # Node.js dependencies
│   └── tailwind.config.js        # Tailwind CSS config
└── README.md                     # Project overview
```

## Key Features

### Backend
- **Game Analysis Engine**: AI-powered move recommendations
- **Multiple Strategies**: Aggressive, Defensive, Normal AI personalities
- **Rule Customization**: Configurable edge case rules
- **Authentication**: JWT-based user authentication
- **Payment Integration**: Stripe integration for credits/subscriptions
- **Database**: PostgreSQL with SQLAlchemy ORM

### Frontend
- **Modern UI**: React 18 with TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **Charts**: Recharts for data visualization
- **State Management**: React Query for API state
- **Routing**: React Router for navigation

## Business Model

- **Free Tier**: 1 analysis per day
- **Pay-per-Game**: $1 per analysis
- **Monthly Subscription**: $15/month for unlimited analyses

## Development Workflow

1. **Backend Changes**: The server auto-reloads with `python start.py`
2. **Frontend Changes**: Vite provides hot module replacement
3. **Database Changes**: Use Alembic for migrations (future enhancement)
4. **Testing**: Add tests in `backend/tests/` directory

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Verify database exists

2. **Port Already in Use**
   - Change ports in .env file
   - Kill existing processes using the ports

3. **Module Import Errors**
   - Ensure virtual environment is activated
   - Check Python path and imports

4. **Frontend Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility

### Getting Help

- Check the API documentation at `/docs`
- Review the console logs for error details
- Ensure all environment variables are set correctly

## Next Steps

1. **Add Tests**: Create comprehensive test suite
2. **Deploy**: Set up production deployment
3. **Monitoring**: Add logging and monitoring
4. **CI/CD**: Set up automated testing and deployment
5. **Analytics**: Track user behavior and game patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details



