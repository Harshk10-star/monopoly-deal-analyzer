#!/usr/bin/env python3
"""
Test game analysis with different edge rule configurations
"""

import requests
import json

def test_analysis_with_configurations():
    print("🎯 Testing Game Analysis with Different Configurations\n")
    
    # Sample game state
    game_state = {
        "players": [
            {
                "id": 0,
                "name": "You",
                "hand": ["Deal Breaker", "Green Property", "House"],
                "bank": [5, 2],
                "properties": {
                    "green": ["Green Property", "Green Property"],
                    "blue": ["Blue Property"]
                }
            },
            {
                "id": 1,
                "name": "Opponent",
                "hand": [],
                "bank": [1, 1],
                "properties": {
                    "red": ["Red Property", "Red Property", "Red Property"],
                    "yellow": ["Yellow Property"]
                }
            }
        ],
        "discard": [],
        "deckCount": 70
    }
    
    # Test with different configurations
    configurations = [
        {
            "name": "Strict Official Rules",
            "rules": {
                "housePayment": "bank",
                "hotelMove": "not_allowed",
                "deckExhaustion": "reshuffle",
                "extraProperties": "cap",
                "buildingForfeiture": "discard",
                "propertyMerging": "auto_merge",
                "quadrupleRent": False,
                "forcedDealToDealBreaker": False,
                "justSayNoEmptyHand": False,
                "justSayNoOnZero": False
            }
        },
        {
            "name": "Flexible House Rules",
            "rules": {
                "housePayment": "floating",
                "hotelMove": "costs_action",
                "deckExhaustion": "reshuffle",
                "extraProperties": "split",
                "buildingForfeiture": "to_bank",
                "propertyMerging": "manual_merge",
                "quadrupleRent": True,
                "forcedDealToDealBreaker": True,
                "justSayNoEmptyHand": True,
                "justSayNoOnZero": True
            }
        }
    ]
    
    for i, config in enumerate(configurations, 1):
        print(f"{i}. Testing with {config['name']}...")
        
        # Create analysis request
        analysis_request = {
            "gameState": {
                **game_state,
                "edgeRules": config["rules"]
            },
            "strategy": "aggressive"
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/analysis/analyze",
                json=analysis_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Analysis successful")
                print(f"      Recommended move: {result['recommendedMove'][:60]}...")
                print(f"      Strongest player: {result['strongestPlayer']}")
                
                # Show win probabilities
                win_probs = result['winProbability']
                for player, prob in win_probs.items():
                    print(f"      {player}: {prob:.1%} win chance")
                    
            else:
                print(f"   ❌ Analysis failed with status {response.status_code}")
                print(f"      Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("🎉 Configuration-based analysis testing complete!")

if __name__ == "__main__":
    test_analysis_with_configurations()