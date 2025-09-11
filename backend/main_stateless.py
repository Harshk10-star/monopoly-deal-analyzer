"""
Stateless FastAPI app - no database dependencies
Perfect for Railway deployment with in-memory configuration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
from pathlib import Path

# Create the API app
app = FastAPI(
    title="Deal Analyzer Pro API",
    description="Stateless property card game analyzer",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for configurations
configurations = {}

# Pydantic models (database-free versions)
class EdgeRules(BaseModel):
    allow_empty_property_sets: bool = True
    allow_partial_set_rent: bool = True
    force_payment_order: bool = False
    allow_overpayment: bool = True
    strict_action_card_limits: bool = False

class GameState(BaseModel):
    player_hand: List[str] = []
    player_properties: Dict[str, List[str]] = {}
    player_money: List[str] = []
    opponents: List[Dict[str, Any]] = []
    deck_remaining: int = 106
    turn_number: int = 1

class AnalysisRequest(BaseModel):
    game_state: GameState
    edge_rules: Optional[EdgeRules] = None
    configuration_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    recommended_action: str
    reasoning: str
    win_probability: float
    alternative_actions: List[Dict[str, Any]]
    risk_assessment: str

class Configuration(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    edge_rules: EdgeRules
    is_active: bool = True

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Deal Analyzer Pro API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_game_state(request: AnalysisRequest):
    """Analyze game state and provide AI recommendations"""
    
    # Get configuration
    config = None
    if request.configuration_id and request.configuration_id in configurations:
        config = configurations[request.configuration_id]
    
    # Use provided edge rules or default
    edge_rules = request.edge_rules or EdgeRules()
    if config:
        edge_rules = config.edge_rules
    
    # Simple AI analysis logic
    game_state = request.game_state
    
    # Basic analysis
    hand_size = len(game_state.player_hand)
    property_sets = len(game_state.player_properties)
    money_count = len(game_state.player_money)
    
    # Determine recommended action
    if hand_size > 7:
        action = "Play action cards or discard excess cards"
        reasoning = "Hand size exceeds limit, must reduce to 7 cards"
        win_prob = 0.4
    elif property_sets < 2:
        action = "Focus on building property sets"
        reasoning = "Need more complete property sets to win"
        win_prob = 0.3
    elif money_count < 3:
        action = "Collect more money cards for rent payments"
        reasoning = "Low money reserves make you vulnerable to rent"
        win_prob = 0.5
    else:
        action = "Play rent cards to collect from opponents"
        reasoning = "Good position to pressure opponents with rent"
        win_prob = 0.7
    
    # Risk assessment
    if money_count < 2:
        risk = "HIGH - Vulnerable to rent attacks"
    elif property_sets >= 2:
        risk = "LOW - Strong defensive position"
    else:
        risk = "MEDIUM - Balanced position"
    
    return AnalysisResponse(
        recommended_action=action,
        reasoning=reasoning,
        win_probability=win_prob,
        alternative_actions=[
            {"action": "Draw cards", "priority": "medium"},
            {"action": "Trade properties", "priority": "low"}
        ],
        risk_assessment=risk
    )

@app.get("/configurations")
async def get_configurations():
    """Get all configurations"""
    return {"configurations": list(configurations.values())}

@app.post("/configurations")
async def create_configuration(config: Configuration):
    """Create a new configuration"""
    import uuid
    config_id = str(uuid.uuid4())
    config.id = config_id
    configurations[config_id] = config
    return {"message": "Configuration created", "id": config_id}

@app.get("/configurations/{config_id}")
async def get_configuration(config_id: str):
    """Get a specific configuration"""
    if config_id not in configurations:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return configurations[config_id]

@app.put("/configurations/{config_id}")
async def update_configuration(config_id: str, config: Configuration):
    """Update a configuration"""
    if config_id not in configurations:
        raise HTTPException(status_code=404, detail="Configuration not found")
    config.id = config_id
    configurations[config_id] = config
    return {"message": "Configuration updated"}

@app.delete("/configurations/{config_id}")
async def delete_configuration(config_id: str):
    """Delete a configuration"""
    if config_id not in configurations:
        raise HTTPException(status_code=404, detail="Configuration not found")
    del configurations[config_id]
    return {"message": "Configuration deleted"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)