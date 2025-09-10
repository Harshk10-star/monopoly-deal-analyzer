#!/usr/bin/env python3
"""
Simple test script for the Monopoly Deal game engine
"""

from app.core.game_engine import MonopolyDealEngine
from app.models.game import GameState, PlayerState, EdgeRules, AIStrategy

def test_game_engine():
    """Test the game engine with a sample game state"""
    
    # Create sample game state
    game_state = GameState(
        players=[
            PlayerState(
                id=1,
                name="Alice",
                hand=["Pass Go", "Deal Breaker", "Green Property"],
                bank=[5, 2],
                properties={"green": ["Green Property", "Green Property"], "blue": []}
            ),
            PlayerState(
                id=2,
                name="Bob",
                hand=["Rent Green/Blue", "House"],
                bank=[1, 1],
                properties={"blue": ["Blue Property", "Blue Property"], "red": ["Red Property"]}
            )
        ],
        discard=["Debt Collector"],
        deckCount=70,
        edgeRules=EdgeRules()
    )
    
    # Test different strategies
    engine = MonopolyDealEngine()
    
    print("Testing Monopoly Deal Game Engine")
    print("=" * 50)
    
    for strategy in [AIStrategy.AGGRESSIVE, AIStrategy.DEFENSIVE, AIStrategy.NORMAL]:
        print(f"\nStrategy: {strategy.value.upper()}")
        print("-" * 30)
        
        try:
            result = engine.analyze_game_state(game_state, strategy)
            print(f"Recommended Move: {result.recommendedMove}")
            print(f"Reasoning: {result.reasoning}")
            print(f"Strongest Player: {result.strongestPlayer}")
            print("Win Probabilities:")
            for player, prob in result.winProbability.items():
                print(f"  {player}: {prob:.2%}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_game_engine()



