"""
Integration tests for rule validation engine with EdgeRules model.

Tests the integration between the validation engine and the existing
EdgeRules model to ensure compatibility and proper functionality.
"""

import pytest
from app.core.validation import RuleValidationEngine, ValidationResult
from app.models.game import EdgeRules


class TestValidationIntegration:
    """Integration tests for validation engine with EdgeRules."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = RuleValidationEngine()
    
    def test_edge_rules_existing_validation_method(self):
        """Test that existing EdgeRules validation method still works."""
        rules = EdgeRules(
            hotelMove="free_move",
            buildingForfeiture="keep_floating"
        )
        
        # Test existing method
        existing_warnings = rules.validate_rule_consistency()
        assert isinstance(existing_warnings, list)
        
        # Test new validation engine
        result = self.validator.validate_rules(rules)
        assert isinstance(result, ValidationResult)
        assert result.is_valid is True  # Should be valid with warnings
        assert len(result.warnings) > 0
    
    def test_edge_rules_get_descriptions_compatibility(self):
        """Test compatibility with EdgeRules description methods."""
        rules = EdgeRules()
        
        descriptions = rules.get_rule_descriptions()
        options = rules.get_rule_options()
        
        # Ensure all rules have descriptions
        assert "housePayment" in descriptions
        assert "hotelMove" in descriptions
        assert "deckExhaustion" in descriptions
        assert "extraProperties" in descriptions
        assert "buildingForfeiture" in descriptions
        assert "propertyMerging" in descriptions
        
        # Ensure all rules have options
        assert "housePayment" in options
        assert "hotelMove" in options
        assert "deckExhaustion" in options
        assert "extraProperties" in options
        assert "buildingForfeiture" in options
        assert "propertyMerging" in options
    
    def test_validation_with_all_enum_values(self):
        """Test validation with all possible enum values."""
        from app.models.game import (
            HousePaymentRule, HotelMoveRule, DeckExhaustionRule,
            ExtraPropertiesRule, BuildingForfeitureRule, PropertyMergingRule
        )
        
        # Test each enum value
        for house_payment in HousePaymentRule:
            for hotel_move in HotelMoveRule:
                for deck_exhaustion in DeckExhaustionRule:
                    for extra_properties in ExtraPropertiesRule:
                        for building_forfeiture in BuildingForfeitureRule:
                            for property_merging in PropertyMergingRule:
                                rules = EdgeRules(
                                    housePayment=house_payment,
                                    hotelMove=hotel_move,
                                    deckExhaustion=deck_exhaustion,
                                    extraProperties=extra_properties,
                                    buildingForfeiture=building_forfeiture,
                                    propertyMerging=property_merging
                                )
                                
                                # Should not raise exceptions
                                result = self.validator.validate_rules(rules)
                                assert isinstance(result, ValidationResult)
                                assert isinstance(result.is_valid, bool)
    
    def test_validation_result_serialization(self):
        """Test that ValidationResult can be serialized for API responses."""
        rules = EdgeRules(
            quadrupleRent=True,
            forcedDealToDealBreaker=False
        )
        
        result = self.validator.validate_rules(rules)
        
        # Test JSON serialization
        json_data = result.model_dump()
        assert isinstance(json_data, dict)
        assert "is_valid" in json_data
        assert "errors" in json_data
        assert "warnings" in json_data
        assert "suggestions" in json_data
        assert "performance_impact" in json_data
        
        # Test that it can be reconstructed
        reconstructed = ValidationResult(**json_data)
        assert reconstructed.is_valid == result.is_valid
        assert reconstructed.errors == result.errors
        assert reconstructed.warnings == result.warnings
        assert reconstructed.suggestions == result.suggestions
        assert reconstructed.performance_impact == result.performance_impact
    
    def test_validation_with_boolean_rules(self):
        """Test validation with all boolean rule combinations."""
        boolean_combinations = [
            (True, True, True, True),
            (True, True, True, False),
            (True, True, False, True),
            (True, False, True, True),
            (False, True, True, True),
            (False, False, False, False),
            (True, False, False, False),
            (False, True, False, False),
            (False, False, True, False),
            (False, False, False, True)
        ]
        
        for quad_rent, forced_deal, just_say_no_empty, just_say_no_zero in boolean_combinations:
            rules = EdgeRules(
                quadrupleRent=quad_rent,
                forcedDealToDealBreaker=forced_deal,
                justSayNoEmptyHand=just_say_no_empty,
                justSayNoOnZero=just_say_no_zero
            )
            
            result = self.validator.validate_rules(rules)
            assert isinstance(result, ValidationResult)
            # All combinations should be valid (may have warnings)
            assert result.is_valid is True
    
    def test_performance_impact_consistency(self):
        """Test that performance impact calculation is consistent."""
        # Test multiple times to ensure consistency
        rules = EdgeRules(
            extraProperties="split",
            propertyMerging="auto_merge",
            hotelMove="free_move"
        )
        
        results = []
        for _ in range(5):
            result = self.validator.validate_rules(rules)
            results.append(result.performance_impact)
        
        # All results should be the same
        assert all(impact == results[0] for impact in results)
        assert results[0] == "high"  # This combination should be high impact


if __name__ == "__main__":
    pytest.main([__file__, "-v"])