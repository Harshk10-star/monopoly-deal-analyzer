from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.game import (
    AnalysisRequest, AnalysisResponse, SimulationRequest, SimulationResponse,
    CardOperationRequest, CardOperationResponse, GameAnalysis, User
)
from app.core.game_engine import MonopolyDealEngine
from app.core.config import settings

router = APIRouter()
game_engine = MonopolyDealEngine()


@router.post("/analyze-test", response_model=AnalysisResponse)
async def analyze_game_test(request: AnalysisRequest):
    """Test endpoint for game analysis without authentication"""
    
    try:
        # Create game engine with edge rules from game state
        game_engine_with_rules = MonopolyDealEngine(request.gameState.edgeRules)
        
        analysis_result = game_engine_with_rules.analyze_game_state(
            request.gameState, 
            request.strategy
        )
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_game(request: AnalysisRequest):
    """Analyze a game state and provide move recommendations - FREE for all users"""
    
    # Perform game analysis (no authentication or payment required)
    try:
        print("=== DEBUGGING REQUEST ===")
        print(f"Request type: {type(request)}")
        print(f"Request dict: {request.dict()}")
        print(f"GameState: {request.gameState}")
        print(f"GameState dict: {request.gameState.dict()}")
        
        for i, player in enumerate(request.gameState.players):
            print(f"Player {i}: {player}")
            print(f"  - Hand: {player.hand} (type: {type(player.hand)})")
            print(f"  - Bank: {player.bank} (type: {type(player.bank)})")
            print(f"  - Properties: {player.properties} (type: {type(player.properties)})")
            if player.hand:
                for j, card in enumerate(player.hand):
                    print(f"    Hand card {j}: {card} (type: {type(card)})")
            if player.bank:
                for j, money in enumerate(player.bank):
                    print(f"    Bank item {j}: {money} (type: {type(money)})")
        print("=== END DEBUGGING ===")

        # Create game engine with edge rules from game state
        game_engine_with_rules = MonopolyDealEngine(request.gameState.edgeRules)
        
        analysis_result = game_engine_with_rules.analyze_game_state(
            request.gameState, 
            request.strategy
        )
        
        return analysis_result
        
    except Exception as e:
        print(f"Analysis endpoint error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/simulate", response_model=SimulationResponse)
async def simulate_games(
    request: SimulationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run multiple game simulations"""
    
    # Check access (same logic as analyze)
    if current_user.subscription_status != "active":
        today = datetime.utcnow().date()
        today_analyses = db.query(GameAnalysis).filter(
            GameAnalysis.user_id == current_user.id,
            GameAnalysis.created_at >= today
        ).count()
        
        if today_analyses >= settings.FREE_ANALYSES_PER_DAY:
            if current_user.credits <= 0:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="No credits remaining. Please purchase credits or subscribe."
                )
            else:
                current_user.credits -= 1
                db.commit()
    
    # Limit simulation count for performance
    if request.numSimulations > 100:
        request.numSimulations = 100
    
    try:
        # Run simulations
        simulation_results = game_engine.simulate_game(
            request.gameState,
            request.strategy,
            request.numSimulations
        )
        
        # Calculate averages
        total_players = len(request.gameState.players)
        player_wins = {player.name: 0 for player in request.gameState.players}
        strategy_performance = {player.name: 0.0 for player in request.gameState.players}
        
        for result in simulation_results:
            for player_name, prob in result.winProbability.items():
                player_wins[player_name] += prob
                strategy_performance[player_name] += prob
        
        # Calculate averages
        num_sims = len(simulation_results)
        average_win_probability = {
            name: round(wins / num_sims, 2) 
            for name, wins in player_wins.items()
        }
        
        strategy_performance = {
            name: round(perf / num_sims, 2) 
            for name, perf in strategy_performance.items()
        }
        
        # Store simulation in database
        db_analysis = GameAnalysis(
            user_id=current_user.id,
            game_state=request.gameState.dict(),
            analysis_result={
                "type": "simulation",
                "num_simulations": request.numSimulations,
                "strategy": request.strategy.value,
                "average_win_probability": average_win_probability,
                "strategy_performance": strategy_performance
            },
            strategy_used=f"{request.strategy.value}_simulation"
        )
        db.add(db_analysis)
        db.commit()
        
        return SimulationResponse(
            results=simulation_results,
            averageWinProbability=average_win_probability,
            strategyPerformance=strategy_performance
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}"
        )


@router.get("/history", response_model=List[dict])
async def get_analysis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's analysis history"""
    
    analyses = db.query(GameAnalysis).filter(
        GameAnalysis.user_id == current_user.id
    ).order_by(
        GameAnalysis.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": analysis.id,
            "strategy": analysis.strategy_used,
            "created_at": analysis.created_at.isoformat(),
            "game_state": analysis.game_state,
            "result": analysis.analysis_result
        }
        for analysis in analyses
    ]


@router.post("/card-operation", response_model=CardOperationResponse)
async def perform_card_operation(
    request: CardOperationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform card operations like transfer, selection, etc."""
    
    try:
        # Validate the card operation based on edge rules
        validation_errors = validate_card_operation(request.operation, request.gameState, request.edgeRules)
        
        if validation_errors:
            return CardOperationResponse(
                success=False,
                newGameState=request.gameState,
                message="Card operation validation failed",
                validationErrors=validation_errors
            )
        
        # Perform the card operation
        new_game_state = execute_card_operation(request.operation, request.gameState)
        
        return CardOperationResponse(
            success=True,
            newGameState=new_game_state,
            message="Card operation completed successfully",
            validationErrors=None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Card operation failed: {str(e)}"
        )


def validate_card_operation(operation, game_state, edge_rules):
    """Validate if a card operation is allowed based on edge rules"""
    errors = []
    
    if isinstance(operation, CardTransfer):
        # Validate card transfer rules
        if operation.fromLocation == "properties" and operation.toLocation == "bank":
            if not edge_rules.houseHotelAsPayment:
                errors.append("House/Hotel cannot be used as payment with current rules")
        
        if operation.fromLocation == "properties" and operation.toLocation == "properties":
            if not edge_rules.movingHouseHotel:
                errors.append("Moving House/Hotel is not allowed with current rules")
    
    elif isinstance(operation, CardSelection):
        # Validate card selection rules
        if operation.action == "transfer" and operation.targetLocation == "properties":
            # Check if property set is valid
            if not is_valid_property_set(operation.selectedCards, operation.propertySet):
                errors.append("Invalid property set combination")
    
    return errors


def execute_card_operation(operation, game_state):
    """Execute the card operation and return new game state"""
    # Create a deep copy of the game state
    new_state = game_state.copy(deep=True)
    
    if isinstance(operation, CardTransfer):
        # Execute card transfer
        if operation.fromLocation == "hand" and operation.toLocation == "properties":
            # Move card from hand to properties
            player = next(p for p in new_state.players if p.id == operation.toPlayerId)
            if operation.cardId in player.hand:
                player.hand.remove(operation.cardId)
                if operation.propertySet not in player.properties:
                    player.properties[operation.propertySet] = []
                player.properties[operation.propertySet].append(operation.cardId)
        
        elif operation.fromLocation == "hand" and operation.toLocation == "bank":
            # Move card from hand to bank
            player = next(p for p in new_state.players if p.id == operation.toPlayerId)
            if operation.cardId in player.hand:
                player.hand.remove(operation.cardId)
                # Convert property card to money value
                if hasattr(operation, 'cardValue'):
                    player.bank.append(operation.cardValue)
    
    elif isinstance(operation, CardSelection):
        # Handle card selection
        if operation.action == "transfer":
            # Process selected cards for transfer
            pass
    
    return new_state


def is_valid_property_set(cards, property_set):
    """Check if selected cards form a valid property set"""
    # This would contain logic to validate property set combinations
    # based on Monopoly Deal rules
    return True  # Placeholder implementation
