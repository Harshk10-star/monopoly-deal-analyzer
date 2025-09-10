"""
Simplified FastAPI app for stateless deployment (no database required)
Perfect for demo/trial usage where users just test configurations and AI analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

# Import your existing models and engines
from app.models.game import EdgeRules, GameState, AnalysisRequest, AnalysisResponse
from app.core.game_engine import MonopolyDealEngine
from app.core.validation import RuleValidationEngine, ValidationResult
from app.models.configuration import OFFICIAL_PRESETS, ConfigurationPreset

# Create FastAPI app
app = FastAPI(
    title="Monopoly Deal Analyzer API",
    description="AI-powered game analysis with configurable edge case rules",
    version="1.0.0"
)

# Configure CORS for web deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173", 
        "https://*.vercel.app",
        "https://*.netlify.app",
        "https://*.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines (no database needed)
validation_engine = RuleValidationEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Monopoly Deal Analyzer API",
        "version": "1.0.0",
        "features": [
            "Edge case rule configuration",
            "AI-powered game analysis", 
            "Rule validation system",
            "No database required - stateless demo"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "not_required"}

# Configuration endpoints (no database - use in-memory presets)
@app.get("/api/v1/configuration/presets", response_model=List[ConfigurationPreset])
async def get_configuration_presets():
    """Get all available configuration presets (from memory)"""
    return list(OFFICIAL_PRESETS.values())

@app.get("/api/v1/configuration/presets/{preset_id}", response_model=ConfigurationPreset)
async def get_configuration_preset(preset_id: str):
    """Get a specific configuration preset by ID"""
    if preset_id not in OFFICIAL_PRESETS:
        raise HTTPException(status_code=404, detail="Configuration preset not found")
    return OFFICIAL_PRESETS[preset_id]

@app.post("/api/v1/configuration/validate", response_model=ValidationResult)
async def validate_configuration(rules: EdgeRules):
    """Validate a configuration for consistency and performance"""
    return validation_engine.validate_rules(rules)

@app.get("/api/v1/configuration/rule-descriptions")
async def get_rule_descriptions():
    """Get descriptions for all configuration rules"""
    sample_rules = EdgeRules()
    return {
        "descriptions": sample_rules.get_rule_descriptions(),
        "options": sample_rules.get_rule_options()
    }

@app.get("/api/v1/configuration/test")
async def test_configuration_system():
    """Test endpoint to verify configuration system is working"""
    return {
        "status": "Configuration system is working!",
        "official_presets": list(OFFICIAL_PRESETS.keys()),
        "validation_available": True,
        "database_required": False,
        "deployment_type": "stateless_demo",
        "features": [
            "Edge case rule configuration",
            "Official presets",
            "Rule validation", 
            "Performance impact analysis",
            "AI analysis integration"
        ]
    }

# Game analysis endpoints (stateless - no user data stored)
@app.post("/api/v1/analysis/analyze", response_model=AnalysisResponse)
async def analyze_game(request: AnalysisRequest):
    """Analyze a game state and provide move recommendations (stateless)"""
    try:
        # Create game engine with edge rules from request
        game_engine = MonopolyDealEngine(request.gameState.edgeRules)
        
        # Perform analysis
        analysis_result = game_engine.analyze_game_state(
            request.gameState,
            request.strategy
        )
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/api/v1/analysis/analyze-test", response_model=AnalysisResponse)
async def analyze_game_test(request: AnalysisRequest):
    """Test endpoint for game analysis without authentication"""
    return await analyze_game(request)

# Export configuration endpoint (stateless)
@app.get("/api/v1/configuration/export/{preset_id}")
async def export_configuration(preset_id: str):
    """Export a configuration preset to JSON format"""
    if preset_id not in OFFICIAL_PRESETS:
        raise HTTPException(status_code=404, detail="Configuration preset not found")
    
    preset = OFFICIAL_PRESETS[preset_id]
    return {
        "name": preset.name,
        "description": preset.description,
        "rules": preset.rules.dict(),
        "exported_at": "2024-01-01T00:00:00Z",
        "version": "1.0",
        "deployment_type": "stateless_demo"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)