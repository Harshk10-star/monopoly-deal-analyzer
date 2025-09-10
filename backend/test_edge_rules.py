#!/usr/bin/env python3
"""
Unit tests for the EdgeRules model and related enums
"""

import pytest
from app.models.game import (
    EdgeRules, 
    HousePaymentRule, 
    HotelMoveRule, 
    DeckExhaustionRule, 
    ExtraPropertiesRule,
    BuildingForfeitureRule,
    PropertyMergingRule
)


class TestEdgeRulesEnums:
    """Test the enum classes for edge rules"""
    
    def test_house_payment_rule_values(self):
        """Test HousePaymentRule enum values"""
        assert HousePaymentRule.BANK == "bank"
        assert HousePaymentRule.INCOMPLETE_SET == "incomplete_set"
        assert HousePaymentRule.FLOATING == "floating"
    
    def test_hotel_move_rule_values(self):
        """Test HotelMoveRule enum values"""
        assert HotelMoveRule.NOT_ALLOWED == "not_allowed"
        assert HotelMoveRule.FREE_MOVE == "free_move"
        assert HotelMoveRule.COSTS_ACTION == "costs_action"
    
    def test_deck_exhaustion_rule_values(self):
        """Test DeckExhaustionRule enum values"""
        assert DeckExhaustionRule.RESHUFFLE == "reshuffle"
        assert DeckExhaustionRule.GAME_OVER == "game_over"
    
    def test_extra_properties_rule_values(self):
        """Test ExtraPropertiesRule enum values"""
        assert ExtraPropertiesRule.CAP_RENT == "cap"
        assert ExtraPropertiesRule.SPLIT_SETS == "split"
    
    def test_building_forfeiture_rule_values(self):
        """Test BuildingForfeitureRule enum values"""
        assert BuildingForfeitureRule.DISCARD == "discard"
        assert BuildingForfeitureRule.TO_BANK == "to_bank"
        assert BuildingForfeitureRule.KEEP_FLOATING == "keep_floating"
    
    def test_property_merging_rule_values(self):
        """Test PropertyMergingRule enum values"""
        assert PropertyMergingRule.AUTO_MERGE == "auto_merge"
        assert PropertyMergingRule.MANUAL_MERGE == "manual_merge"
        assert PropertyMergingRule.NO_MERGE == "no_merge"


class TestEdgeRulesModel:
    """Test the EdgeRules model"""
    
    def test_default_edge_rules(self):
        """Test EdgeRules with default values"""
        rules = EdgeRules()
        
        # Test default values
        assert rules.housePayment == HousePaymentRule.BANK
        assert rules.hotelMove == HotelMoveRule.NOT_ALLOWED
        assert rules.deckExhaustion == DeckExhaustionRule.RESHUFFLE
        assert rules.extraProperties == ExtraPropertiesRule.CAP_RENT
        assert rules.buildingForfeiture == BuildingForfeitureRule.DISCARD
        assert rules.propertyMerging == PropertyMergingRule.AUTO_MERGE
        assert rules.quadrupleRent == False
        assert rules.forcedDealToDealBreaker == True
        assert rules.justSayNoEmptyHand == True
        assert rules.justSayNoOnZero == True
    
    def test_custom_edge_rules(self):
        """Test EdgeRules with custom values"""
        rules = EdgeRules(
            housePayment=HousePaymentRule.FLOATING,
            hotelMove=HotelMoveRule.COSTS_ACTION,
            deckExhaustion=DeckExhaustionRule.GAME_OVER,
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            buildingForfeiture=BuildingForfeitureRule.TO_BANK,
            propertyMerging=PropertyMergingRule.NO_MERGE,
            quadrupleRent=True,
            forcedDealToDealBreaker=False,
            justSayNoEmptyHand=False,
            justSayNoOnZero=False
        )
        
        assert rules.housePayment == HousePaymentRule.FLOATING
        assert rules.hotelMove == HotelMoveRule.COSTS_ACTION
        assert rules.deckExhaustion == DeckExhaustionRule.GAME_OVER
        assert rules.extraProperties == ExtraPropertiesRule.SPLIT_SETS
        assert rules.buildingForfeiture == BuildingForfeitureRule.TO_BANK
        assert rules.propertyMerging == PropertyMergingRule.NO_MERGE
        assert rules.quadrupleRent == True
        assert rules.forcedDealToDealBreaker == False
        assert rules.justSayNoEmptyHand == False
        assert rules.justSayNoOnZero == False
    
    def test_get_rule_descriptions(self):
        """Test the get_rule_descriptions method"""
        rules = EdgeRules()
        descriptions = rules.get_rule_descriptions()
        
        # Check that all rules have descriptions
        expected_keys = [
            "housePayment", "hotelMove", "deckExhaustion", "extraProperties",
            "buildingForfeiture", "propertyMerging", "quadrupleRent",
            "forcedDealToDealBreaker", "justSayNoEmptyHand", "justSayNoOnZero"
        ]
        
        for key in expected_keys:
            assert key in descriptions
            assert isinstance(descriptions[key], str)
            assert len(descriptions[key]) > 0
    
    def test_get_rule_options(self):
        """Test the get_rule_options method"""
        rules = EdgeRules()
        options = rules.get_rule_options()
        
        # Test enum-based options
        assert "bank" in options["housePayment"]
        assert "incomplete_set" in options["housePayment"]
        assert "floating" in options["housePayment"]
        
        assert "not_allowed" in options["hotelMove"]
        assert "free_move" in options["hotelMove"]
        assert "costs_action" in options["hotelMove"]
        
        assert "reshuffle" in options["deckExhaustion"]
        assert "game_over" in options["deckExhaustion"]
        
        assert "cap" in options["extraProperties"]
        assert "split" in options["extraProperties"]
        
        assert "discard" in options["buildingForfeiture"]
        assert "to_bank" in options["buildingForfeiture"]
        assert "keep_floating" in options["buildingForfeiture"]
        
        assert "auto_merge" in options["propertyMerging"]
        assert "manual_merge" in options["propertyMerging"]
        assert "no_merge" in options["propertyMerging"]
        
        # Test boolean options
        assert options["quadrupleRent"] == [True, False]
        assert options["forcedDealToDealBreaker"] == [True, False]
        assert options["justSayNoEmptyHand"] == [True, False]
        assert options["justSayNoOnZero"] == [True, False]
    
    def test_validate_rule_consistency_no_warnings(self):
        """Test rule validation with consistent rules"""
        rules = EdgeRules()  # Default rules should be consistent
        warnings = rules.validate_rule_consistency()
        assert isinstance(warnings, list)
    
    def test_validate_rule_consistency_with_warnings(self):
        """Test rule validation with potentially conflicting rules"""
        # Test free movement with floating forfeiture
        rules = EdgeRules(
            hotelMove=HotelMoveRule.FREE_MOVE,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING
        )
        warnings = rules.validate_rule_consistency()
        assert len(warnings) > 0
        assert any("Free building movement" in warning for warning in warnings)
        
        # Test split sets with auto merge
        rules = EdgeRules(
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            propertyMerging=PropertyMergingRule.AUTO_MERGE
        )
        warnings = rules.validate_rule_consistency()
        assert len(warnings) > 0
        assert any("Auto-merging with split sets" in warning for warning in warnings)
        
        # Test quadruple rent without advanced combos
        rules = EdgeRules(
            quadrupleRent=True,
            forcedDealToDealBreaker=False
        )
        warnings = rules.validate_rule_consistency()
        assert len(warnings) > 0
        assert any("Quadruple rent enabled" in warning for warning in warnings)
    
    def test_edge_rules_serialization(self):
        """Test EdgeRules can be serialized to dict"""
        rules = EdgeRules(
            housePayment=HousePaymentRule.FLOATING,
            quadrupleRent=True
        )
        
        rules_dict = rules.dict()
        assert rules_dict["housePayment"] == "floating"
        assert rules_dict["quadrupleRent"] == True
        
        # Test that it can be reconstructed
        new_rules = EdgeRules(**rules_dict)
        assert new_rules.housePayment == HousePaymentRule.FLOATING
        assert new_rules.quadrupleRent == True
    
    def test_edge_rules_json_schema(self):
        """Test EdgeRules JSON schema example"""
        schema = EdgeRules.schema()
        assert "properties" in schema
        
        # Check that all fields are in the schema
        properties = schema["properties"]
        expected_fields = [
            "housePayment", "hotelMove", "deckExhaustion", "extraProperties",
            "buildingForfeiture", "propertyMerging", "quadrupleRent",
            "forcedDealToDealBreaker", "justSayNoEmptyHand", "justSayNoOnZero"
        ]
        
        for field in expected_fields:
            assert field in properties


def run_tests():
    """Run all tests manually"""
    print("Running EdgeRules Model Tests")
    print("=" * 50)
    
    # Test enum classes
    enum_tests = TestEdgeRulesEnums()
    print("Testing enum values...")
    enum_tests.test_house_payment_rule_values()
    enum_tests.test_hotel_move_rule_values()
    enum_tests.test_deck_exhaustion_rule_values()
    enum_tests.test_extra_properties_rule_values()
    enum_tests.test_building_forfeiture_rule_values()
    enum_tests.test_property_merging_rule_values()
    print("✓ All enum tests passed")
    
    # Test EdgeRules model
    model_tests = TestEdgeRulesModel()
    print("\nTesting EdgeRules model...")
    model_tests.test_default_edge_rules()
    model_tests.test_custom_edge_rules()
    model_tests.test_get_rule_descriptions()
    model_tests.test_get_rule_options()
    model_tests.test_validate_rule_consistency_no_warnings()
    model_tests.test_validate_rule_consistency_with_warnings()
    model_tests.test_edge_rules_serialization()
    model_tests.test_edge_rules_json_schema()
    print("✓ All EdgeRules model tests passed")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")


if __name__ == "__main__":
    run_tests()