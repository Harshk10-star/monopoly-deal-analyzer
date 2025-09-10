from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Monopoly Deal Analyzer"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/monopoly_deal"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Stripe
    STRIPE_SECRET_KEY: str = "sk_test_..."
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_..."
    STRIPE_WEBHOOK_SECRET: str = "whsec_..."
    
    # Business Logic
    FREE_ANALYSES_PER_DAY: int = 1
    PAY_PER_GAME_PRICE: int = 100  # $1.00 in cents
    MONTHLY_SUBSCRIPTION_PRICE: int = 1500  # $15.00 in cents
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

