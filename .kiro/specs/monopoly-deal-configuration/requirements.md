# Requirements Document

## Introduction

The Monopoly Deal game engine currently has hardcoded rule interpretations for various edge cases that are ambiguous in the official rules. Players need a configuration system that allows them to customize how these edge cases are handled, ensuring the game can accommodate different house rules and interpretations while maintaining consistency within each game session.

## Requirements

### Requirement 1: House/Hotel Payment Handling

**User Story:** As a player, I want to configure how house/hotel cards are handled when received as payment by players without complete property sets, so that the game follows my preferred interpretation of the rules.

#### Acceptance Criteria

1. WHEN a player without a complete property set receives a house/hotel card as payment THEN the system SHALL handle it according to the configured rule
2. IF the rule is set to "bank" THEN the system SHALL place the card in the player's cash pile with its monetary value
3. IF the rule is set to "incomplete_set" THEN the system SHALL allow placement on incomplete sets but not count for rent calculations
4. IF the rule is set to "allocate_later" THEN the system SHALL hold the card for later allocation to a complete set

### Requirement 2: House/Hotel Movement Rules

**User Story:** As a player, I want to configure whether and how house/hotel cards can be moved between property sets, so that the game matches my preferred strategic depth.

#### Acceptance Criteria

1. WHEN a player has multiple complete property sets with houses/hotels THEN the system SHALL enforce the configured movement rule
2. IF movement is "not_allowed" THEN the system SHALL prevent any house/hotel transfers between sets
3. IF movement is "free_before_action" THEN the system SHALL allow movement before any player action without cost
4. IF movement is "costs_action" THEN the system SHALL require one action to move house/hotel cards
5. WHEN movement is allowed THEN the system SHALL update rent calculations accordingly

### Requirement 3: Deck Exhaustion Handling

**User Story:** As a player, I want to configure what happens when the deck runs out of cards, so that the game continues according to my preferred rules.

#### Acceptance Criteria

1. WHEN the deck is exhausted during play THEN the system SHALL follow the configured exhaustion rule
2. IF the rule is "reshuffle" THEN the system SHALL shuffle the discard pile to create a new deck
3. IF the rule is "game_ends" THEN the system SHALL trigger end-game scoring
4. WHEN reshuffling occurs THEN the system SHALL maintain game state consistency

### Requirement 4: Extra Properties Handling

**User Story:** As a player, I want to configure how extra property cards beyond the complete set requirement are handled, so that wildcards and additional properties work as expected.

#### Acceptance Criteria

1. WHEN a player has more property cards than needed for a complete set THEN the system SHALL apply the configured handling rule
2. IF the rule is "single_set" THEN the system SHALL treat all cards as one oversized set with capped rent
3. IF the rule is "multiple_sets" THEN the system SHALL allow separate complete and incomplete sets
4. IF the rule is "cap_rent" THEN the system SHALL limit rent to the maximum for that color regardless of extra cards
5. WHEN multiple sets are allowed THEN the system SHALL handle rent collection and vulnerability separately

### Requirement 5: Property Set Merging Rules

**User Story:** As a player, I want to configure whether separate property sets of the same color can be merged, so that wildcard management follows consistent rules.

#### Acceptance Criteria

1. WHEN a player has separate property sets of the same color THEN the system SHALL apply the merging configuration
2. IF merging is enabled THEN the system SHALL automatically combine matching color sets when beneficial
3. IF merging is disabled THEN the system SHALL maintain separate sets even of the same color
4. WHEN wildcard reallocation occurs THEN the system SHALL respect the merging rules

### Requirement 6: Building Forfeiture Rules

**User Story:** As a player, I want to configure what happens to house/hotel cards when their property set becomes incomplete, so that the consequences are clear and consistent.

#### Acceptance Criteria

1. WHEN a complete property set with buildings becomes incomplete THEN the system SHALL apply the forfeiture rule
2. IF the rule is "discard" THEN the system SHALL move buildings to the discard pile
3. IF the rule is "to_bank" THEN the system SHALL move buildings to the player's bank at cash value
4. WHEN forfeiture occurs THEN the system SHALL update all affected calculations

### Requirement 7: Advanced Action Combinations

**User Story:** As a player, I want to configure whether advanced action combinations are allowed, so that complex strategies can be enabled or disabled.

#### Acceptance Criteria

1. WHEN multiple "Double the Rent" cards are played THEN the system SHALL check if quadruple rent is enabled
2. IF quadruple rent is disabled THEN the system SHALL limit to one "Double the Rent" card per rent action
3. IF quadruple rent is enabled THEN the system SHALL allow up to two cards for 4x rent multiplier
4. WHEN "Forced Deal" + "Deal Breaker" combinations are attempted THEN the system SHALL apply the configured rule

### Requirement 8: "Just Say No" Edge Cases

**User Story:** As a player, I want to configure when "Just Say No" cards can be played, including edge cases with empty hands and zero-cost actions.

#### Acceptance Criteria

1. WHEN a "Just Say No" is played against a zero-cost action THEN the system SHALL check the configuration
2. IF "just_say_no_on_zero" is enabled THEN the system SHALL allow blocking zero-cost actions
3. IF "just_say_no_empty_hand" is enabled THEN the system SHALL allow playing from empty hands to trigger card draw
4. WHEN these edge cases occur THEN the system SHALL maintain game flow consistency

### Requirement 9: Configuration Management Interface

**User Story:** As a player, I want an intuitive interface to view and modify game configuration settings, so that I can easily customize the game rules before starting.

#### Acceptance Criteria

1. WHEN accessing the configuration interface THEN the system SHALL display all available rule options
2. WHEN a rule option is changed THEN the system SHALL provide clear explanations of the implications
3. WHEN configuration is saved THEN the system SHALL validate all settings for consistency
4. WHEN starting a new game THEN the system SHALL apply the saved configuration settings

### Requirement 10: Configuration Presets

**User Story:** As a player, I want to save and load configuration presets, so that I can quickly switch between different rule interpretations for different groups.

#### Acceptance Criteria

1. WHEN creating a configuration preset THEN the system SHALL save all current settings with a custom name
2. WHEN loading a preset THEN the system SHALL apply all saved settings at once
3. WHEN sharing presets THEN the system SHALL provide export/import functionality
4. WHEN conflicts exist between presets THEN the system SHALL highlight differences clearly