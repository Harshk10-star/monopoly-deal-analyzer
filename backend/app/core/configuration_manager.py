"""
Configuration Manager for Monopoly Deal edge rules and presets.
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.configuration import ConfigurationPreset, OFFICIAL_PRESETS, ConfigurationPresetDB, UserConfiguration
from app.models.game import EdgeRules
from app.core.validation import RuleValidationEngine, ValidationResult
from app.core.database import get_db


class ConfigurationManager:
    """
    Manages configuration presets and rule validation for Monopoly Deal.
    """
    
    def __init__(self):
        self.validation_engine = RuleValidationEngine()
        self.official_presets = OFFICIAL_PRESETS
    
    def get_all_presets(self, db: Session, user_id: Optional[int] = None) -> List[ConfigurationPreset]:
        """
        Get all available configuration presets (official + user custom).
        
        Args:
            db: Database session
            user_id: Optional user ID to include user-specific presets
            
        Returns:
            List of configuration presets
        """
        presets = []
        
        # Add official presets
        presets.extend(self.official_presets.values())
        
        # Add user custom presets if user_id provided
        if user_id:
            custom_presets = db.query(ConfigurationPresetDB).filter(
                ConfigurationPresetDB.created_by == user_id
            ).all()
            
            for preset_db in custom_presets:
                preset = ConfigurationPreset(
                    id=preset_db.id,
                    name=preset_db.name,
                    description=preset_db.description or "",
                    rules=EdgeRules(**preset_db.rules_json),
                    is_official=preset_db.is_official,
                    created_by=preset_db.created_by,
                    usage_count=preset_db.usage_count
                )
                presets.append(preset)
        
        return presets
    
    def get_preset_by_id(self, preset_id: str, db: Session, user_id: Optional[int] = None) -> Optional[ConfigurationPreset]:
        """
        Get a specific configuration preset by ID.
        
        Args:
            preset_id: Preset identifier
            db: Database session
            user_id: Optional user ID for access control
            
        Returns:
            Configuration preset or None if not found
        """
        # Check official presets first
        if preset_id in self.official_presets:
            return self.official_presets[preset_id]
        
        # Check database for custom presets
        preset_db = db.query(ConfigurationPresetDB).filter(
            ConfigurationPresetDB.id == preset_id
        ).first()
        
        if preset_db:
            # Check access permissions
            if preset_db.is_official or preset_db.created_by == user_id:
                return ConfigurationPreset(
                    id=preset_db.id,
                    name=preset_db.name,
                    description=preset_db.description or "",
                    rules=EdgeRules(**preset_db.rules_json),
                    is_official=preset_db.is_official,
                    created_by=preset_db.created_by,
                    usage_count=preset_db.usage_count
                )
        
        return None
    
    def validate_configuration(self, rules: EdgeRules) -> ValidationResult:
        """
        Validate a configuration for consistency and performance.
        
        Args:
            rules: EdgeRules configuration to validate
            
        Returns:
            ValidationResult with errors, warnings, and suggestions
        """
        return self.validation_engine.validate_rules(rules)
    
    def save_custom_preset(self, name: str, description: str, rules: EdgeRules, 
                          user_id: int, db: Session) -> ConfigurationPreset:
        """
        Save a custom configuration preset.
        
        Args:
            name: Preset name
            description: Preset description
            rules: EdgeRules configuration
            user_id: User creating the preset
            db: Database session
            
        Returns:
            Created configuration preset
        """
        # Generate unique ID
        preset_id = f"custom_{user_id}_{name.lower().replace(' ', '_')}"
        
        # Create database record
        preset_db = ConfigurationPresetDB(
            id=preset_id,
            name=name,
            description=description,
            rules_json=rules.dict(),
            is_official=False,
            created_by=user_id,
            usage_count=0
        )
        
        db.add(preset_db)
        db.commit()
        db.refresh(preset_db)
        
        return ConfigurationPreset(
            id=preset_db.id,
            name=preset_db.name,
            description=preset_db.description or "",
            rules=rules,
            is_official=False,
            created_by=user_id,
            usage_count=0
        )
    
    def update_preset_usage(self, preset_id: str, db: Session):
        """
        Increment usage count for a preset.
        
        Args:
            preset_id: Preset identifier
            db: Database session
        """
        if preset_id not in self.official_presets:
            # Update custom preset usage
            preset_db = db.query(ConfigurationPresetDB).filter(
                ConfigurationPresetDB.id == preset_id
            ).first()
            
            if preset_db:
                preset_db.usage_count += 1
                db.commit()
    
    def set_user_default_preset(self, user_id: int, preset_id: str, db: Session):
        """
        Set a user's default configuration preset.
        
        Args:
            user_id: User ID
            preset_id: Preset to set as default
            db: Database session
        """
        # Clear existing default
        db.query(UserConfiguration).filter(
            UserConfiguration.user_id == user_id,
            UserConfiguration.is_default == True
        ).update({"is_default": False})
        
        # Set new default
        user_config = UserConfiguration(
            user_id=user_id,
            preset_id=preset_id,
            is_default=True
        )
        
        db.add(user_config)
        db.commit()
    
    def get_user_default_preset(self, user_id: int, db: Session) -> Optional[ConfigurationPreset]:
        """
        Get a user's default configuration preset.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Default configuration preset or None
        """
        user_config = db.query(UserConfiguration).filter(
            UserConfiguration.user_id == user_id,
            UserConfiguration.is_default == True
        ).first()
        
        if user_config:
            return self.get_preset_by_id(user_config.preset_id, db, user_id)
        
        # Return default official preset if no user default set
        return self.official_presets["strict_official"]
    
    def get_preset_recommendations(self, rules: EdgeRules) -> List[str]:
        """
        Get recommendations for similar or better presets.
        
        Args:
            rules: Current EdgeRules configuration
            
        Returns:
            List of recommended preset IDs
        """
        recommendations = []
        
        # Analyze current configuration
        validation = self.validate_configuration(rules)
        
        # Recommend based on validation results
        if validation.performance_impact == "high":
            recommendations.append("balanced_competitive")
        
        if len(validation.warnings) > 3:
            recommendations.append("strict_official")
        
        # Check for defensive patterns
        defensive_score = 0
        if rules.housePayment == "bank":
            defensive_score += 1
        if rules.hotelMove == "not_allowed":
            defensive_score += 1
        if not rules.quadrupleRent:
            defensive_score += 1
        if not rules.forcedDealToDealBreaker:
            defensive_score += 1
        
        if defensive_score >= 3:
            recommendations.append("defensive_play")
        else:
            recommendations.append("flexible_house_rules")
        
        return list(set(recommendations))  # Remove duplicates
    
    def export_configuration(self, preset_id: str, db: Session, user_id: Optional[int] = None) -> Optional[Dict]:
        """
        Export a configuration preset to a dictionary format.
        
        Args:
            preset_id: Preset to export
            db: Database session
            user_id: Optional user ID for access control
            
        Returns:
            Configuration dictionary or None if not found
        """
        preset = self.get_preset_by_id(preset_id, db, user_id)
        if preset:
            return {
                "name": preset.name,
                "description": preset.description,
                "rules": preset.rules.dict(),
                "exported_at": "2024-01-01T00:00:00Z",  # Would use actual timestamp
                "version": "1.0"
            }
        return None
    
    def import_configuration(self, config_data: Dict, user_id: int, db: Session) -> ConfigurationPreset:
        """
        Import a configuration from dictionary format.
        
        Args:
            config_data: Configuration dictionary
            user_id: User importing the configuration
            db: Database session
            
        Returns:
            Imported configuration preset
        """
        rules = EdgeRules(**config_data["rules"])
        
        return self.save_custom_preset(
            name=config_data["name"],
            description=config_data.get("description", ""),
            rules=rules,
            user_id=user_id,
            db=db
        )