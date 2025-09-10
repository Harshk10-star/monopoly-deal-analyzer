from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


# Enums for game rules and card types
class HousePaymentRule(str, Enum):
    BANK = "bank"
    INCOMPLETE_SET = "incomplete_set"
    FLOATING = "floating"


class HotelMoveRule(str, Enum):
    NOT_ALLOWED = "not_allowed"
    FREE_MOVE = "free_move"
    COSTS_ACTION = "costs_action"


class DeckExhaustionRule(str, Enum):
    RESHUFFLE = "reshuffle"
    GAME_OVER = "game_over"


class ExtraPropertiesRule(str, Enum):
    CAP_RENT = "cap"
    SPLIT_SETS = "split"


class BuildingForfeitureRule(str, Enum):
    DISCARD = "discard"
    TO_BANK = "to_bank"
    KEEP_FLOATING = "keep_floating"


class PropertyMergingRule(str, Enum):
    AUTO_MERGE = "auto_merge"
    MANUAL_MERGE = "manual_merge"
    NO_MERGE = "no_merge"


class AIStrategy(str, Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    NORMAL = "normal"


# Pydantic models for API requests/responses
class MoneyCard(BaseModel):
    value: int = Field(..., ge=1, le=10)
    
    class Config:
        json_schema_extra = {
            "example": {"value": 5}
        }


class PropertyCard(BaseModel):
    color: str
    name: str
    value: int = Field(..., ge=1, le=10)
    
    class Config:
        json_schema_extra = {
            "example": {"color": "green", "name": "Green Property", "value": 3}
        }


class ActionCard(BaseModel):
    name: str
    type: str
    rules: str
    
    class Config:
        json_schema_extra = {
            "example": {"name": "Deal Breaker", "type": "steal", "rules": "Steal a complete property set"}
        }


class PlayerState(BaseModel):
    id: int
    name: str
    hand: List[Union[str, MoneyCard, PropertyCard, ActionCard]]
    bank: List[int]
    properties: Dict[str, List[str]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Alice",
                "hand": ["Pass Go", "Deal Breaker", "Green Property"],
                "bank": [5, 2],
                "properties": {"green": ["Green Property", "Green Property"], "blue": []}
            }
        }


class CardTransfer(BaseModel):
    """Model for transferring cards between piles"""
    cardId: str
    fromLocation: str  # "hand", "bank", "properties", "opponent_hand", "opponent_properties"
    toLocation: str    # "hand", "bank", "properties", "discard"
    fromPlayerId: Optional[int] = None
    toPlayerId: Optional[int] = None
    propertySet: Optional[str] = None  # For property transfers
    
    class Config:
        json_schema_extra = {
            "example": {
                "cardId": "green_property_1",
                "fromLocation": "hand",
                "toLocation": "properties",
                "propertySet": "green"
            }
        }


class CardSelection(BaseModel):
    """Model for selecting cards from hand or other locations"""
    selectedCards: List[str]
    action: str  # "transfer", "play", "discard"
    targetLocation: Optional[str] = None
    targetPlayerId: Optional[int] = None
    propertySet: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "selectedCards": ["green_property_1", "green_property_2"],
                "action": "transfer",
                "targetLocation": "properties",
                "propertySet": "green"
            }
        }


class EdgeRules(BaseModel):
    # Core rule configurations
    housePayment: HousePaymentRule = HousePaymentRule.BANK
    hotelMove: HotelMoveRule = HotelMoveRule.NOT_ALLOWED
    deckExhaustion: DeckExhaustionRule = DeckExhaustionRule.RESHUFFLE
    extraProperties: ExtraPropertiesRule = ExtraPropertiesRule.CAP_RENT
    
    # Enhanced rules for edge cases
    buildingForfeiture: BuildingForfeitureRule = BuildingForfeitureRule.DISCARD
    propertyMerging: PropertyMergingRule = PropertyMergingRule.AUTO_MERGE
    quadrupleRent: bool = False
    forcedDealToDealBreaker: bool = True
    justSayNoEmptyHand: bool = True
    justSayNoOnZero: bool = True
    
    def get_rule_descriptions(self) -> Dict[str, str]:
        """Get human-readable descriptions for all rules"""
        return {
            "housePayment": "How house/hotel cards are handled when received by players without complete sets",
            "hotelMove": "Whether house/hotel cards can be moved between property sets",
            "deckExhaustion": "What happens when the deck runs out of cards",
            "extraProperties": "How extra property cards beyond complete sets are handled",
            "buildingForfeiture": "What happens to buildings when property sets become incomplete",
            "propertyMerging": "Whether separate property sets of the same color can be merged",
            "quadrupleRent": "Whether two 'Double the Rent' cards can be played together",
            "forcedDealToDealBreaker": "Whether Forced Deal can be used to set up Deal Breaker combos",
            "justSayNoEmptyHand": "Whether 'Just Say No' can be played from an empty hand",
            "justSayNoOnZero": "Whether 'Just Say No' can block zero-cost actions"
        }
    
    def get_rule_options(self) -> Dict[str, List[str]]:
        """Get available options for each rule"""
        return {
            "housePayment": [rule.value for rule in HousePaymentRule],
            "hotelMove": [rule.value for rule in HotelMoveRule],
            "deckExhaustion": [rule.value for rule in DeckExhaustionRule],
            "extraProperties": [rule.value for rule in ExtraPropertiesRule],
            "buildingForfeiture": [rule.value for rule in BuildingForfeitureRule],
            "propertyMerging": [rule.value for rule in PropertyMergingRule],
            "quadrupleRent": [True, False],
            "forcedDealToDealBreaker": [True, False],
            "justSayNoEmptyHand": [True, False],
            "justSayNoOnZero": [True, False]
        }
    
    def validate_rule_consistency(self) -> List[str]:
        """Validate rule combinations for logical consistency"""
        warnings = []
        
        # Check for potentially conflicting rules
        if self.hotelMove == HotelMoveRule.FREE_MOVE and self.buildingForfeiture == BuildingForfeitureRule.KEEP_FLOATING:
            warnings.append("Free building movement with floating forfeiture may create complex edge cases")
        
        if self.extraProperties == ExtraPropertiesRule.SPLIT_SETS and self.propertyMerging == PropertyMergingRule.AUTO_MERGE:
            warnings.append("Auto-merging with split sets may cause frequent recalculations")
        
        if self.quadrupleRent and not self.forcedDealToDealBreaker:
            warnings.append("Quadruple rent enabled but advanced combos disabled - consider consistency")
        
        return warnings
    
    class Config:
        json_schema_extra = {
            "example": {
                "housePayment": "bank",
                "hotelMove": "not_allowed",
                "deckExhaustion": "reshuffle",
                "extraProperties": "cap",
                "buildingForfeiture": "discard",
                "propertyMerging": "auto_merge",
                "quadrupleRent": False,
                "forcedDealToDealBreaker": True,
                "justSayNoEmptyHand": True,
                "justSayNoOnZero": True
            }
        }


class GameState(BaseModel):
    players: List[PlayerState]
    discard: List[str]
    deckCount: int
    edgeRules: EdgeRules
    
    class Config:
        json_schema_extra = {
            "example": {
                "players": [
                    {
                        "id": 1,
                        "name": "Alice",
                        "hand": ["Pass Go", "Deal Breaker", "Green Property"],
                        "bank": [5, 2],
                        "properties": {"green": ["Green Property", "Green Property"], "blue": []}
                    },
                    {
                        "id": 2,
                        "name": "Bob",
                        "hand": ["Rent Green/Blue", "House"],
                        "bank": [1, 1],
                        "properties": {"blue": ["Blue Property", "Blue Property"], "red": ["Red Property"]}
                    }
                ],
                "discard": ["Debt Collector"],
                "deckCount": 70,
                "edgeRules": {
                    "housePayment": "bank",
                    "hotelMove": "not_allowed",
                    "deckExhaustion": "reshuffle",
                    "extraProperties": "cap",
                    "buildingForfeiture": "discard",
                    "propertyMerging": "auto_merge",
                    "quadrupleRent": False,
                    "forcedDealToDealBreaker": True,
                    "justSayNoEmptyHand": True,
                    "justSayNoOnZero": True
                }
            }
        }


class AnalysisRequest(BaseModel):
    gameState: GameState
    strategy: AIStrategy = AIStrategy.NORMAL


class AnalysisResponse(BaseModel):
    recommendedMove: str
    reasoning: str
    strongestPlayer: str
    winProbability: Dict[str, float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommendedMove": "Play Deal Breaker on Bob's Blue set",
                "reasoning": "Completing 3 property sets ensures victory immediately.",
                "strongestPlayer": "Alice",
                "winProbability": {"Alice": 0.82, "Bob": 0.18}
            }
        }


class SimulationRequest(BaseModel):
    gameState: GameState
    strategy: AIStrategy
    numSimulations: int = Field(..., ge=1, le=1000)


class SimulationResponse(BaseModel):
    results: List[AnalysisResponse]
    averageWinProbability: Dict[str, float]
    strategyPerformance: Dict[str, float]


class CardOperationRequest(BaseModel):
    """Request model for card operations (transfer, selection, etc.)"""
    gameState: GameState
    operation: Union[CardTransfer, CardSelection]
    edgeRules: EdgeRules


class CardOperationResponse(BaseModel):
    """Response model for card operations"""
    success: bool
    newGameState: GameState
    message: str
    validationErrors: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Card transferred successfully",
                "validationErrors": None
            }
        }


# SQLAlchemy models for database
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    subscription_status = Column(String, default="free")
    credits = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Configuration relationships
    configuration_presets = relationship("ConfigurationPresetDB", back_populates="creator")
    configurations = relationship("UserConfiguration", back_populates="user")
    analyses = relationship("GameAnalysis", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class GameAnalysis(Base):
    __tablename__ = "game_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_state = Column(JSON)
    analysis_result = Column(JSON)
    strategy_used = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_payment_intent_id = Column(String)
    amount = Column(Integer)
    currency = Column(String, default="usd")
    status = Column(String)
    payment_type = Column(String)  # "per_game" or "subscription"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
