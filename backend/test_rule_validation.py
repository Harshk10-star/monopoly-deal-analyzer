"""
Comprehensive tests for the rule validation engine.

Tests cover all validation scenarios including:
- Rule conflicts and logical consistency
- Performance impact analysis
- Gameplay balance validation
- Edge case handling
"""

import pytest
from app.core.validation import RuleValidationEngine, ValidationResult
from app.models.game import (
    EdgeRules, HousePaymentRule, HotelMoveRule, DeckExhaustionRule,
    ExtraPropertiesRule, BuildingForfeitureRule, PropertyMergingRule
)


class TestRuleValidationEngine:
    """Test suite for RuleValidationEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = RuleValidationEngine()
    
    def test_default_rules_validation(self):
        """Test validation of default EdgeRules configuration."""
        default_rules = EdgeRules()
        result = self.validator.validate_rules(default_rules)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.performance_impact in ["low", "medium", "high"]
    
    def test_building_movement_conflict(self):
        """Test detection of building movement and forfeiture conflicts."""
        rules = EdgeRules(
            hotelMove=HotelMoveRule.FREE_MOVE,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING
        )
        result = self.validator.validate_rules(rules)
        
        assert result.is_valid is True  # Warning, not error
        assert any("complex edge cases" in warning for warning in result.warnings)
    
    def test_property_merging_conflict(self):
        """Test detection of property merging and extra properties conflicts."""
        rules = EdgeRules(
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            propertyMerging=PropertyMergingRule.AUTO_MERGE
        )
        result = self.validator.validate_rules(rules)
        
        assert result.is_valid is True  # Warning, not error
        assert any("frequent recalculations" in warning for warning in result.warnings)
    
    def test_house_payment_forfeiture_conflict(self):
        """Test detection of house payment and building forfeiture conflicts."""
        rules = EdgeRules(
            housePayment=HousePaymentRule.FLOATING,
            buildingForfeiture=BuildingForfeitureRule.DISCARD
        )
        result = self.validator.validate_rules(rules)
        
        assert result.is_valid is True  # Warning, not error
        assert any("inconsistent building handling" in warning for warning in result.warnings)
    
    def test_advanced_action_consistency(self):
        """Test detection of advanced action rule inconsistencies."""
        rules = EdgeRules(
            quadrupleRent=True,
            forcedDealToDealBreaker=False
        )
        result = self.validator.validate_rules(rules)
        
        assert result.is_valid is True  # Warning, not error
        assert any("consistency" in warning for warning in result.warnings)
    
    def test_just_say_no_consistency(self):
        """Test detection of Just Say No rule inconsistencies."""
        rules = EdgeRules(
            justSayNoEmptyHand=True,
            justSayNoOnZero=False
        )
        result = self.validator.validate_rules(rules)
        
        assert result.is_valid is True  # Warning, not error
        assert any("confusing interaction patterns" in warning for warning in result.warnings)
    
    def test_high_performance_impact_rules(self):
        """Test detection of high-performance impact rule combinations."""
        rules = EdgeRules(
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            propertyMerging=PropertyMergingRule.AUTO_MERGE,
            hotelMove=HotelMoveRule.FREE_MOVE,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING
        )
        result = self.validator.validate_rules(rules)
        
        assert result.performance_impact == "high"
        assert any("high-computation rules" in warning for warning in result.warnings)
    
    def test_medium_performance_impact_rules(self):
        """Test detection of medium-performance impact rule combinations."""
        rules = EdgeRules(
            hotelMove=HotelMoveRule.FREE_MOVE,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING
        )
        result = self.validator.validate_rules(rules)
        
        assert result.performance_impact == "medium"
    
    def test_low_performance_impact_rules(self):
        """Test detection of low-performance impact rule combinations."""
        rules = EdgeRules(
            housePayment=HousePaymentRule.BANK,
            hotelMove=HotelMoveRule.NOT_ALLOWED,
            deckExhaustion=DeckExhaustionRule.RESHUFFLE,
            extraProperties=ExtraPropertiesRule.CAP_RENT,
            buildingForfeiture=BuildingForfeitureRule.DISCARD,
            propertyMerging=PropertyMergingRule.NO_MERGE
        )
        result = self.validator.validate_rules(rules)
        
        assert result.performance_impact == "low"
    
    def test_very_permissive_rules_balance(self):
        """Test detection of overly permissive rule configurations."""
        rules = EdgeRules(
            housePayment=HousePaymentRule.FLOATING,
            hotelMove=HotelMoveRule.FREE_MOVE,
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            propertyMerging=PropertyMergingRule.AUTO_MERGE,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING,
            quadrupleRent=True,
            forcedDealToDealBreaker=True,
            justSayNoEmptyHand=True,
            justSayNoOnZero=True
        )
        result = self.validator.validate_rules(rules)
        
        assert any("permissive rule set" in warning for warning in result.warnings)
        assert any("restrictive rules" in suggestion for suggestion in result.suggestions)
    
    def test_very_restrictive_rules_balance(self):
        """Test detection of overly restrictive rule configurations."""
        rules = EdgeRules(
            housePayment=HousePaymentRule.BANK,
            hotelMove=HotelMoveRule.NOT_ALLOWED,
            extraProperties=ExtraPropertiesRule.CAP_RENT,
            propertyMerging=PropertyMergingRule.NO_MERGE,
            buildingForfeiture=BuildingForfeitureRule.DISCARD,
            quadrupleRent=False,
            forcedDealToDealBreaker=False,
            justSayNoEmptyHand=False,
            justSayNoOnZero=False
        )
        result = self.validator.validate_rules(rules)
        
        assert any("restrictive rule set" in warning for warning in result.warnings)
        assert any("advanced features" in suggestion for suggestion in result.suggestions)
    
    def test_deck_exhaustion_edge_cases(self):
        """Test detection of deck exhaustion edge cases."""
        rules = EdgeRules(
            deckExhaustion=DeckExhaustionRule.GAME_OVER,
            hotelMove=HotelMoveRule.FREE_MOVE
        )
        result = self.validator.validate_rules(rules)
        
        assert any("optimize their property arrangements" in suggestion for suggestion in result.suggestions)
    
    def test_floating_buildings_edge_cases(self):
        """Test detection of floating buildings edge cases."""
        # Test floating forfeiture without floating payments
        rules1 = EdgeRules(
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING,
            housePayment=HousePaymentRule.BANK
        )
        result1 = self.validator.validate_rules(rules1)
        
        assert any("inconsistent building handling" in warning for warning in result1.warnings)
        
        # Test floating forfeiture with no movement
        rules2 = EdgeRules(
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING,
            hotelMove=HotelMoveRule.NOT_ALLOWED
        )
        result2 = self.validator.validate_rules(rules2)
        
        assert any("permanently unusable" in warning for warning in result2.warnings)
    
    def test_property_merging_edge_cases(self):
        """Test detection of property merging edge cases."""
        rules = EdgeRules(
            propertyMerging=PropertyMergingRule.AUTO_MERGE,
            extraProperties=ExtraPropertiesRule.CAP_RENT
        )
        result = self.validator.validate_rules(rules)
        
        assert any("split sets for more strategic" in suggestion for suggestion in result.suggestions)
    
    def test_just_say_no_defensive_gameplay(self):
        """Test detection of overly defensive Just Say No configurations."""
        rules = EdgeRules(
            justSayNoEmptyHand=True,
            justSayNoOnZero=True
        )
        result = self.validator.validate_rules(rules)
        
        assert any("defensive gameplay" in suggestion for suggestion in result.suggestions)
    
    def test_performance_computation_suggestions(self):
        """Test performance optimization suggestions."""
        rules = EdgeRules(
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            hotelMove=HotelMoveRule.FREE_MOVE
        )
        result = self.validator.validate_rules(rules)
        
        assert any("costs_action" in suggestion for suggestion in result.suggestions)
    
    def test_validation_result_structure(self):
        """Test ValidationResult model structure and content."""
        rules = EdgeRules(
            hotelMove=HotelMoveRule.FREE_MOVE,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING
        )
        result = self.validator.validate_rules(rules)
        
        # Check all required fields are present
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'warnings')
        assert hasattr(result, 'suggestions')
        assert hasattr(result, 'performance_impact')
        
        # Check field types
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)
        assert isinstance(result.warnings, list)
        assert isinstance(result.suggestions, list)
        assert isinstance(result.performance_impact, str)
        assert result.performance_impact in ["low", "medium", "high"]
    
    def test_no_duplicate_messages(self):
        """Test that validation doesn't produce duplicate messages."""
        # Create rules that might trigger multiple similar warnings
        rules = EdgeRules(
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            propertyMerging=PropertyMergingRule.AUTO_MERGE,
            hotelMove=HotelMoveRule.FREE_MOVE
        )
        result = self.validator.validate_rules(rules)
        
        # Check for duplicates in each list
        assert len(result.errors) == len(set(result.errors))
        assert len(result.warnings) == len(set(result.warnings))
        assert len(result.suggestions) == len(set(result.suggestions))
    
    def test_rule_compatibility_matrix(self):
        """Test rule compatibility matrix functionality."""
        compatibility_matrix = self.validator.get_rule_compatibility_matrix()
        
        assert isinstance(compatibility_matrix, dict)
        
        # Check that known interactions are present
        house_building_key = ("housePayment", "buildingForfeiture")
        if house_building_key in compatibility_matrix:
            interactions = compatibility_matrix[house_building_key]
            assert isinstance(interactions, dict)
            
            # Check that interaction values are valid
            for interaction_key, status in interactions.items():
                assert status in ["good", "warning", "error"]
    
    def test_edge_case_coverage(self):
        """Test that all major edge cases are covered by validation."""
        # Test all enum combinations that should trigger warnings
        test_cases = [
            # Building-related conflicts
            {
                "hotelMove": HotelMoveRule.FREE_MOVE,
                "buildingForfeiture": BuildingForfeitureRule.KEEP_FLOATING
            },
            # Property-related conflicts
            {
                "extraProperties": ExtraPropertiesRule.SPLIT_SETS,
                "propertyMerging": PropertyMergingRule.AUTO_MERGE
            },
            # Action-related conflicts
            {
                "quadrupleRent": True,
                "forcedDealToDealBreaker": False
            }
        ]
        
        for case in test_cases:
            rules = EdgeRules(**case)
            result = self.validator.validate_rules(rules)
            
            # Each case should produce at least one warning or suggestion
            assert len(result.warnings) > 0 or len(result.suggestions) > 0


class TestValidationResultModel:
    """Test suite for ValidationResult model."""
    
    def test_validation_result_creation(self):
        """Test ValidationResult model creation and validation."""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=["Test warning"],
            suggestions=["Test suggestion"],
            performance_impact="medium"
        )
        
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == ["Test warning"]
        assert result.suggestions == ["Test suggestion"]
        assert result.performance_impact == "medium"
    
    def test_validation_result_defaults(self):
        """Test ValidationResult model with default values."""
        result = ValidationResult(is_valid=False)
        
        assert result.is_valid is False
        assert result.errors == []
        assert result.warnings == []
        assert result.suggestions == []
        assert result.performance_impact == "low"
    
    def test_validation_result_json_serialization(self):
        """Test ValidationResult JSON serialization."""
        result = ValidationResult(
            is_valid=True,
            warnings=["Test warning"],
            performance_impact="high"
        )
        
        json_data = result.model_dump()
        
        assert json_data["is_valid"] is True
        assert json_data["warnings"] == ["Test warning"]
        assert json_data["performance_impact"] == "high"
        assert "errors" in json_data
        assert "suggestions" in json_data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])