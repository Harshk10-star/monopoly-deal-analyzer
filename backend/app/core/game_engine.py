"""
Monopoly Deal Game Engine
Handles game logic, analysis, and AI recommendations with comprehensive rule validation
Based on research: "Implementation of Artificial Intelligence with 3 Different Characters of AI Player on Monopoly Deal Computer Game"
"""

from typing import Dict, List, Any, Tuple, Optional
from app.models.game import GameState, AnalysisResponse, AIStrategy
from enum import Enum
import random


class PlayerCharacter(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    NORMAL = "normal"


class AssetEvaluation(Enum):
    LOGICAL = "logical"
    VALUE = "value"
    LOGICAL_VALUE = "logical_value"


class GamePhase(Enum):
    EARLY = "early"
    MIDDLE = "middle"
    LATE = "late"


class MonopolyDealEngine:
    """
    Main game engine for Monopoly Deal analysis and AI recommendations
    Implements BFS algorithm with 3 character types and asset evaluation methods
    """
    
    def __init__(self, edge_rules=None):
        self.edge_rules = edge_rules
        self.property_values = {
            'brown': 1, 'light-blue': 1, 'pink': 2, 'orange': 2,
            'red': 3, 'yellow': 3, 'green': 4, 'dark-blue': 4,
            'railroad': 2, 'utility': 2
        }
        
        self.complete_sets = {
            'brown': 2, 'light-blue': 3, 'pink': 3, 'orange': 3,
            'red': 3, 'yellow': 3, 'green': 3, 'dark-blue': 2,
            'railroad': 4, 'utility': 2
        }
        
        # Rent values for complete sets
        self.rent_values = {
            'brown': [1, 2], 'light-blue': [1, 2, 3], 'pink': [1, 2, 4], 
            'orange': [1, 3, 5], 'red': [2, 3, 6], 'yellow': [2, 4, 6],
            'green': [2, 4, 7], 'dark-blue': [3, 8], 'railroad': [1, 2, 3, 4],
            'utility': [1, 2]
        }
        
        # Action card effects and values
        self.action_cards = {
            'deal_breaker': {'cost': 5, 'effect': 'steal_complete_set', 'value': 5},
            'sly_deal': {'cost': 3, 'effect': 'steal_property', 'value': 3},
            'force_deal': {'cost': 3, 'effect': 'swap_property', 'value': 3},
            'debt_collector': {'cost': 3, 'effect': 'collect_5m', 'value': 3},
            'birthday': {'cost': 2, 'effect': 'collect_2m_all', 'value': 2},
            'just_say_no': {'cost': 4, 'effect': 'block_action', 'value': 4},
            'pass_go': {'cost': 1, 'effect': 'draw_2_cards', 'value': 1},
            'house': {'cost': 3, 'effect': 'add_rent_1', 'value': 3},
            'hotel': {'cost': 4, 'effect': 'add_rent_3', 'value': 4},
            'double_rent': {'cost': 1, 'effect': 'double_rent', 'value': 1}
        }
        
        # Character-specific multipliers based on research findings
        self.character_multipliers = {
            PlayerCharacter.AGGRESSIVE: {
                'property_acquisition': 1.5,
                'action_card_usage': 1.8,
                'risk_tolerance': 2.0,
                'money_hoarding': 0.7
            },
            PlayerCharacter.DEFENSIVE: {
                'property_acquisition': 1.0,
                'action_card_usage': 0.8,
                'risk_tolerance': 0.5,
                'money_hoarding': 1.5
            },
            PlayerCharacter.NORMAL: {
                'property_acquisition': 1.2,
                'action_card_usage': 1.0,
                'risk_tolerance': 1.0,
                'money_hoarding': 1.0
            }
        }
    
    def calculate_game_phase(self, game_state: GameState) -> GamePhase:
        """Calculate current game phase based on research formula"""
        total_cards = 106  # Standard Monopoly Deal deck
        cards_dealt_beginning = len(game_state.players) * 5
        cards_in_play = sum(len(player.hand) + len(player.bank) + 
                           sum(len(props) for props in player.properties.values()) 
                           for player in game_state.players)
        
        # Estimate cycles based on cards dealt
        cycles = (total_cards - cards_dealt_beginning - cards_in_play) // (2 * len(game_state.players))
        
        if cycles <= 3:
            return GamePhase.EARLY
        elif cycles <= 8:
            return GamePhase.MIDDLE
        else:
            return GamePhase.LATE
    
    def evaluate_assets_logical(self, player_data: dict) -> float:
        """Logical asset evaluation - focuses on property set completion"""
        try:
            score = 0.0
            
            # Property set completion score
            properties = player_data.get('properties', {})
            if isinstance(properties, dict):
                for color, property_list in properties.items():
                    if color in self.complete_sets and isinstance(property_list, list):
                        completion_ratio = len(property_list) / self.complete_sets[color]
                        if completion_ratio >= 1.0:
                            score += 50  # Complete set bonus
                        else:
                            score += completion_ratio * 30  # Partial completion
            
            # Money for protection
            bank_cards = player_data.get('bank', [])
            money_value = 0
            if isinstance(bank_cards, list):
                for card in bank_cards:
                    if isinstance(card, dict):
                        money_value += card.get('value', 0)
                    elif isinstance(card, (int, float)):
                        money_value += card
            
            score += min(money_value * 2, 20)  # Cap money contribution
            
            return max(0.0, score)  # Ensure non-negative score
            
        except Exception as e:
            print(f"Error in evaluate_assets_logical: {e}")
            return 10.0  # Default score
    
    def evaluate_assets_value(self, player_data: dict) -> float:
        """Value asset evaluation - focuses on monetary worth"""
        try:
            score = 0.0
            
            # Direct money value
            bank_cards = player_data.get('bank', [])
            money_value = 0
            if isinstance(bank_cards, list):
                for card in bank_cards:
                    if isinstance(card, dict):
                        money_value += card.get('value', 0)
                    elif isinstance(card, (int, float)):
                        money_value += card
            score += money_value * 3
            
            # Property monetary value
            properties = player_data.get('properties', {})
            if isinstance(properties, dict):
                for color, property_list in properties.items():
                    if color in self.property_values and isinstance(property_list, list):
                        score += len(property_list) * self.property_values[color] * 2
            
            # Action cards value
            hand_cards = player_data.get('hand', [])
            if isinstance(hand_cards, list):
                for card in hand_cards:
                    if isinstance(card, dict):
                        card_type = card.get('type', '')
                        card_name = card.get('name', '')
                        if card_type == 'action' and card_name in self.action_cards:
                            score += self.action_cards[card_name]['value']
            
            return max(0.0, score)  # Ensure non-negative score
            
        except Exception as e:
            print(f"Error in evaluate_assets_value: {e}")
            return 15.0  # Default score
    
    def evaluate_assets_logical_value(self, player_data: dict) -> float:
        """Combined logical-value asset evaluation"""
        logical_score = self.evaluate_assets_logical(player_data)
        value_score = self.evaluate_assets_value(player_data)
        return (logical_score + value_score) / 2
    
    def bfs_decision_tree(self, game_state: GameState, character: PlayerCharacter, 
                         asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """
        BFS implementation for decision making as described in research paper
        Returns prioritized list of possible moves
        """
        current_player = game_state.players[0]  # Assume first player is current
        moves = []
        
        # Level 1: Analyze each card in hand
        for card in current_player.hand:
            move_options = self._analyze_card_bfs(card, game_state, character, asset_type)
            moves.extend(move_options)
        
        # Level 2: Analyze combinations and strategic plays
        strategic_moves = self._analyze_strategic_combinations(game_state, character, asset_type)
        moves.extend(strategic_moves)
        
        # Sort moves by priority score
        moves.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
        
        return moves[:5]  # Return top 5 moves
    
    def _analyze_card_bfs(self, card, game_state: GameState, 
                         character: PlayerCharacter, asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """Analyze individual card using BFS approach"""
        moves = []
        
        # Handle both string and dict card formats
        if isinstance(card, str):
            card_name = card
            # Infer card type from name
            if 'Property' in card_name:
                card_type = 'property'
            elif any(money in card_name for money in ['$1M', '$2M', '$3M', '$4M', '$5M', '$10M']):
                card_type = 'money'
            else:
                card_type = 'action'
            
            # Convert to dict format
            card_dict = {'name': card_name, 'type': card_type}
        else:
            card_dict = card
            card_type = card_dict.get('type', '')
        
        if card_type == 'money':
            moves.append({
                'action': 'play_money',
                'card': card_dict,
                'priority_score': self._calculate_money_priority(card_dict, character, asset_type),
                'reasoning': f"Play {card_dict.get('name', 'money card')} to bank for security"
            })
        
        elif card_type == 'property':
            moves.append({
                'action': 'play_property',
                'card': card_dict,
                'priority_score': self._calculate_property_priority(card_dict, game_state, character, asset_type),
                'reasoning': f"Play {card_dict.get('name', 'property')} to build set"
            })
        
        elif card_type == 'action':
            action_moves = self._analyze_action_card(card_dict, game_state, character, asset_type)
            moves.extend(action_moves)
        
        return moves
    
    def _analyze_action_card(self, card: dict, game_state: GameState, 
                           character: PlayerCharacter, asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """Analyze action cards for optimal play"""
        moves = []
        card_name = card.get('name', '').lower()
        current_player = game_state.players[0]
        opponents = game_state.players[1:]
        
        # Handle "It's My Birthday" card
        if "it's my birthday" in card_name or "birthday" in card_name:
            if opponents:
                total_potential = sum(len(getattr(opp, 'bank', [])) for opp in opponents)
                if total_potential > 0:
                    moves.append({
                        'action': 'play_birthday',
                        'card': card,
                        'priority_score': total_potential * 15 * self.character_multipliers[character]['action_card_usage'],
                        'reasoning': f"Use It's My Birthday to collect 2M from each opponent"
                    })
        
        # Handle rent cards
        elif 'rent' in card_name:
            # Only suggest if player has properties to charge rent for
            if current_player.properties and opponents:
                best_property_set = max(current_player.properties.items(), 
                                      key=lambda x: len(x[1]) if x[0] in self.rent_values else 0)
                if best_property_set[0] in self.rent_values:
                    rent_value = self.rent_values[best_property_set[0]][min(len(best_property_set[1]) - 1, 
                                                                          len(self.rent_values[best_property_set[0]]) - 1)]
                    moves.append({
                        'action': 'play_rent',
                        'card': card,
                        'property_set': best_property_set[0],
                        'rent_value': rent_value,
                        'priority_score': rent_value * 12 * self.character_multipliers[character]['action_card_usage'],
                        'reasoning': f"Use rent card to collect {rent_value}M from {best_property_set[0]} properties"
                    })
        
        # Handle other action cards (Deal Breaker, Sly Deal, etc.)
        elif 'deal breaker' in card_name and character == PlayerCharacter.AGGRESSIVE:
            # Find best complete set to steal
            for opponent in opponents:
                for color, props in getattr(opponent, 'properties', {}).items():
                    if color in self.complete_sets and len(props) >= self.complete_sets[color]:
                        moves.append({
                            'action': 'play_deal_breaker',
                            'card': card,
                            'target_set': color,
                            'priority_score': 50 * self.character_multipliers[character]['action_card_usage'],
                            'reasoning': f"Use Deal Breaker to steal complete {color} set"
                        })
                        break
        
        return moves
    
    def _calculate_money_priority(self, card: dict, character: PlayerCharacter, 
                                asset_type: AssetEvaluation) -> float:
        """Calculate priority for playing money cards"""
        # Extract value from card name if not provided
        base_value = card.get('value', 1)
        if base_value == 1:  # Default value, try to extract from name
            card_name = card.get('name', '')
            if '$1M' in card_name:
                base_value = 1
            elif '$2M' in card_name:
                base_value = 2
            elif '$3M' in card_name:
                base_value = 3
            elif '$4M' in card_name:
                base_value = 4
            elif '$5M' in card_name:
                base_value = 5
            elif '$10M' in card_name:
                base_value = 10
        
        multiplier = self.character_multipliers[character]['money_hoarding']
        
        if asset_type == AssetEvaluation.VALUE:
            return base_value * multiplier * 1.5
        elif asset_type == AssetEvaluation.LOGICAL:
            return base_value * multiplier * 0.8
        else:  # LOGICAL_VALUE
            return base_value * multiplier * 1.2
    
    def _calculate_property_priority(self, card: dict, game_state: GameState, 
                                   character: PlayerCharacter, asset_type: AssetEvaluation) -> float:
        """Calculate priority for playing property cards"""
        current_player = game_state.players[0]
        
        # Extract color from card name if not provided
        color = card.get('color', '')
        if not color:
            card_name = card.get('name', '')
            # Map card names to colors
            color_mapping = {
                'Brown Property': 'brown',
                'Light Blue Property': 'light-blue', 
                'Pink Property': 'pink',
                'Orange Property': 'orange',
                'Red Property': 'red',
                'Yellow Property': 'yellow',
                'Green Property': 'green',
                'Dark Blue Property': 'dark-blue',
                'Railroad Property': 'railroad',
                'Utility Property': 'utility'
            }
            color = color_mapping.get(card_name, 'unknown')
        
        if color not in self.complete_sets:
            return 10.0
        
        # Check current progress toward complete set
        current_count = len(current_player.properties.get(color, []))
        needed_for_complete = self.complete_sets[color]
        completion_ratio = current_count / needed_for_complete
        
        base_priority = 20 + (completion_ratio * 30)
        
        # Apply character multiplier
        multiplier = self.character_multipliers[character]['property_acquisition']
        
        if asset_type == AssetEvaluation.LOGICAL:
            # Logical prioritizes set completion
            if completion_ratio >= 0.66:  # Close to completion
                base_priority *= 2.0
        elif asset_type == AssetEvaluation.VALUE:
            # Value prioritizes high-value properties
            property_value = self.property_values.get(color, 1)
            base_priority += property_value * 5
        
        return base_priority * multiplier
    
    def _analyze_action_card(self, card: dict, game_state: GameState, 
                           character: PlayerCharacter, asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """Analyze action card usage options"""
        moves = []
        card_name = card.get('name', '').lower().replace(' ', '_')
        
        # Map common action card names
        action_name_mapping = {
            'deal_breaker': 'deal_breaker',
            'sly_deal': 'sly_deal', 
            'force_deal': 'force_deal',
            'debt_collector': 'debt_collector',
            'its_my_birthday': 'birthday',
            'just_say_no': 'just_say_no',
            'pass_go': 'pass_go',
            'house': 'house',
            'hotel': 'hotel',
            'double_the_rent': 'double_rent'
        }
        
        mapped_name = action_name_mapping.get(card_name, card_name)
        
        if mapped_name in self.action_cards:
            action_info = self.action_cards[mapped_name]
            base_priority = action_info['value'] * 10
            
            # Apply character-specific action usage multiplier
            multiplier = self.character_multipliers[character]['action_card_usage']
            priority = base_priority * multiplier
            
            moves.append({
                'action': 'play_action',
                'card': card,
                'priority_score': priority,
                'reasoning': f"Use {card.get('name', 'action card')} for {action_info['effect']}"
            })
        
        return moves
    
    def _analyze_strategic_combinations(self, game_state: GameState, 
                                      character: PlayerCharacter, asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """Analyze strategic combinations and advanced plays"""
        moves = []
        current_player = game_state.players[0]
        
        # Check for rent collection opportunities
        rent_moves = self._analyze_rent_opportunities(game_state, character, asset_type)
        moves.extend(rent_moves)
        
        # Check for deal breaker opportunities (aggressive character)
        if character == PlayerCharacter.AGGRESSIVE:
            deal_breaker_moves = self._analyze_deal_breaker_opportunities(game_state, asset_type)
            moves.extend(deal_breaker_moves)
        
        return moves
    
    def _analyze_rent_opportunities(self, game_state: GameState, 
                                  character: PlayerCharacter, asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """Analyze rent collection opportunities"""
        moves = []
        current_player = game_state.players[0]
        
        # Only suggest rent collection if player has rent cards in hand
        has_rent_card = any('rent' in str(card).lower() for card in current_player.hand)
        if not has_rent_card:
            return moves
        
        # Check each property set for rent potential
        for color, properties in current_player.properties.items():
            if len(properties) > 0 and color in self.rent_values:
                rent_value = self.rent_values[color][min(len(properties) - 1, len(self.rent_values[color]) - 1)]
                
                # Calculate target selection based on character
                target_priority = self._calculate_rent_target_priority(game_state.players[1:], character)
                
                if target_priority > 0:
                    moves.append({
                        'action': 'collect_rent',
                        'property_set': color,
                        'rent_value': rent_value,
                        'priority_score': rent_value * 8 * self.character_multipliers[character]['action_card_usage'],
                        'reasoning': f"Use rent card to collect {rent_value}M from {color} properties"
                    })
        
        return moves
    
    def _analyze_deal_breaker_opportunities(self, game_state: GameState, 
                                          asset_type: AssetEvaluation) -> List[Dict[str, Any]]:
        """Analyze deal breaker opportunities for aggressive players"""
        moves = []
        
        # Check if any opponent has complete sets worth stealing
        for opponent in game_state.players[1:]:
            for color, properties in opponent.properties.items():
                if color in self.complete_sets and len(properties) >= self.complete_sets[color]:
                    set_value = len(properties) * self.property_values.get(color, 1)
                    
                    moves.append({
                        'action': 'deal_breaker',
                        'target_player': opponent.name,
                        'target_set': color,
                        'priority_score': set_value * 15,  # High priority for complete sets
                        'reasoning': f"Steal complete {color} set from {opponent.name}"
                    })
        
        return moves
    
    def _calculate_rent_target_priority(self, opponents: List, character: PlayerCharacter) -> float:
        """Calculate priority for rent collection targets"""
        if not opponents:
            return 0.0
        
        # Aggressive: Target richest player
        if character == PlayerCharacter.AGGRESSIVE:
            max_wealth = max(self._calculate_player_wealth(opp) for opp in opponents)
            return max_wealth
        
        # Defensive: Target based on threat level
        elif character == PlayerCharacter.DEFENSIVE:
            min_threat = min(self._calculate_threat_level(opp) for opp in opponents)
            return min_threat
        
        # Normal: Balanced approach
        else:
            avg_wealth = sum(self._calculate_player_wealth(opp) for opp in opponents) / len(opponents)
            return avg_wealth
    
    def _calculate_player_wealth(self, player) -> float:
        """Calculate total wealth of a player"""
        bank = getattr(player, 'bank', [])
        # Handle both integer values and card objects in bank
        money_value = 0
        for item in bank:
            if isinstance(item, int):
                money_value += item
            elif isinstance(item, dict):
                money_value += item.get('value', 0)
            else:
                # Assume it's a card object with value attribute
                money_value += getattr(item, 'value', 0)
        
        property_value = sum(
            len(props) * self.property_values.get(color, 1)
            for color, props in getattr(player, 'properties', {}).items()
        )
        return money_value + property_value
    
    def _calculate_threat_level(self, player) -> float:
        """Calculate threat level of a player"""
        complete_sets = sum(
            1 for color, props in getattr(player, 'properties', {}).items()
            if color in self.complete_sets and len(props) >= self.complete_sets[color]
        )
        return complete_sets * 20 + self._calculate_player_wealth(player)

    def analyze_game_state(self, game_state: GameState, strategy: AIStrategy) -> AnalysisResponse:
        """
        Analyze game state using research-based BFS algorithm with character types
        Based on "Implementation of Artificial Intelligence with 3 Different Characters"
        """
        try:
            # Map strategy to character and asset type (based on research findings)
            character_mapping = {
                'aggressive': (PlayerCharacter.AGGRESSIVE, AssetEvaluation.LOGICAL),  # 45% win rate
                'defensive': (PlayerCharacter.DEFENSIVE, AssetEvaluation.VALUE),     # 35% win rate  
                'normal': (PlayerCharacter.NORMAL, AssetEvaluation.LOGICAL),         # 40% win rate
                'balanced': (PlayerCharacter.NORMAL, AssetEvaluation.LOGICAL_VALUE)  # Fallback
            }
            
            strategy_key = strategy.value if hasattr(strategy, 'value') else str(strategy).lower()
            character, asset_type = character_mapping.get(strategy_key, 
                                                        (PlayerCharacter.NORMAL, AssetEvaluation.LOGICAL_VALUE))
            
            # Calculate current game phase
            game_phase = self.calculate_game_phase(game_state)
            
            # Get current player
            current_player = game_state.players[0] if game_state.players else None
            if not current_player:
                return AnalysisResponse(
                    recommendedMove="No players found in game state",
                    reasoning="Invalid game state - no players detected",
                    strongestPlayer="Unknown",
                    winProbability={}
                )
            
            # Use BFS decision tree to get recommended moves
            possible_moves = self.bfs_decision_tree(game_state, character, asset_type)
            
            # Analyze each player using appropriate asset evaluation
            player_evaluations = {}
            complete_sets_count = {}
            
            for player in game_state.players:
                # Convert bank integers to card-like objects for consistency
                bank_cards = []
                if player.bank:
                    for val in player.bank:
                        if isinstance(val, int):
                            bank_cards.append({'value': val})
                        elif isinstance(val, dict) and 'value' in val:
                            bank_cards.append(val)
                        else:
                            # Handle string or other formats
                            try:
                                bank_cards.append({'value': int(val)})
                            except (ValueError, TypeError):
                                bank_cards.append({'value': 1})  # Default value
                
                # Convert hand items to consistent format
                hand_cards = []
                if hasattr(player, 'hand') and player.hand:
                    for card in player.hand:
                        if isinstance(card, dict):
                            hand_cards.append(card)
                        elif isinstance(card, str):
                            # Convert string card names to basic card objects
                            hand_cards.append({'name': card, 'type': 'unknown'})
                        else:
                            hand_cards.append({'name': str(card), 'type': 'unknown'})
                
                player_data = {
                    'properties': player.properties or {},
                    'bank': bank_cards,
                    'hand': hand_cards
                }
                
                # Use research-based asset evaluation
                if asset_type == AssetEvaluation.LOGICAL:
                    score = self.evaluate_assets_logical(player_data)
                elif asset_type == AssetEvaluation.VALUE:
                    score = self.evaluate_assets_value(player_data)
                else:  # LOGICAL_VALUE
                    score = self.evaluate_assets_logical_value(player_data)
                
                player_evaluations[player.name] = score
                
                # Count complete sets
                sets_completed = sum(
                    1 for color, props in (player.properties or {}).items()
                    if color in self.complete_sets and len(props) >= self.complete_sets[color]
                )
                complete_sets_count[player.name] = sets_completed
            
            # Determine strongest player
            strongest_player = max(player_evaluations.keys(), 
                                 key=lambda x: player_evaluations[x]) if player_evaluations else "Unknown"
            
            # Calculate win probabilities based on research methodology
            win_probabilities = self._calculate_research_based_probabilities(
                player_evaluations, complete_sets_count, character, game_phase
            )
            
            # Generate recommendation from BFS results
            if possible_moves:
                best_move = possible_moves[0]
                recommendation = f"{best_move['action']}: {best_move.get('reasoning', 'Execute optimal move')}"
                reasoning = self._generate_research_based_reasoning(
                    best_move, character, asset_type, game_phase, possible_moves[:3]
                )
            else:
                recommendation = "Draw cards and assess hand"
                reasoning = f"No optimal moves found. Focus on {asset_type.value} asset building in {game_phase.value} game phase."
            
            return AnalysisResponse(
                recommendedMove=recommendation,
                reasoning=reasoning,
                strongestPlayer=strongest_player,
                winProbability=win_probabilities
            )
            
        except Exception as e:
            print(f"Analysis error: {e}")
            import traceback
            traceback.print_exc()
            return AnalysisResponse(
                recommendedMove="Unable to analyze game state",
                reasoning=f"Analysis error: {str(e)}",
                strongestPlayer="Unknown",
                winProbability={}
            )
    
    def _generate_recommendation(self, player, game_state: GameState, strategy: AIStrategy, complete_sets: Dict) -> str:
        """Generate move recommendation based on current game state"""
        
        # Check if player is close to winning
        player_sets = complete_sets.get(player.name, 0)
        if player_sets >= 2:
            return "You're close to winning! Focus on completing your third property set or use action cards to disrupt opponents."
        
        # Analyze hand for immediate plays
        hand_cards = player.hand or []
        action_cards = [card for card in hand_cards if any(action in str(card).lower() for action in ['deal breaker', 'sly deal', 'force deal', 'rent'])]
        
        if action_cards:
            return f"Play action cards from your hand: {', '.join(action_cards[:2])}. Focus on disrupting the strongest opponent."
        
        # Property building recommendations
        properties = player.properties or {}
        incomplete_sets = []
        
        for color, props in properties.items():
            required = self.complete_sets.get(color, 3)
            if len(props) < required:
                incomplete_sets.append(f"{color} ({len(props)}/{required})")
        
        if incomplete_sets:
            return f"Focus on completing property sets: {', '.join(incomplete_sets[:2])}. Draw cards or trade to complete sets."
        
        # Default recommendations based on strategy
        if strategy == AIStrategy.AGGRESSIVE:
            return "Play aggressively - use action cards to steal properties and disrupt opponents' sets."
        elif strategy == AIStrategy.DEFENSIVE:
            return "Build your property sets defensively and save Just Say No cards for protection."
        else:
            return "Balance building your properties with strategic action card plays. Draw cards when possible."
    
    def _generate_reasoning(self, player, game_state: GameState, scores: Dict, complete_sets: Dict) -> str:
        """Generate reasoning for the recommendation"""
        
        player_score = scores.get(player.name, 0)
        max_score = max(scores.values()) if scores else 0
        
        reasoning_parts = []
        
        # Position analysis
        if player_score >= max_score:
            reasoning_parts.append("You're currently in the lead.")
        else:
            reasoning_parts.append("You're behind the leader.")
        
        # Set completion analysis
        player_sets = complete_sets.get(player.name, 0)
        max_sets = max(complete_sets.values()) if complete_sets else 0
        
        if player_sets >= 2:
            reasoning_parts.append("You have 2+ complete sets - victory is within reach!")
        elif max_sets >= 2:
            reasoning_parts.append("An opponent has 2+ complete sets - you need to act quickly!")
        else:
            reasoning_parts.append("Focus on building complete property sets to gain advantage.")
        
        # Hand analysis
        hand_size = len(player.hand) if player.hand else 0
        if hand_size > 7:
            reasoning_parts.append("You have many cards - consider playing action cards or building properties.")
        elif hand_size < 3:
            reasoning_parts.append("Your hand is small - focus on drawing more cards.")
        
        return " ".join(reasoning_parts)
    
    def simulate_game(self, game_state: GameState, strategy: AIStrategy, num_simulations: int) -> List[AnalysisResponse]:
        """
        Run multiple game simulations (simplified implementation)
        """
        results = []
        
        for _ in range(min(num_simulations, 10)):  # Limit simulations for performance
            # Create a variation of the analysis with some randomness
            analysis = self.analyze_game_state(game_state, strategy)
            
            # Add some randomness to win probabilities for simulation variety
            varied_probs = {}
            for player, prob in analysis.winProbability.items():
                variation = random.uniform(-0.1, 0.1)
                varied_probs[player] = max(0.0, min(1.0, prob + variation))
            
            # Normalize
            total = sum(varied_probs.values())
            if total > 0:
                varied_probs = {name: prob/total for name, prob in varied_probs.items()}
            
            varied_analysis = AnalysisResponse(
                recommendedMove=analysis.recommendedMove,
                reasoning=analysis.reasoning,
                strongestPlayer=analysis.strongestPlayer,
                winProbability=varied_probs
            )
            
            results.append(varied_analysis)
        
        return results
    
    def _calculate_research_based_probabilities(self, player_evaluations: Dict[str, float], 
                                              complete_sets_count: Dict[str, int],
                                              character: PlayerCharacter, 
                                              game_phase: GamePhase) -> Dict[str, float]:
        """Calculate win probabilities based on research methodology"""
        win_probabilities = {}
        total_evaluation = sum(player_evaluations.values()) if player_evaluations else 1
        
        for player_name, evaluation in player_evaluations.items():
            # Base probability from evaluation score
            base_prob = evaluation / total_evaluation if total_evaluation > 0 else 0
            
            # Complete sets bonus (critical factor in Monopoly Deal)
            sets_completed = complete_sets_count.get(player_name, 0)
            sets_bonus = sets_completed * 0.25  # 25% bonus per complete set
            
            # Game phase adjustment
            phase_multiplier = {
                GamePhase.EARLY: 0.8,   # Less predictable early game
                GamePhase.MIDDLE: 1.0,  # Standard calculation
                GamePhase.LATE: 1.2     # More decisive late game
            }.get(game_phase, 1.0)
            
            # Character-specific risk adjustment
            risk_factor = self.character_multipliers[character]['risk_tolerance']
            
            final_prob = (base_prob + sets_bonus) * phase_multiplier * risk_factor
            win_probabilities[player_name] = min(0.95, max(0.05, final_prob))
        
        # Normalize probabilities to sum to 1.0
        total_prob = sum(win_probabilities.values())
        if total_prob > 0:
            win_probabilities = {name: prob/total_prob for name, prob in win_probabilities.items()}
        
        return win_probabilities
    
    def _generate_research_based_reasoning(self, best_move: Dict[str, Any], 
                                         character: PlayerCharacter,
                                         asset_type: AssetEvaluation,
                                         game_phase: GamePhase,
                                         top_moves: List[Dict[str, Any]]) -> str:
        """Generate reasoning based on research findings"""
        reasoning_parts = []
        
        # Character-specific reasoning
        character_descriptions = {
            PlayerCharacter.AGGRESSIVE: "aggressive strategy focuses on rapid property acquisition and offensive actions",
            PlayerCharacter.DEFENSIVE: "defensive strategy prioritizes asset protection and conservative play", 
            PlayerCharacter.NORMAL: "balanced strategy combines property building with tactical flexibility"
        }
        
        asset_descriptions = {
            AssetEvaluation.LOGICAL: "logical asset evaluation prioritizes property set completion",
            AssetEvaluation.VALUE: "value-based evaluation focuses on monetary worth and card values",
            AssetEvaluation.LOGICAL_VALUE: "combined evaluation balances set completion with monetary value"
        }
        
        reasoning_parts.append(f"Using {character.value} character with {asset_type.value} asset evaluation.")
        reasoning_parts.append(character_descriptions[character])
        reasoning_parts.append(asset_descriptions[asset_type])
        
        # Game phase context
        phase_context = {
            GamePhase.EARLY: "In early game, focus on building foundation and collecting key properties",
            GamePhase.MIDDLE: "In mid-game, execute strategic plays and build toward complete sets",
            GamePhase.LATE: "In late game, prioritize aggressive moves and set completion"
        }
        reasoning_parts.append(phase_context[game_phase])
        
        # Move-specific reasoning
        reasoning_parts.append(f"Recommended action: {best_move.get('reasoning', 'Execute optimal play')}")
        
        # Alternative considerations
        if len(top_moves) > 1:
            alt_move = top_moves[1]
            reasoning_parts.append(f"Alternative: {alt_move.get('reasoning', 'Secondary option available')}")
        
        return " ".join(reasoning_parts)

    # Legacy methods for backward compatibility
    def _generate_recommendation(self, current_player, game_state: GameState, 
                               strategy: AIStrategy, complete_sets_count: Dict[str, int]) -> str:
        """Legacy method - redirects to research-based analysis"""
        character = PlayerCharacter.NORMAL
        asset_type = AssetEvaluation.LOGICAL_VALUE
        
        moves = self.bfs_decision_tree(game_state, character, asset_type)
        if moves:
            return f"{moves[0]['action']}: {moves[0].get('reasoning', 'Execute recommended move')}"
        return "Focus on property set completion"
    
    def _generate_reasoning(self, current_player, game_state: GameState, 
                          player_scores: Dict[str, float], complete_sets_count: Dict[str, int]) -> str:
        """Legacy method - provides basic reasoning"""
        game_phase = self.calculate_game_phase(game_state)
        return f"Analysis based on current {game_phase.value} game phase and player positions."