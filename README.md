# Monopoly Deal Analyzer

A full-stack SaaS application that provides AI-powered analysis and move recommendations for Monopoly Deal card games.

## Features

- **Game Analysis**: Analyze any game state and get AI-powered move recommendations
- **Card Selection & Transfer**: Interactive card management for hands, properties, and money
- **Multiple AI Strategies**: Aggressive, Defensive, and Normal AI personalities
- **Advanced Rule Customization**: Comprehensive edge case configuration for different house rules
- **Win Probability**: Calculate win probabilities for all players
- **Game Simulation**: Run multiple simulations to test strategies
- **Subscription Model**: Pay-per-game or monthly subscription options

## Tech Stack

### Backend
- **Python 3.9+** with FastAPI
- **PostgreSQL** for user data and game history
- **Stripe** for payment processing
- **JWT** for authentication
- **Pydantic** for data validation

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Recharts** for data visualization
- **React Query** for API state management

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /analyze` - Analyze game state and get recommendations
- `POST /simulate` - Run game simulations
- `POST /card-operation` - Perform card transfers and selections
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /payments/create-checkout` - Create Stripe checkout session

## Game Rules

The analyzer supports the standard Monopoly Deal rules with comprehensive configurable edge cases:

### Core Rules
- House/Hotel payment methods
- Property movement rules
- Deck exhaustion handling
- Extra property handling
- Double rent stacking
- Just Say No on zero payment

### Advanced Edge Cases
- **House/Hotel as Payment**: Configure where buildings go (bank, incomplete set, floating)
- **Moving House/Hotel**: Set rules for relocating buildings (not allowed, free move, costs action)
- **Deck Exhaustion**: Choose between reshuffle or game over
- **Extra Properties**: Handle overflow properties (cap rent, split into sets)
- **Property Set Merging**: Allow orphaned cards to combine after wildcard reallocation
- **Building Forfeiture**: Configure when buildings are discarded
- **Quadruple Rent**: Enable/disable playing two Double Rent cards simultaneously
- **Forced Deal → Deal Breaker**: Validate this sequence
- **Just Say No Empty Hand**: Allow usage with no payment ability

### Card Operations
- **Hand Management**: Select and transfer cards from hand to properties or bank
- **Property Transfers**: Move cards between property sets
- **Opponent Interactions**: Transfer cards to/from opponents via action cards
- **Money Conversion**: Convert property cards to money values

## AI Strategies

1. **Aggressive**: Prioritizes stealing, Deal Breaker usage, and rent multipliers
2. **Defensive**: Focuses on banking, Just Say No, and avoiding exposure
3. **Normal**: Balanced approach between offensive and defensive play

## Business Model

- **Free Tier**: 1 free analysis per day
- **Pay-per-Game**: $1 per analysis
- **Monthly Subscription**: $15/month for unlimited analyses

## License

MIT License
