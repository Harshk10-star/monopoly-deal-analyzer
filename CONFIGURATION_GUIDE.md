# Monopoly Deal Edge Case Configuration System

This system provides comprehensive configuration options for handling the edge cases and rule ambiguities in Monopoly Deal that the official rules don't clearly address.

## Overview

The configuration system allows users to:
- Choose from predefined rule presets
- Create custom rule configurations
- Validate rule combinations for consistency
- Export/import configurations
- Apply configurations to AI analysis

## Edge Cases Covered

### 1. House/Hotel Payment Rules (`housePayment`)
**The Problem**: If a player without a complete property set receives a house or hotel as incoming payment, where does it go?

**Options**:
- `bank`: Card goes to the cash pile, losing its special property-card handling (Conservative)
- `incomplete_set`: Card can be placed on an incomplete property set, but doesn't count for rent until completed
- `floating`: Card is placed as property but not in a specific set, can be allocated later to a complete set

### 2. Building Movement Rules (`hotelMove`)
**The Problem**: Can players move house/hotel cards between property sets? When and at what cost?

**Options**:
- `not_allowed`: Buildings cannot be moved once played (Strict)
- `free_move`: Buildings can be moved freely between complete sets before any action
- `costs_action`: Moving buildings costs one action

### 3. Deck Exhaustion Rules (`deckExhaustion`)
**The Problem**: What happens when the deck runs out during play?

**Options**:
- `reshuffle`: Discard pile gets shuffled to become the new deck
- `game_over`: Game ends immediately

### 4. Extra Properties Rules (`extraProperties`)
**The Problem**: How to handle holding more property cards of a color than needed for a complete set?

**Options**:
- `cap`: One property set with extra cards, rent capped at maximum value
- `split`: Multiple property sets, incomplete sets vulnerable to actions

### 5. Building Forfeiture Rules (`buildingForfeiture`)
**The Problem**: What happens to house/hotel cards when their property set becomes incomplete?

**Options**:
- `discard`: Buildings are discarded to the discard pile
- `to_bank`: Buildings return to the player's bank
- `keep_floating`: Buildings remain as floating property cards

### 6. Property Merging Rules (`propertyMerging`)
**The Problem**: Can separate property sets of the same color be merged?

**Options**:
- `auto_merge`: Automatically merge same-color sets
- `manual_merge`: Allow manual merging as a player choice
- `no_merge`: No merging allowed once sets are separate

### 7. Advanced Action Rules

#### Quadruple Rent (`quadrupleRent`)
**The Problem**: Can two "Double the Rent" cards be played simultaneously?
- `true`: Allows 4x rent (uses all 3 actions)
- `false`: Only one DTR card per rent action

#### Forced Deal → Deal Breaker Combo (`forcedDealToDealBreaker`)
**The Problem**: Can Forced Deal be used to set up Deal Breaker combos?
- `true`: Allows using Forced Deal to complete opponent sets for Deal Breaker
- `false`: Prevents this strategic combination

#### Just Say No from Empty Hand (`justSayNoEmptyHand`)
**The Problem**: Can "Just Say No" be played from an empty hand to trigger card draw?
- `true`: Allows playing JSN from empty hand
- `false`: Requires cards in hand to play JSN

#### Just Say No on Zero-Cost Actions (`justSayNoOnZero`)
**The Problem**: Can "Just Say No" block actions that cost the player nothing?
- `true`: JSN can block any action
- `false`: JSN cannot block zero-cost actions

## Predefined Presets

### Strict Official Rules
Conservative interpretation following official rules closely:
- House payment: Bank
- Hotel movement: Not allowed
- Building forfeiture: Discard
- Advanced combos: Disabled

### Flexible House Rules
Permissive rules allowing advanced strategies:
- House payment: Floating
- Hotel movement: Costs action
- Building forfeiture: To bank
- Advanced combos: Enabled

### Balanced Competitive
Tournament-style rules balancing strategy and flow:
- House payment: Incomplete set
- Hotel movement: Costs action
- Building forfeiture: To bank
- Some advanced combos enabled

### Defensive Play Style
Rules favoring defensive strategies:
- House payment: Bank
- Hotel movement: Not allowed
- Building forfeiture: Keep floating
- Defensive options enabled

## Using the Configuration System

### In the UI
1. Go to the "Rules" tab in the Dashboard
2. Select a preset or customize individual rules
3. View validation warnings and suggestions
4. Apply configuration to affect AI analysis
5. Save custom presets for reuse

### API Endpoints
- `GET /api/v1/configuration/presets` - List all presets
- `POST /api/v1/configuration/validate` - Validate rule combinations
- `POST /api/v1/configuration/presets` - Create custom preset
- `GET /api/v1/configuration/export/{preset_id}` - Export configuration

### Validation System
The system automatically validates rule combinations and provides:
- **Errors**: Logically impossible combinations
- **Warnings**: Potentially problematic interactions
- **Suggestions**: Recommendations for better balance
- **Performance Impact**: Computational complexity assessment

## Impact on AI Analysis

The AI analysis engine uses your configuration to:
- Determine valid moves based on your rules
- Calculate win probabilities under your rule set
- Provide recommendations that respect your edge case handling
- Simulate games with consistent rule application

## Best Practices

1. **Start with a preset** that matches your play style
2. **Test configurations** with the validation system
3. **Consider performance impact** for complex rule combinations
4. **Document custom rules** when sharing with other players
5. **Use consistent rules** within your gaming group

## Technical Implementation

The configuration system is built with:
- **Pydantic models** for type-safe rule definitions
- **Validation engine** for consistency checking
- **Database storage** for custom presets
- **React components** for user-friendly configuration
- **API integration** with the game analysis engine

This ensures that your edge case preferences are consistently applied across all game analysis and recommendations.