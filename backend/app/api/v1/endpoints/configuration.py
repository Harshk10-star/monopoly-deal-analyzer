"""
Configuration API endpoints for Monopoly Deal edge rules management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
try:
    from app.core.auth import get_current_user
except ImportError:
    # Fallback for when auth is not available
    def get_current_user():
        return None
from app.models.game import User, EdgeRules
from app.models.configuration import (
    ConfigurationPreset, ConfigurationRequest, ConfigurationResponse
)
from app.core.configuration_manager import ConfigurationManager
from app.core.validation import ValidationResult

router = APIRouter()
config_manager = ConfigurationManager()


@router.get("/presets", response_model=List[ConfigurationPreset])
async def get_configuration_presets(
    db: Session = Depends(get_db)
):
    """Get all available configuration presets (public endpoint)"""
    # Return only official presets for unauthenticated users
    presets = config_manager.get_all_presets(db, user_id=None)
    return presets


@router.get("/presets/{preset_id}", response_model=ConfigurationPreset)
async def get_configuration_preset(
    preset_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific configuration preset by ID (public endpoint)"""
    preset = config_manager.get_preset_by_id(preset_id, db, user_id=None)
    
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration preset not found"
        )
    
    return preset


@router.post("/validate", response_model=ValidationResult)
async def validate_configuration(rules: EdgeRules):
    """Validate a configuration for consistency and performance"""
    validation_result = config_manager.validate_configuration(rules)
    return validation_result


@router.post("/presets", response_model=ConfigurationResponse)
async def create_custom_preset(
    request: ConfigurationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a custom configuration preset"""
    if not request.custom_rules or not request.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom rules and name are required"
        )
    
    try:
        # Validate the configuration
        validation = config_manager.validate_configuration(request.custom_rules)
        
        if not validation.is_valid:
            return ConfigurationResponse(
                success=False,
                validation_warnings=validation.errors,
                message="Configuration validation failed"
            )
        
        # Save the preset
        preset = config_manager.save_custom_preset(
            name=request.name,
            description=request.description or "",
            rules=request.custom_rules,
            user_id=current_user.id,
            db=db
        )
        
        return ConfigurationResponse(
            success=True,
            preset=preset,
            validation_warnings=validation.warnings,
            message="Custom preset created successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create preset: {str(e)}"
        )


@router.put("/presets/{preset_id}/usage")
async def increment_preset_usage(
    preset_id: str,
    db: Session = Depends(get_db)
):
    """Increment usage count for a preset"""
    config_manager.update_preset_usage(preset_id, db)
    return {"message": "Usage count updated"}


@router.post("/default")
async def set_default_preset(
    request: ConfigurationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set user's default configuration preset"""
    if not request.preset_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preset ID is required"
        )
    
    # Verify preset exists and user has access
    preset = config_manager.get_preset_by_id(request.preset_id, db, current_user.id)
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration preset not found"
        )
    
    config_manager.set_user_default_preset(current_user.id, request.preset_id, db)
    
    return {"message": "Default preset updated successfully"}


@router.get("/default", response_model=ConfigurationPreset)
async def get_default_preset(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's default configuration preset"""
    preset = config_manager.get_user_default_preset(current_user.id, db)
    
    if not preset:
        # Return strict official as fallback
        preset = config_manager.official_presets["strict_official"]
    
    return preset


@router.get("/recommendations")
async def get_preset_recommendations(
    rules: EdgeRules,
    db: Session = Depends(get_db)
):
    """Get recommended presets based on current configuration"""
    recommendations = config_manager.get_preset_recommendations(rules)
    
    # Get full preset details for recommendations
    recommended_presets = []
    for preset_id in recommendations:
        preset = config_manager.get_preset_by_id(preset_id, db)
        if preset:
            recommended_presets.append(preset)
    
    return {
        "recommendations": recommended_presets,
        "reasoning": "Based on your current configuration patterns"
    }


@router.get("/export/{preset_id}")
async def export_configuration(
    preset_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Export a configuration preset to JSON format"""
    user_id = current_user.id if current_user else None
    config_data = config_manager.export_configuration(preset_id, db, user_id)
    
    if not config_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration preset not found"
        )
    
    return config_data


@router.post("/import", response_model=ConfigurationResponse)
async def import_configuration(
    config_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import a configuration from JSON format"""
    try:
        preset = config_manager.import_configuration(config_data, current_user.id, db)
        
        return ConfigurationResponse(
            success=True,
            preset=preset,
            message="Configuration imported successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to import configuration: {str(e)}"
        )


@router.get("/rule-descriptions")
async def get_rule_descriptions():
    """Get descriptions for all configuration rules"""
    sample_rules = EdgeRules()
    return {
        "descriptions": sample_rules.get_rule_descriptions(),
        "options": sample_rules.get_rule_options()
    }


@router.get("/test")
async def test_configuration_system():
    """Test endpoint to verify configuration system is working"""
    return {
        "status": "Configuration system is working!",
        "official_presets": list(config_manager.official_presets.keys()),
        "validation_available": True,
        "features": [
            "Edge case rule configuration",
            "Official presets",
            "Rule validation",
            "Performance impact analysis",
            "Import/Export functionality"
        ]
    }