#!/usr/bin/env python3
"""
Comprehensive demonstration of the Monopoly Deal Configuration System
"""

import requests
import json

def demo_configuration_system():
    print("🎯 Monopoly Deal Edge Case Configuration System Demo")
    print("=" * 60)
    
    # 1. Show available presets
    print("\n📋 AVAILABLE CONFIGURATION PRESETS")
    print("-" * 40)
    
    response = requests.get("http://localhost:8000/api/v1/configuration/presets")
    presets = response.json()
    
    for preset in presets:
        print(f"🔧 {preset['name']}")
        print(f"   Type: {'Official' if preset['is_official'] else 'Custom'}")
        print(f"   Description: {preset['description']}")
        print(f"   Usage: {preset['usage_count']} times")
        print()
    
    # 2. Demonstrate rule validation
    print("\n⚠️  RULE VALIDATION EXAMPLES")
    print("-" * 40)
    
    # Example 1: Conflicting rules
    print("Example 1: High-complexity configuration")
    conflicting_rules = {
        "housePayment": "floating",
        "hotelMove": "free_move",
        "deckExhaustion": "reshuffle", 
        "extraProperties": "split",
        "buildingForfeiture": "keep_floating",
        "propertyMerging": "auto_merge",
        "quadrupleRent": True,
        "forcedDealToDealBreaker": True,
        "justSayNoEmptyHand": True,
        "justSayNoOnZero": True
    }
    
    response = requests.post("http://localhost:8000/api/v1/configuration/validate", json=conflicting_rules)
    validation = response.json()
    
    print(f"   Valid: {validation['is_valid']}")
    print(f"   Performance Impact: {validation['performance_impact'].upper()}")
    print(f"   Warnings: {len(validation['warnings'])}")
    
    if validation['warnings']:
        print("   Key warnings:")
        for warning in validation['warnings'][:3]:
            print(f"     • {warning}")
    
    if validation['suggestions']:
        print("   Suggestions:")
        for suggestion in validation['suggestions'][:2]:
            print(f"     💡 {suggestion}")
    
    print()
    
    # Example 2: Conservative rules
    print("Example 2: Conservative configuration")
    conservative_rules = {
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
    
    response = requests.post("http://localhost:8000/api/v1/configuration/validate", json=conservative_rules)
    validation = response.json()
    
    print(f"   Valid: {validation['is_valid']}")
    print(f"   Performance Impact: {validation['performance_impact'].upper()}")
    print(f"   Warnings: {len(validation['warnings'])}")
    print()
    
    # 3. Show edge case handling
    print("\n🎲 EDGE CASE SCENARIOS COVERED")
    print("-" * 40)
    
    response = requests.get("http://localhost:8000/api/v1/configuration/rule-descriptions")
    rule_info = response.json()
    
    edge_cases = [
        ("housePayment", "House/Hotel payment without complete sets"),
        ("hotelMove", "Moving buildings between property sets"),
        ("buildingForfeiture", "What happens to buildings when sets break"),
        ("extraProperties", "Handling extra property cards"),
        ("quadrupleRent", "Double 'Double the Rent' cards"),
        ("forcedDealToDealBreaker", "Forced Deal → Deal Breaker combos"),
        ("justSayNoEmptyHand", "Just Say No from empty hand"),
        ("justSayNoOnZero", "Just Say No on zero-cost actions")
    ]
    
    for rule_key, description in edge_cases:
        options = rule_info['options'].get(rule_key, [])
        print(f"🎯 {description}")
        if isinstance(options[0], bool):
            print(f"   Options: Enable/Disable")
        else:
            print(f"   Options: {', '.join(options)}")
        print()
    
    # 4. Demonstrate AI analysis with different configs
    print("\n🤖 AI ANALYSIS WITH DIFFERENT CONFIGURATIONS")
    print("-" * 40)
    
    # Sample game state
    game_state = {
        "players": [
            {
                "id": 0,
                "name": "You",
                "hand": ["Deal Breaker", "House", "Green Property"],
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
                "bank": [3, 1],
                "properties": {
                    "red": ["Red Property", "Red Property", "Red Property"]
                }
            }
        ],
        "discard": [],
        "deckCount": 70
    }
    
    # Test with strict vs flexible rules
    configs_to_test = [
        ("Strict Official", conservative_rules),
        ("Flexible House Rules", conflicting_rules)
    ]
    
    for config_name, rules in configs_to_test:
        print(f"Testing with {config_name}:")
        
        analysis_request = {
            "gameState": {**game_state, "edgeRules": rules},
            "strategy": "aggressive"
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/analysis/analyze",
                json=analysis_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Recommended: {result['recommendedMove'][:50]}...")
                print(f"   🏆 Strongest: {result['strongestPlayer']}")
                
                win_probs = result['winProbability']
                for player, prob in win_probs.items():
                    print(f"   📊 {player}: {prob:.1%}")
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    # 5. Summary
    print("\n🎉 CONFIGURATION SYSTEM FEATURES")
    print("-" * 40)
    
    features = [
        "✅ 10 edge case rules configured",
        "✅ 4 official presets available", 
        "✅ Real-time rule validation",
        "✅ Performance impact analysis",
        "✅ AI integration with configurations",
        "✅ Import/Export functionality",
        "✅ Custom preset creation",
        "✅ Consistency checking",
        "✅ User-friendly interface",
        "✅ Comprehensive documentation"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n🚀 The Monopoly Deal Configuration System is ready!")
    print(f"   Users can now configure edge case handling to match their play style.")
    print(f"   The AI will provide recommendations that respect these configurations.")

if __name__ == "__main__":
    demo_configuration_system()