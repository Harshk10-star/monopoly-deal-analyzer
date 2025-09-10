#!/usr/bin/env python3
"""
Test script for card operations in Monopoly Deal Analyzer
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.game import (
    GameState, PlayerState, EdgeRules, CardTransfer, CardSelection,
    CardOperationRequest
)
from app.core.game_engine import MonopolyDealEngine

def test_card_operations():
    print("Testing Card Operations in Monopoly Deal Analyzer")
    print("=" * 50)
    
    # Create a sample game state
    game_state = GameState(
        players=[
            PlayerState(
                id=1, 
                name="Alice", 
                hand=["Green Property", "Deal Breaker", "Pass Go"], 
                bank=[5, 2], 
                properties={"green": ["Green Property", "Green Property"], "blue": []}
            ),
            PlayerState(
                id=2, 
                name="Bob", 
                hand=["Blue Property", "Rent Green/Blue"], 
                bank=[1, 1], 
                properties={"blue": ["Blue Property", "Blue Property"], "red": ["Red Property"]}
            )
        ],
        discard=["Debt Collector"],
        deckCount=70,
        edgeRules=EdgeRules()
    )
    
    # Test card transfer operation
    print("\n1. Testing Card Transfer Operation")
    print("-" * 30)
    
    transfer_operation = CardTransfer(
        cardId="Green Property",
        fromLocation="hand",
        toLocation="properties",
        fromPlayerId=1,
        toPlayerId=1,
        propertySet="green"
    )
    
    print(f"Transfer: {transfer_operation.cardId} from {transfer_operation.fromLocation} to {transfer_operation.toLocation}")
    print(f"Property Set: {transfer_operation.propertySet}")
    
    # Test card selection operation
    print("\n2. Testing Card Selection Operation")
    print("-" * 30)
    
    selection_operation = CardSelection(
        selectedCards=["Green Property", "Green Property"],
        action="transfer",
        targetLocation="properties",
        targetPlayerId=1,
        propertySet="green"
    )
    
    print(f"Selected Cards: {selection_operation.selectedCards}")
    print(f"Action: {selection_operation.action}")
    print(f"Target: {selection_operation.targetLocation}")
    
    # Test edge rules validation
    print("\n3. Testing Edge Rules Validation")
    print("-" * 30)
    
    engine = MonopolyDealEngine()
    
    # Test with different edge rules
    edge_rules = EdgeRules(
        houseHotelAsPayment="bank",
        movingHouseHotel="not_allowed",
        deckExhaustionReshuffle=True,
        extraPropertiesHandling="cap",
        mergingPropertySets=True,
        forfeitingBuildings=True,
        quadrupleRent=False,
        forcedDealToDealBreaker=True,
        justSayNoEmptyHand=True
    )
    
    print("Edge Rules Configuration:")
    print(f"  House/Hotel as Payment: {edge_rules.houseHotelAsPayment}")
    print(f"  Moving House/Hotel: {edge_rules.movingHouseHotel}")
    print(f"  Deck Exhaustion Reshuffle: {edge_rules.deckExhaustionReshuffle}")
    print(f"  Extra Properties Handling: {edge_rules.extraPropertiesHandling}")
    print(f"  Merging Property Sets: {edge_rules.mergingPropertySets}")
    print(f"  Forfeiting Buildings: {edge_rules.forfeitingBuildings}")
    print(f"  Quadruple Rent: {edge_rules.quadrupleRent}")
    print(f"  Forced Deal → Deal Breaker: {edge_rules.forcedDealToDealBreaker}")
    print(f"  Just Say No Empty Hand: {edge_rules.justSayNoEmptyHand}")
    
    # Test edge case validation
    validation_errors = engine.validate_edge_case_rules(game_state, edge_rules)
    if validation_errors:
        print(f"\nValidation Errors: {validation_errors}")
    else:
        print("\n✅ No validation errors found")
    
    print("\n4. Testing Game State Analysis")
    print("-" * 30)
    
    try:
        from app.models.game import AIStrategy
        analysis_result = engine.analyze_game_state(game_state, AIStrategy.NORMAL)
        print(f"Recommended Move: {analysis_result.recommendedMove}")
        print(f"Reasoning: {analysis_result.reasoning}")
        print(f"Strongest Player: {analysis_result.strongestPlayer}")
        print("Win Probabilities:")
        for player, prob in analysis_result.winProbability.items():
            print(f"  {player}: {prob:.2%}")
    except Exception as e:
        print(f"Analysis failed: {e}")
    
    print("\n" + "=" * 50)
    print("Card Operations Test Completed!")

if __name__ == "__main__":
    test_card_operations()



