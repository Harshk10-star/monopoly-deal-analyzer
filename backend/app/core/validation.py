"""
Rule validation engine for Monopoly Deal configuration system.

This module provides comprehensive validation for EdgeRules configurations,
checking for logical consistency, performance implications, and potential conflicts.
"""

from typing import List, Dict, Set, Tuple
from pydantic import BaseModel
from app.models.game import (
    EdgeRules, HousePaymentRule, HotelMoveRule, DeckExhaustionRule,
    ExtraPropertiesRule, BuildingForfeitureRule, PropertyMergingRule
)


class ValidationResult(BaseModel):
    """Result of rule validation with errors, warnings, and suggestions."""
    
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []
    performance_impact: str = "low"  # "low", "medium", "high"
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": True,
                "errors": [],
                "warnings": ["Free building movement with floating forfeiture may create complex edge cases"],
                "suggestions": ["Consider using 'costs_action' for hotel movement to balance gameplay"],
                "performance_impact": "medium"
            }
        }


class RuleValidationEngine:
    """
    Comprehensive validation engine for EdgeRules configurations.
    
    Validates rule combinations for:
    - Logical consistency
    - Performance implications
    - Gameplay balance
    - Edge case handling
    """
    
    def __init__(self):
        self.conflict_rules = self._initialize_conflict_rules()
        self.performance_rules = self._initialize_performance_rules()
        self.balance_suggestions = self._initialize_balance_suggestions()
    
    def validate_rules(self, rules: EdgeRules) -> ValidationResult:
        """
        Perform comprehensive validation of EdgeRules configuration.
        
        Args:
            rules: EdgeRules configuration to validate
            
        Returns:
            ValidationResult with errors, warnings, and suggestions
        """
        errors = []
        warnings = []
        suggestions = []
        
        # Check for logical conflicts
        conflict_results = self._check_rule_conflicts(rules)
        errors.extend(conflict_results["errors"])
        warnings.extend(conflict_results["warnings"])
        
        # Check performance implications
        performance_results = self._check_performance_impact(rules)
        warnings.extend(performance_results["warnings"])
        suggestions.extend(performance_results["suggestions"])
        
        # Check gameplay balance
        balance_results = self._check_gameplay_balance(rules)
        suggestions.extend(balance_results["suggestions"])
        warnings.extend(balance_results["warnings"])
        
        # Check edge case handling
        edge_case_results = self._check_edge_cases(rules)
        warnings.extend(edge_case_results["warnings"])
        suggestions.extend(edge_case_results["suggestions"])
        
        # Determine performance impact
        performance_impact = self._calculate_performance_impact(rules)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=list(set(errors)),  # Remove duplicates
            warnings=list(set(warnings)),
            suggestions=list(set(suggestions)),
            performance_impact=performance_impact
        )
    
    def _check_rule_conflicts(self, rules: EdgeRules) -> Dict[str, List[str]]:
        """Check for logical conflicts between rules."""
        errors = []
        warnings = []
        
        # Building movement vs forfeiture conflicts
        if (rules.hotelMove == HotelMoveRule.FREE_MOVE and 
            rules.buildingForfeiture == BuildingForfeitureRule.KEEP_FLOATING):
            warnings.append(
                "Free building movement with floating forfeiture may create "
                "complex edge cases where buildings can be moved indefinitely"
            )
        
        # Property merging vs extra properties conflicts
        if (rules.extraProperties == ExtraPropertiesRule.SPLIT_SETS and 
            rules.propertyMerging == PropertyMergingRule.AUTO_MERGE):
            warnings.append(
                "Auto-merging with split sets may cause frequent recalculations "
                "and unexpected property set changes"
            )
        
        # House payment vs building forfeiture logical conflict
        if (rules.housePayment == HousePaymentRule.FLOATING and 
            rules.buildingForfeiture == BuildingForfeitureRule.DISCARD):
            warnings.append(
                "Floating house payments with discard forfeiture creates inconsistent "
                "building handling - consider using 'to_bank' forfeiture instead"
            )
        
        # Advanced action consistency
        if rules.quadrupleRent and not rules.forcedDealToDealBreaker:
            warnings.append(
                "Quadruple rent enabled but advanced action combos disabled - "
                "consider enabling all advanced features for consistency"
            )
        
        # Just Say No consistency
        if rules.justSayNoEmptyHand and not rules.justSayNoOnZero:
            warnings.append(
                "Just Say No from empty hand enabled but not on zero-cost actions - "
                "this may create confusing interaction patterns"
            )
        
        return {"errors": errors, "warnings": warnings}
    
    def _check_performance_impact(self, rules: EdgeRules) -> Dict[str, List[str]]:
        """Check for performance implications of rule combinations."""
        warnings = []
        suggestions = []
        
        # High-computation rule combinations
        high_computation_rules = [
            (rules.extraProperties == ExtraPropertiesRule.SPLIT_SETS, "split property sets"),
            (rules.propertyMerging == PropertyMergingRule.AUTO_MERGE, "auto-merging properties"),
            (rules.hotelMove == HotelMoveRule.FREE_MOVE, "free building movement"),
            (rules.buildingForfeiture == BuildingForfeitureRule.KEEP_FLOATING, "floating buildings")
        ]
        
        active_high_computation = [desc for condition, desc in high_computation_rules if condition]
        
        if len(active_high_computation) >= 3:
            warnings.append(
                f"Multiple high-computation rules active: {', '.join(active_high_computation)}. "
                "This may impact game performance with large property collections."
            )
        
        # Specific performance concerns
        if (rules.extraProperties == ExtraPropertiesRule.SPLIT_SETS and 
            rules.hotelMove == HotelMoveRule.FREE_MOVE):
            suggestions.append(
                "Consider limiting building movement to 'costs_action' when using split sets "
                "to reduce computational complexity"
            )
        
        return {"warnings": warnings, "suggestions": suggestions}
    
    def _check_gameplay_balance(self, rules: EdgeRules) -> Dict[str, List[str]]:
        """Check for gameplay balance implications."""
        warnings = []
        suggestions = []
        
        # Count permissive vs restrictive rules
        permissive_count = 0
        restrictive_count = 0
        
        # Analyze each rule for permissiveness
        if rules.housePayment in [HousePaymentRule.INCOMPLETE_SET, HousePaymentRule.FLOATING]:
            permissive_count += 1
        else:
            restrictive_count += 1
        
        if rules.hotelMove != HotelMoveRule.NOT_ALLOWED:
            permissive_count += 1
        else:
            restrictive_count += 1
        
        if rules.extraProperties == ExtraPropertiesRule.SPLIT_SETS:
            permissive_count += 1
        else:
            restrictive_count += 1
        
        if rules.propertyMerging != PropertyMergingRule.NO_MERGE:
            permissive_count += 1
        else:
            restrictive_count += 1
        
        if rules.buildingForfeiture != BuildingForfeitureRule.DISCARD:
            permissive_count += 1
        else:
            restrictive_count += 1
        
        # Boolean rules
        boolean_permissive = sum([
            rules.quadrupleRent,
            rules.forcedDealToDealBreaker,
            rules.justSayNoEmptyHand,
            rules.justSayNoOnZero
        ])
        
        permissive_count += boolean_permissive
        restrictive_count += (4 - boolean_permissive)
        
        # Balance analysis
        total_rules = permissive_count + restrictive_count
        permissive_ratio = permissive_count / total_rules
        
        if permissive_ratio > 0.8:
            warnings.append(
                "Very permissive rule set may lead to overly complex gameplay "
                "and longer game sessions"
            )
            suggestions.append(
                "Consider adding some restrictive rules to maintain game balance"
            )
        elif permissive_ratio < 0.2:
            warnings.append(
                "Very restrictive rule set may limit strategic options "
                "and reduce gameplay variety"
            )
            suggestions.append(
                "Consider enabling some advanced features to increase strategic depth"
            )
        
        return {"warnings": warnings, "suggestions": suggestions}
    
    def _check_edge_cases(self, rules: EdgeRules) -> Dict[str, List[str]]:
        """Check for potential edge case handling issues."""
        warnings = []
        suggestions = []
        
        # Deck exhaustion with complex rules
        if (rules.deckExhaustion == DeckExhaustionRule.GAME_OVER and 
            rules.hotelMove == HotelMoveRule.FREE_MOVE):
            suggestions.append(
                "Game-over deck exhaustion with free building movement may end games "
                "before players can optimize their property arrangements"
            )
        
        # Floating buildings edge cases
        if rules.buildingForfeiture == BuildingForfeitureRule.KEEP_FLOATING:
            if rules.housePayment != HousePaymentRule.FLOATING:
                warnings.append(
                    "Floating building forfeiture without floating house payments "
                    "creates inconsistent building handling"
                )
            
            if rules.hotelMove == HotelMoveRule.NOT_ALLOWED:
                warnings.append(
                    "Floating buildings with no movement allowed may create "
                    "permanently unusable building cards"
                )
        
        # Property merging edge cases
        if rules.propertyMerging == PropertyMergingRule.AUTO_MERGE:
            if rules.extraProperties == ExtraPropertiesRule.CAP_RENT:
                suggestions.append(
                    "Auto-merging with rent capping may not provide expected benefits - "
                    "consider using split sets for more strategic options"
                )
        
        # Just Say No edge cases
        if rules.justSayNoEmptyHand and rules.justSayNoOnZero:
            suggestions.append(
                "Both Just Say No edge cases enabled may create very defensive gameplay - "
                "monitor for game length impact"
            )
        
        return {"warnings": warnings, "suggestions": suggestions}
    
    def _calculate_performance_impact(self, rules: EdgeRules) -> str:
        """Calculate overall performance impact of rule configuration."""
        impact_score = 0
        
        # High-impact rules (2 points each)
        if rules.extraProperties == ExtraPropertiesRule.SPLIT_SETS:
            impact_score += 2
        if rules.propertyMerging == PropertyMergingRule.AUTO_MERGE:
            impact_score += 2
        
        # Medium-impact rules (1 point each)
        if rules.hotelMove == HotelMoveRule.FREE_MOVE:
            impact_score += 1
        if rules.buildingForfeiture == BuildingForfeitureRule.KEEP_FLOATING:
            impact_score += 1
        if rules.housePayment == HousePaymentRule.FLOATING:
            impact_score += 1
        if rules.quadrupleRent:
            impact_score += 1
        
        # Determine impact level
        if impact_score >= 5:
            return "high"
        elif impact_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _initialize_conflict_rules(self) -> Dict[str, List[Tuple[str, str]]]:
        """Initialize rule conflict detection patterns."""
        return {
            "building_conflicts": [
                ("hotelMove", "buildingForfeiture"),
                ("housePayment", "buildingForfeiture")
            ],
            "property_conflicts": [
                ("extraProperties", "propertyMerging")
            ],
            "action_conflicts": [
                ("quadrupleRent", "forcedDealToDealBreaker"),
                ("justSayNoEmptyHand", "justSayNoOnZero")
            ]
        }
    
    def _initialize_performance_rules(self) -> Dict[str, int]:
        """Initialize performance impact weights for rules."""
        return {
            "extraProperties_split": 2,
            "propertyMerging_auto": 2,
            "hotelMove_free": 1,
            "buildingForfeiture_floating": 1,
            "housePayment_floating": 1,
            "quadrupleRent": 1
        }
    
    def _initialize_balance_suggestions(self) -> Dict[str, str]:
        """Initialize gameplay balance suggestions."""
        return {
            "too_permissive": "Consider adding restrictive rules to maintain balance",
            "too_restrictive": "Consider enabling advanced features for strategic depth",
            "mixed_building_rules": "Ensure building-related rules are consistent",
            "defensive_gameplay": "Monitor for overly defensive gameplay patterns"
        }
    
    def get_rule_compatibility_matrix(self) -> Dict[str, Dict[str, str]]:
        """
        Get compatibility matrix showing how rules interact.
        
        Returns:
            Dictionary mapping rule pairs to compatibility status
        """
        compatibility = {}
        
        # Define rule interactions
        interactions = {
            ("housePayment", "buildingForfeiture"): {
                (HousePaymentRule.FLOATING, BuildingForfeitureRule.DISCARD): "warning",
                (HousePaymentRule.FLOATING, BuildingForfeitureRule.KEEP_FLOATING): "good",
                (HousePaymentRule.BANK, BuildingForfeitureRule.TO_BANK): "good"
            },
            ("hotelMove", "buildingForfeiture"): {
                (HotelMoveRule.FREE_MOVE, BuildingForfeitureRule.KEEP_FLOATING): "warning",
                (HotelMoveRule.NOT_ALLOWED, BuildingForfeitureRule.KEEP_FLOATING): "warning"
            },
            ("extraProperties", "propertyMerging"): {
                (ExtraPropertiesRule.SPLIT_SETS, PropertyMergingRule.AUTO_MERGE): "warning",
                (ExtraPropertiesRule.CAP_RENT, PropertyMergingRule.AUTO_MERGE): "good"
            }
        }
        
        return interactions