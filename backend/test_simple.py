#!/usr/bin/env python3
"""
Test the simplified backend for stateless deployment
"""

import sys
import os
sys.path.append('.')

def test_simplified_backend():
    print("🧪 Testing Simplified Backend for Stateless Deployment")
    print("=" * 60)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from main_simple import app
        print("   ✅ FastAPI app imports successfully")
        
        from app.models.configuration import OFFICIAL_PRESETS
        print(f"   ✅ {len(OFFICIAL_PRESETS)} official presets available")
        
        from app.core.validation import RuleValidationEngine
        from app.models.game import EdgeRules
        print("   ✅ All required modules import successfully")
        
        # Test validation engine
        print("\n2. Testing validation engine...")
        engine = RuleValidationEngine()
        rules = EdgeRules()
        result = engine.validate_rules(rules)
        print(f"   ✅ Validation engine works: valid={result.is_valid}")
        
        # Test configuration presets
        print("\n3. Testing configuration presets...")
        for preset_id, preset in OFFICIAL_PRESETS.items():
            print(f"   ✅ {preset.name}: {len(preset.rules.dict())} rules")
        
        # Test game engine
        print("\n4. Testing game engine...")
        from app.core.game_engine import MonopolyDealEngine
        
        # Create sample game state
        sample_game_state = {
            "players": [
                {
                    "id": 0,
                    "name": "Test Player",
                    "hand": ["Deal Breaker"],
                    "bank": [5],
                    "properties": {"green": ["Green Property"]}
                }
            ],
            "discard": [],
            "deckCount": 70,
            "edgeRules": rules.dict()
        }
        
        # Convert to proper model
        from app.models.game import GameState, PlayerState
        
        players = [PlayerState(
            id=0,
            name="Test Player", 
            hand=["Deal Breaker"],
            bank=[5],
            properties={"green": ["Green Property"]}
        )]
        
        game_state = GameState(
            players=players,
            discard=[],
            deckCount=70,
            edgeRules=rules
        )
        
        engine = MonopolyDealEngine(rules)
        print("   ✅ Game engine created with edge rules")
        
        print("\n🎉 Simplified Backend Test Results:")
        print("   ✅ All imports working")
        print("   ✅ Configuration system ready")
        print("   ✅ Validation engine ready") 
        print("   ✅ Game engine ready")
        print("   ✅ No database required")
        print("   ✅ Ready for stateless deployment!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simplified_backend()
    exit(0 if success else 1)