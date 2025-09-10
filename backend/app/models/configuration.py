"""
Configuration models for Monopoly Deal edge rules and presets.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.game import EdgeRules, HousePaymentRule, HotelMoveRule, DeckExhaustionRule, ExtraPropertiesRule, BuildingForfeitureRule, PropertyMergingRule


class ConfigurationPreset(BaseModel):
    """Pydantic model for configuration presets"""
    id: str
    name: str
    description: str
    rules: EdgeRules
    is_official: bool = False
    created_by: Optional[int] = None
    usage_count: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "strict_official",
                "name": "Strict Official Rules",
                "description": "Conservative interpretation following official rules closely",
                "is_official": True,
                "usage_count": 1250,
                "rules": {
                    "housePayment": "bank",
                    "hotelMove": "not_allowed",
                    "deckExhaustion": "reshuffle",
                    "extraProperties": "cap",
                    "buildingForfeiture": "discard",
                    "propertyMerging": "auto_merge",
                    "quadrupleRent": False,
                    "forcedDealToDealBreaker": False,
                    "justSayNoEmptyHand": False,
                    "justSayNoOnZero": False
                }
            }
        }


class ConfigurationRequest(BaseModel):
    """Request model for configuration operations"""
    preset_id: Optional[str] = None
    custom_rules: Optional[EdgeRules] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ConfigurationResponse(BaseModel):
    """Response model for configuration operations"""
    success: bool
    preset: Optional[ConfigurationPreset] = None
    validation_warnings: List[str] = []
    message: str


# Predefined official presets
OFFICIAL_PRESETS = {
    "strict_official": ConfigurationPreset(
        id="strict_official",
        name="Strict Official Rules",
        description="Conservative interpretation of official rules with minimal edge case allowances",
        rules=EdgeRules(
            housePayment=HousePaymentRule.BANK,
            hotelMove=HotelMoveRule.NOT_ALLOWED,
            deckExhaustion=DeckExhaustionRule.RESHUFFLE,
            extraProperties=ExtraPropertiesRule.CAP_RENT,
            buildingForfeiture=BuildingForfeitureRule.DISCARD,
            propertyMerging=PropertyMergingRule.AUTO_MERGE,
            quadrupleRent=False,
            forcedDealToDealBreaker=False,
            justSayNoEmptyHand=False,
            justSayNoOnZero=False
        ),
        is_official=True
    ),
    
    "flexible_house_rules": ConfigurationPreset(
        id="flexible_house_rules",
        name="Flexible House Rules",
        description="More permissive rules allowing advanced strategies and edge case exploitation",
        rules=EdgeRules(
            housePayment=HousePaymentRule.FLOATING,
            hotelMove=HotelMoveRule.COSTS_ACTION,
            deckExhaustion=DeckExhaustionRule.RESHUFFLE,
            extraProperties=ExtraPropertiesRule.SPLIT_SETS,
            buildingForfeiture=BuildingForfeitureRule.TO_BANK,
            propertyMerging=PropertyMergingRule.MANUAL_MERGE,
            quadrupleRent=True,
            forcedDealToDealBreaker=True,
            justSayNoEmptyHand=True,
            justSayNoOnZero=True
        ),
        is_official=False
    ),
    
    "balanced_competitive": ConfigurationPreset(
        id="balanced_competitive",
        name="Balanced Competitive",
        description="Tournament-style rules balancing strategy depth with game flow",
        rules=EdgeRules(
            housePayment=HousePaymentRule.INCOMPLETE_SET,
            hotelMove=HotelMoveRule.COSTS_ACTION,
            deckExhaustion=DeckExhaustionRule.RESHUFFLE,
            extraProperties=ExtraPropertiesRule.CAP_RENT,
            buildingForfeiture=BuildingForfeitureRule.TO_BANK,
            propertyMerging=PropertyMergingRule.AUTO_MERGE,
            quadrupleRent=False,
            forcedDealToDealBreaker=True,
            justSayNoEmptyHand=True,
            justSayNoOnZero=False
        ),
        is_official=False
    ),
    
    "defensive_play": ConfigurationPreset(
        id="defensive_play",
        name="Defensive Play Style",
        description="Rules favoring defensive strategies and property protection",
        rules=EdgeRules(
            housePayment=HousePaymentRule.BANK,
            hotelMove=HotelMoveRule.NOT_ALLOWED,
            deckExhaustion=DeckExhaustionRule.RESHUFFLE,
            extraProperties=ExtraPropertiesRule.CAP_RENT,
            buildingForfeiture=BuildingForfeitureRule.KEEP_FLOATING,
            propertyMerging=PropertyMergingRule.NO_MERGE,
            quadrupleRent=False,
            forcedDealToDealBreaker=False,
            justSayNoEmptyHand=True,
            justSayNoOnZero=True
        ),
        is_official=False
    )
}


# SQLAlchemy models for database storage
class ConfigurationPresetDB(Base):
    """Database model for configuration presets"""
    __tablename__ = "configuration_presets"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    rules_json = Column(JSON, nullable=False)
    is_official = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    usage_count = Column(Integer, default=0)
    
    creator = relationship("User", back_populates="configuration_presets")


class UserConfiguration(Base):
    """Database model for user-specific configuration preferences"""
    __tablename__ = "user_configurations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    preset_id = Column(String, ForeignKey("configuration_presets.id"))
    is_default = Column(Boolean, default=False)
    last_used = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="configurations")
    preset = relationship("ConfigurationPresetDB")