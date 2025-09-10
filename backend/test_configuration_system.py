#!/usr/bin/env python3
"""
Test script for the Monopoly Deal configuration system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.game import EdgeRules
from app.core.validation import RuleValidationEngine
from app.models.configuration import OFFICIAL_PRESETS

def test_edge_rules_model():
    """Test EdgeRules model creation and validation"""
    print("Testing EdgeRules model...")
    
    # Test default rules
    default_rules = EdgeRules()
    print(f"Default rules: {default_rules.dict()}")
    
    # Test rule descriptions
    descriptions = default_rules.get_rule_descriptions()
    print(f"Rule descriptions count: {len(descriptions)}")
    
    # Test rule options
    options = default_rules.get_rule_options()
    print(f"Rule options count: {len(options)}")
    
    # Test consistency validation
    warnings = default_rules.validate_rule_consistency()
    print(f"Default rules warnings: {warnings}")
    
    print("✅ EdgeRules model test passed\n")

def test_validation_engine():
    """Test rule validation engine"""
    print("Testing RuleValidationEngine...")
    
    validator = RuleValidationEngine()
    
    # Test with default rules
    default_rules = EdgeRules()
    result = validator.validate_rules(default_rules)
    print(f"Default rules validation: valid={result.is_valid}, warnings={len(result.warnings)}")
    
    # Test with conflicting rules
    conflicting_rules = EdgeRules(
        hotelMove="free_move",
        buildingForfeiture="keep_floating",
        extraProperties="split",
        propertyMerging="auto_merge"
    )
    result = validator.validate_rules(conflicting_rules)
    print(f"Conflicting rules validation: valid={result.is_valid}, warnings={len(result.warnings)}")
    print(f"Performance impact: {result.performance_impact}")
    
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings[:3]:  # Show first 3 warnings
            print(f"  - {warning}")
    
    print("✅ RuleValidationEngine test passed\n")

def test_official_presets():
    """Test official configuration presets"""
    print("Testing official presets...")
    
    print(f"Number of official presets: {len(OFFICIAL_PRESETS)}")
    
    for preset_id, preset in OFFICIAL_PRESETS.items():
        print(f"Preset: {preset.name}")
        print(f"  ID: {preset.id}")
        print(f"  Official: {preset.is_official}")
        print(f"  Description: {preset.description[:50]}...")
        
        # Validate each preset
        validator = RuleValidationEngine()
        result = validator.validate_rules(preset.rules)
        print(f"  Validation: valid={result.is_valid}, warnings={len(result.warnings)}")
        print()
    
    print("✅ Official presets test passed\n")

def test_edge_case_scenarios():
    """Test specific edge case scenarios"""
    print("Testing edge case scenarios...")
    
    # Scenario 1: House/Hotel payment without complete set
    print("Scenario 1: House payment rules")
    for payment_rule in ["bank", "incomplete_set", "floating"]:
        rules = EdgeRules(housePayment=payment_rule)
        print(f"  {payment_rule}: {rules.get_rule_descriptions()['housePayment']}")
    
    # Scenario 2: Building movement
    print("\nScenario 2: Building movement rules")
    for move_rule in ["not_allowed", "free_move", "costs_action"]:
        rules = EdgeRules(hotelMove=move_rule)
        print(f"  {move_rule}: {rules.get_rule_descriptions()['hotelMove']}")
    
    # Scenario 3: Extra properties handling
    print("\nScenario 3: Extra properties rules")
    for extra_rule in ["cap", "split"]:
        rules = EdgeRules(extraProperties=extra_rule)
        print(f"  {extra_rule}: {rules.get_rule_descriptions()['extraProperties']}")
    
    # Scenario 4: Advanced action combinations
    print("\nScenario 4: Advanced action rules")
    rules = EdgeRules(
        quadrupleRent=True,
        forcedDealToDealBreaker=True,
        justSayNoEmptyHand=True,
        justSayNoOnZero=True
    )
    print(f"  All advanced rules enabled")
    validator = RuleValidationEngine()
    result = validator.validate_rules(rules)
    print(f"  Validation warnings: {len(result.warnings)}")
    
    print("✅ Edge case scenarios test passed\n")

def main():
    """Run all configuration system tests"""
    print("🎯 Testing Monopoly Deal Configuration System\n")
    
    try:
        test_edge_rules_model()
        test_validation_engine()
        test_official_presets()
        test_edge_case_scenarios()
        
        print("🎉 All configuration system tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())